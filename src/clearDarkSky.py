import re
import datetime
import time

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
            return int(text.split('%')[0])
        # Transparency is an enum
        case WeatherAttribute.TRANSPARENCY:
            return Transparency.getAttributeFromText(text)
        # Seeing is a float (x/5)
        case WeatherAttribute.SEEING:
            return float(REGEX_INT.search(text).group(0))/5
        # Darkness is a float (-4 to 6.5)
        case WeatherAttribute.DARKNESS:
            return float(REGEX_DECIMAL.search(text).group(0))
        # Smoke is an int (0 to 500 ug/m^3)
        case WeatherAttribute.SMOKE:
            if 'Smoke' in text:
                return 0
            return int(REGEX_INT.search(text).group(0))
        # Wind is a tuple of ints (0 to 45 mph)
        case WeatherAttribute.WIND:
            first = int(REGEX_INT.search(text).group(0))
            if first == 45:
                return (first, math.inf)
            second = int(REGEX_INT.findall(text)[1])
            return (first, second)
        # Humidity is a tuple of ints (0 to 100%)
        case WeatherAttribute.HUMIDITY:
            first = int(REGEX_INT.search(text).group(0))
            if text[0] == '<':
                return (0, first)
            second = int(REGEX_INT.findall(text)[1])
            return (first, second)
        # Temperature is a tuple of ints (-40 to 113 F)
        case WeatherAttribute.TEMPERATURE:
            first = int(REGEX_INT_NEG.search(text).group(0))
            if text[0] == '<':
                return (-math.inf, first)
            if first == 113:
                return (first, math.inf)
            second = int(REGEX_INT_NEG.findall(text)[1])
            return (first, second)


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


def main():
    # Set url
    locationKey = 'AlbanyNYkey'

    # Get data
    data = extractWeatherData(locationKey)

    for clock_time in data:
        print(data[clock_time])


if __name__ == '__main__':
    main()

