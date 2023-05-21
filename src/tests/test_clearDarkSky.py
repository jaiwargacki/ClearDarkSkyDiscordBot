import pytest
import math
import datetime

import clearDarkSky

class TestPointInTime:
    def test_PointInTime_String(self):
        timestamp = datetime.datetime(2020, 1, 1, 12, 0, 0)
        pointInTime = clearDarkSky.PointInTime(timestamp)
        assert str(pointInTime) == '2020-01-01 12:00:00 with 0 attributes'

    def test_PointInTime_Repr(self):
        timestamp = datetime.datetime(2020, 1, 1, 12, 0, 0)
        pointInTime = clearDarkSky.PointInTime(timestamp)
        pointInTime.add(clearDarkSky.WeatherAttribute.CLOUD_COVER, 0)
        pointInTime.add(clearDarkSky.WeatherAttribute.TRANSPARENCY, clearDarkSky.Transparency.POOR)
        assert repr(pointInTime) == '2020-01-01 12:00:00\nWeatherAttribute.CLOUD_COVER: 0\nWeatherAttribute.TRANSPARENCY: Transparency.POOR\n'

    def test_PointInTime_Add(self):
        timestamp = datetime.datetime(2020, 1, 1, 12, 0, 0)
        pointInTime = clearDarkSky.PointInTime(timestamp)
        pointInTime.add(clearDarkSky.WeatherAttribute.CLOUD_COVER, 0)
        assert pointInTime.data[clearDarkSky.WeatherAttribute.CLOUD_COVER] == 0

    def test_PointInTime_Add_Darkness(self):
        timestamp = datetime.datetime(2020, 1, 1, 12, 0, 0)
        pointInTime = clearDarkSky.PointInTime(timestamp)
        pointInTime.add(clearDarkSky.WeatherAttribute.DARKNESS, 4.8)
        assert pointInTime.data[clearDarkSky.WeatherAttribute.DARKNESS] == [4.8]

    def test_PointInTime_Add_Darkness_Twice(self):
        timestamp = datetime.datetime(2020, 1, 1, 12, 0, 0)
        pointInTime = clearDarkSky.PointInTime(timestamp)
        pointInTime.add(clearDarkSky.WeatherAttribute.DARKNESS, 4.8)
        pointInTime.add(clearDarkSky.WeatherAttribute.DARKNESS, -4.8)
        assert pointInTime.data[clearDarkSky.WeatherAttribute.DARKNESS] == [4.8, -4.8]
