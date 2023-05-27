import datetime
import math

from clearDarkSkyEnums import WeatherAttribute, Transparency
from clearDarkSkyHelpers import getDateFromText, textToValue, \
    temperatureToTextRange, valueToText

class TestGetDateFromText:
    def test_getDateFromText_Simple(self):
        assert getDateFromText('2021-09-12') == datetime.datetime(2021, 9, 12)

    def test_getDateFromText_Real(self):
        text = 'Last updated 2023-05-25 13:12:13.'
        assert getDateFromText(text) == datetime.datetime(2023, 5, 25, 0, 0)


class TestTextToValue:
    # Cloud Cover
    def test_textToValue_CloudCover_Clear(self):
        assert textToValue(WeatherAttribute.CLOUD_COVER, 'Clear (00Z+17hr)') == 0

    def test_textToValue_CloudCover_Overcast(self):
        assert textToValue(WeatherAttribute.CLOUD_COVER, 'Overcast (00Z+17hr)') == 100

    def test_textToValue_CloudCover_Value(self):
        assert textToValue(WeatherAttribute.CLOUD_COVER, '50% covered (00Z+17hr)"') == 50

    def test_textToValue_CloudCover_Invalid(self):
        assert textToValue(WeatherAttribute.CLOUD_COVER, 'foo') == 100
    
    # Transparency
    def test_textToValue_Transparency(self):
        assert textToValue(WeatherAttribute.TRANSPARENCY, 'Below Average (00Z+49hr)') == Transparency.BELOW_AVERAGE

    # Seeing
    def test_textToValue_Seeing_ToCloudy(self):
        assert textToValue(WeatherAttribute.SEEING, 'Too cloudy to forecast (00Z+57hr)') == 0

    def test_textToValue_Seeing_Valid(self):
        assert textToValue(WeatherAttribute.SEEING, 'Average 3/5 (00Z+57hr)') == 3/5

    def test_textToValue_Seeing_Invalid(self):
        assert textToValue(WeatherAttribute.SEEING, 'foo') == 0

    # Darkness
    def test_textToValue_Darkness_Valid_Neg(self):
        assert textToValue(WeatherAttribute.DARKNESS, 'Limiting Mag:-4.8, SunAlt: -9.7°, MoonAlt -11.1°, MoonIllum 1%') == -4.8

    def test_textToValue_Darkness_Valid_Pos(self):
        assert textToValue(WeatherAttribute.DARKNESS, 'Limiting Mag:4.8, SunAlt: 9.7°, MoonAlt 11.1°, MoonIllum 1%') == 4.8

    def test_textToValue_Darkness_Invalid(self):
        assert textToValue(WeatherAttribute.DARKNESS, 'foo') == -4

    # Smoke
    def test_textToValue_Smoke_NoSmoke(self):
        assert textToValue(WeatherAttribute.SMOKE, 'No Smoke (12Z+18hr)') == 0

    def test_textToValue_Smoke_Smoke(self):
        assert textToValue(WeatherAttribute.SMOKE, '2ug/m^3 (12Z+68hr)') == 2

    def test_textToValue_Smoke_Invalid(self):
        assert textToValue(WeatherAttribute.SMOKE, 'foo') == 500

    # Wind
    def test_textToValue_Wind_Max(self):
        assert textToValue(WeatherAttribute.WIND, '>45 mph (00Z+6hr)') == (45, math.inf)

    def test_textToValue_Wind_Valid(self):
        assert textToValue(WeatherAttribute.WIND, '12 to 16 mph (00Z+6hr)') == (12, 16)

    def test_textToValue_Wind_Invalid(self):
        assert textToValue(WeatherAttribute.WIND, 'foo') == (45, math.inf)

    # Humidity
    def test_textToValue_Humidity_Min(self):
        assert textToValue(WeatherAttribute.HUMIDITY, '<25% (00Z+68hr)') == (0, 25)

    def test_textToValue_Humidity_Valid(self):
        assert textToValue(WeatherAttribute.HUMIDITY, '25% to 30% (00Z+67hr)"') == (25, 30)

    def test_textToValue_Humidity_Invalid(self):
        assert textToValue(WeatherAttribute.HUMIDITY, 'foo') == (95, 100)

    # Temperature
    def test_textToValue_Temperature_Min(self):
        assert textToValue(WeatherAttribute.TEMPERATURE, '< -40F(00Z+68hr)') == (-math.inf, -40)

    def test_textToValue_Temperature_Max(self):
        assert textToValue(WeatherAttribute.TEMPERATURE, '>113F (00Z+68hr)') == (113, math.inf)

    def test_textToValue_Temperature_Valid(self):
        assert textToValue(WeatherAttribute.TEMPERATURE, '50F to 59F (00Z+6hr)') == (50, 59)

    def test_textToValue_Temperature_Valid_Neg(self):
        assert textToValue(WeatherAttribute.TEMPERATURE, '-3F to 5F (00Z+6hr)') == (-3, 5)

    def test_textToValue_Temperature_Invalid(self):
        assert textToValue(WeatherAttribute.TEMPERATURE, 'foo') == (113, math.inf)

