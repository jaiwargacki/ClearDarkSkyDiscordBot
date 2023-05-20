import pytest
import math
import datetime

import clearDarkSky

class TestTextToValue:
    # Cloud Cover
    def test_textToValue_CloudCover_Clear(self):
        assert clearDarkSky.textToValue(clearDarkSky.WeatherAttribute.CLOUD_COVER, 'Clear (00Z+17hr)') == 0

    def test_textToValue_CloudCover_Overcast(self):
        assert clearDarkSky.textToValue(clearDarkSky.WeatherAttribute.CLOUD_COVER, 'Overcast (00Z+17hr)') == 100

    def test_textToValue_CloudCover_Value(self):
        assert clearDarkSky.textToValue(clearDarkSky.WeatherAttribute.CLOUD_COVER, '50% covered (00Z+17hr)"') == 50

    def test_textToValue_CloudCover_Invalid(self):
        assert clearDarkSky.textToValue(clearDarkSky.WeatherAttribute.CLOUD_COVER, 'foo') == 100
    
    # Transparency
    def test_textToValue_Transparency(self):
        assert clearDarkSky.textToValue(clearDarkSky.WeatherAttribute.TRANSPARENCY, 'Below Average (00Z+49hr)') == clearDarkSky.Transparency.BELOW_AVERAGE

    # Seeing
    def test_textToValue_Seeing_Valid(self):
        assert clearDarkSky.textToValue(clearDarkSky.WeatherAttribute.SEEING, 'Average 3/5 (00Z+57hr)') == 3/5

    def test_textToValue_Seeing_Invalid(self):
        assert clearDarkSky.textToValue(clearDarkSky.WeatherAttribute.SEEING, 'foo') == 1/5

    # Darkness
    def test_textToValue_Darkness_Valid_Neg(self):
        assert clearDarkSky.textToValue(clearDarkSky.WeatherAttribute.DARKNESS, 'Limiting Mag:-4.8, SunAlt: -9.7°, MoonAlt -11.1°, MoonIllum 1%') == -4.8

    def test_textToValue_Darkness_Valid_Pos(self):
        assert clearDarkSky.textToValue(clearDarkSky.WeatherAttribute.DARKNESS, 'Limiting Mag:4.8, SunAlt: 9.7°, MoonAlt 11.1°, MoonIllum 1%') == 4.8

    def test_textToValue_Darkness_Invalid(self):
        assert clearDarkSky.textToValue(clearDarkSky.WeatherAttribute.DARKNESS, 'foo') == -4

    # Smoke
    def test_textToValue_Smoke_NoSmoke(self):
        assert clearDarkSky.textToValue(clearDarkSky.WeatherAttribute.SMOKE, 'No Smoke (12Z+18hr)') == 0

    def test_textToValue_Smoke_Smoke(self):
        assert clearDarkSky.textToValue(clearDarkSky.WeatherAttribute.SMOKE, '2ug/m^3 (12Z+68hr)') == 2

    def test_textToValue_Smoke_Invalid(self):
        assert clearDarkSky.textToValue(clearDarkSky.WeatherAttribute.SMOKE, 'foo') == 500

    # Wind
    def test_textToValue_Wind_Max(self):
        assert clearDarkSky.textToValue(clearDarkSky.WeatherAttribute.WIND, '>45 mph (00Z+6hr)') == (45, math.inf)

    def test_textToValue_Wind_Valid(self):
        assert clearDarkSky.textToValue(clearDarkSky.WeatherAttribute.WIND, '12 to 16 mph (00Z+6hr)') == (12, 16)

    def test_textToValue_Wind_Invalid(self):
        assert clearDarkSky.textToValue(clearDarkSky.WeatherAttribute.WIND, 'foo') == (45, math.inf)

    # Humidity
    def test_textToValue_Humidity_Min(self):
        assert clearDarkSky.textToValue(clearDarkSky.WeatherAttribute.HUMIDITY, '<25% (00Z+68hr)') == (0, 25)

    def test_textToValue_Humidity_Valid(self):
        assert clearDarkSky.textToValue(clearDarkSky.WeatherAttribute.HUMIDITY, '25% to 30% (00Z+67hr)"') == (25, 30)

    def test_textToValue_Humidity_Invalid(self):
        assert clearDarkSky.textToValue(clearDarkSky.WeatherAttribute.HUMIDITY, 'foo') == (95, 100)

    # Temperature
    def test_textToValue_Temperature_Min(self):
        assert clearDarkSky.textToValue(clearDarkSky.WeatherAttribute.TEMPERATURE, '< -40F(00Z+68hr)') == (-math.inf, -40)

    def test_textToValue_Temperature_Max(self):
        assert clearDarkSky.textToValue(clearDarkSky.WeatherAttribute.TEMPERATURE, '>113F (00Z+68hr)') == (113, math.inf)

    def test_textToValue_Temperature_Valid(self):
        assert clearDarkSky.textToValue(clearDarkSky.WeatherAttribute.TEMPERATURE, '50F to 59F (00Z+6hr)') == (50, 59)

    def test_textToValue_Temperature_Valid_Neg(self):
        assert clearDarkSky.textToValue(clearDarkSky.WeatherAttribute.TEMPERATURE, '-3F to 5F (00Z+6hr)') == (-3, 5)

    def test_textToValue_Temperature_Invalid(self):
        assert clearDarkSky.textToValue(clearDarkSky.WeatherAttribute.TEMPERATURE, 'foo') == (113, math.inf)

