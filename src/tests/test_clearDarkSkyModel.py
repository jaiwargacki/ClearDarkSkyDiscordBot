import datetime
import random
import os

from clearDarkSkyModel import AlertProfile, PointInTime
from clearDarkSkyEnums import WeatherAttribute, Transparency

class TestPointInTime:
    def test_PointInTime_String(self):
        timestamp = datetime.datetime(2020, 1, 1, 12, 0, 0)
        pointInTime = PointInTime(timestamp)
        assert str(pointInTime) == '2020-01-01 12:00:00 with 0 attributes'

    def test_PointInTime_Repr(self):
        timestamp = datetime.datetime(2020, 1, 1, 12, 0, 0)
        pointInTime = PointInTime(timestamp)
        pointInTime.add(WeatherAttribute.CLOUD_COVER, 0)
        pointInTime.add(WeatherAttribute.TRANSPARENCY, Transparency.POOR)
        assert repr(pointInTime) == '2020-01-01 12:00:00\nWeatherAttribute.CLOUD_COVER: 0\nWeatherAttribute.TRANSPARENCY: Transparency.POOR\n'

    def test_PointInTime_Add(self):
        timestamp = datetime.datetime(2020, 1, 1, 12, 0, 0)
        pointInTime = PointInTime(timestamp)
        pointInTime.add(WeatherAttribute.CLOUD_COVER, 0)
        assert pointInTime.data[WeatherAttribute.CLOUD_COVER] == 0

    def test_PointInTime_Add_Darkness(self):
        timestamp = datetime.datetime(2020, 1, 1, 12, 0, 0)
        pointInTime = PointInTime(timestamp)
        pointInTime.add(WeatherAttribute.DARKNESS, 4.8)
        assert pointInTime.data[WeatherAttribute.DARKNESS] == [4.8]

    def test_PointInTime_Add_Darkness_Twice(self):
        timestamp = datetime.datetime(2020, 1, 1, 12, 0, 0)
        pointInTime = PointInTime(timestamp)
        pointInTime.add(WeatherAttribute.DARKNESS, 4.8)
        pointInTime.add(WeatherAttribute.DARKNESS, -4.8)
        assert pointInTime.data[WeatherAttribute.DARKNESS] == [4.8, -4.8]

