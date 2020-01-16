#!/usr/bin/python
import __future__
from optparse import OptionParser
from sys import argv
import gzip


colours = {
    "HEADER": "\033[95m",
    "BOLD": "\033[1m",
    "UNDERLINE": "\033[4m",
    "ENDC": "\033[0m",
    "GREEN": "\033[92m",
    "RED": "\033[91m",
    "PURPLE": "\033[35m",
    "YELLOW": "\033[93m",
    "CYAN": "\033[36m",
}


# Patching gzip.open due to bug (not fixed in python <= 2.6.6)
# https://bugs.python.org/issue3860
# https://bugs.python.org/file12398/withgzip.patch
class gzipPatch(gzip.GzipFile):
    """
    Patch gzip.GzipFile if python version <= 2.6.6
    """
    def __enter__(self):
        if self.fileobj is None:
            raise ValueError("I/O operation on closed GzipFile object")
        return self

    def __exit__(self, *args):
        self.close()


def openfile(filename):
    '''
    Check if input file is a compressed or regular file
    '''
    try:
        if filename.endswith('.gz'):
            return gzipPatch(filename, "rt")
        return open(filename, "r")
    except AttributeError:
        return open(filename, "r")


def usage_overview(log):
    """
    Total bandwidth for each unique resource
    """
    d = {}
    
    with openfile(log) as log:
        for line in log:
            line = line.split()
            try:
                d[line[6]] = d.setdefault(line[6], 0) + int(line[9])
            except IndexError:
                pass
    
    sorted_d = sorted(d.items(), key=lambda kv: kv[1])
    
    for i in sorted_d:
        total_size = round((float(i[1]/1024) / 1024), 2)
        if total_size != 0:
            print("File: {0}  {2}Total Bandwidth{4} {3}{1}{4} MB".format(i[0], total_size, colours["YELLOW"], colours["RED"], colours["ENDC"]))


def main():
    '''
    Usage and help overview
    Option pasring
    '''
    parser = OptionParser(usage='usage: %prog [option]')
    parser.add_option(
    "-f", "--file",
    action="store",
    dest="file",
    metavar="File",
    help="Specify a log to check")


    (options, args) = parser.parse_args()
    if options.file:
        usage_overview(options.file)

if __name__ == '__main__':
    main()
