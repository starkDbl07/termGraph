#!/usr/bin/env python

import curses as cs
import time as tm
import random
import time as tm
import subprocess

graphTitle="Free Memory"
graphTitleLength=len(graphTitle)
graphUnit="MB"
graphChar=" "
graphHeight=10
graphWidth=80
graphHigh=graphHeight
graphLow=0
graphScale=(graphLow + graphHigh) // graphHeight 
graphValues=[]
graphTitlePosition=(graphWidth/2 - graphTitleLength/2)

stdscr = cs.initscr()
cs.start_color()
cs.use_default_colors()
cs.noecho()
cs.curs_set(0)
cs.cbreak()
if cs.can_change_color():
	cs.init_color(cs.COLOR_RED,50,10,10) 
cs.init_pair(2, cs.COLOR_BLACK, cs.COLOR_BLUE)
cs.init_pair(3, cs.COLOR_BLACK, cs.COLOR_BLACK)
cs.init_pair(4, cs.COLOR_WHITE, -1)
cs.init_pair(5, cs.COLOR_BLUE, cs.COLOR_BLACK)


graphTitleWindow = cs.newwin(1, graphWidth, 0, 0)
graphWindowBox = cs.newwin(graphHeight+2, graphWidth+2, 1, 1)
graphWindow = cs.newwin(graphHeight, graphWidth, 2, 2)
graphIndexWindow = cs.newwin(1, graphWidth, graphHeight+3, 1)
graphWindowBox.box()
areaProperty = cs.color_pair(2)

def drawArea(areaHeight, x):
	global graphWindow, areaProperty, graphHeight, graphWidth, graphScale, graphHigh, graphLow
	if(areaHeight < graphLow):
		graphLow = areaHeight
		graphScale = ( graphLow + graphHigh ) // graphHeight
		#graphWindow.addstr("GLMatch")
	if(areaHeight > graphHigh):
		graphHigh = areaHeight
		graphScale = ( graphLow + graphHigh ) // graphHeight
		#graphWindow.addstr("GHMatch")
	drawHeight=( graphHeight- (areaHeight // graphScale) ) - 1
	for level in range(graphHeight-1, drawHeight,-1):
		#graphWindow.addstr(str(level) + ",")
		try:
			graphWindow.addch(level,x,graphChar, areaProperty)
		except Exception as e:
			graphWindow.addstr(str(level) + "," + str(x))
			#graphWindow.addstr(str(e))

	if (graphHeight - drawHeight ) <=1:	
		graphWindow.addch(graphHeight-1, x, "_", cs.color_pair(5))

def updateIndex(value):
    global graphIndexWindow, graphHigh, graphLow
    graphIndexWindow.addstr(0,3," ".join(("Current: ", str(value), graphUnit, "\tMin: ", str(graphLow), "\tMax: ", str(graphHigh), "         ")))
    graphIndexWindow.refresh()

def drawGraph():
	global graphValues, graphWindow
	graphWindow.clear()
	cursor=0
	for value in graphValues:
		drawArea(value, cursor)
		cursor=cursor+1
	graphWindow.refresh()

def feedGraph(value):
	global graphValues
	updateIndex(value)
	graphValues.append(value)
	drawGraph()

graphTitleWindow.addstr(0, graphTitlePosition, graphTitle, cs.color_pair(4))
graphWindowBox.refresh()
graphWindow.bkgd("-", cs.color_pair(3))
graphTitleWindow.refresh()

for i in range(0,graphWidth-1):
	feedGraph(int(subprocess.check_output("./memory.sh")))
	#feedGraph(random.randint(1,50))
	tm.sleep(1)

cs.endwin()
