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

def loadForecast(city, key):
	#primitive error handling
	try:
		response = urllib2.urlopen('http://api.openweathermap.org/data/2.5/forecast?q=' + str(city) +
					   '&units=metric&APPID=' + str(key))
	#exit curses clealy before rising an exception
	except urllib2.URLError:
		endCurses()
		print "urllib2.URLError raised"
		sys.exit()

	rawData = response.read()
	jsonData = json.loads(rawData)

	return jsonData

def loadCurrent(city, key):
	try:
		response = urllib2.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + str(city) + 
					   '&units=metric&APPID=' + str(key))
	except urllib2.URLError:
		endCurses()
		print "urllib2.URLError raised"
		sys.exit()

	rawData = response.read()
	jsonData = json.loads(rawData)

	return jsonData

def initCurses():

	locale.setlocale(locale.LC_ALL,'')
	
	#init curses interface
	stdscr = curses.initscr()

	#colors
	curses.start_color()
	curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
	curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
	curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
	curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)
	curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_BLACK)

	curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_BLUE)

	curses.noecho()
	curses.cbreak()
	stdscr.keypad(1)
	curses.curs_set(0) #no cursor
	
	return stdscr


def endCurses():
	#terminate curses application
	curses.nocbreak();curses.echo();stdscr.keypad(0)
	curses.endwin()

def drawCityData(cityData, cityWindow):

	winSize = cityWindow.getmaxyx()
	headline = 'Location'

	cityWindow.clear()
	drawWindowBorder(cityWindow)

	lon = "{:.4f}".format(cityData['coord']['lon'])
	lat = "{:.4f}".format(cityData['coord']['lat'])

	try:
		cityWindow.addstr(1, (winSize[1] - len(headline))//2, headline, 
				curses.A_BOLD | curses.color_pair(3))
		cityWindow.addstr(2,1,cityData['name'], curses.A_BOLD | curses.color_pair(1))
		cityWindow.addstr(3,1,'Lon: ' + lon, curses.color_pair(2))
		cityWindow.addstr(4,1,'Lat: ' + lat, curses.color_pair(2))
		cityWindow.addstr(5,1,'Country: ' + cityData['country'], curses.color_pair(5))

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
			window.addch(row,i,curses.ACS_HLINE, curses.A_BOLD | curses.color_pair(color))
		except:
			curses.error

def drawVLineCorners(row, col, length, window, color, right):

	upperCorner = curses.ACS_ULCORNER
	lowerCorner = curses.ACS_LLCORNER

	if right == True:
		upperCorner = curses.ACS_URCORNER
		lowerCorner = curses.ACS_LRCORNER

	try:
		window.addch(row,col, upperCorner,
				curses.A_BOLD | curses.color_pair(color))
		window.addch(row + length - 1, col, lowerCorner, 
				curses.A_BOLD | curses.color_pair(color))
	except:
		curses.error


	for i in range(row + 1, row + length - 1):
		try:
			window.addch(i,col,curses.ACS_VLINE, curses.A_BOLD | curses.color_pair(color))
		except:
			curses.error

def drawWindowBorder(window):
	winSize = window.getmaxyx()

	drawHLine(0,0,winSize[1], window,1)
	drawHLine(winSize[0]-1,0,winSize[1], window,1)

	drawVLineCorners(0, winSize[1]-1, winSize[0], window, 1, True)
	drawVLineCorners(0,0,winSize[0], window, 1, False)
	

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
	

