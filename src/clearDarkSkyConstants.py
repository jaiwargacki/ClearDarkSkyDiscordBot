""" Constants for project """

import discord
from clearDarkSkyEnums import *

# Program parameters
REQUEST_RETRY_COUNT = 20
REQUEST_RETRY_DELAY = 2

# Help convert values to text
SEEING_VALUE_TO_TEXT = {
    1.0: 'Excellent',
    0.8: 'Good',
    0.6: 'Average',
    0.4: 'Poor',
    0.2: 'Terrible',
    0.0: 'Too cloudy to forecast'
}

# cleardarksky.com related constants
BASE_URL = 'https://www.cleardarksky.com/c/%skey.html'

COORDS_LABEL = 'coords'
TITLE_LABEL = 'title'
FONT_LABEL = 'font'
MAP_LABEL = 'map'
MAP_DICT = {"name":"ckmap"}
AREA_LABEL = 'area'
LAST_UPDATE_TEXT = 'Last updated 20'

X_START_CORD = 134

Y_CORD_TO_ATTRIBUTE = {
    77: WeatherAttribute.CLOUD_COVER,
    93: WeatherAttribute.TRANSPARENCY,
    109: WeatherAttribute.SEEING,
    125: WeatherAttribute.DARKNESS,
    173: WeatherAttribute.SMOKE,
    189: WeatherAttribute.WIND,
    205: WeatherAttribute.HUMIDITY,
    221: WeatherAttribute.TEMPERATURE
}

# Discord Select Options
ATTRIBUTE_OPTIONS = list(map(lambda x: discord.SelectOption(label=x.name, value=x.value), \
    WeatherAttribute))

CLOUD_COVER_OPTIONS = list(map(lambda x: discord.SelectOption(label='Clear' if x == 0 else \
    (f'{x}% covered' if x != 100 else 'Overcast'), value=str(x)), range(0,101,10)))

TRANSPARENCY_OPTIONS = list(map(lambda x: discord.SelectOption(label=x.name, value=x.value), \
    Transparency))

SEEING_OPTIONS = list(map(lambda x: discord.SelectOption(label=SEEING_VALUE_TO_TEXT[x], value=str(x)), \
    SEEING_VALUE_TO_TEXT))

DARKNESS_OPTIONS = list(map(lambda x: discord.SelectOption(label=str(x), value=str(x)), \
    [6.5, 6.0, 5.5, 5.0, 4.5, 4.0, 3.5,3.0,2.0,1.0,0.0,-1.0,-2.0,-3.0,-4.0]))

SMOKE_OPTIONS = list(map(lambda x: discord.SelectOption(label='No Smoke' if x == 0 else f'{x} ug/m^3', \
    value=str(x)), [0.0, 2.0, 5.0, 10.0, 20.0, 50.0, 100.0, 200.0, 500.0]))

WIND_OPTIONS = list(map(lambda x: discord.SelectOption(label=f'{x[0]} to {x[1]} mph' \
    if x[1] != 100 else f'>{x[0]} mph', value=str(x[1])), \
    [(0, 5), (6, 11), (12, 16), (17, 28), (29, 45), (45, 100)]))

HUMIDITY_OPTIONS = list(map(lambda x: discord.SelectOption(label=f'{x-5}% to {x}%' \
    if x != 25 else '<25%', value=str(x)), range(25, 101, 5)))

TEMPERATURE_OPTIONS = list(map(lambda x: discord.SelectOption(label=f'< -40F' \
    if x[2] == -40 else (f'{x[0]}F to {x[2]}F' if x[0] < 113 else '>113F'), \
    value=str(x[1])), [(-100, -40, -40), (-40, -35.5, -31), (-30, -25.5, -21), \
        (-21, -16.5, -12), (-12, -7.5, -3), (-3, 1.0, 5), (5, 9.5, 14), \
        (14, 18.5, 23), (23, 27.5, 32), (32, 36.5, 41), (41, 45.5, 50), \
        (50, 54.5, 59), (59, 63.5, 68), (68, 72.5, 77), (77, 81.5, 86), \
        (86, 90.5, 95), (95, 99.5, 104), (104, 108.5, 113), (113, 113, 1000)]))

OPTIONS_LOOKUP = {
    WeatherAttribute.CLOUD_COVER: ("Maximum cloud cover", CLOUD_COVER_OPTIONS, 1, 1),
    WeatherAttribute.TRANSPARENCY: ("Worst transparency", TRANSPARENCY_OPTIONS, 1, 1),
    WeatherAttribute.SEEING: ("Worst seeing", SEEING_OPTIONS, 1, 1),
    WeatherAttribute.DARKNESS: ("Brightest", DARKNESS_OPTIONS, 1, 1),
    WeatherAttribute.SMOKE: ("Worst smoke", SMOKE_OPTIONS, 1, 1),
    WeatherAttribute.WIND: ("Worst wind", WIND_OPTIONS, 1, 1),
    WeatherAttribute.HUMIDITY: ("Worst humidity", HUMIDITY_OPTIONS, 1, 1),
    WeatherAttribute.TEMPERATURE: ("Temperature Min and Max", TEMPERATURE_OPTIONS, 2, 2)
}