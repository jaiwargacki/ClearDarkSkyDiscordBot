
import datetime
import time
import math
import json
import os

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from clearDarkSkyConstants import *
import clearDarkSkyHelpers as helpers
from clearDarkSkyModel import AlertProfile, PointInTime

load_dotenv()
FORECAST_DATA = os.getenv('FORECAST_DATA')
SCALE_DATA = os.getenv('SCALE_DATA')
LOCATION_DATA = os.getenv('LOCATION_DATA')


def validateLocationKey(location):
    """ Validate the location key. Attempts up to 5 times.
    Parameters:
        location (str): The location key to validate.
    Returns:
        bool: True if the location key is valid, False otherwise.
    """
    locations = requests.get(LOCATION_DATA)
    for loc in locations.text.split('\n'):
        if location == loc.split('|')[0].strip():
            return True
    return False


def extractDate(soup):
    """ Extract the date of generation from website html. 
    Parameters:
        soup (BeautifulSoup): The html response from the website.
    Returns:
        datetime.datetime: The date of generation (0 hours, 0 min).
    """
    try:
        date_content = soup.find(lambda tag: tag.name == FONT_LABEL and LAST_UPDATE_TEXT in tag.text)
        return helpers.getDateFromText(date_content.text)
    except:
        return datetime.datetime(1970, 1, 1)


def extractWeatherData(location):
    """ Extract weather data from website html.
    Parameters:
        location (str): The location key to extract weather data for.
    Returns:
        dictionary: A dictionary of weather data. Keys are datetime.datetime objects
                    and values are PointInTime objects.
    """
    # Create url
    url = BASE_URL % location

    # Get html from website
    tries = 0
    while True:
        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")
            start_date = extractDate(soup)
            details = soup.find(MAP_LABEL, MAP_DICT)
            areas = details.find_all(AREA_LABEL)
            break
        except:
            tries += 1
            if tries == REQUEST_RETRY_COUNT:
                return None
            time.sleep(REQUEST_RETRY_DELAY)

    data = dict()
    for area in areas:
        if TITLE_LABEL in area.attrs and COORDS_LABEL in area.attrs:
            x_coord = int(area[COORDS_LABEL].split(',')[0])
            y_coord = int(area[COORDS_LABEL].split(',')[1])
            if x_coord == X_START_CORD:
                day = 0
            currentAttribute = Y_CORD_TO_ATTRIBUTE[int(y_coord)]
            hour = int(helpers.REGEX_INT.match(area[TITLE_LABEL]).group(0))
            minute = int(helpers.REGEX_INT.findall(area[TITLE_LABEL])[1])
            if hour == 0 and minute == 0:
                day += 1
            timestamp = start_date + datetime.timedelta(days=day, hours=hour)
            if timestamp not in data:
                data[timestamp] = PointInTime(timestamp)
            value = ':'.join(area[TITLE_LABEL].split(':')[2:]).strip()
            data[timestamp].add(currentAttribute, helpers.textToValue(currentAttribute, value))

    return data
