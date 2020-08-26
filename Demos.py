"""
Author: Kyle Mabry
Goes over some of the basics of PyCharm and Python programming language.
Last edit made: 08/25/2020
"""

import pymysql

# this connects to the database that brian created.
db = pymysql.connect('107.180.37.106', 'superRasberry', ')9Vr[dQzo8bG', 'RasberryPI')
cursor = db.cursor()
sql = "UPDATE `Controller` SET `response`='Hi, '\n' who is this'"
cursor.execute(sql)

# We're currently doing polling, but we should do events.
# What's the difference between polling and events? polling is a get request, like refreshing the webpage.
# A socket
