# -*- coding: utf-8 -*-

import argparse
import inspect
import json
import math
import os
import sys
from utils import *

# input
parser = argparse.ArgumentParser()
parser.add_argument('-in', dest="INPUT_FILE", default="co2/config.json", help="JSON file that contains manifest and config")
parser.add_argument('-present', dest="PRESENT", type=int, default=1988, help="The year to consider present")
parser.add_argument('-start', dest="START_YEARS_BP", type=int, default=110939, help="The years before present to start")
parser.add_argument('-graph', dest="SHOW_GRAPH", type=int, default=0, help="Display graph")
parser.add_argument('-round', dest="ROUND_RANGE_TO_NEAREST", type=int, default=10, help="Round the range to nearest number")
parser.add_argument('-out', dest="OUTPUT_FILE", default="co2/data/co2.json", help="Files to output to")
args = parser.parse_args()

INPUT_FILE = args.INPUT_FILE
PRESENT = args.PRESENT
START_YEARS_BP = args.START_YEARS_BP
SHOW_GRAPH = args.SHOW_GRAPH > 0
ROUND_RANGE_TO_NEAREST = args.ROUND_RANGE_TO_NEAREST
OUTPUT_FILES = [args.OUTPUT_FILE, "all-data.json"]

DATA = []
JSON_OUT = {}

with open(INPUT_FILE) as f:
    jsonIn = json.load(f)
    DATA = jsonIn["dataFiles"]
    JSON_OUT = jsonIn["output"]

# plot the data
if SHOW_GRAPH:
    showGraph(DATA, PRESENT, START_YEARS_BP)

# otherwise, output the data
else:
    dataOut = parseData(DATA, PRESENT, START_YEARS_BP)
    dataRange = getRange([d[1] for d in dataOut], ROUND_RANGE_TO_NEAREST)

    jsonOut = JSON_OUT
    jsonOut["domain"] = [START_YEARS_BP, 0]
    jsonOut["range"] = dataRange
    jsonOut["data"] = dataOut

    for filename in OUTPUT_FILES:
        dOut = {}

        # Read existing data if it exists
        if os.path.isfile(filename):
            with open(filename) as f:
                dOut = json.load(f)

        dOut[jsonOut["id"]] = jsonOut

        # Write to file
        with open(filename, 'w') as f:
            json.dump(dOut, f)
            print "Wrote %s items to %s" % (len(dataOut), filename)
