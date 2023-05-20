import re
import datetime
import time
import math

import requests
from bs4 import BeautifulSoup

from clearDarkSkyEnums import *

# Messages
ERROR_TRY_AGAIN = 'Error getting page, trying again in 2 seconds...'
ERROR_EXITING = 'Error getting page, exiting...'

# Website URL
BASE_URL = 'https://www.cleardarksky.com/c/%s.html'

# HTML attributes
COORDS_LABEL = 'coords'
TITLE_LABEL = 'title'
FONT_LABEL = 'font'
MAP_LABEL = 'map'
MAP_DICT = {"name":"ckmap"}
AREA_LABEL = 'area'
LAST_UPDATE_TEXT = 'Last updated 20'

# X coordinate of first data point in row
X_START_CORD = 134

# Y coordinates to weather attribute
Y_CORD_TO_ATTRIBUTE = {
    77: WeatherAttribute.CLOUD_COVER,
    93: WeatherAttribute.TRANSPARENCY,
    109: WeatherAttribute.SEEING,
    125: WeatherAttribute.DARKNESS,
    173: WeatherAttribute.SMOKE,
    189: WeatherAttribute.WIND,
    205: WeatherAttribute.HUMIDITY,
    221: WeatherAttribute.TEMPERATURE
}

# Regex for extracting data from html
REGEX_INT = re.compile(r'\d+')
REGEX_INT_NEG = re.compile(r'-?\d+')
REGEX_DECIMAL = re.compile(r'-?\d+\.\d+')


def extractDate(soup):
    """ Extract the date of generation from website html. 
    Parameters:
        soup (BeautifulSoup): The html response from the website.
    Returns:
        datetime.datetime: The date of generation (0 hours, 0 min).
    """
    date_content = soup.find(lambda tag: tag.name == FONT_LABEL and LAST_UPDATE_TEXT in tag.text)
    regex_date = REGEX_INT.findall(date_content.text)
    return datetime.datetime(int(regex_date[0]), int(regex_date[1]), int(regex_date[2]))


def textToValue(attribute, text):
    """ Convert text to value based on attribute. 
    Parameters:
        attribute (WeatherAttribute): The attribute to convert text to value for.
        text (str): The text to convert to value.
    Returns:
        int, float, tuple, or enum: The value of the text.
    """
    match attribute:
        # Cloud Cover is a percentage (0 to 100)
        case WeatherAttribute.CLOUD_COVER:
            if 'Clear' in text:
                return 0
            elif 'Overcast' in text:
                return 100
            try:
                return int(text.split('%')[0])
            except:
                return 100
        # Transparency is an enum
        case WeatherAttribute.TRANSPARENCY:
            return Transparency.getAttributeFromText(text)
        # Seeing is a float (x/5)
        case WeatherAttribute.SEEING:
            try:
                return float(REGEX_INT.search(text).group(0))/5
            except:
                return 1/5
        # Darkness is a float (-4 to 6.5)
        case WeatherAttribute.DARKNESS:
            try:
                return float(REGEX_DECIMAL.search(text).group(0))
            except:
                return -4
        # Smoke is an int (0 to 500 ug/m^3)
        case WeatherAttribute.SMOKE:
            if 'No Smoke' in text:
                return 0
            try:
                return int(REGEX_INT.search(text).group(0))
            except:
                return 500
        # Wind is a tuple of ints (0 to 45 mph)
        case WeatherAttribute.WIND:
            try:
                first = int(REGEX_INT.search(text).group(0))
                if first == 45:
                    return (first, math.inf)
                second = int(REGEX_INT.findall(text)[1])
                return (first, second)
            except:
                return (45, math.inf)
        # Humidity is a tuple of ints (0 to 100%)
        case WeatherAttribute.HUMIDITY:
            try:
                first = int(REGEX_INT.search(text).group(0))
                if text[0] == '<':
                    return (0, first)
                second = int(REGEX_INT.findall(text)[1])
                return (first, second)
            except:
                return (95, 100)
        # Temperature is a tuple of ints (-40 to 113 F)
        case WeatherAttribute.TEMPERATURE:
            try:
                first = int(REGEX_INT_NEG.search(text).group(0))
                if text[0] == '<':
                    return (-math.inf, first)
                if first == 113:
                    return (first, math.inf)
                second = int(REGEX_INT_NEG.findall(text)[1])
                return (first, second)
            except:
                return (113, math.inf)


