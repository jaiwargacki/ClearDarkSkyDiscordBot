import discord
import clearDarkSkyEnums as cde

CLOUD_COVER_OPTIONS = [
    discord.SelectOption(label='Clear', value='0'),
    discord.SelectOption(label='10% covered', value='10'),
    discord.SelectOption(label='20% covered', value='20'),
    discord.SelectOption(label='30% covered', value='30'),
    discord.SelectOption(label='40% covered', value='40'),
    discord.SelectOption(label='50% covered', value='50'),
    discord.SelectOption(label='60% covered', value='60'),
    discord.SelectOption(label='70% covered', value='70'),
    discord.SelectOption(label='80% covered', value='80'),
    discord.SelectOption(label='90% covered', value='90'),
    discord.SelectOption(label='Overcast', value='100')
]

TRANSPARENCY_OPTIONS = [
    discord.SelectOption(label='Transparent', value=cde.Transparency.TRANSPARENT.value),
    discord.SelectOption(label='Above Average', value=cde.Transparency.ABOVE_AVERAGE.value),
    discord.SelectOption(label='Average', value=cde.Transparency.AVERAGE.value),
    discord.SelectOption(label='Below Average', value=cde.Transparency.BELOW_AVERAGE.value),
    discord.SelectOption(label='Poor', value=cde.Transparency.POOR.value),
    discord.SelectOption(label='Too cloudy to forecast', value=cde.Transparency.TOO_CLOUDY.value)
]

SEEING_OPTIONS = [
    discord.SelectOption(label='Excellent', value='1.0'),
    discord.SelectOption(label='Good', value='0.8'),
    discord.SelectOption(label='Average', value='0.6'),
    discord.SelectOption(label='Poor', value='0.4'),
    discord.SelectOption(label='Bad', value='0.2'),
    discord.SelectOption(label='Too cloudy to forecast', value='0.0')
]

DARKNESS_OPTIONS = [
    discord.SelectOption(label='6.5 (Darkest)', value='6.5'),
    discord.SelectOption(label='6.0', value='6.0'),
    discord.SelectOption(label='5.5', value='5.5'),
    discord.SelectOption(label='5.0', value='5.0'),
    discord.SelectOption(label='4.5', value='4.5'),
    discord.SelectOption(label='4.0', value='4.0'),
    discord.SelectOption(label='3.5', value='3.5'),
    discord.SelectOption(label='3.0', value='3.0'),
    discord.SelectOption(label='2.0', value='2.0'),
    discord.SelectOption(label='1.0', value='1.0'),
    discord.SelectOption(label='0.0', value='0.0'),
    discord.SelectOption(label='-1.0', value='-1.0'),
    discord.SelectOption(label='-2.0', value='-2.0'),
    discord.SelectOption(label='-3.0', value='-3.0'),
    discord.SelectOption(label='-4.0', value='-4.0')
]

SMOKES_OPTIONS = [
    discord.SelectOption(label='No Smoke', value='0.0'),
    discord.SelectOption(label='2 ug/m^3', value='2.0'),
    discord.SelectOption(label='5 ug/m^3', value='5.0'),
    discord.SelectOption(label='10 ug/m^3', value='10.0'),
    discord.SelectOption(label='20 ug/m^3', value='20.0'),
    discord.SelectOption(label='40 ug/m^3', value='40.0'),
    discord.SelectOption(label='60 ug/m^3', value='60.0'),
    discord.SelectOption(label='80 ug/m^3', value='80.0'),
    discord.SelectOption(label='100 ug/m^3', value='100.0'),
    discord.SelectOption(label='200 ug/m^3', value='200.0'),
    discord.SelectOption(label='500 ug/m^3', value='500.0')
]

WIND_OPTIONS = [
    discord.SelectOption(label='0 to 5 mph', value='5.0'),
    discord.SelectOption(label='6 to 11 mph', value='11.0'),
    discord.SelectOption(label='12 to 16 mph', value='16.0'),
    discord.SelectOption(label='17 to 28 mph', value='28.0'),
    discord.SelectOption(label='29 to 45 mph', value='45.0'),
    discord.SelectOption(label='>45 mph', value='100.0')
]

HUMIDITY_OPTIONS = [
    discord.SelectOption(label='<25%', value='25.0'),
    discord.SelectOption(label='25% to 30%', value='30.0'),
    discord.SelectOption(label='30% to 35%', value='35.0'),
    discord.SelectOption(label='35% to 40%', value='40.0'),
    discord.SelectOption(label='40% to 45%', value='45.0'),
    discord.SelectOption(label='45% to 50%', value='50.0'),
    discord.SelectOption(label='50% to 55%', value='55.0'),
    discord.SelectOption(label='55% to 60%', value='60.0'),
    discord.SelectOption(label='60% to 65%', value='65.0'),
    discord.SelectOption(label='65% to 70%', value='70.0'),
    discord.SelectOption(label='70% to 75%', value='75.0'),
    discord.SelectOption(label='75% to 80%', value='80.0'),
    discord.SelectOption(label='80% to 85%', value='85.0'),
    discord.SelectOption(label='85% to 90%', value='90.0'),
    discord.SelectOption(label='90% to 95%', value='95.0'),
    discord.SelectOption(label='95% to 100%', value='100.0')
]

TEMPERATURE_OPTIONS = [
    discord.SelectOption(label='< -40F', value='-40.0'),
    discord.SelectOption(label='-40F to -31F', value='-35.5'),
    discord.SelectOption(label='-30F to -21F', value='-25.5'),
    discord.SelectOption(label='-21F to -12F', value='-16.5'),
    discord.SelectOption(label='-12F to -3F', value='-7.5'),
    discord.SelectOption(label='-3F to 5F', value='1.0'),
    discord.SelectOption(label='5F to 14F', value='9.5'),
    discord.SelectOption(label='14F to 23F', value='18.5'),
    discord.SelectOption(label='23F to 32F', value='27.5'),
    discord.SelectOption(label='32F to 41F', value='36.5'),
    discord.SelectOption(label='41F to 50F', value='45.5'),
    discord.SelectOption(label='50F to 59F', value='54.5'),
    discord.SelectOption(label='59F to 68F', value='63.5'),
    discord.SelectOption(label='68F to 77F', value='72.5'),
    discord.SelectOption(label='77F to 86F', value='81.5'),
    discord.SelectOption(label='86F to 95F', value='90.5'),
    discord.SelectOption(label='95F to 104F', value='99.5'),
    discord.SelectOption(label='104F to 113F', value='108.5'),
    discord.SelectOption(label='>113F', value='113.0')
]


