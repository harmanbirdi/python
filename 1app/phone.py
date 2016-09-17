#!usr/bin.env python

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
# More Info   : Asked by Nour for 1app phone screen interview
# __author__  : Harman Birdi
# Date        : Sep 16, 2016
# TODO        : Detect phone numbers with its country code
#

import os
import sys
import re
import mimetypes
from optparse import OptionParser


# To colorize the output - assume terminal can handle this for now.
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def __init__(self):
        pass


# Tree class to recursively process all text/plain files in a directory structure.
# It also prints out the phone number matches in all of those files that have
# 10 digit numbers in a normalized manner
class Tree:
    depth = 1  # The depth of the tree

    def __init__(self):
        pass

    @staticmethod
    def find_phones(fle):
        digits = []

        fh = open(fle)
        lines = fh.readlines()

        # Remove all non-digits from the line - quick hack instead of doing various pattern recognition
        # for phone numbers. Proper regex would be better way to go. It returns only first 10 numbers
        # matched on each line.
        for line in lines:
            digits.append(re.sub('\D', '', line))

        return [phone for phone in digits if len(phone) == 10]

    # This method normalizes and returns phone list to (xxx) xxx-xxxx format
    @staticmethod
    def normalize(phones):
        fones = []

        for phone in phones:
            fones.append('(%s) %s-%s' % (phone[0:3], phone[3:6], phone[6:]))

        return fones

    # This method processes the directory recursively and prints out all files that
    # match extension type of files
    def process_tree(self, dname):
        dirlist = os.listdir(dname)
        separator = ' ' * 4  # Tabs are showing up as 8 chars on terminal, so using 4 spaces instead - its absolute

        if dirlist:
            for fle in dirlist:
                full_path = os.path.join(dname, fle)
                if fle.startswith('.'):  # Ignore hidden files and directories
                    continue
                elif os.path.isdir(full_path):
                    Tree.depth += 1
                    self.process_tree(full_path)
                elif os.path.isfile(full_path):
                    mime = mimetypes.guess_type(full_path)

                    if mime[0] == 'text/plain':  # Look in only plain text files
                        try:
                            phones = Tree.normalize(Tree.find_phones(full_path))

                            if phones:
                                print separator * Tree.depth,
                                print Colors.OKBLUE + '%s' % full_path + Colors.ENDC
                                for phone in phones:
                                    print separator * (Tree.depth + 1), phone
                        except ValueError:
                            pass
                    else:
                        pass

            Tree.depth -= 1
        else:
            Tree.depth -= 1

        return


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
    tree.process_tree(dirname)