class TestPointInTime:
    def test_PointInTime_String(self):
        timestamp = datetime.datetime(2020, 1, 1, 12, 0, 0)
        pointInTime = clearDarkSky.PointInTime(timestamp)
        assert str(pointInTime) == '2020-01-01 12:00:00 with 0 attributes'

    def test_PointInTime_Repr(self):
        timestamp = datetime.datetime(2020, 1, 1, 12, 0, 0)
        pointInTime = clearDarkSky.PointInTime(timestamp)
        pointInTime.add(clearDarkSky.WeatherAttribute.CLOUD_COVER, 'Clear')
        pointInTime.add(clearDarkSky.WeatherAttribute.TRANSPARENCY, 'Poor')
        assert repr(pointInTime) == '2020-01-01 12:00:00\nWeatherAttribute.CLOUD_COVER: 0\nWeatherAttribute.TRANSPARENCY: Transparency.POOR\n'

    def test_PointInTime_Add(self):
        timestamp = datetime.datetime(2020, 1, 1, 12, 0, 0)
        pointInTime = clearDarkSky.PointInTime(timestamp)
        pointInTime.add(clearDarkSky.WeatherAttribute.CLOUD_COVER, 'Clear')
        assert pointInTime.data[clearDarkSky.WeatherAttribute.CLOUD_COVER] == 0

    def test_PointInTime_Add_Darkness(self):
        timestamp = datetime.datetime(2020, 1, 1, 12, 0, 0)
        pointInTime = clearDarkSky.PointInTime(timestamp)
        pointInTime.add(clearDarkSky.WeatherAttribute.DARKNESS, '4.8')
        assert pointInTime.data[clearDarkSky.WeatherAttribute.DARKNESS] == [4.8]

    def test_PointInTime_Add_Darkness_Twice(self):
        timestamp = datetime.datetime(2020, 1, 1, 12, 0, 0)
        pointInTime = clearDarkSky.PointInTime(timestamp)
        pointInTime.add(clearDarkSky.WeatherAttribute.DARKNESS, '4.8')
        pointInTime.add(clearDarkSky.WeatherAttribute.DARKNESS, '-4.8')
        assert pointInTime.data[clearDarkSky.WeatherAttribute.DARKNESS] == [4.8, -4.8]