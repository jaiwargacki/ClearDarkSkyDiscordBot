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

class TestExtractWeatherData:
    # These tests leave something to be desired, but I'm not sure how to test this function better
    def test_extractWeatherData_Valid(self):
        data = clearDarkSkyWeb.extractWeatherData('AlbanyNY')
        assert data != None
        assert len(data) >= 1

    def test_extractWeatherData_Invalid(self):
        assert clearDarkSkyWeb.extractWeatherData('foo') == None