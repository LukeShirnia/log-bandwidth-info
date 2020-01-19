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
                if not resources.get(location):
                    resources[location] = {}
                # Calculate total size of all occurrences
                resources[location]["total_size"] = \
                    resources[location].setdefault("total_size", 0) + \
                    int(line[9])
                resources[location]["count"] = \
                    resources[location].setdefault("count", 0) + 1
                resources[location]["average"] = \
                    resources[location].setdefault("average", 0)
                resources[location]["average"] = \
                    (resources[location]["total_size"] /
                     resources[location]["count"] / 1024) / 1024
                total += int(line[9])
            except IndexError:
                pass
        if not end:
            end = datetime.datetime.strptime(
                (line[3]).strip("[]"), "%d/%b/%Y:%H:%M:%S")

    general_info = (start, end, total)

    return resources, general_info


def top_consumers(raw_info, number, general_info, sort):
    """
    Print function for gathered log information
    """
    sorted_resources = sorted(raw_info.items(), key=lambda k: k[1][sort])

    for item in sorted_resources[number:]:
        total_size = round((float(item[1]["total_size"]/1024) / 1024), 2)
        if total_size != 0:
            print("R: {0:>65}  "
                  "{4}C:{6} {5}{2}{6}  {4}"
                  "TB: {5}{1:,} MB{6} {4}"
                  "A:{6} {5}{3} MB{6}".format(
                      item[0], total_size, item[1]["count"],
                      round(item[1]["average"], 2),
                      COLOURS["YELLOW"], COLOURS["RED"], COLOURS["ENDC"]))

    print()
    print("R = Resource, C = Count, TB = Total Bandwidth, A = Average size")

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
    parser.add_option(
        "-S", "--sort",
        action="store",
        dest="sort",
        metavar="t/c/s",
        help="Specify a sort method (total(t)/count(c)/size(s)/average(a))")

    (options, _) = parser.parse_args()

    # Defaults
    num = 25  # Default number of instances to print
    sort_methods = \
        {"t": "total_size", "c": "count", "s": "size", "a": "average"}
    sort = sort_methods["t"]  # Default sorting method

    if options.file:
        raw_log_info, general_info = get_log_info(options.file)

    if options.num:
        num = "{0}".format(options.num)

    if options.sort in sort_methods.keys():
        sort = sort_methods[options.sort]

    try:
        top_consumers(raw_log_info, -int(num), general_info, sort)
    except UnboundLocalError:
        print("No Log File Provided")


if __name__ == '__main__':
    main()
