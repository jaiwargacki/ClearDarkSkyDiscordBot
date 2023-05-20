from enum import Enum
import re
import datetime
import time

import requests
from bs4 import BeautifulSoup

# Enums
class WeatherAttribute(Enum):
    CLOUD_COVER = 1
    TRANSPARENCY = 2
    SEEING = 3
    DARKNESS = 4
    SMOKE = 5
    WIND = 6
    HUMIDITY = 7
    TEMPERATURE = 8

class Transparency(Enum):
    TRANSPARENT = 0
    ABOVE_AVERAGE = 1
    AVERAGE = 2
    BELOW_AVERAGE = 3
    POOR = 4

    @staticmethod
    def getAttributeFromText(text):
        if 'Transparent' in text:
            return Transparency.TRANSPARENT
        elif 'Above Average' in text:
            return Transparency.ABOVE_AVERAGE
        elif 'Average' in text:
            return Transparency.AVERAGE
        elif 'Below Average' in text:
            return Transparency.BELOW_AVERAGE
        elif 'Poor' in text:
            return Transparency.POOR
        return Transparency.POOR

# Constants
BASE_URL = 'https://www.cleardarksky.com/c/%s.html'
COORDS_LABEL = 'coords'
TITLE_LABEL = 'title'

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

# Functions
def extractDate(soup):
    date_content = soup.find(lambda tag: tag.name == 'font' and 'Last updated 20' in tag.text)
    regex_date = re.compile(r'\d+').findall(date_content.text)
    return datetime.datetime(int(regex_date[0]), int(regex_date[1]), int(regex_date[2]))

def textToValue(attribute, text):
    match attribute:
        case WeatherAttribute.CLOUD_COVER:
            if 'Clear' in text:
                return 0
            elif 'Overcast' in text:
                return 100
            return int(text.split('%')[0])
        case WeatherAttribute.TRANSPARENCY:
            return Transparency.getAttributeFromText(text)
        case WeatherAttribute.SEEING:
            return float(re.compile(r'\d+').search(text).group(0))/5
        case WeatherAttribute.DARKNESS:
            return float(re.compile(r'-?\d+\.\d').search(text).group(0))
        case WeatherAttribute.SMOKE:
            if 'Smoke' in text:
                return 0
            return int(re.compile(r'\d+').search(text).group(0))
        case WeatherAttribute.WIND:
            first = int(re.compile(r'\d+').search(text).group(0))
            if first == 45:
                return (first, math.inf)
            second = int(re.compile(r'\d+').findall(text)[1])
            return (first, second)
        case WeatherAttribute.HUMIDITY:
            first = int(re.compile(r'\d+').search(text).group(0))
            if text[0] == '<':
                return (0, first)
            second = int(re.compile(r'\d+').findall(text)[1])
            return (first, second)
        case WeatherAttribute.TEMPERATURE:
            first = int(re.compile(r'-?\d+').search(text).group(0))
            if text[0] == '<':
                return (-math.inf, first)
            second = int(re.compile(r'-?\d+').findall(text)[1])
            return (first, second)

class DataPoint:
    def __init__(self, timestamp):
        self.timestamp = timestamp
        self.data = dict()
    
    def __str__(self):
        output = f'{self.timestamp}\n'
        for attribute in self.data:
            output += f'{attribute}: {self.data[attribute]}\n'
        return output

    def __repr__(self):
        return self.__str__()

    def add(self, attribute, text):
        if attribute == WeatherAttribute.DARKNESS:
            if attribute not in self.data:
                self.data[attribute] = [textToValue(attribute, text)]
            else:
                self.data[attribute].append(textToValue(attribute, text))
        else:
            self.data[attribute] = textToValue(attribute, text)

def main():
    # Set url
    locationKey = 'AlbanyNYkey'
    url = BASE_URL % locationKey

    # Get html from website
    while True:
        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")
            start_date = extractDate(soup)
            details = soup.find("map", {"name":"ckmap"})
            areas = details.find_all('area')
            break
        except:
            print('Error getting page, trying again in 2 seconds...')
            time.sleep(2)

    # Get data from html response
    data = dict()
    for area in areas:
        if TITLE_LABEL in area.attrs and COORDS_LABEL in area.attrs:
            x_coord = int(area[COORDS_LABEL].split(',')[0])
            y_coord = int(area[COORDS_LABEL].split(',')[1])
            if x_coord == X_START_CORD:
                day = 0
            currentAttribute = Y_CORD_TO_ATTRIBUTE[int(y_coord)]
            hour = int(re.compile(r'(\d+)').match(area[TITLE_LABEL]).group(0))
            minute = int(re.compile(r'(\d+)').findall(area[TITLE_LABEL])[1])
            if hour == 0 and minute == 0:
                day += 1
            timestamp = start_date + datetime.timedelta(days=day, hours=hour)
            if timestamp not in data:
                data[timestamp] = DataPoint(timestamp)
            value = ':'.join(area[TITLE_LABEL].split(':')[2:]).strip()
            data[timestamp].add(currentAttribute, value)

    # Print data
    for clock_time in data:
        print(data[clock_time])

if __name__ == '__main__':
    main()