class PointInTime:
    """ A point in time with weather data. 
    Attributes:
        timestamp (datetime.datetime): The date and time of of weather data.
        data (dict): The weather data. Keys are WeatherAttribute enums and values 
                     are ints, floats, tuples, or enums.
    Methods:
        __init__(self, timestamp): Initialize the point in time with a timestamp.
        __str__(self): Return a string representation of the point in time.
        __repr__(self): Return a string representation of the point in time.
        add(self, attribute, text): Add a weather attribute and its value to the point in time.
    """

    def __init__(self, timestamp):
        """ Initialize the point in time with a timestamp.
        Parameters:
            timestamp (datetime.datetime): The date and time of of weather data.
        """
        self.timestamp = timestamp
        self.data = dict()
    
    def __str__(self):
        """ Return a string representation of the point in time. """
        output = f'{self.timestamp}\n'
        for attribute in self.data:
            output += f'{attribute}: {self.data[attribute]}\n'
        return output

    def __repr__(self):
        """ Return a string representation of the point in time. """
        return self.__str__()

    def add(self, attribute, text):
        """ Add a weather attribute and its value to the point in time.
        Parameters:
            attribute (WeatherAttribute): The attribute to add.
            text (str): The text to convert to value.
        """
        if attribute == WeatherAttribute.DARKNESS:
            # Darkness is a special because it is provide in 15 min increments 
            if attribute not in self.data:
                self.data[attribute] = [textToValue(attribute, text)]
            else:
                self.data[attribute].append(textToValue(attribute, text))
        else:
            self.data[attribute] = textToValue(attribute, text)


def extractWeatherData(location):
    """ Extract weather data from website html.
    Parameters:
        location (str): The location key to extract weather data for.
    Returns:
        dictionary: A dictionary of weather data. Keys are datetime.datetime objects
                    and values are PointInTime objects.
    """
    # Create url
    url = BASE_URL % location

    # Get html from website
    tries = 0
    while True:
        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")
            start_date = extractDate(soup)
            details = soup.find(MAP_LABEL, MAP_DICT)
            areas = details.find_all(AREA_LABEL)
            break
        except:
            tries += 1
            if tries == 5:
                print(ERROR_EXITING)
                return None
            print(ERROR_TRY_AGAIN)
            time.sleep(2)

    data = dict()
    for area in areas:
        if TITLE_LABEL in area.attrs and COORDS_LABEL in area.attrs:
            x_coord = int(area[COORDS_LABEL].split(',')[0])
            y_coord = int(area[COORDS_LABEL].split(',')[1])
            if x_coord == X_START_CORD:
                day = 0
            currentAttribute = Y_CORD_TO_ATTRIBUTE[int(y_coord)]
            hour = int(REGEX_INT.match(area[TITLE_LABEL]).group(0))
            minute = int(REGEX_INT.findall(area[TITLE_LABEL])[1])
            if hour == 0 and minute == 0:
                day += 1
            timestamp = start_date + datetime.timedelta(days=day, hours=hour)
            if timestamp not in data:
                data[timestamp] = PointInTime(timestamp)
            value = ':'.join(area[TITLE_LABEL].split(':')[2:]).strip()
            data[timestamp].add(currentAttribute, value)

    return data


