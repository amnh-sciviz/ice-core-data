
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

    yearbp = present-year
    if "bp" in entry:
        bp = entry["bp"]
        yearbp = (present - bp) + year

    if yearbp > startYearsBP or yearbp < 0 or yearbp in years:
        return False

    error = 0
    if "error" in entry:
        error = entry["error"]
    elif "errorKey" in entry:
        error = row[entry["errorKey"]]
    elif "errorUpperKey" in entry:
        errorUpper = row[entry["errorUpperKey"]]
        error = abs(errorUpper-value)

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
        return string

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

def rounddown(x, nearest):
    return int(math.floor(1.0 * x / nearest)) * nearest

def roundup(x, nearest):
    return int(math.ceil(1.0 * x / nearest)) * nearest

def showGraph(dataManifest, present, startYearsBP):
    import matplotlib.pyplot as plt

    for entry in dataManifest:
        data = readTxt(entry["file"])
        years = []
        values = []
        for row in data:
            result = getTuple(entry, row, present, startYearsBP)
            if result:
                yearbp, value, error = result
                years.append(yearbp)
                values.append(value)
        plt.plot(years, values, color=entry["color"], label=entry["label"])

    plt.ylabel('Value')
    plt.xlabel('Years Before %s' % present)
    plt.gca().invert_xaxis()
    plt.legend()
    plt.show()