def drawCurrentData(currentData, currentWindow):
	winSize = currentWindow.getmaxyx()
	headline = 'Current weather'

	temperature = 'Temperature: ' + str(currentData['main']['temp']) + ' °C '
	pressure = 'Pressure: ' + str(currentData['main']['pressure']) + ' hPa '
	humidity = 'Humidity: ' + str(currentData['main']['humidity']) + ' % '
	wind = 'Wind: ' + str(currentData['wind']['speed']) + ' m/s '

	sunriseUnix = currentData['sys']['sunrise']
	sunsetUnix = currentData['sys']['sunset']

	sunrise = 'Sunrise: ' + getTimeFormat(sunriseUnix)
	sunset = 'Sunset: ' + getTimeFormat(sunsetUnix)
	date = getDateFormat(sunsetUnix)
	curWeather = currentData['weather'][0]['description']

	icon = getIcon(currentData['weather'][0]['icon'])
	

	rightOffset = winSize[1] - len(temperature)
	leftOffset = 1

	currentWindow.clear()
	drawWindowBorder(currentWindow)

	try:
		currentWindow.addstr(1, (winSize[1] - len(headline))//2, headline,
			curses.A_BOLD | curses.color_pair(3))
	except curses.error:
		pass

	try:
		currentWindow.addstr(2,rightOffset, temperature)
		currentWindow.addstr(3,rightOffset, pressure)
		currentWindow.addstr(4,rightOffset, humidity)
		currentWindow.addstr(5, rightOffset, wind)
			
	except curses.error:
		pass

	try:
		currentWindow.addstr(2,leftOffset + icons.iconWidth + 1, date)
		currentWindow.addstr(3,leftOffset + icons.iconWidth + 1, curWeather)
		currentWindow.addstr(4,leftOffset + icons.iconWidth + 1, sunrise)
		currentWindow.addstr(5,leftOffset + icons.iconWidth + 1, sunset)

	except curses.error:
		pass

	try:
		#currentWindow.addstr(1, rightOffset - icons.iconWidth - 1, 'ikona')
		#icons.drawIcon(rightOffset - icons.iconWidth - 1,2, icon, currentWindow)
		icons.drawIcon(leftOffset, 2, icon, currentWindow)
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
		forecastWindow.addstr(1, (winSize[1] - len(headline))//2, headline,
				curses.A_BOLD | curses.color_pair(3))
	
	except curses.error:
		pass

	for day in days:
		drawDay(dayY, dayX, day, forecastWindow)
		dayX = dayX + dayWidth


	forecastWindow.refresh()

def drawDay(yPos, xPos, dayData, forecastWindow):
	
	date = getDateFormat(dayData['dt'])
	time = getTimeFormat(dayData['dt'])
	icon = getIcon(dayData['weather'][0]['icon'])

	temp =str(dayData['main']['temp']) + ' °C'
	humidity ='Hum: ' + str(dayData['main']['humidity']) + '%'
	pressure = str(dayData['main']['pressure']) + 'hPa'

	try:
		forecastWindow.addstr(yPos, xPos, date, curses.A_BOLD | curses.color_pair(2))
		forecastWindow.addstr(yPos + 1, xPos, time, curses.A_BOLD | curses.color_pair(4))
		icons.drawIcon(xPos,yPos + 2, icon, forecastWindow)
		forecastWindow.addstr(yPos + 6, xPos, temp)
		forecastWindow.addstr(yPos + 7, xPos, humidity)
		forecastWindow.addstr(yPos + 8, xPos, pressure)
	except curses.error:
		pass

def drawInfoWindow(infoWindow, curLoc, numLoc):
	
	winSize = infoWindow.getmaxyx()
	navInf = '<Prev ' + str(curLoc + 1) + '/' + str(numLoc)  + ' Next> '
	
	infoWindow.clear()

	try:
		infoWindow.addstr(0,1,'Weather from www.openweathermap.org', 
				curses.A_BOLD | curses.color_pair(5))
		infoWindow.addstr(0, winSize[1] - len(navInf), navInf,
				curses.A_BOLD | curses.color_pair(1))
	except:
		pass

	infoWindow.refresh()

#maybe use some global variables next time
def refreshWeather(cityWindow, currentWindow, forecastWindow, infoWindow, location, curLoc, numLoc, key):

	forecastData = loadForecast(location, key)
	currentData = loadCurrent(location, key)

	drawCityData(forecastData['city'], cityWindow)

	drawCurrentData(currentData, currentWindow)
	
	drawForecastData(forecastData, forecastWindow)

	drawInfoWindow(infoWindow, curLoc, numLoc)

if __name__ == '__main__':

	stdscr = initCurses()
	stdscr.refresh()

	#config read from config.toml file
	config = {}

	#reading config
	with open('config.toml') as config_file:
		config = toml.load(config_file)

	#curren location
	curLoc = 0
	locations = config['weather']['locations']
	
	apiKey = config['api']['key']

	#terminal size
	rows, columns = subprocess.check_output(['stty', 'size']).split()
	rows = int(rows) 
	columns = int(columns)

	cityWindow = curses.newwin(7, 14, 0, 0)

	currentWindow = curses.newwin(7,columns - 15, 0, 15)
	
	forecastWindow = curses.newwin(rows - 8, columns, 7,0)

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




