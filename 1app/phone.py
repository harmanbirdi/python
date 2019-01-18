#!/usr/bin/env python

#
# Description : Let's say I have some files and sub-directories in a directory tree.
#               Given the path to this directory, I want you to write a script or even a single command-line/shell
#               statement (if you can) that will examine each file found within the directory tree and print out any
#               lines that contain possible phone numbers. Let's assume a phone number is 10 digits in length.
#                   o xxx.xxx.xxxx is a valid phone number
#                   o (xxx) xxx-xxxx is also a valid phone number
#                   o xxxxxxxxxx is also a valid phone number
#
#               Bonus:
#                   o if the script can also print out the full path and filename of the file before printing
#                     the matching lines with phone numbers
#                   o if the script can reformat the phone number into a standard, normalized form
#                   o if the script can also detect possible phone numbers with country codes
#                     e.g. +20 010 012 5486
# Implementation: Uses the Tree class with the optional function processing capability for each file.
#                 The print_phones function is passes to the Tree class, which prints the tree and runs
#                 print_phones function for text (ASCII) files, but displays errors for binary files.
# More Info   : Asked by Nour for 1app phone screen interview
# __author__  : Harman Birdi
# Date        : Sep 16, 2016
# TODO        : Detect phone numbers with its country code
#

import sys
import re
import commands

from colors import Colors
from tree import Tree
from optparse import OptionParser


def find_phones(fle):
    """
    This method finds all the phones that match on a line (only one per line)
    :param fle:
        Full path to the input file
    :return:
        List of phone numbers
    """
    digits = []

    fh = open(fle)
    lines = fh.readlines()

    # Remove all non-digits from the line - quick hack instead of doing various pattern recognition
    # for phone numbers. Proper regex would be better way to go. It returns only first 10 numbers
    # matched on each line.
    for line in lines:
        digits.append(re.sub('\D', '', line))

    fh.close()

    return [phone for phone in digits if len(phone) == 10]


def normalize(phones):
    """
    This method normalizes and returns phone list to (xxx) xxx-xxxx format
    :param phones:
        List of phone numbers that needs to be normalized.
    :return:
        List of normalized phone numbers.
    """
    fones = []

    for phone in phones:
        fones.append('(%s) %s-%s' % (phone[0:3], phone[3:6], phone[6:]))

    return fones


def print_phones(**kwargs):
    """
    Function passed to tree which is called for a file by the Tree.process_tree() method
    :param kwargs:
    :return:
    """
    full_path = kwargs['full_path']
    separator = kwargs['separator']
    depth = kwargs['depth']

    mime = commands.getoutput('file %s' % full_path)

    try:
        if 'empty' in mime:
            pass
        elif 'text' in mime:
            phones = normalize(find_phones(full_path))
            for phone in phones:
                print separator * (Tree.depth + 1), phone
        else:
            print separator * (depth + 1),
            print Colors.FAIL + 'ERROR: File is of binary type' + Colors.ENDC

    except ValueError:
        pass


# Main starts here
if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-d", "--dir", dest="dirname", help="Directory name for tree", metavar="DIR")

    (options, args) = parser.parse_args()

    if options.dirname is None:
        err = Colors.FAIL + ' Dirname argument cannot be empty.\n'
        err += ' Use -h flag for additional help.\n' + Colors.ENDC
        sys.stderr.write(err)
        exit(1)

    dirname = options.dirname
    tree = Tree()
    tree.process_tree(dirname, func=print_phones)
