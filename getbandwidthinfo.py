#!/usr/bin/python
"""
Place holder
"""
import __future__
from optparse import OptionParser
import gzip
import platform
import datetime


COLOURS = {
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
class GzipPatch(gzip.GzipFile):
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
            if float(platform.python_version().replace(".", "")) < 270:
                return GzipPatch(filename, "rt")
            return gzip.open(filename, "rt")
        return open(filename, "r")
    except AttributeError:
        return open(filename, "r")


def get_log_info(log):
    """
    Total bandwidth for each unique resource
    """
    resources = {}
    start = ""
    end = ""
    total = 0

    with openfile(log) as access_log:
        for line in access_log:
            line = line.split()
            if not start:
                start = datetime.datetime.strptime(
                    (line[3]).strip("[]"), "%d/%b/%Y:%H:%M:%S")
            try:
                location = line[6].split("?id", 1)[0]
                resources[location] = \
                    resources.setdefault(location, 0) + int(line[9])
                total += int(line[9])
            except IndexError:
                pass
        if not end:
            end = datetime.datetime.strptime(
                (line[3]).strip("[]"), "%d/%b/%Y:%H:%M:%S")

    general_info = (start, end, total)
    sorted_resources = sorted(resources.items(), key=lambda kv: kv[1])
    return sorted_resources, general_info


def top_consumers(resource_info, number, general_info):
    """
    Print function for gathered log information
    """
    for i in resource_info[number:]:
        total_size = round((float(i[1]/1024) / 1024), 2)
        if total_size != 0:
            print("Resource: {0}  {2}Total Bandwidth{4} {3}{1:,}{4} MB".format(
                i[0], total_size,
                COLOURS["YELLOW"], COLOURS["RED"], COLOURS["ENDC"]))

    print()
    print("Start Time: {0}".format(
        datetime.datetime.strftime(general_info[0], '%d/%b/%Y %H:%M:%S')))
    print("End Time  : {0}".format(
        datetime.datetime.strftime(general_info[1], '%d/%b/%Y %H:%M:%S')))
    print("Total Time: {0}".format(
        general_info[1] - general_info[0]))
    print("Total Size in timeframe: {0:,} MB".format(
        round((float(general_info[2]/1024) / 1024), 2)))
    print()


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
    parser.add_option(
        "-s", "--show",
        action="store",
        dest="num",
        metavar="Number",
        help="Show number of instances you wish to display")

    (options, _) = parser.parse_args()
    num = 25  # Default number of instances to print

    if options.file:
        log_info, general_info = get_log_info(options.file)

    if options.num:
        num = "{0}".format(options.num)

    try:
        top_consumers(log_info, -int(num), general_info)
    except UnboundLocalError:
        print("No Log File Provided")


if __name__ == '__main__':
    main()
