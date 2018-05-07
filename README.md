# Ice core data

Scripts for processing and standardizing ice core data

## The processed data

The processed data is found in a single json file [all-data.json](all-data.json), but is also split into individual data files:

- [co2/data/co2.json](co2/data/co2.json)
- [temperature/data/temperature.json](temperature/data/temperature.json)
- [sealevel/data/sealevel.json](sealevel/data/sealevel.json)
- [population/data/population.json](population/data/population.json)

## Instructions for generating new data

Each dataset is in their own subdirectory (./co2, ./temperature, ./sealevel, ./population) and each subdirectory has a `config.json` file that acts like a manifest for the data files to process as well as configurable variables.

CO2 data is processed by default:

```
python processData.py
```

You can also view a graph of the data:

```
python processData.py -graph 1
```

For temperature:

```
python processData.py -in temperature/config.json -graph 1
python processData.py -in temperature/config.json -out temperature/data/temperature.json -round 5
```

For sea level:

```
python processData.py -in sealevel/config.json -graph 1
python processData.py -in sealevel/config.json -out sealevel/data/sealevel.json -round 20
```

For population:

```
python processData.py -in population/config.json -graph 1
python processData.py -in population/config.json -out population/data/population.json
```

Each will output it's own data file as well as add to a `all-data.json` combined dataset in the format:

```
"id": {
  "id": "<string>",
  "title": "<string>",
  "description": "<string>",
  "domain": [<int in years bp>, <int in years bp>],
  "range": [<float>, <float>],
  "xLabel": "<string>",
  "yLabel": "<string>",
  "header": ["yearsbp", "value", "error"],
  "data": [
    [<the year bp>, <the value>, <the error>],
    [<the year bp>, <the value>, <the error>],
    [<the year bp>, <the value>, <the error>],
    ...
  ]
}
```
