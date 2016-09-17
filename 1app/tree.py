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
import commands
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


# Tree class to print out a directory structure. It also prints out the contents of
# text (.txt) files by default unless a different extension is provided.
# TODO: Figure out if the file is of text type and accept only that extension
# TODO: For other show message saying its a binary file.
class Tree:
    depth = 1  # The depth of the tree

    def __init__(self):
        pass

    # This method just prints out the contents of the file
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

    # This method processes the directory recursively and prints out all files that
    # match extension type of files
    def process_tree(self, dname, extn='txt'):
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
                    self.process_tree(full_path, extn)
                elif os.path.isfile(full_path):
                    mime = commands.getoutput('file %s' % full_path)

                    try:
                        (fname, ext) = fle.split('.')
                        print separator * Tree.depth,
                        print Colors.OKBLUE + "%s" % fle + Colors.ENDC

                        if ext == extn and 'ASCII' in mime:
                             Tree.print_file(full_path)
                        elif ext == extn and 'ASCII' not in mime:
                            print separator * (Tree.depth + 1),
                            print Colors.FAIL +'ERROR: Extension matches but file is not of text/plain type' + Colors.ENDC

                    except ValueError:
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
