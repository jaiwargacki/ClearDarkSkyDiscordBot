import pytest

import clearDarkSkyEnums

class TestTransparency:
    def test_getAttributeFromText_Transparent(self):
        assert clearDarkSkyEnums.Transparency.getAttributeFromText('Transparent') == clearDarkSkyEnums.Transparency.TRANSPARENT

    def test_getAttributeFromText_AboveAverage(self):
        assert clearDarkSkyEnums.Transparency.getAttributeFromText('Above Average') == clearDarkSkyEnums.Transparency.ABOVE_AVERAGE

    def test_getAttributeFromText_Average(self):
        assert clearDarkSkyEnums.Transparency.getAttributeFromText('Average') == clearDarkSkyEnums.Transparency.AVERAGE

    def test_getAttributeFromText_BelowAverage(self):
        assert clearDarkSkyEnums.Transparency.getAttributeFromText('Below Average') == clearDarkSkyEnums.Transparency.BELOW_AVERAGE

    def test_getAttributeFromText_Poor(self):
        assert clearDarkSkyEnums.Transparency.getAttributeFromText('Poor') == clearDarkSkyEnums.Transparency.POOR

    def test_getAttributeFromText_Invalid(self):
        assert clearDarkSkyEnums.Transparency.getAttributeFromText('foo') == clearDarkSkyEnums.Transparency.POOR

    def test_confirmRanking(self):
        assert clearDarkSkyEnums.Transparency.TRANSPARENT.value < clearDarkSkyEnums.Transparency.ABOVE_AVERAGE.value
        assert clearDarkSkyEnums.Transparency.ABOVE_AVERAGE.value < clearDarkSkyEnums.Transparency.AVERAGE.value
        assert clearDarkSkyEnums.Transparency.AVERAGE.value < clearDarkSkyEnums.Transparency.BELOW_AVERAGE.value
        assert clearDarkSkyEnums.Transparency.BELOW_AVERAGE.value < clearDarkSkyEnums.Transparency.POOR.value