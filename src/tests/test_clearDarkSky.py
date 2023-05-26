import pytest
import math
import datetime
import random
import os

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

class TestAlertProfile:
    def test_AlertProfile_String(self):
        alertProfile = clearDarkSky.AlertProfile('user', 'name of profile')
        assert str(alertProfile) == 'name of profile by user'

    def test_AlertProfile_Repr(self):
        alertProfile = clearDarkSky.AlertProfile('user', 'name of profile', 'location')
        alertProfile.add(clearDarkSky.WeatherAttribute.CLOUD_COVER, 10)
        alertProfile.add(clearDarkSky.WeatherAttribute.TRANSPARENCY, clearDarkSky.Transparency.POOR)
        assert repr(alertProfile) == 'Alert profile name of profile for location.\n\nCurrent alert profile:\nCLOUD_COVER: 10\nTRANSPARENCY: Transparency.POOR\nConditions must occur for at least 0 hour(s).'

    def test_AlertProfile_Duration(self):
        alertProfile = clearDarkSky.AlertProfile('user', 'name of profile')
        assert alertProfile.get(clearDarkSky.AlertProfile.DURATION) == 0
        alertProfile.setDuration(10)
        assert alertProfile.get(clearDarkSky.AlertProfile.DURATION) == 10

    def test_AlertProfile_Add(self):
        alertProfile = clearDarkSky.AlertProfile('user', 'name of profile')
        alertProfile.add(clearDarkSky.WeatherAttribute.HUMIDITY, 50)
        assert alertProfile.get(clearDarkSky.WeatherAttribute.HUMIDITY) == 50

    def test_AlertProfile_Remove(self):
        alertProfile = clearDarkSky.AlertProfile('user', 'name of profile')
        alertProfile.add(clearDarkSky.WeatherAttribute.SEEING, 0.8)
        assert alertProfile.get(clearDarkSky.WeatherAttribute.SEEING) == 0.8
        alertProfile.remove(clearDarkSky.WeatherAttribute.SEEING)
        assert alertProfile.get(clearDarkSky.WeatherAttribute.SEEING) == None

    def test_AlertProfile_CheckForAlert_NoMatches(self):
        weatherData = dict()
        startDay = datetime.datetime(2020, 1, 1, 12, 0, 0)
        for i in range(0, 80):
            timestamp = startDay + datetime.timedelta(minutes=i)
            pointInTime = clearDarkSky.PointInTime(timestamp)
            pointInTime.add(clearDarkSky.WeatherAttribute.CLOUD_COVER, random.randint(5, 100))
            pointInTime.add(clearDarkSky.WeatherAttribute.TRANSPARENCY, clearDarkSky.Transparency(random.randint(1, 5)))
            pointInTime.add(clearDarkSky.WeatherAttribute.SEEING, random.randint(0, 4) / 5)
            for j in range(0, random.randint(0, 4)):
                pointInTime.add(clearDarkSky.WeatherAttribute.DARKNESS, random.randint(-4, 4))
            pointInTime.add(clearDarkSky.WeatherAttribute.SMOKE, random.randint(2, 500))
            wind = random.randint(5, 50)
            pointInTime.add(clearDarkSky.WeatherAttribute.WIND, (wind, wind + 10))
            humidity = random.randint(10, 100)
            pointInTime.add(clearDarkSky.WeatherAttribute.HUMIDITY, (humidity, humidity + 10))
            temp = random.randint(-40, 50)
            pointInTime.add(clearDarkSky.WeatherAttribute.TEMPERATURE, (temp, temp + 10))
            weatherData[timestamp] = pointInTime

        alertProfile = clearDarkSky.AlertProfile('user', 'name of profile')
        alertProfile.setDuration(1)
        alertProfile.add(clearDarkSky.WeatherAttribute.CLOUD_COVER, 2)
        alertProfile.add(clearDarkSky.WeatherAttribute.TRANSPARENCY, clearDarkSky.Transparency.TRANSPARENT)
        alertProfile.add(clearDarkSky.WeatherAttribute.SEEING, 1.0)
        alertProfile.add(clearDarkSky.WeatherAttribute.DARKNESS, 4.5)
        alertProfile.add(clearDarkSky.WeatherAttribute.SMOKE, 1)
        alertProfile.add(clearDarkSky.WeatherAttribute.WIND, 3)
        alertProfile.add(clearDarkSky.WeatherAttribute.HUMIDITY, 5)
        alertProfile.add(clearDarkSky.WeatherAttribute.TEMPERATURE, (66, 80))
        
        alerts = alertProfile.checkForAlert(weatherData)
        assert alerts == []

    def test_AlertProfile_CheckForAlert_Match(self):
        weatherData = dict()
        startDay = datetime.datetime(2020, 1, 1, 12, 0, 0)
        for i in range(0, 80):
            timestamp = startDay + datetime.timedelta(hours=i)
            pointInTime = clearDarkSky.PointInTime(timestamp)
            pointInTime.add(clearDarkSky.WeatherAttribute.CLOUD_COVER, random.randint(0, 95))
            pointInTime.add(clearDarkSky.WeatherAttribute.TRANSPARENCY, clearDarkSky.Transparency(random.randint(0, 4)))
            pointInTime.add(clearDarkSky.WeatherAttribute.SEEING, random.randint(1, 5) / 5)
            for j in range(0, 4):
                pointInTime.add(clearDarkSky.WeatherAttribute.DARKNESS, random.randint(-3, 6))
            pointInTime.add(clearDarkSky.WeatherAttribute.SMOKE, random.randint(2, 400))
            wind = random.randint(5, 20)
            pointInTime.add(clearDarkSky.WeatherAttribute.WIND, (wind, wind + 10))
            humidity = random.randint(10, 70)
            pointInTime.add(clearDarkSky.WeatherAttribute.HUMIDITY, (humidity, humidity + 10))
            temp = random.randint(-20, 70)
            pointInTime.add(clearDarkSky.WeatherAttribute.TEMPERATURE, (temp, temp + 10))
            weatherData[timestamp] = pointInTime

        alertProfile = clearDarkSky.AlertProfile('user', 'name of profile')
        alertProfile.setDuration(1)
        alertProfile.add(clearDarkSky.WeatherAttribute.CLOUD_COVER, 100)
        alertProfile.add(clearDarkSky.WeatherAttribute.TRANSPARENCY, clearDarkSky.Transparency.TOO_CLOUDY)
        alertProfile.add(clearDarkSky.WeatherAttribute.SEEING, 0.0)
        alertProfile.add(clearDarkSky.WeatherAttribute.DARKNESS, -4.0)
        alertProfile.add(clearDarkSky.WeatherAttribute.SMOKE, 500)
        alertProfile.add(clearDarkSky.WeatherAttribute.WIND, 45)
        alertProfile.add(clearDarkSky.WeatherAttribute.HUMIDITY, 95)
        alertProfile.add(clearDarkSky.WeatherAttribute.TEMPERATURE, (-30, 100))
        
        alerts = alertProfile.checkForAlert(weatherData)
        assert len(alerts) == 1
        assert alerts[0] == (startDay, startDay + datetime.timedelta(hours=79))

    def test_AlertProfile_CheckForAlert_MultipleMatches(self):
        weatherData = dict()
        startDay = datetime.datetime(2020, 1, 1, 12, 0, 0)
        for i in range(0, 80):
            timestamp = startDay + datetime.timedelta(hours=i)
            pointInTime = clearDarkSky.PointInTime(timestamp)
            if i == 40:
                pointInTime.add(clearDarkSky.WeatherAttribute.CLOUD_COVER, 100)
            else:
                pointInTime.add(clearDarkSky.WeatherAttribute.CLOUD_COVER, random.randint(0, 95))
            pointInTime.add(clearDarkSky.WeatherAttribute.TRANSPARENCY, clearDarkSky.Transparency(random.randint(0, 4)))
            pointInTime.add(clearDarkSky.WeatherAttribute.SEEING, random.randint(1, 5) / 5)
            for j in range(0, 4):
                pointInTime.add(clearDarkSky.WeatherAttribute.DARKNESS, random.randint(-3, 6))
            pointInTime.add(clearDarkSky.WeatherAttribute.SMOKE, random.randint(2, 400))
            wind = random.randint(5, 20)
            pointInTime.add(clearDarkSky.WeatherAttribute.WIND, (wind, wind + 10))
            humidity = random.randint(10, 70)
            pointInTime.add(clearDarkSky.WeatherAttribute.HUMIDITY, (humidity, humidity + 10))
            temp = random.randint(-20, 70)
            pointInTime.add(clearDarkSky.WeatherAttribute.TEMPERATURE, (temp, temp + 10))
            weatherData[timestamp] = pointInTime

        alertProfile = clearDarkSky.AlertProfile('user', 'name of profile')
        alertProfile.setDuration(1)
        alertProfile.add(clearDarkSky.WeatherAttribute.CLOUD_COVER, 99)
        alertProfile.add(clearDarkSky.WeatherAttribute.TRANSPARENCY, clearDarkSky.Transparency.TOO_CLOUDY)
        alertProfile.add(clearDarkSky.WeatherAttribute.SEEING, 0.0)
        alertProfile.add(clearDarkSky.WeatherAttribute.DARKNESS, -4.0)
        alertProfile.add(clearDarkSky.WeatherAttribute.SMOKE, 500)
        alertProfile.add(clearDarkSky.WeatherAttribute.WIND, 45)
        alertProfile.add(clearDarkSky.WeatherAttribute.HUMIDITY, 95)
        alertProfile.add(clearDarkSky.WeatherAttribute.TEMPERATURE, (-30, 100))
        
        alerts = alertProfile.checkForAlert(weatherData)
        assert len(alerts) == 2
        assert alerts[0] == (startDay, startDay + datetime.timedelta(hours=39))
        assert alerts[1] == (startDay + datetime.timedelta(hours=41), startDay + datetime.timedelta(hours=79))

    def test_AlertProfile_CheckForAlert_NoAttributes(self):
        weatherData = dict()
        startDay = datetime.datetime(2020, 1, 1, 12, 0, 0)
        for i in range(0, 80):
            timestamp = startDay + datetime.timedelta(hours=i)
            pointInTime = clearDarkSky.PointInTime(timestamp)
            pointInTime.add(clearDarkSky.WeatherAttribute.CLOUD_COVER, random.randint(0, 95))
            pointInTime.add(clearDarkSky.WeatherAttribute.TRANSPARENCY, clearDarkSky.Transparency(random.randint(0, 4)))
            pointInTime.add(clearDarkSky.WeatherAttribute.SEEING, random.randint(1, 5) / 5)
            for j in range(0, 4):
                pointInTime.add(clearDarkSky.WeatherAttribute.DARKNESS, random.randint(-3, 6))
            pointInTime.add(clearDarkSky.WeatherAttribute.SMOKE, random.randint(2, 400))
            wind = random.randint(5, 20)
            pointInTime.add(clearDarkSky.WeatherAttribute.WIND, (wind, wind + 10))
            humidity = random.randint(10, 70)
            pointInTime.add(clearDarkSky.WeatherAttribute.HUMIDITY, (humidity, humidity + 10))
            temp = random.randint(-20, 70)
            pointInTime.add(clearDarkSky.WeatherAttribute.TEMPERATURE, (temp, temp + 10))
            weatherData[timestamp] = pointInTime

        alertProfile = clearDarkSky.AlertProfile('user', 'name of profile')
        alerts = alertProfile.checkForAlert(weatherData)
        assert len(alerts) == 1
        assert alerts[0] == (startDay, startDay + datetime.timedelta(hours=79))

    def test_AlertProfile_Save(self):
        alertProfile = clearDarkSky.AlertProfile('user', 'name of profile')
        alertProfile.save()
        assert os.path.exists('AlertProfiles/user-name of profile.json')
        os.remove('AlertProfiles/user-name of profile.json')

    def test_AlertProfile_Delete_Exists(self):
        alertProfile = clearDarkSky.AlertProfile('user', 'name of profile')
        alertProfile.save()
        assert os.path.exists('AlertProfiles/user-name of profile.json')
        assert alertProfile.delete()
        assert not os.path.exists('AlertProfiles/user-name of profile.json')

    def test_AlertProfile_Delete_NotExists(self):
        alertProfile = clearDarkSky.AlertProfile('user', 'name of profile')
        assert not alertProfile.delete()

    def test_AlertProfile_Load(self):
        alertProfile = clearDarkSky.AlertProfile('user', 'name of profile')
        alertProfile.setDuration(123)
        alertProfile.save()
        alertProfile2 = clearDarkSky.AlertProfile('user', 'name of profile')
        alertProfile2.load()
        assert alertProfile.get(clearDarkSky.AlertProfile.DURATION) == alertProfile2.get(clearDarkSky.AlertProfile.DURATION)
        os.remove('AlertProfiles/user-name of profile.json')

    def test_AlertProfile_Load_NotFound(self):
        alertProfile = clearDarkSky.AlertProfile('not found', 'name of profile')
        try:
            alertProfile.load()
            assert False
        except:
            assert True

    def test_AlertProfile_GetAll_None(self):
        assert clearDarkSky.AlertProfile.getAll('user_none') == []

    def test_AlertProfile_GetAll(self):
        alertProfile = clearDarkSky.AlertProfile('userAll', 'profile 1')
        alertProfile.save()
        alertProfile = clearDarkSky.AlertProfile('userAll', 'profile 2')
        alertProfile.save()
        assert len(clearDarkSky.AlertProfile.getAll('userAll')) == 2
        os.remove('AlertProfiles/userAll-profile 1.json')
        os.remove('AlertProfiles/userAll-profile 2.json')
