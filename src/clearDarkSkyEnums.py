""" Enumerations for the Clear Dark Sky Tool. """

from enum import Enum

class WeatherAttribute(Enum):
    """ Enum for the attributes of the weather. """
    CLOUD_COVER = 1
    TRANSPARENCY = 2
    SEEING = 3
    DARKNESS = 4
    SMOKE = 5
    WIND = 6
    HUMIDITY = 7
    TEMPERATURE = 8

class Transparency(Enum):
    """ Enum for the transparency of the sky. """
    TRANSPARENT = 0
    ABOVE_AVERAGE = 1
    AVERAGE = 2
    BELOW_AVERAGE = 3
    POOR = 4

    @staticmethod
    def getAttributeFromText(text):
        if 'Transparent' in text:
            return Transparency.TRANSPARENT
        elif 'Above Average' in text:
            return Transparency.ABOVE_AVERAGE
        elif 'Below Average' in text:
            return Transparency.BELOW_AVERAGE
        elif 'Average' in text:
            return Transparency.AVERAGE
        elif 'Poor' in text:
            return Transparency.POOR
        # Default to poor
        return Transparency.POOR