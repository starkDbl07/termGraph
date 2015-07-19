#!/usr/bin/env python

import curses as cs
import time as tm
import random

height=30
width=80

stdscr = cs.initscr()
cs.noecho()
cs.curs_set(0)

graph=[0,0]


while True:
	for x in range(0,len(graph)):
		for y in range(height,height-(graph[x]%height),-1):
			stdscr.addstr(height+1, 2, "Current: {current_value}            ".format(current_value=graph[x]))
			stdscr.addch(y,width-x,"-",cs.A_REVERSE)
	stdscr.refresh()
	stdscr.clear()
	tm.sleep(1)
	if(len(graph)>=width):
		graph.pop(0)
	graph.append(random.randint(1,10))

stdscr.getch()
cs.endwin()
