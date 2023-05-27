from clearDarkSkyEnums import Transparency

class TestTransparency:
    def test_getAttributeFromText_Transparent(self):
        assert Transparency.getAttributeFromText('Transparent') == Transparency.TRANSPARENT

    def test_getAttributeFromText_AboveAverage(self):
        assert Transparency.getAttributeFromText('Above Average') == Transparency.ABOVE_AVERAGE

    def test_getAttributeFromText_Average(self):
        assert Transparency.getAttributeFromText('Average') == Transparency.AVERAGE

    def test_getAttributeFromText_BelowAverage(self):
        assert Transparency.getAttributeFromText('Below Average') == Transparency.BELOW_AVERAGE

    def test_getAttributeFromText_Poor(self):
        assert Transparency.getAttributeFromText('Poor') == Transparency.POOR

    def test_getAttributeFromText_TooCloudy(self):
        assert Transparency.getAttributeFromText('Too Cloudy') == Transparency.TOO_CLOUDY_TO_FORECAST

    def test_getAttributeFromText_Invalid(self):
        assert Transparency.getAttributeFromText('foo') == Transparency.TOO_CLOUDY_TO_FORECAST

    def test_confirmRanking(self):
        assert Transparency.TRANSPARENT.value < Transparency.ABOVE_AVERAGE.value
        assert Transparency.ABOVE_AVERAGE.value < Transparency.AVERAGE.value
        assert Transparency.AVERAGE.value < Transparency.BELOW_AVERAGE.value
        assert Transparency.BELOW_AVERAGE.value < Transparency.POOR.value