# -*- coding: utf-8 -*-

import curses
import locale
import subprocess
import time
import sys

import urllib2
import json
import icons

import pytoml as toml

# curses color pairs
PAIR_RED = 1
PAIR_GREEN = 2
PAIR_BLUE = 3
PAIR_YELLOW = 4
PAIR_CYAN = 5
PAIR_WHITE = 6
PAIR_BLACK = 7

PAIR_BLACK_BLUE = 8

MIN_ROWS = 24
MIN_COLS = 70

def loadForecast(city, key):
    # primitive error handling
    try:
        response = urllib2.urlopen('http://api.openweathermap.org/data/2.5/forecast?q=' + str(city) +
                                   '&units=metric&APPID=' + str(key))
    # exit curses clealy before rising an exception
    except urllib2.URLError, e:
        endCurses()
        print "urllib2.URLError raised"
        print str(e)
        sys.exit()

    rawData = response.read()
    jsonData = json.loads(rawData)

    return jsonData


def loadCurrent(city, key):
    try:
        response = urllib2.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + str(city) +
                                   '&units=metric&APPID=' + str(key))
    except urllib2.URLError, e:
        endCurses()
        print "urllib2.URLError raised"
        print str(e)
        sys.exit()

    rawData = response.read()
    jsonData = json.loads(rawData)

    return jsonData


