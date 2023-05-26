import discord
import clearDarkSkyEnums as cde

# Values to text
SEEING_TO_TEXT = {
    1.0: 'Excellent',
    0.8: 'Good',
    0.6: 'Average',
    0.4: 'Poor',
    0.2: 'Terrible',
    0.0: 'Too cloudy to forecast'
}

def getWindValueRange(value):
    if value < 5:
        return '0 to 5 mph'
    elif value < 11:
        return '6 to 11 mph'
    elif value < 16:
        return '12 to 16 mph'
    elif value < 28:
        return '17 to 28 mph'
    elif value < 45:
        return '29 to 45 mph'
    return '>45 mph'

def getHumidityValueRange(value):
    if value < 25:
        '<25%'
    for i in range(25, 100, 5):
        if value < i:
            return f'{i-5}% to {i}%'
    return '95% to 100%'

def getTemperatureValueRangeRange(value):
    return f'From ({getTemperatureValueRange(value[0])}) to ({getTemperatureValueRange(value[1])})'

def getTemperatureValueRange(value):
    if value < -40:
        return '< -40F'
    mins = [-40, -30, -21, -12, -3, 5, 14, 23, 32, 41, 50, 59, 68, 77, 86, 95, 104, 113]
    for i in range(1, len(mins) + 1):
        if value < i:
            return f'{mins[i-1]}F to {mins[i]}F'
    return '>113F'


# Discord Lists
ATTRIBUTE_OPTIONS = [
    discord.SelectOption(label='Cloud Cover', value=cde.WeatherAttribute.CLOUD_COVER.value),
    discord.SelectOption(label='Transparency', value=cde.WeatherAttribute.TRANSPARENCY.value),
    discord.SelectOption(label='Seeing', value=cde.WeatherAttribute.SEEING.value),
    discord.SelectOption(label='Darkness', value=cde.WeatherAttribute.DARKNESS.value),
    discord.SelectOption(label='Smoke', value=cde.WeatherAttribute.SMOKE.value),
    discord.SelectOption(label='Wind', value=cde.WeatherAttribute.WIND.value),
    discord.SelectOption(label='Humidity', value=cde.WeatherAttribute.HUMIDITY.value),
    discord.SelectOption(label='Temperature', value=cde.WeatherAttribute.TEMPERATURE.value),
]

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
    discord.SelectOption(label='Transparent', value='Transparent'),
    discord.SelectOption(label='Above Average', value='Above Average'),
    discord.SelectOption(label='Average', value='Average'),
    discord.SelectOption(label='Below Average', value='Below Average'),
    discord.SelectOption(label='Poor', value='Poor'),
    discord.SelectOption(label='Too cloudy to forecast', value='Too cloudy to forecast')
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

SMOKE_OPTIONS = [
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


