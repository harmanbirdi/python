#!/usr/bin/env python

#
# Description : Print the directory tree of a given directory using any scripting language
#              (i.e. anything *except* for a Bash script or a plain shell command). If the file
#              ends in '.txt', also print its contents line-by-line. It utilizes the Tree class
#              in order to print out the directory and files, and sends in print_file function
#              to print out files with 'txt' extension.
# More Info   : Asked by Nour for 1app phone screen interview
# __author__  : Harman Birdi
# Date        : Sep 16, 2016
#

import commands
import os
import sys

from colors import Colors
from tree import Tree
from optparse import OptionParser


def print_file(**kwargs):
    """
    Function passed to tree which is called for a file by the Tree.process_tree() method
    :param kwargs:
    :return:
    """
    full_path = kwargs['full_path']
    separator = kwargs['separator']
    depth = kwargs['depth']
    extn = kwargs['extn']

    fle = os.path.basename(full_path)
    mime = commands.getoutput('file %s' % full_path)

    try:
        (fname, ext) = fle.split('.')

        if ext == extn and 'ASCII' in mime:
            msg = "START: File contents: %s" % fle
            print '-' * len(msg)
            print msg
            print '-' * len(msg)
            fh = open(full_path)
            print ''.join(fh.readlines())
            msg = "END: File contents: %s" % fle
            print '-' * len(msg)
            print msg
            print '-' * len(msg)
            fh.close()
        elif ext == extn and 'ASCII' not in mime:
            print separator * (depth + 1),
            print Colors.FAIL + 'ERROR: Extension matches but file is not of text type' + Colors.ENDC

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
    tree.process_tree(dirname, extn='txt', func=print_file)