class AlertProfile:
    """ An alert profile for a user.
    Attributes:
        username (str): The username of the alert profile.
        name (str): The name of the alert profile.
        location (str): The location key of the alert profile.
        cloudCoverage (int): The maximum cloud coverage (0 to 100%).
        transparency (Transparency): The minimum transparency.
        seeing (float): The minimum seeing (n/5).
        darkness (float): The minimum darkness.
        smoke (int): The maximum smoke (0 to 500).
        wind (int): The maximum wind (0 to 45+ mph).
        humidity (int): The maximum humidity (0 to 100%).
        temperatureMax (int): The maximum temperature (-40 to 113 F).
        temperatureMin (int): The minimum temperature (-40 to 113 F).
        duration (int): The minimum duration in hours.
    Methods:
        __init__(self, username, name, location): Initialize the alert profile with a username and name.
        __str__(self): Return a string representation of the alert profile.
        __repr__(self): Return a string representation of the alert profile.
        setCloudCoverage(self, worstCloudCoverage): Set the maximum cloud coverage.
        setTransparency(self, worstTransparency): Set the minimum transparency.
        setSeeing(self, worstSeeing): Set the minimum seeing.
        setDarkness(self, worstDarkness): Set the minimum darkness.
        setSmoke(self, worstSmoke): Set the maximum smoke.
        setWind(self, worstWind): Set the maximum wind.
        setHumidity(self, worstHumidity): Set the maximum humidity.
        setTemperatureMax(self, worstTemperatureMax): Set the maximum temperature.
        setTemperatureMin(self, worstTemperatureMin): Set the minimum temperature.
        setDuration(self, duration): Set the minimum duration.
        checkForAlert(location, weatherData): Check if the weather data is acceptable.
    """
    
    def __init__(self, username, name, location):
        """ Initialize the alert profile with a username and name.
        Parameters:
            username (str): The username of the alert profile.
            name (str): The name of the alert profile.
        """
        self.username = username
        self.name = name
        self.location = location

        # Set default values
        self.__cloudCoverage = 100
        self.__transparency = Transparency.POOR
        self.__seeing = 0.0
        self.__darkness = -4.0
        self.__smoke = 500
        self.__wind = math.inf
        self.__humidity = 100
        self.__temperatureMax = math.inf
        self.__temperatureMin = -math.inf
        self.__duration = 0

    def __str__(self):
        """ Return a string representation of the alert profile. """
        return f'{self.name} by {self.username}'

    def __repr__(self):
        """ Return a string representation of the alert profile. """
        return self.__str__()

    def setCloudCoverage(self, worstCloudCoverage):
        """ Set the worst cloud coverage for the alert profile.
        Parameters:
            worstCloudCoverage (int): The worst cloud coverage for the alert profile.
        """
        self.__cloudCoverage = worstCloudCoverage

    def setTransparency(self, worstTransparency):
        """ Set the worst transparency for the alert profile.
        Parameters:
            worstTransparency (Transparency): The worst transparency for the alert profile.
        """
        self.__transparency = worstTransparency

    def setSeeing(self, worstSeeing):
        """ Set the worst seeing for the alert profile.
        Parameters:
            worstSeeing (float): The worst seeing for the alert profile.
        """
        self.__seeing = worstSeeing

    def setDarkness(self, worstDarkness):
        """ Set the worst darkness for the alert profile.
        Parameters:
            worstDarkness (float): The worst darkness for the alert profile.
        """
        self.__darkness = worstDarkness

    def setSmoke(self, worstSmoke):
        """ Set the worst smoke for the alert profile.
        Parameters:
            worstSmoke (int): The worst smoke for the alert profile.
        """
        self.__smoke = worstSmoke
    
    def setWind(self, worstWind):
        """ Set the worst wind for the alert profile.
        Parameters:
            worstWind (int): The worst wind for the alert profile.
        """
        self.__wind = worstWind

    def setHumidity(self, worstHumidity):
        """ Set the worst humidity for the alert profile.
        Parameters:
            worstHumidity (int): The worst humidity for the alert profile.
        """
        self.__humidity = worstHumidity

    def setTemperatureMax(self, worstTemperatureMax):
        """ Set the worst maximum temperature for the alert profile.
        Parameters:
            worstTemperatureMax (int): The worst maximum temperature for the alert profile.
        """
        self.__temperatureMax = worstTemperatureMax

    def setTemperatureMin(self, worstTemperatureMin):
        """ Set the worst minimum temperature for the alert profile.
        Parameters:
            worstTemperatureMin (int): The worst minimum temperature for the alert profile.
        """
        self.__temperatureMin = worstTemperatureMin

    def setDuration(self, shortestDuration):
        """ Set the shortest duration for the alert profile.
        Parameters:
            shortestDuration (int): The shortest duration for the alert profile.
        """
        self.__duration = shortestDuration

    def checkForCloudCoverage(self, hour):
        """ Check if the cloud coverage matches the alert profile.
        Parameters:
            hour (PointInTime): The hour to check.
        Returns:
            bool: True if the cloud coverage matches the alert profile, False otherwise.
        """
        return hour.data[Attribute.CLOUD_COVERAGE] <= self.__cloudCoverage

    def __checkForTransparency(self, hour):
        """ Check if the transparency matches the alert profile.
        Parameters:
            hour (PointInTime): The hour to check.
        Returns:
            bool: True if the transparency matches the alert profile, False otherwise.
        """
        return hour.data[Attribute.TRANSPARENCY].value  <= self.__transparency.value 

    def __checkForSeeing(self, hour):
        """ Check if the seeing matches the alert profile.
        Parameters:
            hour (PointInTime): The hour to check.
        Returns:
            bool: True if the seeing matches the alert profile, False otherwise.
        """
        return hour.data[Attribute.SEEING] >= self.__seeing

    def __checkForDarkness(self, hour):
        """ Check if the darkness matches the alert profile.
        Parameters:
            hour (PointInTime): The hour to check.
        Returns:
            bool: True if the darkness matches the alert profile, False otherwise.
        """
        return hour.data[Attribute.DARKNESS] >= self.__darkness

    def __checkForSmoke(self, hour):
        """ Check if the smoke matches the alert profile.
        Parameters:
            hour (PointInTime): The hour to check.
        Returns:
            bool: True if the smoke matches the alert profile, False otherwise.
        """
        return hour.data[Attribute.SMOKE] <= self.__smoke

    def __checkForWind(self, hour):
        """ Check if the wind matches the alert profile.
        Parameters:
            hour (PointInTime): The hour to check.
        Returns:
            bool: True if the wind matches the alert profile, False otherwise.
        """
        return min(hour.data[Attribute.WIND]) <= self.__wind

    def __checkForHumidity(self, hour):
        """ Check if the humidity matches the alert profile.
        Parameters:
            hour (PointInTime): The hour to check.
        Returns:
            bool: True if the humidity matches the alert profile, False otherwise.
        """
        return min(hour.data[Attribute.HUMIDITY]) <= self.__humidity

    def __checkForTemperature(self, hour):
        """ Check if the temperature matches the alert profile.
        Parameters:
            hour (PointInTime): The hour to check.
        Returns:
            bool: True if the temperature matches the alert profile, False otherwise.
        """
        return min(hour.data[Attribute.TEMPERATURE]) <= self.__temperatureMax and max(hour.data[Attribute.TEMPERATURE]) >= self.__temperatureMin

    def __checkHour(self, hour):
        """ Check if the hour matches the alert profile.
        Parameters:
            hour (PointInTime): The hour to check.
        Returns:
            bool: True if the hour matches the alert profile, False otherwise.
        """
        conditions = [self.__checkForCloudCoverage(hour),
                        self.__checkForTransparency(hour),
                        self.__checkForSeeing(hour),
                        self.__checkForDarkness(hour),
                        self.__checkForSmoke(hour),
                        self.__checkForWind(hour),
                        self.__checkForHumidity(hour),
                        self.__checkForTemperature(hour)]
        return all(conditions)

    def checkForAlert(location, weatherData):
        """ Check if the weather data matches the alert profile.
        Parameters:
            weatherData (PointInTime): The weather data to check.
        Returns:
            list: A list of tuples datetime.datetime objects representing 
                the start and end of the matching conditions.
        """
        if location != weatherData.location:
            return None
        matches = []
        matching_num = 0
        for h in range(0, len(weatherData.data)):
            hour = weatherData.data[h]
            if self.__checkHour(hour):
                matching_num += 1
                if matching_num == 1:
                    start = hour.timestamp
            elif matching_num >= self.__duration:
                end = weatherData.data[h-1].timestamp
                matches.append((start, end))
                matching_num = 0
        return matches

def main():
    # Set url
    locationKey = 'AlbanyNYkey'

    # Get data
    data = extractWeatherData(locationKey)

    for clock_time in data:
        print(data[clock_time])


if __name__ == '__main__':
    main()

