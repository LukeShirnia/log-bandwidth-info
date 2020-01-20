# logfile-bandwidth-info

Status: In Progress - The script is in a working state

### Travis ###

![Build Status](https://travis-ci.com/LukeShirnia/logfile-bandwidth-info.svg?branch=master)

## Description ##

This script is designed to gather information from a specified log file. 
<br />
It gathers the resources requested from the web server and calculates the outgoing Bandwidth used to serve the content.
In addition to Bandwidth, it also calculates;

- Resource Count (how many times a resource was requested)
- The average process size (total / count)

### Usage ###

```
(python3)[local@local]$ python getbandwidthinfo.py  -h
Usage: getbandwidthinfo.py [option]

Options:
  -h, --help            show this help message and exit
  -f File, --file=File  Specify a log to check
  -s Number, --show=Number
                        Show number of instances you wish to display
  -S t/c/s, --sort=t/c/s
                        Specify a sort method (total(t)/count(c)/average(a))
  -H hours, --hours=hours
                        Check the last x hours in log file
```

##### Basic Examples #####
No options - Sorts by Total Bandwidth - Prints top 25 items
```
$ python getbandwidthinfo.py -f access_ssl_log.processed.1.gz
```
Number (-S/--show) Option Specified - Sorts by Total Bandwidth - Prints 1000 items from file
```
$ python getbandwidthinfo.py -f access_ssl_log.processed.1.gz --show 1000
```
Sort (-s/--sort) Option Specified - Sorts by Count - Prints top 25 items
```
$ python getbandwidthinfo.py -f access_ssl_log.processed.1.gz --sort c
```
Hour (-H/--hours) option Specified - Sorts by Total Bandwidth - Calculates on entries displayed in the last 2 hours
```
$ python getbandwidthinfo.py -f access_ssl_log.processed.1.gz --hours 2
```
#### Compatibility ####

Python:
- 2.6.x
- 2.7.x
- 3.6.x
- 3.7.x