import pytest
import math
import datetime

from bs4 import BeautifulSoup

import clearDarkSkyWeb

class TestValidateLocationKey:
    def test_validateLocationKey_Valid(self):
        assert clearDarkSkyWeb.validateLocationKey('AlbanyNY')

    def test_validateLocationKey_Invalid(self):
        assert not clearDarkSkyWeb.validateLocationKey('foo')

class TestExtractDate:
    def test_extractDate_Valid(self):
        html = '<table><tbody><tr><td><table><tbody><tr><td><embed width="1547" height="30" \
                src="/t/html_alerts/active_alert.html"></td></tr></tbody></table><font size="-1"> \
                Last updated 2023-05-25 13:12:13. </font><font size="-1" color="#00A000"><font \
                size="-1" color="#0000A">No Image below? Read <a href="/csk/faq/1.html">this</a>. \
                Not showing todays data? <a href="/csk/faq/6.html">Clear your cache</a>.</font></font>\
                </td></tr><tr><td><noindex> Also used by members of the <a \
                href="http://userweb.esu10.org/~murwille/PVAO/pvao.htm">Platte Valley Astronomical \
                Observers</a>.</td></tr><tr><td><embed width="1242" height="60" \
                src="https://www.cleardarksky.com/alerts/HstngCObNE.html"></td></tr></tbody></table>'
        soup = BeautifulSoup(html, "html.parser")
        assert clearDarkSkyWeb.extractDate(soup) == datetime.datetime(2023, 5, 25, 0, 0)

    def test_extractDate_Invalid(self):
        html = '<table><tbody><tr><td><table><tbody><tr><td><embed width="1547" height="30"'
        soup = BeautifulSoup(html, "html.parser")
        assert clearDarkSkyWeb.extractDate(soup) == datetime.datetime(1970, 1, 1)