def initCurses():

    locale.setlocale(locale.LC_ALL, '')

    # init curses interface
    stdscr = curses.initscr()

    # colors
    curses.start_color()
    curses.init_pair(PAIR_RED, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(PAIR_GREEN, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(PAIR_BLUE, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(PAIR_YELLOW, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(PAIR_CYAN, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(PAIR_WHITE, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(PAIR_BLACK, curses.COLOR_BLACK, curses.COLOR_BLACK)

    curses.init_pair(PAIR_BLACK_BLUE, curses.COLOR_BLACK, curses.COLOR_BLUE)

    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)
    curses.curs_set(0)  # no cursor

    return stdscr


def endCurses():
    # terminate curses application
    curses.nocbreak()
    curses.echo()
    stdscr.keypad(0)
    curses.endwin()


def drawCityData(cityData, cityWindow):

    winSize = cityWindow.getmaxyx()
    headline = 'Location'

    cityWindow.clear()
    drawWindowBorder(cityWindow)

    lon = "{:.4f}".format(cityData['coord']['lon'])
    lat = "{:.4f}".format(cityData['coord']['lat'])

    try:
        cityWindow.addstr(1, (winSize[1] - len(headline)) // 2, headline,
                          curses.A_BOLD | curses.color_pair(3))
        cityWindow.addstr(
            2, 1, cityData['name'], curses.A_BOLD | curses.color_pair(PAIR_RED))
        cityWindow.addstr(3, 1, 'Lon: ' + lon, curses.color_pair(PAIR_GREEN))
        cityWindow.addstr(4, 1, 'Lat: ' + lat, curses.color_pair(PAIR_GREEN))
        cityWindow.addstr(5, 1, 'Country:  ' +
                          cityData['country'], curses.color_pair(PAIR_CYAN))

    except curses.error:
        pass

    cityWindow.refresh()


def getDateFormat(unixTime):
    timeStruct = time.localtime(unixTime)
    dateString = time.strftime('%Y-%m-%d', timeStruct)
    return dateString


def getTimeFormat(unixTime):
    timeStruct = time.localtime(unixTime)
    timeString = time.strftime('%H:%M:%S', timeStruct)

    return timeString


def drawHLine(row, col, length, window, color):
    for i in range(col, col + length):
        try:
            window.addch(row, i, curses.ACS_HLINE,
                         curses.A_BOLD | curses.color_pair(color))
        except:
            curses.error


def drawVLineCorners(row, col, length, window, color, right):

    upperCorner = curses.ACS_ULCORNER
    lowerCorner = curses.ACS_LLCORNER

    if right == True:
        upperCorner = curses.ACS_URCORNER
        lowerCorner = curses.ACS_LRCORNER

    try:
        window.addch(row, col, upperCorner,
                     curses.A_BOLD | curses.color_pair(color))
        window.addch(row + length - 1, col, lowerCorner,
                     curses.A_BOLD | curses.color_pair(color))
    except:
        curses.error

    for i in range(row + 1, row + length - 1):
        try:
            window.addch(i, col, curses.ACS_VLINE,
                         curses.A_BOLD | curses.color_pair(color))
        except:
            curses.error


def drawWindowBorder(window):
    winSize = window.getmaxyx()

    drawHLine(0, 0, winSize[1], window, PAIR_RED)
    drawHLine(winSize[0] - 1, 0, winSize[1], window, PAIR_RED)

    drawVLineCorners(0, winSize[1] - 1, winSize[0], window, PAIR_RED, True)
    drawVLineCorners(0, 0, winSize[0], window, PAIR_RED, False)


def getIcon(iconType):
    iconType = iconType[:2]
    if iconType == '01':
        return icons.clear
    if iconType == '02':
        return icons.fewClouds
    if iconType == '03':
        return icons.scatteredClouds
    if iconType == '04':
        return icons.brokenClouds

    if iconType == '09' or iconType == '10':
        return icons.rain

    if iconType == '11':
        return icons.storm

    if iconType == '13':
        return icons.snow
    if iconType == '50':
        return icons.mist

    return icons.default

def padEntry(entry, maxLen, separator, padChar):
    separatorIndex = entry.index(separator) + 1
    padding = maxLen - len(entry)
    return entry[:separatorIndex] + (padChar * padding) + entry[separatorIndex:]


def drawCurrentData(currentData, currentWindow):
    winSize = currentWindow.getmaxyx()
    headline = 'Current weather'

    temperature = 'Temperature: {} C '.format(currentData['main']['temp']) 
    pressure = 'Pressure: {} hPa '.format(currentData['main']['pressure'])
    humidity = 'Humidity: {} % '.format(currentData['main']['humidity'])
    wind = 'Wind: {} ms '.format(currentData['wind']['speed'])

    sunriseUnix = currentData['sys']['sunrise']
    sunsetUnix = currentData['sys']['sunset']

    sunrise = 'Sunrise: ' + getTimeFormat(sunriseUnix)
    sunset = 'Sunset:  ' + getTimeFormat(sunsetUnix)
    date = getDateFormat(sunsetUnix)
    curWeather = currentData['weather'][0]['description']

    icon = getIcon(currentData['weather'][0]['icon'])

    maxLen = max([len(temperature),len(pressure),len(humidity),len(wind)])
   
    temperature = padEntry(temperature, maxLen, ':', ' ')
    pressure = padEntry(pressure, maxLen, ':', ' ')
    humidity = padEntry(humidity, maxLen, ':', ' ')
    wind = padEntry(wind, maxLen, ':', ' ')

    rightOffset = winSize[1] - maxLen - 1
    leftOffset = 1

    currentWindow.clear()
    drawWindowBorder(currentWindow)

    try:
        currentWindow.addstr(1, (winSize[1] - len(headline)) // 2, headline,
                             curses.A_BOLD | curses.color_pair(PAIR_BLUE))
    except curses.error:
        pass

    try:
        currentWindow.addstr(2, rightOffset, temperature,
                             curses.color_pair(PAIR_YELLOW))
        currentWindow.addstr(3, rightOffset, pressure,
                             curses.color_pair(PAIR_YELLOW))
        currentWindow.addstr(4, rightOffset, humidity,
                             curses.color_pair(PAIR_YELLOW))
        currentWindow.addstr(5, rightOffset, wind,
                             curses.color_pair(PAIR_YELLOW))

    except curses.error:
        pass

    try:
        currentWindow.addstr(2, leftOffset + icons.iconWidth +
                             1, date, curses.color_pair(PAIR_CYAN))
        currentWindow.addstr(3, leftOffset + icons.iconWidth + 1,
                             curWeather, curses.color_pair(PAIR_CYAN))
        currentWindow.addstr(4, leftOffset + icons.iconWidth + 1,
                             sunrise, curses.color_pair(PAIR_CYAN))
        currentWindow.addstr(5, leftOffset + icons.iconWidth + 1,
                             sunset, curses.color_pair(PAIR_CYAN))

    except curses.error:
        pass

    try:
        #currentWindow.addstr(1, rightOffset - icons.iconWidth - 1, 'ikona')
        #icons.drawIcon(rightOffset - icons.iconWidth - 1,2, icon, currentWindow)
        icons.drawIcon(leftOffset, 1, icon, currentWindow)
    except curses.error:
        pass

    currentWindow.refresh()


def drawForecastData(forecastData, forecastWindow):

    winSize = forecastWindow.getmaxyx()
    headline = 'Forecast'
    days = forecastData['list']
    dayWidth = 12
    daysNum = winSize[1] // dayWidth

    days = days[:daysNum]
    dayX = (winSize[1] - daysNum * dayWidth) // 2
    dayY = 3

    forecastWindow.clear()
    drawWindowBorder(forecastWindow)

    try:
        forecastWindow.addstr(1, (winSize[1] - len(headline)) // 2, headline,
                              curses.A_BOLD | curses.color_pair(PAIR_BLUE))

    except curses.error:
        pass

    for day in days:
        drawDay(dayY, dayX, day, forecastWindow)
        dayX = dayX + dayWidth

    forecastWindow.refresh()


def drawDay(yPos, xPos, dayData, forecastWindow):

    date = getDateFormat(dayData['dt'])
    time = ' ' + getTimeFormat(dayData['dt'])
    icon = getIcon(dayData['weather'][0]['icon'])

    temp = str(dayData['main']['temp']) + ' °C'
    humidity = 'Hum: ' + str(dayData['main']['humidity']) + '%'
    pressure = str(dayData['main']['pressure']) + 'hPa'

    try:
        forecastWindow.addstr(
            yPos, xPos, date, curses.A_BOLD | curses.color_pair(PAIR_GREEN))
        forecastWindow.addstr(yPos + 1, xPos, time,
                              curses.A_BOLD | curses.color_pair(PAIR_YELLOW))
        icons.drawIcon(xPos, yPos + 2, icon, forecastWindow)
        forecastWindow.addstr(yPos + icons.iconHeight + 2, xPos, temp,
                              curses.color_pair(PAIR_GREEN))
        forecastWindow.addstr(yPos + icons.iconHeight + 3, xPos, humidity,
                              curses.color_pair(PAIR_GREEN))
        forecastWindow.addstr(yPos + icons.iconHeight + 4, xPos, pressure,
                              curses.color_pair(PAIR_GREEN))
    except curses.error:
        pass


def drawInfoWindow(infoWindow, curLoc, numLoc):

    winSize = infoWindow.getmaxyx()
    navInf = '<Prev ' + str(curLoc + 1) + '/' + str(numLoc) + ' Next> '

    infoWindow.clear()

    try:
        infoWindow.addstr(0, 1, 'Weather from www.openweathermap.org',
                          curses.A_BOLD | curses.color_pair(5))
        infoWindow.addstr(0, winSize[1] - len(navInf), navInf,
                          curses.A_BOLD | curses.color_pair(1))
    except:
        pass

    infoWindow.refresh()

# maybe use some global variables next time


def refreshWeather(cityWindow, currentWindow, forecastWindow, infoWindow, location, curLoc, numLoc, key):

    forecastData = loadForecast(location, key)
    currentData = loadCurrent(location, key)

    drawCityData(forecastData['city'], cityWindow)

    drawCurrentData(currentData, currentWindow)

    drawForecastData(forecastData, forecastWindow)

    drawInfoWindow(infoWindow, curLoc, numLoc)

if __name__ == '__main__':

    # terminal size
    rows, columns = subprocess.check_output(['stty', 'size']).split()
    rows = int(rows)
    columns = int(columns)

    if rows < MIN_ROWS or columns < MIN_COLS:
        print "requires minimal terminal size {}x{} (yours {}x{})".format(MIN_COLS, MIN_ROWS, columns,rows)
        sys.exit()


    stdscr = initCurses()
    stdscr.refresh()

    # config read from config.toml file
    config = {}

    # reading config
    with open('config.toml') as config_file:
        config = toml.load(config_file)

    # curren location
    curLoc = 0
    locations = config['weather']['locations']

    apiKey = config['api']['key']

    
    cityWindow = curses.newwin(7, 14, 0, 0)

    currentWindow = curses.newwin(7, columns - 15, 0, 15)

    forecastWindow = curses.newwin(rows - 8, columns, 7, 0)

    infoWindow = curses.newwin(1, columns, rows - 1, 0)

    refreshWeather(cityWindow, currentWindow, forecastWindow,
                   infoWindow, locations[0], 0, len(locations), apiKey)

    while True:
        c = stdscr.getch()
        if c == ord('q'):
            break
        if c == curses.KEY_F5:
            refreshWeather(cityWindow, currentWindow, forecastWindow,
                           infoWindow, locations[curLoc], curLoc, len(locations), apiKey)
        if c == curses.KEY_RIGHT:
            curLoc = (curLoc + 1) % len(locations)
            refreshWeather(cityWindow, currentWindow, forecastWindow,
                           infoWindow, locations[curLoc], curLoc, len(locations), apiKey)
        if c == curses.KEY_LEFT:
            curLoc = (curLoc - 1) % len(locations)
            refreshWeather(cityWindow, currentWindow, forecastWindow,
                           infoWindow, locations[curLoc], curLoc, len(locations), apiKey)

    endCurses()
