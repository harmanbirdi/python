#!usr/bin.env python

#
# Description : You have a list of numbers from -50 to 50; please write code that traverses this list
#               and for each number prints out a line conforming to the following:
#                   o if the number is a multiple of 3, print 'Fizz', or
#                   o if the number is a multiple of 5, print 'Buzz', or
#                   o if the number is a multiple of both 3 and 5, print 'Fizzbuzz'
#                   o otherwise, just print the number
# More Info   : Asked by Nour for 1app phone screen interview
# __author__  : Harman Birdi
# Date        : Sep 16, 2016
#

#n = int(raw_input("Enter fizz buzz: "))
n = -50

for i in range(n, abs(n) + 1):
    if i % 3 == i % 5 == 0:
        print "FizzBuzz"
        continue
    elif i % 3 == 0:
        print "Fizz"
        continue
    elif i % 5 == 0:
        print "Buzz"
        continue
    else:
        print i