class TestAlertProfile:
    def test_AlertProfile_String(self):
        alertProfile = AlertProfile('user', 'name of profile')
        assert str(alertProfile) == 'name of profile by user'

    def test_AlertProfile_Repr(self):
        alertProfile = AlertProfile('user', 'name of profile', 'location')
        alertProfile.setDuration(7)
        alertProfile.add(WeatherAttribute.CLOUD_COVER, 10)
        alertProfile.add(WeatherAttribute.TRANSPARENCY, Transparency.POOR)
        alertProfile.add(WeatherAttribute.SEEING, 0.8)
        alertProfile.add(WeatherAttribute.DARKNESS, 4.5)
        alertProfile.add(WeatherAttribute.SMOKE, 1)
        alertProfile.add(WeatherAttribute.WIND, 3)
        alertProfile.add(WeatherAttribute.HUMIDITY, 5)
        alertProfile.add(WeatherAttribute.TEMPERATURE, (10, 68))
        assert repr(alertProfile) == 'Alert profile name of profile for location.\n\nCurrent alert profile:\nCLOUD_COVER: 10% covered\nTRANSPARENCY: POOR\nSEEING: Good\nDARKNESS: 4.5\nSMOKE: 1 ug/m^3\nWIND: 0 to 5 mph\nHUMIDITY: <25%\nTEMPERATURE: From (5F to 14F) to (68F to 77F)\n\nConditions must occur for at least 7 hour(s).'

    def test_AlertProfile_Duration(self):
        alertProfile = AlertProfile('user', 'name of profile')
        assert alertProfile.get(AlertProfile.DURATION) == 0
        alertProfile.setDuration(10)
        assert alertProfile.get(AlertProfile.DURATION) == 10

    def test_AlertProfile_Add(self):
        alertProfile = AlertProfile('user', 'name of profile')
        alertProfile.add(WeatherAttribute.HUMIDITY, 50)
        assert alertProfile.get(WeatherAttribute.HUMIDITY) == 50

    def test_AlertProfile_Remove(self):
        alertProfile = AlertProfile('user', 'name of profile')
        alertProfile.add(WeatherAttribute.SEEING, 0.8)
        assert alertProfile.get(WeatherAttribute.SEEING) == 0.8
        alertProfile.remove(WeatherAttribute.SEEING)
        assert alertProfile.get(WeatherAttribute.SEEING) == None

    def test_AlertProfile_CheckForAlert_NoMatches(self):
        weatherData = dict()
        startDay = datetime.datetime(2020, 1, 1, 12, 0, 0)
        for i in range(0, 80):
            timestamp = startDay + datetime.timedelta(minutes=i)
            pointInTime = PointInTime(timestamp)
            pointInTime.add(WeatherAttribute.CLOUD_COVER, random.randint(5, 100))
            pointInTime.add(WeatherAttribute.TRANSPARENCY, Transparency(random.randint(1, 5)))
            pointInTime.add(WeatherAttribute.SEEING, random.randint(0, 4) / 5)
            for j in range(0, random.randint(0, 4)):
                pointInTime.add(WeatherAttribute.DARKNESS, random.randint(-4, 4))
            pointInTime.add(WeatherAttribute.SMOKE, random.randint(2, 500))
            wind = random.randint(5, 50)
            pointInTime.add(WeatherAttribute.WIND, (wind, wind + 10))
            humidity = random.randint(10, 100)
            pointInTime.add(WeatherAttribute.HUMIDITY, (humidity, humidity + 10))
            temp = random.randint(-40, 50)
            pointInTime.add(WeatherAttribute.TEMPERATURE, (temp, temp + 10))
            weatherData[timestamp] = pointInTime

        alertProfile = AlertProfile('user', 'name of profile')
        alertProfile.setDuration(1)
        alertProfile.add(WeatherAttribute.CLOUD_COVER, 2)
        alertProfile.add(WeatherAttribute.TRANSPARENCY, Transparency.TRANSPARENT)
        alertProfile.add(WeatherAttribute.SEEING, 1.0)
        alertProfile.add(WeatherAttribute.DARKNESS, 4.5)
        alertProfile.add(WeatherAttribute.SMOKE, 1)
        alertProfile.add(WeatherAttribute.WIND, 3)
        alertProfile.add(WeatherAttribute.HUMIDITY, 5)
        alertProfile.add(WeatherAttribute.TEMPERATURE, (66, 80))
        
        alerts = alertProfile.checkForAlert(weatherData)
        assert alerts == []

    def test_AlertProfile_CheckForAlert_Match(self):
        weatherData = dict()
        startDay = datetime.datetime(2020, 1, 1, 12, 0, 0)
        for i in range(0, 80):
            timestamp = startDay + datetime.timedelta(hours=i)
            pointInTime = PointInTime(timestamp)
            pointInTime.add(WeatherAttribute.CLOUD_COVER, random.randint(0, 95))
            pointInTime.add(WeatherAttribute.TRANSPARENCY, Transparency(random.randint(0, 4)))
            pointInTime.add(WeatherAttribute.SEEING, random.randint(1, 5) / 5)
            for j in range(0, 4):
                pointInTime.add(WeatherAttribute.DARKNESS, random.randint(-3, 6))
            pointInTime.add(WeatherAttribute.SMOKE, random.randint(2, 400))
            wind = random.randint(5, 20)
            pointInTime.add(WeatherAttribute.WIND, (wind, wind + 10))
            humidity = random.randint(10, 70)
            pointInTime.add(WeatherAttribute.HUMIDITY, (humidity, humidity + 10))
            temp = random.randint(-20, 70)
            pointInTime.add(WeatherAttribute.TEMPERATURE, (temp, temp + 10))
            weatherData[timestamp] = pointInTime

        alertProfile = AlertProfile('user', 'name of profile')
        alertProfile.setDuration(1)
        alertProfile.add(WeatherAttribute.CLOUD_COVER, 100)
        alertProfile.add(WeatherAttribute.TRANSPARENCY, Transparency.TOO_CLOUDY_TO_FORECAST)
        alertProfile.add(WeatherAttribute.SEEING, 0.0)
        alertProfile.add(WeatherAttribute.DARKNESS, -4.0)
        alertProfile.add(WeatherAttribute.SMOKE, 500)
        alertProfile.add(WeatherAttribute.WIND, 45)
        alertProfile.add(WeatherAttribute.HUMIDITY, 95)
        alertProfile.add(WeatherAttribute.TEMPERATURE, (-30, 100))
        
        alerts = alertProfile.checkForAlert(weatherData)
        assert len(alerts) == 1
        assert alerts[0] == (startDay, startDay + datetime.timedelta(hours=79))

    def test_AlertProfile_CheckForAlert_MultipleMatches(self):
        weatherData = dict()
        startDay = datetime.datetime(2020, 1, 1, 12, 0, 0)
        for i in range(0, 80):
            timestamp = startDay + datetime.timedelta(hours=i)
            pointInTime = PointInTime(timestamp)
            if i == 40:
                pointInTime.add(WeatherAttribute.CLOUD_COVER, 100)
            else:
                pointInTime.add(WeatherAttribute.CLOUD_COVER, random.randint(0, 95))
            pointInTime.add(WeatherAttribute.TRANSPARENCY, Transparency(random.randint(0, 4)))
            pointInTime.add(WeatherAttribute.SEEING, random.randint(1, 5) / 5)
            for j in range(0, 4):
                pointInTime.add(WeatherAttribute.DARKNESS, random.randint(-3, 6))
            pointInTime.add(WeatherAttribute.SMOKE, random.randint(2, 400))
            wind = random.randint(5, 20)
            pointInTime.add(WeatherAttribute.WIND, (wind, wind + 10))
            humidity = random.randint(10, 70)
            pointInTime.add(WeatherAttribute.HUMIDITY, (humidity, humidity + 10))
            temp = random.randint(-20, 70)
            pointInTime.add(WeatherAttribute.TEMPERATURE, (temp, temp + 10))
            weatherData[timestamp] = pointInTime

        alertProfile = AlertProfile('user', 'name of profile')
        alertProfile.setDuration(1)
        alertProfile.add(WeatherAttribute.CLOUD_COVER, 99)
        alertProfile.add(WeatherAttribute.TRANSPARENCY, Transparency.TOO_CLOUDY_TO_FORECAST)
        alertProfile.add(WeatherAttribute.SEEING, 0.0)
        alertProfile.add(WeatherAttribute.DARKNESS, -4.0)
        alertProfile.add(WeatherAttribute.SMOKE, 500)
        alertProfile.add(WeatherAttribute.WIND, 45)
        alertProfile.add(WeatherAttribute.HUMIDITY, 95)
        alertProfile.add(WeatherAttribute.TEMPERATURE, (-30, 100))
        
        alerts = alertProfile.checkForAlert(weatherData)
        assert len(alerts) == 2
        assert alerts[0] == (startDay, startDay + datetime.timedelta(hours=39))
        assert alerts[1] == (startDay + datetime.timedelta(hours=41), startDay + datetime.timedelta(hours=79))

    def test_AlertProfile_CheckForAlert_NoAttributes(self):
        weatherData = dict()
        startDay = datetime.datetime(2020, 1, 1, 12, 0, 0)
        for i in range(0, 80):
            timestamp = startDay + datetime.timedelta(hours=i)
            pointInTime = PointInTime(timestamp)
            pointInTime.add(WeatherAttribute.CLOUD_COVER, random.randint(0, 95))
            pointInTime.add(WeatherAttribute.TRANSPARENCY, Transparency(random.randint(0, 4)))
            pointInTime.add(WeatherAttribute.SEEING, random.randint(1, 5) / 5)
            for j in range(0, 4):
                pointInTime.add(WeatherAttribute.DARKNESS, random.randint(-3, 6))
            pointInTime.add(WeatherAttribute.SMOKE, random.randint(2, 400))
            wind = random.randint(5, 20)
            pointInTime.add(WeatherAttribute.WIND, (wind, wind + 10))
            humidity = random.randint(10, 70)
            pointInTime.add(WeatherAttribute.HUMIDITY, (humidity, humidity + 10))
            temp = random.randint(-20, 70)
            pointInTime.add(WeatherAttribute.TEMPERATURE, (temp, temp + 10))
            weatherData[timestamp] = pointInTime

        alertProfile = AlertProfile('user', 'name of profile')
        alerts = alertProfile.checkForAlert(weatherData)
        assert len(alerts) == 1
        assert alerts[0] == (startDay, startDay + datetime.timedelta(hours=79))

    def test_AlertProfile_Save(self):
        alertProfile = AlertProfile('user', 'name of profile')
        alertProfile.save()
        assert os.path.exists('AlertProfiles/user-name of profile.json')
        os.remove('AlertProfiles/user-name of profile.json')

    def test_AlertProfile_Delete_Exists(self):
        alertProfile = AlertProfile('user', 'name of profile')
        alertProfile.save()
        assert os.path.exists('AlertProfiles/user-name of profile.json')
        assert alertProfile.delete()
        assert not os.path.exists('AlertProfiles/user-name of profile.json')

    def test_AlertProfile_Delete_NotExists(self):
        alertProfile = AlertProfile('user', 'name of profile')
        assert not alertProfile.delete()

    def test_AlertProfile_Load(self):
        alertProfile = AlertProfile('user', 'name of profile')
        alertProfile.setDuration(123)
        alertProfile.save()
        alertProfile2 = AlertProfile('user', 'name of profile')
        alertProfile2.load()
        assert alertProfile.get(AlertProfile.DURATION) == alertProfile2.get(AlertProfile.DURATION)
        os.remove('AlertProfiles/user-name of profile.json')

    def test_AlertProfile_Load_NotFound(self):
        alertProfile = AlertProfile('not found', 'name of profile')
        try:
            alertProfile.load()
            assert False
        except:
            assert True

    def test_AlertProfile_GetAllForUser_None(self):
        assert AlertProfile.getAllForUser('user_none') == []

    def test_AlertProfile_GetAllForUser(self):
        alertProfile = AlertProfile('userAll', 'profile 1')
        alertProfile.save()
        alertProfile = AlertProfile('userAll', 'profile 2')
        alertProfile.save()
        assert len(AlertProfile.getAllForUser('userAll')) == 2
        os.remove('AlertProfiles/userAll-profile 1.json')
        os.remove('AlertProfiles/userAll-profile 2.json')
