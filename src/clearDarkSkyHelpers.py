""" Standalone helper functions for clearDarkSky project. """

import re
import datetime
import math

from clearDarkSkyConstants import *

# Regex for extracting data
REGEX_INT = re.compile(r'\d+')
REGEX_INT_NEG = re.compile(r'-?\d+')
REGEX_DECIMAL = re.compile(r'-?\d+\.\d+')

def getDateFromText(text: str) -> datetime:
    """ Returns a datetime object from a string. """
    regex_date = REGEX_INT.findall(text)
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
        case WeatherAttribute.CLOUD_COVER:
            try:
                return 0 if 'Clear' in text else (100 if 'Overcast' in text else int(text.split('%')[0]))
            except:
                return 100
        case WeatherAttribute.TRANSPARENCY:
            return Transparency.getAttributeFromText(text)
        case WeatherAttribute.SEEING:
            try:
                return 0.0 if 'Too cloudy to forecast' in text else float(REGEX_INT.search(text).group(0))/5
            except:
                return 0.0
        case WeatherAttribute.DARKNESS:
            try:
                return float(REGEX_DECIMAL.search(text).group(0))
            except:
                return -4
        case WeatherAttribute.SMOKE:
            try:
                return 0 if 'No Smoke' in text else int(REGEX_INT.search(text).group(0))
            except:
                return 500
        case WeatherAttribute.WIND:
            try:
                first = int(REGEX_INT.search(text).group(0))
                if first == 45:
                    return (first, math.inf)
                second = int(REGEX_INT.findall(text)[1])
                return (first, second)
            except:
                return (45, math.inf)
        case WeatherAttribute.HUMIDITY:
            try:
                first = int(REGEX_INT.search(text).group(0))
                if text[0] == '<':
                    return (0, first)
                second = int(REGEX_INT.findall(text)[1])
                return (first, second)
            except:
                return (95, 100)
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

def temperatureToTextRange(temp):
    """ Convert temperature to text range.
    Parameters:
        temp (int): The temperature to convert to text range.
    Returns:
        str: The text range of the temperature.
    """
    if temp < -40:
        return '< -40F'
    mins = [-40, -30, -21, -12, -3, 5, 14, 23, 32, 41, 50, 59, 68, 77, 86, 95, 104, 113]
    for i in range(1, len(mins)):
        if temp < mins[i]:
            return f'{mins[i-1]}F to {mins[i]}F'
    return '> 113F'


def valueToText(attribute, value):
    """ Convert value to text based on attribute.
    Parameters:
        attribute (WeatherAttribute): The attribute to convert value to text for.
        value (int, float, tuple, or enum): The value to convert to text.
    Returns:
        str: The text of the value.
    """
    try:
        match attribute:
            case WeatherAttribute.CLOUD_COVER:
                if value == 0:
                    return 'Clear'
                elif value < 100:
                    return str(value) + '% covered'
                return 'Overcast'
            case WeatherAttribute.TRANSPARENCY:
                return value.name
            case WeatherAttribute.SEEING:
                return SEEING_VALUE_TO_TEXT[value]
            case WeatherAttribute.DARKNESS:
                return str(value)
            case WeatherAttribute.SMOKE:
                return 'No Smoke' if value == 0 else (str(value) + ' ug/m^3')
            case WeatherAttribute.WIND:
                if value <= 5:
                    return '0 to 5 mph'
                elif value <= 11:
                    return '6 to 11 mph'
                elif value <= 16:
                    return '12 to 16 mph'
                elif value <= 28:
                    return '17 to 28 mph'
                elif value <= 45:
                    return '29 to 45 mph'
                return '>45 mph'
            case WeatherAttribute.HUMIDITY:
                if value < 25:
                    return '<25%'
                for i in range(25, 100, 5):
                    if value <= i:
                        return f'{i-5}% to {i}%'
                return '95% to 100%'
            case WeatherAttribute.TEMPERATURE:
                return f'From ({temperatureToTextRange(value[0])}) to ({temperatureToTextRange(value[1])})'
    except:
        return 'ERROR'
    