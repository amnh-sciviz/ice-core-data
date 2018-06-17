
import math
import os
import sys

def getRange(values, nearest=1):
    minValue = rounddown(min(values), nearest)
    maxValue = roundup(max(values), nearest)
    return [minValue, maxValue]

def getTuple(entry, row, present, startYearsBP, years=[]):
    year = row[entry["yearKey"]]
    value = row[entry["valueKey"]]

    if "yearMult" in entry:
        year *= entry["yearMult"]

    if "valueMult" in entry:
        value *= entry["valueMult"]

    if "emptyValue" in entry:
        emptyValue = entry["emptyValue"]
        if int(value) == int(emptyValue):
            value = False

    yearbp = present-year
    if "bp" in entry:
        bp = entry["bp"]
        yearbp = (present - bp) + year

    if yearbp > startYearsBP or yearbp < 0 or yearbp in years:
        return False

    error = False

    if "errorKey" in entry:
        error = row[entry["errorKey"]]
    elif "errorUpperKey" in entry:
        errorUpper = row[entry["errorUpperKey"]]
        if errorUpper is not False:
            error = abs(errorUpper-value)

    if error is False and "error" in entry:
        error = entry["error"]

    if error is False:
        error = 0

    return (yearbp, value, error)


def parseData(dataManifest, present, startYearsBP):
    years = []
    dataOut = []

    for entry in dataManifest:
        data = readTxt(entry["file"])

        for row in data:
            result = getTuple(entry, row, present, startYearsBP, years)
            if result:
                yearbp, value, error = result
                if value is not False:
                    years.append(yearbp)
                    dataOut.append([
                        int(yearbp),
                        value,
                        error
                    ])

    # sort by year descending
    dataOut = sorted(dataOut, key=lambda k: k[0], reverse=True)
    return dataOut

def parseNumber(string):
    try:
        num = float(string)
        return num
    except ValueError:
        return False

def parseNumbers(arr):
    for i, item in enumerate(arr):
        for key in item:
            arr[i][key] = parseNumber(item[key])
    return arr

def readTxt(filename):
    rows = []
    if os.path.isfile(filename):
        with open(filename, 'rb') as f:
            lines = [line.split() for line in f if not line.startswith("#")]
            header = lines.pop(0)
            rows = []
            for line in lines:
                row = {}
                for i,h in enumerate(header):
                    try:
                        row[h] = line[i]
                    except IndexError:
                        print "Index Error %s" % filename
                        sys.exit(1)
                rows.append(row)
            rows = parseNumbers(rows)
    return rows

def reduceData(data):
    reducedLookup = {}
    years = []
    nearest = 100
    digits = len(str(nearest))
    for d in data:
        year = d[0]
        value = d[1]

        if len(str(year)) > digits:
            year = str(roundto(year, nearest))
            if year not in reducedLookup:
                years.append(year)
                reducedLookup[year] = d
        else:
            year = str(year)
            years.append(year)
            reducedLookup[year] = d

    reduced = [reducedLookup[y] for y in years]
    return reduced

def rounddown(x, nearest):
    return int(math.floor(1.0 * x / nearest)) * nearest

def roundto(x, nearest):
    return int(round(1.0 * x / nearest)) * nearest

def roundup(x, nearest):
    return int(math.ceil(1.0 * x / nearest)) * nearest

def showGraph(dataManifest, present, startYearsBP, cropData=False):
    import matplotlib.pyplot as plt

    ranges = []

    for entry in dataManifest:
        data = readTxt(entry["file"])
        years = []
        values = []
        for row in data:
            result = getTuple(entry, row, present, startYearsBP)
            if result:
                yearbp, value, error = result
                if value is not False:
                    found = False
                    for r in ranges:
                        if r[0] <= yearbp <= r[1]:
                            found = True
                    if not cropData or not found:
                        years.append(yearbp)
                        values.append(value)
        plt.plot(years, values, color=entry["color"], label=entry["label"])
        ranges.append([min(years), max(years)])

    plt.ylabel('Value')
    plt.xlabel('Years BP')
    plt.gca().invert_xaxis()
    plt.legend()
    plt.show()