class TestTextToValue:
    # Cloud Cover
    def test_textToValue_CloudCover_Clear(self):
        assert clearDarkSkyWeb.textToValue(clearDarkSkyWeb.WeatherAttribute.CLOUD_COVER, 'Clear (00Z+17hr)') == 0

    def test_textToValue_CloudCover_Overcast(self):
        assert clearDarkSkyWeb.textToValue(clearDarkSkyWeb.WeatherAttribute.CLOUD_COVER, 'Overcast (00Z+17hr)') == 100

    def test_textToValue_CloudCover_Value(self):
        assert clearDarkSkyWeb.textToValue(clearDarkSkyWeb.WeatherAttribute.CLOUD_COVER, '50% covered (00Z+17hr)"') == 50

    def test_textToValue_CloudCover_Invalid(self):
        assert clearDarkSkyWeb.textToValue(clearDarkSkyWeb.WeatherAttribute.CLOUD_COVER, 'foo') == 100
    
    # Transparency
    def test_textToValue_Transparency(self):
        assert clearDarkSkyWeb.textToValue(clearDarkSkyWeb.WeatherAttribute.TRANSPARENCY, 'Below Average (00Z+49hr)') == clearDarkSkyWeb.Transparency.BELOW_AVERAGE

    # Seeing
    def test_textToValue_Seeing_ToCloudy(self):
        assert clearDarkSkyWeb.textToValue(clearDarkSkyWeb.WeatherAttribute.SEEING, 'Too cloudy to forecast (00Z+57hr)') == 0

    def test_textToValue_Seeing_Valid(self):
        assert clearDarkSkyWeb.textToValue(clearDarkSkyWeb.WeatherAttribute.SEEING, 'Average 3/5 (00Z+57hr)') == 3/5

    def test_textToValue_Seeing_Invalid(self):
        assert clearDarkSkyWeb.textToValue(clearDarkSkyWeb.WeatherAttribute.SEEING, 'foo') == 0

    # Darkness
    def test_textToValue_Darkness_Valid_Neg(self):
        assert clearDarkSkyWeb.textToValue(clearDarkSkyWeb.WeatherAttribute.DARKNESS, 'Limiting Mag:-4.8, SunAlt: -9.7°, MoonAlt -11.1°, MoonIllum 1%') == -4.8

    def test_textToValue_Darkness_Valid_Pos(self):
        assert clearDarkSkyWeb.textToValue(clearDarkSkyWeb.WeatherAttribute.DARKNESS, 'Limiting Mag:4.8, SunAlt: 9.7°, MoonAlt 11.1°, MoonIllum 1%') == 4.8

    def test_textToValue_Darkness_Invalid(self):
        assert clearDarkSkyWeb.textToValue(clearDarkSkyWeb.WeatherAttribute.DARKNESS, 'foo') == -4

    # Smoke
    def test_textToValue_Smoke_NoSmoke(self):
        assert clearDarkSkyWeb.textToValue(clearDarkSkyWeb.WeatherAttribute.SMOKE, 'No Smoke (12Z+18hr)') == 0

    def test_textToValue_Smoke_Smoke(self):
        assert clearDarkSkyWeb.textToValue(clearDarkSkyWeb.WeatherAttribute.SMOKE, '2ug/m^3 (12Z+68hr)') == 2

    def test_textToValue_Smoke_Invalid(self):
        assert clearDarkSkyWeb.textToValue(clearDarkSkyWeb.WeatherAttribute.SMOKE, 'foo') == 500

    # Wind
    def test_textToValue_Wind_Max(self):
        assert clearDarkSkyWeb.textToValue(clearDarkSkyWeb.WeatherAttribute.WIND, '>45 mph (00Z+6hr)') == (45, math.inf)

    def test_textToValue_Wind_Valid(self):
        assert clearDarkSkyWeb.textToValue(clearDarkSkyWeb.WeatherAttribute.WIND, '12 to 16 mph (00Z+6hr)') == (12, 16)

    def test_textToValue_Wind_Invalid(self):
        assert clearDarkSkyWeb.textToValue(clearDarkSkyWeb.WeatherAttribute.WIND, 'foo') == (45, math.inf)

    # Humidity
    def test_textToValue_Humidity_Min(self):
        assert clearDarkSkyWeb.textToValue(clearDarkSkyWeb.WeatherAttribute.HUMIDITY, '<25% (00Z+68hr)') == (0, 25)

    def test_textToValue_Humidity_Valid(self):
        assert clearDarkSkyWeb.textToValue(clearDarkSkyWeb.WeatherAttribute.HUMIDITY, '25% to 30% (00Z+67hr)"') == (25, 30)

    def test_textToValue_Humidity_Invalid(self):
        assert clearDarkSkyWeb.textToValue(clearDarkSkyWeb.WeatherAttribute.HUMIDITY, 'foo') == (95, 100)

    # Temperature
    def test_textToValue_Temperature_Min(self):
        assert clearDarkSkyWeb.textToValue(clearDarkSkyWeb.WeatherAttribute.TEMPERATURE, '< -40F(00Z+68hr)') == (-math.inf, -40)

    def test_textToValue_Temperature_Max(self):
        assert clearDarkSkyWeb.textToValue(clearDarkSkyWeb.WeatherAttribute.TEMPERATURE, '>113F (00Z+68hr)') == (113, math.inf)

    def test_textToValue_Temperature_Valid(self):
        assert clearDarkSkyWeb.textToValue(clearDarkSkyWeb.WeatherAttribute.TEMPERATURE, '50F to 59F (00Z+6hr)') == (50, 59)

    def test_textToValue_Temperature_Valid_Neg(self):
        assert clearDarkSkyWeb.textToValue(clearDarkSkyWeb.WeatherAttribute.TEMPERATURE, '-3F to 5F (00Z+6hr)') == (-3, 5)

    def test_textToValue_Temperature_Invalid(self):
        assert clearDarkSkyWeb.textToValue(clearDarkSkyWeb.WeatherAttribute.TEMPERATURE, 'foo') == (113, math.inf)

class TestExtractWeatherData:
    # These tests leave something to be desired, but I'm not sure how to test this function better
    def test_extractWeatherData_Valid(self):
        data = clearDarkSkyWeb.extractWeatherData('AlbanyNY')
        assert data != None
        assert len(data) == 80

    def test_extractWeatherData_Invalid(self):
        assert clearDarkSkyWeb.extractWeatherData('foo') == None