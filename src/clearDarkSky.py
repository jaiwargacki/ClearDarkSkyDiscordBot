import re
import datetime
import time
import math
import json
import os

import requests
from bs4 import BeautifulSoup

from clearDarkSkyEnums import *
from clearDarkSkyOptions import SEEING_TO_TEXT, getWindValueRange, getHumidityValueRange, getTemperatureValueRangeRange


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
        return f'{self.timestamp} with {len(self.data)} attributes'

    def __repr__(self):
        """ Return a string representation of the point in time. """
        output = f'{self.timestamp}\n'
        for attribute in self.data:
            output += f'{attribute}: {self.data[attribute]}\n'
        return output

    def add(self, attribute, value):
        """ Add a weather attribute and its value to the point in time.
        Parameters:
            attribute (WeatherAttribute): The attribute to add.
            value (int, float, enum or tuple): The value of the attribute.
        """
        if attribute == WeatherAttribute.DARKNESS:
            # Darkness is a special because it is provide in 15 min increments 
            if attribute not in self.data:
                self.data[attribute] = [value]
            else:
                self.data[attribute].append(value)
        else:
            self.data[attribute] = value


class AlertProfile:
    """ An alert profile for a user. """

    DIRECTORY = 'AlertProfiles'

    LOCATION = 'LOCATION'
    DURATION = 'DURATION'
    
    def __init__(self, username, name, location='0'):
        """ Initialize the alert profile with a username and name.
        Parameters:
            username (str): The username of the alert profile.
            name (str): The name of the alert profile.
            location (str): The location key of the alert profile.
        """
        self.username = str(username)
        self.name = name
        self.__attributes = dict()
        self.__attributes[AlertProfile.LOCATION] = location
        self.__attributes[AlertProfile.DURATION] = 0

    def __str__(self):
        """ Return a string representation of the alert profile. """
        return f'{self.name} by {self.username}'

    def __repr__(self):
        """ Return a string representation of the alert profile. """
        response = f"Alert profile {self.name} for {self.get(AlertProfile.LOCATION)}."
        response += f"\n\nCurrent alert profile:"
        noConditions = True
        for attribute in WeatherAttribute:
            if self.get(attribute) is not None:
                if attribute == WeatherAttribute.SEEING:
                    response += f"\n{attribute.name}: {SEEING_TO_TEXT[self.get(attribute)]}"
                elif attribute == WeatherAttribute.WIND:
                    response += f"\n{attribute.name}: {getWindValueRange(self.get(attribute))}"
                elif attribute == WeatherAttribute.HUMIDITY:
                    response += f"\n{attribute.name}: {getHumidityValueRange(self.get(attribute))}"
                elif attribute == WeatherAttribute.TEMPERATURE:
                    response += f"\n{attribute.name}: {getTemperatureValueRangeRange(self.get(attribute))}"
                else:
                    response += f"\n{attribute.name}: {self.get(attribute)}"
                if attribute == WeatherAttribute.SMOKE:
                    response += f" ug/m^3"
            noConditions = False
        if noConditions:
            response += "\nNo conditions set."
        response += f"\nConditions must occur for at least {self.get(AlertProfile.DURATION)} hour(s)."
        return response

    def setDuration(self, duration):
        """ Set the duration of the alert profile.
        Parameters:
            duration (int): The duration of the alert profile.
        """
        self.__attributes[AlertProfile.DURATION] = duration

    def add(self, attribute, value):
        """ Add an attribute to the alert profile.
        Parameters:
            attribute (WeatherAttribute): The attribute to add.
            value (int, float, enum or tuple): The value of the attribute.
        """
        self.__attributes[str(attribute)] = value

    def remove(self, attribute):
        """ Remove an attribute from the alert profile.
        Parameters:
            attribute (WeatherAttribute): The attribute to remove.
        """
        del self.__attributes[str(attribute)]

    def get(self, attribute):
        """ Get the value of an attribute.
        Parameters:
            attribute (WeatherAttribute): The attribute to get.
        Returns:
            int, float, enum or tuple: The value of the attribute.
        """
        try:
            return self.__attributes[str(attribute)]
        except KeyError:
            return None

    def __checkForCloudCoverage(self, hour):
        """ Check if the cloud coverage matches the alert profile.
        Parameters:
            hour (PointInTime): The hour to check.
        Returns:
            bool: True if the cloud coverage matches the alert profile, False otherwise.
        """
        try:
            return hour.data[WeatherAttribute.CLOUD_COVER] <= self.get(WeatherAttribute.CLOUD_COVER)
        except:
            return True

    def __checkForTransparency(self, hour):
        """ Check if the transparency matches the alert profile.
        Parameters:
            hour (PointInTime): The hour to check.
        Returns:
            bool: True if the transparency matches the alert profile, False otherwise.
        """
        try:
            return hour.data[WeatherAttribute.TRANSPARENCY].value  <= self.get(WeatherAttribute.TRANSPARENCY).value
        except:
            return True

    def __checkForSeeing(self, hour):
        """ Check if the seeing matches the alert profile.
        Parameters:
            hour (PointInTime): The hour to check.
        Returns:
            bool: True if the seeing matches the alert profile, False otherwise.
        """
        try:
            return hour.data[WeatherAttribute.SEEING] >= self.get(WeatherAttribute.SEEING)
        except:
            return True

    def __checkForDarkness(self, hour):
        """ Check if the darkness matches the alert profile.
        Parameters:
            hour (PointInTime): The hour to check.
        Returns:
            bool: True if the darkness matches the alert profile, False otherwise.
        """
        try:
            for darkness in hour.data[WeatherAttribute.DARKNESS]:
                if darkness >= self.get(WeatherAttribute.DARKNESS):
                    return True
            return False
        except:
            return True

    def __checkForSmoke(self, hour):
        """ Check if the smoke matches the alert profile.
        Parameters:
            hour (PointInTime): The hour to check.
        Returns:
            bool: True if the smoke matches the alert profile, False otherwise.
        """
        try:
            return hour.data[WeatherAttribute.SMOKE] <= self.get(WeatherAttribute.SMOKE)
        except:
            return True

    def __checkForWind(self, hour):
        """ Check if the wind matches the alert profile.
        Parameters:
            hour (PointInTime): The hour to check.
        Returns:
            bool: True if the wind matches the alert profile, False otherwise.
        """
        try:
            return min(hour.data[WeatherAttribute.WIND]) <= self.get(WeatherAttribute.WIND)
        except:
            return True

    def __checkForHumidity(self, hour):
        """ Check if the humidity matches the alert profile.
        Parameters:
            hour (PointInTime): The hour to check.
        Returns:
            bool: True if the humidity matches the alert profile, False otherwise.
        """
        try:
            return min(hour.data[WeatherAttribute.HUMIDITY]) <= self.get(WeatherAttribute.HUMIDITY)
        except:
            return True

    def __checkForTemperature(self, hour):
        """ Check if the temperature matches the alert profile.
        Parameters:
            hour (PointInTime): The hour to check.
        Returns:
            bool: True if the temperature matches the alert profile, False otherwise.
        """
        try:
            min_pass = min(hour.data[WeatherAttribute.TEMPERATURE]) >= min(self.get(WeatherAttribute.TEMPERATURE))
            max_pass = max(hour.data[WeatherAttribute.TEMPERATURE]) <= max(self.get(WeatherAttribute.TEMPERATURE))
            return min_pass and max_pass
        except:
            return True

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

    def checkForAlert(self, weatherData):
        """ Check if the weather data matches the alert profile.
        Parameters:
            weatherData (dictionary): A dictionary of PointInTime objects.
        Returns:
            list: A list of tuples datetime.datetime objects representing 
                the start and end of the matching conditions.
        """
        matches = []
        matching_num = 0
        start = None
        for h in range(0, len(weatherData)):
            key = list(weatherData.keys())[h]
            hour = weatherData[key]
            isValid = self.__checkHour(hour)
            if isValid:
                matching_num += 1
                if matching_num == 1:
                    start = hour.timestamp
            if not isValid and matching_num >= self.__attributes[AlertProfile.DURATION]:
                key = list(weatherData.keys())[h-1]
                end = weatherData[key].timestamp
                matches.append((start, end))
                matching_num = 0
            if h == len(weatherData) - 1 and matching_num >= self.__attributes[AlertProfile.DURATION]:
                end = weatherData[key].timestamp
                matches.append((start, end))
        return matches

    def __getFilename(self):
        """ Get the filename for the alert profile. """
        return AlertProfile.DIRECTORY + '/' + self.username + '-' + self.name + '.json'

    def save(self):
        """ Save the alert profile to file. """
        if not os.path.exists(AlertProfile.DIRECTORY):
            os.makedirs(AlertProfile.DIRECTORY)
        with open(self.__getFilename(), 'w') as f:
            transparency = self.get(WeatherAttribute.TRANSPARENCY)
            if transparency is not None:
                self.add(WeatherAttribute.TRANSPARENCY, transparency.value)
            json.dump(self.__attributes, f)
            if transparency is not None:
                self.add(WeatherAttribute.TRANSPARENCY, transparency)

    def delete(self):
        """ Delete the alert profile from file. """
        try:
            if os.path.exists(self.__getFilename()):
                os.remove(self.__getFilename())
                return True
        except:
            return False
        return False

    def load(self):
        """ Load the alert profile from file. """
        with open(self.__getFilename(), 'r') as f:
            self.__attributes = json.load(f)
            transparency = self.get(WeatherAttribute.TRANSPARENCY)
            if transparency is not None:
                self.add(WeatherAttribute.TRANSPARENCY, Transparency(transparency))

    @staticmethod
    def getAll(username):    
        """ Get all alert profiles for a user.
        Parameters:
            username (string): The username of the user.
        Returns:
            list: A list of AlertProfile objects.
        """
        username = str(username)
        profiles = []
        for filename in os.listdir(AlertProfile.DIRECTORY):
            if filename.startswith(username):
                profile = AlertProfile(username, filename.split('-')[1].split('.')[0])
                profile.load()
                profiles.append(profile)
        return profiles
