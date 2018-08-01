#!usr/bin/env python

#
# Description : Print the directory tree of a given directory using any scripting language
#              (i.e. anything *except* for a Bash script or a plain shell command).
# More Info   : Asked by Nour for 1app phone screen interview
# __author__  : Harman Birdi
# Date        : Sep 16, 2016
#

import os
import sys
from colors import Colors
from optparse import OptionParser


class Tree:
    """
    Tree class to print out a directory structure. It also prints out the contents of
    text (.txt) files by default unless a different extension is provided and file is
    of ASCII type.
    """
    depth = 1  # The depth of the tree

    def __init__(self):
        pass

    def process_tree(self, dname, extn='txt', func=None):
        """
        This method processes the directory recursively and prints out all files that
        match extension type of files.

        :param dname:
        :param extn:
        :param func:
            An optional function can be passed in for processing a file that can utilize the following
            keyword parameters.
                full_path: Full path to the file
                depth: The tree depth at which this file was found
                extn: Extension of the file, in case matches need to be done against a particular type of file
                separator: Spacing needed to preserve padded output, if needed
        :return:
        """
        dirlist = os.listdir(dname)
        separator = '    '

        if dirlist:
            for fle in dirlist:
                full_path = os.path.join(dname, fle)

                if fle.startswith('.'):  # Ignore hidden files and directories
                    continue
                elif os.path.isdir(full_path):
                    print separator * Tree.depth,
                    print Colors.HEADER + "%s/" % fle + Colors.ENDC
                    Tree.depth += 1
                    self.process_tree(full_path, extn, func)
                elif os.path.isfile(full_path):
                    print separator * Tree.depth,
                    print Colors.OKBLUE + "%s" % fle + Colors.ENDC

                    if func is not None:
                        func(full_path=full_path, depth=Tree.depth, extn=extn, separator=separator)

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
