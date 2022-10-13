#!/usr/bin/python3

# Import libraries
import csv
import dataclasses
import logging
import os
from typing import List, Dict

import matplotlib.pyplot as plt

ROOT: str = '.data/comparison'


@dataclasses.dataclass
class Data:
    timestamp: int
    elapsed: int


@dataclasses.dataclass
class Source:
    name: str
    location: str
    data: dict[str, Data]


things: Dict[str, Dict[str, List[int]]] = dict()
combined: Dict[str, List[int]] = dict()

for root, dirs, files in os.walk(ROOT):
    print(root)
    print(dirs)
    print(files)

    for dirname in dirs:
        if dirname in ['cpu', 'memory']:
            continue
        try:
            key = "{:.0f}m".format(float(dirname.split('_')[0]) * 1000)
            # key = str(int(dirname.split('_')[1])) + 'M'
        except:
            key = dirname

        things[key] = dict()
        combined[key] = []

        with open("{}/{}/log.jtl".format(root, dirname), 'r') as file:
            csvFile = csv.reader(file)
            next(csvFile)  # Skip header row
            for line in csvFile:

                if line[7] != 'true':
                    del things[key]
                    del combined[key]
                    logging.info("Ignoring results, " + key)
                    break

                try:
                    elapsed = int(line[1])
                    if things[key].get(line[2]) is None:
                        things[key][line[2]] = []
                    things[key][line[2]].append(elapsed)
                    combined[key].append(elapsed)
                except ValueError:
                    print(line)

    break

plots: List = []

label_map: Dict[str, List[List[int]]] = dict()
for run in things.values():
    for label in run.keys():
        if label_map.get(label) is None:
            label_map[label] = []
        label_map[label].append(run[label])

for k, v in label_map.items():
    bx = plt.boxplot(
        v,
        labels=things.keys(),
        showfliers=False
    )
    # ['Solarize_Light2', '_classic_test_patch', '_mpl-gallery', '_mpl-gallery-nogrid', 'bmh', 'classic', 'dark_background', 'fast', 'fivethirtyeight', 'ggplot', 'grayscale', 'seaborn', 'seaborn-bright', 'seaborn-colorblind', 'seaborn-dar
    # k', 'seaborn-dark-palette', 'seaborn-darkgrid', 'seaborn-deep', 'seaborn-muted', 'seaborn-notebook', 'seaborn-paper', 'seaborn-pastel', 'seaborn-poster', 'seaborn-talk', 'seaborn-ticks', 'seaborn-white', 'seaborn-whitegrid', 'tableau-colorblind10']
    plt.title(k)
    plt.xlabel("Run")
    plt.ylabel("Response Time (ms)")
    plt.savefig('{}/{}.png'.format(ROOT, k))
    plt.close()

plt.boxplot(
    combined.values(),
    labels=combined.keys(),
    showfliers=False
)
plt.title('Combined')
plt.xlabel("Run")
plt.ylabel("Response Time (ms)")
plt.savefig('{}/{}.png'.format(ROOT, 'combined'))
plt.close()
