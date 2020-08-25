"""
Author: Kyle Mabry
Goes over some of the basics of PyCharm and Python programming language.
Last edit made: 08/25/2020
"""

import mysql

# for loops
x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
y = []
for number in x:
    z = number + 5
    y.append(z)

# print the result of the for loop.
print("Each element in x has 5 added to it in 'y': " + str(y))


# mydb = mysql.connector.connect(
#     host="107.180.37.106",
#     user="superRasberry",
#     password=")9Vr[dQzo8bG"
#     )
#
# print(mydb)
