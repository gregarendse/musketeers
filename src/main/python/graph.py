#!/usr/bin/python3

# Import libraries
import csv
import dataclasses
import os
from typing import List, Dict

import matplotlib.pyplot as plt


@dataclasses.dataclass
class Data:
    timestamp: int
    elapsed: int


@dataclasses.dataclass
class Source:
    name: str
    location: str
    data: dict[str, Data]


sources: List[Source] = [Source(
    name="unrestricted",
    location='.data/Unrestricted host/log.jtl',
    data=dict()
), Source(
    name="Host 128M",
    location='.data/Host 128M/log.jtl',
    data=dict()
), Source(
    name="Host 64M",
    location='.data/Host 64M/log.jtl',
    data=dict()
), Source(
    name="Host 32M",
    location='.data/Host 32M/log.jtl',
    data=dict()
), Source(
    name="Docker 128M",
    location='.data/Docker 128M/log.jtl',
    data=dict()
)]

things: Dict[str, Dict[str, List[int]]] = dict()

for root, dirs, files in os.walk('.data/docker'):
    print(root)
    print(dirs)
    print(files)

    for dirname in dirs:
        things[dirname] = dict()

        with open("{}/{}/log.jtl".format(root, dirname), 'r') as file:
            csvFile = csv.reader(file)
            for line in csvFile:
                try:
                    elapsed = int(line[1])
                    if things[dirname].get(line[2]) is None:
                        things[dirname][line[2]] = []
                    things[dirname][line[2]].append(elapsed)
                except:
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
    plt.savefig('.data/{}.png'.format(k))
    plt.close()

exit()

for source in sources:

    with open('.data/Unrestricted host/log.jtl', 'r') as file:
        data: [Dict[str, List[Data]]] = dict()
        for line in file.readlines()[1:]:
            parts = line.split(',')

            if len(parts) < 2:
                print(parts)
                continue

            if data.get(parts[2]) is None:
                data[parts[2]] = []

            try:
                data[parts[2]].append(Data(
                    timestamp=int(parts[0]),
                    elapsed=int(parts[1])
                ))
            except:
                print(parts)

        source.data = data

        # timeStamp,elapsed,label,responseCode,responseMessage,threadName,dataType,success,failureMessage,bytes,sentBytes,grpThreads,allThreads,URL,Latency,IdleTime,Connect

creates: List[List[int]] = []

for source in sources:
    creates.append([data.elapsed for data in source.data.get('Create')])

plt.boxplot(
    creates,
    labels=[source.name for source in sources],
    showfliers=False
)

plt.show()
