#!usr/bin.env python

#
# Description : Print the directory tree of a given directory using any scripting language
#              (i.e. anything *except* for a Bash script or a plain shell command). If the file
#              ends in '.txt', also print its contents line-by-line.
# More Info   : Asked by Nour for 1app phone screen interview
# __author__  : Harman Birdi
# Date        : Sep 16, 2016
#

import os
import sys
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


class Tree:
    depth = 1  # The depth of the tree

    def __init__(self):
        pass

    @staticmethod
    def print_file(fle):
        msg = "START: File contents: %s" % fle
        print '-' * len(msg)
        print msg
        print '-' * len(msg)
        fh = open(fle)
        print ''.join(fh.readlines())
        msg = "END: File contents: %s" % fle
        print '-' * len(msg)
        print msg
        print '-' * len(msg)

    def process_tree(self, dname, extn='txt'):

        dirlist = os.listdir(dname)

        if dirlist:
            for fle in dirlist:
                if fle.startswith('.'):  # Ignore hidden files and directories
                    continue
                elif os.path.isdir(os.path.join(dname, fle)):
                    print '\t' * Tree.depth,
                    print Colors.HEADER + "%s/" % fle + Colors.ENDC
                    Tree.depth += 1
                    self.process_tree(os.path.join(dname, fle), extn)
                elif os.path.isfile(os.path.join(dname, fle)):
                    try:
                        (fname, ext) = fle.split('.')
                        print '\t' * Tree.depth,
                        print Colors.OKBLUE + "%s" % fle + Colors.ENDC

                        if ext == extn:
                            Tree.print_file(os.path.join(dname, fle))

                    except ValueError:
                        pass

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