class TestTemperatureToTextRange:
    def test_temperatureToTextRange_Min(self):
        assert temperatureToTextRange(-41) == '< -40F'

    def test_temperatureToTextRange_Max(self):
        assert temperatureToTextRange(114) == '> 113F'

    def test_temperatureToTextRange_Valid(self):
        assert temperatureToTextRange(52) == '50F to 59F'

    def test_temperatureToTextRange_Valid_Neg(self):
        assert temperatureToTextRange(-1) == '-3F to 5F'

class TestValueToText:
    # Cloud Cover
    def test_valueToText_CloudCover_Clear(self):
        assert valueToText(WeatherAttribute.CLOUD_COVER, 0) == 'Clear'

    def test_valueToText_CloudCover_Overcast(self):
        assert valueToText(WeatherAttribute.CLOUD_COVER, 100) == 'Overcast'

    def test_valueToText_CloudCover_Value(self):
        assert valueToText(WeatherAttribute.CLOUD_COVER, 50) == '50% covered'

    def test_valueToText_CloudCover_Invalid(self):
        assert valueToText(WeatherAttribute.CLOUD_COVER, 101) == 'Overcast'
    # Transparency
    def test_valueToText_Transparency(self):
        assert valueToText(WeatherAttribute.TRANSPARENCY, Transparency.BELOW_AVERAGE) == 'BELOW_AVERAGE'

    def test_valueToText_Transparency_Invalid(self):
        assert valueToText(WeatherAttribute.TRANSPARENCY, 5) == 'ERROR'

    # Seeing
    def test_valueToText_Seeing(self):
        assert valueToText(WeatherAttribute.SEEING, 1.0) == 'Excellent'
        assert valueToText(WeatherAttribute.SEEING, 0.8) == 'Good'
        assert valueToText(WeatherAttribute.SEEING, 0.6) == 'Average'
        assert valueToText(WeatherAttribute.SEEING, 0.4) == 'Poor'
        assert valueToText(WeatherAttribute.SEEING, 0.2) == 'Terrible'
        assert valueToText(WeatherAttribute.SEEING, 0.0) == 'Too cloudy to forecast'

    def test_valueToText_Seeing_Invalid(self):
        assert valueToText(WeatherAttribute.SEEING, 1.1) == 'ERROR'

    # Darkness
    def test_valueToText_Darkness(self):
        assert valueToText(WeatherAttribute.DARKNESS, 4.8) == '4.8'

    def test_valueToText_Darkness_Invalid(self):
        assert valueToText(WeatherAttribute.DARKNESS, 'foo') == 'foo'

    # Smoke
    def test_valueToText_SMOKE_NoSmoke(self):
        assert valueToText(WeatherAttribute.SMOKE, 0) == 'No Smoke'

    def test_valueToText_SMOKE(self):
        assert valueToText(WeatherAttribute.SMOKE, -4.8) == '-4.8 ug/m^3'

    def test_valueToText_SMOKE_Invalid(self):
        assert valueToText(WeatherAttribute.SMOKE, 'foo') == 'foo ug/m^3'

    # Wind
    def test_valueToText_Wind_Max(self):
        assert valueToText(WeatherAttribute.WIND, 47) == '>45 mph'

    def test_valueToText_Wind_Valid(self):
        assert valueToText(WeatherAttribute.WIND, 14) == '12 to 16 mph'

    def test_valueToText_Wind_Invalid(self):
        assert valueToText(WeatherAttribute.WIND, 'foo') == 'ERROR'

    # Humidity
    def test_valueToText_Humidity_Min(self):
        assert valueToText(WeatherAttribute.HUMIDITY, 3) == '<25%'

    def test_valueToText_Humidity_Max(self):
        assert valueToText(WeatherAttribute.HUMIDITY, 97) == '95% to 100%'

    def test_valueToText_Humidity_Valid(self):
        assert valueToText(WeatherAttribute.HUMIDITY, 67) == '65% to 70%'

    def test_valueToText_Humidity_Invalid(self):
        assert valueToText(WeatherAttribute.HUMIDITY, 'foo') == 'ERROR'

    # Temperature
    def test_valueToText_Temperature_Min(self):
        assert valueToText(WeatherAttribute.TEMPERATURE, (-41, 3)) == 'From (< -40F) to (-3F to 5F)'

    def test_valueToText_Temperature_Max(self):
        assert valueToText(WeatherAttribute.TEMPERATURE, (13, 114)) == 'From (5F to 14F) to (> 113F)'

    def test_valueToText_Temperature_Valid(self):
        assert valueToText(WeatherAttribute.TEMPERATURE, (52, 74)) == 'From (50F to 59F) to (68F to 77F)'

    def test_valueToText_Temperature_Valid_Neg(self):
        assert valueToText(WeatherAttribute.TEMPERATURE, 'foo') == 'ERROR'