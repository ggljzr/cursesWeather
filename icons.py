#code:
#3 = sky(blue)
#4 = sun (yellow)
#6 = cloud (white)
#7 = cloud (grey)

import curses

iconWidth = 8
iconHeight = 4

clear = [
	[3,3,3,4,4,4,3,3],
	[3,3,4,4,4,4,4,3],
	[3,3,4,4,4,4,4,3],
	[3,3,3,4,4,4,3,3]
	]

fewClouds = [
	[3,3,3,3,3,3,4,4],
	[3,3,6,6,3,4,4,4],
	[3,6,6,6,6,6,6,6],
	[6,6,6,6,6,6,6,6]
	]

scatteredClouds = [
		[3,3,3,3,3,3,3,3],
		[3,6,6,6,3,6,6,3],
		[6,6,6,6,6,6,6,6],
		[3,6,6,6,6,6,6,3]
		]

brokenClouds = [
		[7,7,7,7,7,7,7,7],
		[7,6,6,6,7,6,6,7],
		[6,6,6,6,6,6,6,6],
		[7,6,6,6,6,6,6,7]
	]

rain = [
		[6,6,6,6,6,6,6,6],
		[3,7,3,7,7,3,7,3],
		[7,3,7,7,3,7,3,7],
		[3,7,7,3,7,7,7,3]
	]


mist = [
		[7,6,7,6,7,6,7,6],
		[6,7,6,7,6,7,6,7],
		[7,6,7,6,7,6,7,6],
		[6,7,6,7,6,7,6,7]
	]

snow = [
		[6,6,6,6,6,6,6,6],
		[6,7,6,7,7,6,7,6],
		[7,6,7,7,6,7,6,7],
		[6,7,7,6,7,7,7,6]
	]



storm = [
		[6,6,6,6,6,6,6,6],
		[7,4,7,7,7,7,7,4],
		[7,7,4,7,7,7,4,7],
		[7,4,7,4,7,7,7,4]
	]



default = [
		[7,7,7,7,7,7,7,7],
		[7,1,1,1,1,1,1,7],
		[7,1,1,1,1,1,1,7],
		[7,7,7,7,7,7,7,7]
	]






def drawIcon(beginX, beginY, icon, window):
	
	indexX = 0
	indexY = 0

	for y in range(beginY, beginY + iconHeight):
		for x in range(beginX, beginX + iconWidth):

			color = icon[indexY][indexX]
			window.addch(y,x,curses.ACS_BLOCK,curses.color_pair(color) | curses.A_BOLD)

			indexX = indexX + 1

		indexX = 0
		indexY = indexY + 1

	window.refresh()

