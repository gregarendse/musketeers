#!/bin/python3

import logging
import os
import threading
import time
from time import sleep
from typing import List

import httpx
import yaml
from python_on_whales import docker

DIRECTORY: str = ".data/docker/{cpu}_{mem}/"
# -n    This specifies JMeter is to run in cli mode
# -t    [name of JMX file that contains the Test Plan].
# -l    [name of JTL file to log sample results to].
# -j    [name of JMeter run log file].
# -r    Run the test in the servers specified by the JMeter property "remote_hosts"
# -R    [list of remote servers] Run the test in the specified remote servers
# -g    [path to CSV file] generate report dashboard only
# -e    generate report dashboard after load test
# -o    output folder where to generate the report dashboard after load test. Folder must not exist or be empty
# -f    force delete existing results files and web report folder if present before starting the test
COMMAND: str = "jmeter -n -t {test_file} -e -l .data/docker/{cpu}_{mem}/log.jtl  -o .data/docker/{cpu}_{mem} -f"

statuses: List[bool] = [False]
stop: List[bool] = [False]
logging.basicConfig(level=logging.INFO)


def readiness() -> bool:
    try:
        r = httpx.get("http://localhost:8080/actuator/health/readiness")
        logging.info(r)
        return r.is_success
    except:
        return False


def probe(i: int = 1, readies: List = None):
    logging.info("starting probe")
    while True not in stop:
        sleep(i)
        readies[0] = readiness()


def wait_for_ready() -> bool:
    logging.info("Wait for readiness")
    start = time.time()  # Time in seconds
    while time.time() - start < 60:
        sleep(1)

        # Check if container is still running
        for container in docker.compose.ps():
            if container.name == "musketeers-musketeers-1":
                if not container.state.running:
                    logging.warning("Not running")
                    return False

        # Check if container is ready
        if True in statuses:
            logging.info("status: Ready, duration: {}".format(time.time() - start))
            return True

    logging.warning("Timmd out")
    return False


threads: List[threading.Thread] = []

threads.append(
    threading.Thread(target=probe, args=(1, statuses))
)

for thread in threads:
    thread.start()

# Restore values
with open('../../../docker-compose.yaml.bak', 'r') as file:
    compose = yaml.safe_load(file)
with open('../../../docker-compose.yaml', 'w') as file:
    yaml.dump(compose, file)

memory = int(
    str(compose['services']['musketeers']['deploy']['resources']['limits']['memory']).replace('M', '')
)
cpu = float(compose['services']['musketeers']['deploy']['resources']['limits']['cpus'])
step = memory

# # Find memory limit
# status = True
# while step > 1:
#     memory = int(
#         str(compose['services']['musketeers']['deploy']['resources']['limits']['memory']).replace('M', '')
#     )
#     step = int(step / 2)#     logging.info("Start services")
#     docker.compose.up(detach=True)
#
#     status = wait_for_ready()
#     logging.info(status)
#
#     with open('docker-compose.yaml', 'r') as file:
#         compose = yaml.safe_load(file)
#
#     logging.info(memory)
#     logging.info(step)
#
#     if not status:
#         # Increase memory (half)
#         logging.info("Increase memory")
#         logging.info(str(memory) + "M -> " + str(memory + step) + "M")
#         compose['services']['musketeers']['deploy']['resources']['limits']['memory'] = str(memory + step) + "M"
#     else:
#         # Decrease memory (half)
#         logging.info("Decrease memory")
#         logging.info(str(memory) + "M -> " + str(step) + "M")
#         compose['services']['musketeers']['deploy']['resources']['limits']['memory'] = str(memory - step) + "M"
#
#     with open('docker-compose.yaml', 'w') as file:
#         yaml.dump(compose, file)

# TODO: Run test

cmd: str = "jmeter -n -t \"test.jmx\" -e -l log.jtl -o .data\jmeter -f"
# Find CPU limit
step = cpu
while step > 0.01:
    with open('../../../docker-compose.yaml', 'r') as file:
        compose = yaml.safe_load(file)

    cpu = float(
        str(compose['services']['musketeers']['deploy']['resources']['limits']['cpus'])
    )
    step = step / 2

    logging.info("Start services")
    docker.compose.up(detach=True)

    status: bool = wait_for_ready()
    logging.info(status)

    if status:
        # Run tests
        os.mkdir(DIRECTORY.format(cpu=cpu, mem=memory))
        os.system(COMMAND.format(test_file="../../../test.jmx", cpu=cpu, mem=memory))

    logging.info(memory)
    logging.info(step)

    if not status:
        # Increase CPU (half)
        logging.info("Increase CPU")
        logging.info(str(cpu) + " -> " + str(cpu + step))
        compose['services']['musketeers']['deploy']['resources']['limits']['cpus'] = str(cpu + step)
    else:
        # Decrease CPU (half)
        logging.info("Decrease cpu")
        logging.info(str(cpu) + " -> " + str(cpu - step))
        compose['services']['musketeers']['deploy']['resources']['limits']['cpus'] = str(cpu - step)

    with open('../../../docker-compose.yaml', 'w') as file:
        yaml.dump(compose, file)

logging.info("Stop probes")
for thread in threads:
    stop[0] = True
    thread.join()

logging.info("Shut down")
docker.compose.down()
