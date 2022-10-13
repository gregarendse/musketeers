#!/bin/python3

import csv
import logging
import os
import threading
import time
from time import sleep
from typing import List

import httpx
import yaml
from python_on_whales import docker

DIRECTORY: str = ".data/native/{cpu}_{mem}/"
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
# COMMAND: str = "jmeter -n -t {test_file} -l .data/docker/{cpu}_{mem}/log.jtl -j .data/docker/{cpu}_{mem}/jmeter.log -e  -o .data/docker/{cpu}_{mem} -f"
COMMAND: str = "jmeter -n -t {test_file} -l {directory}log.jtl -j {directory}jmeter.log -e  -o {directory} -f".format(
    directory=DIRECTORY,
    test_file="{test_file}"
)

statuses: List[bool] = [False]
stop: List[bool] = [False]
logging.basicConfig(level=logging.INFO)


def readiness() -> bool:
    try:
        r = httpx.get("http://localhost:8080/actuator/health/readiness")
        logging.debug(r)
        return r.is_success
    except:
        return False


def probe(i: int = 1, readies: List = None):
    logging.info("starting probe")
    while True not in stop:
        sleep(i)
        readies[0] = readiness()


def wait_for_ready(timeout: int = 120) -> bool:
    logging.info("Wait for readiness")
    start = time.time()  # Time in seconds
    while time.time() - start < timeout:
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

    logging.warning("Timed out")
    return False


threads: List[threading.Thread] = [
    threading.Thread(target=probe, args=(1, statuses))
]

# Start probes
for thread in threads:
    thread.start()

# Restore values
with open('docker-compose.yaml.bak', 'r') as file:
    compose = yaml.safe_load(file)
with open('docker-compose.yaml', 'w') as file:
    yaml.dump(compose, file)

memory: int = int(
    str(compose['services']['musketeers']['deploy']['resources']['limits']['memory']).replace('M', '')
)
cpu: float = float(compose['services']['musketeers']['deploy']['resources']['limits']['cpus'])


def verify_run():
    _success: bool = True
    with open(DIRECTORY.format(cpu=cpu, mem=memory) + "/log.jtl") as _file:
        csv_file = csv.reader(_file)
        next(csv_file)  # Skip header row

        for line in csv_file:
            _success = _success and (line[7] == 'true')
            if not _success:
                logging.info(line)
                break
    logging.info(line)
    return _success


def run_tests() -> bool:
    docker.compose.up(detach=True)

    _status: bool = wait_for_ready()

    if _status:
        logging.info("Starting Tests")
        # Run tests
        try:
            os.mkdir(DIRECTORY.format(cpu=cpu, mem=memory))
            os.system(COMMAND.format(test_file="test.jmx", cpu=cpu, mem=memory))
        except FileExistsError:
            pass
        _status = verify_run()
        logging.info("End Tests, status=" + str(_status))

    return _status


run_tests()

exit()

logging.info("Find memory limit")
step_memory: int = memory
status: bool = True
while step_memory > 8 or not status:
    with open('docker-compose.yaml', 'r') as file:
        compose = yaml.safe_load(file)

    step_memory = int(step_memory / 2)  # logging.info("Start services")

    logging.info("Check status: " + str(status))
    if not status:
        # Increase memory (half)
        logging.info("Increase memory, step={} : {}M -> {}M".format(step_memory, memory, memory + step_memory))
        memory = memory + step_memory
    else:
        # Decrease memory (half)
        logging.info("Decrease memory, step={} : {}M -> {}M".format(step_memory, memory, memory - step_memory))
        memory = memory - step_memory

    compose['services']['musketeers']['deploy']['resources']['limits']['memory'] = str(memory) + "M"
    with open('docker-compose.yaml', 'w') as file:
        yaml.dump(compose, file)

    status = run_tests()

logging.info("Memory limit=" + str(memory))

# Find CPU limit
step_cpu: float = cpu
status: bool = True
while step_cpu > 0.01 or not status:
    with open('docker-compose.yaml', 'r') as file:
        compose = yaml.safe_load(file)

    step_cpu = step_cpu / 2

    logging.info("Check status: " + str(status))
    if not status:
        # Increase CPU (half)
        logging.info("Increase CPU, step={} : {} -> {}".format(step_cpu, cpu, cpu + step_cpu))
        cpu = cpu + step_cpu
    else:
        # Decrease CPU (half)
        logging.info("Decrease CPU, step={} : {} -> {}".format(step_cpu, cpu, cpu - step_cpu))
        cpu = cpu - step_cpu

    if cpu < 0.01:
        cpu = 0.01

    compose['services']['musketeers']['deploy']['resources']['limits']['cpus'] = "{:.03f}".format(cpu)
    with open('docker-compose.yaml', 'w') as file:
        yaml.dump(compose, file)

    status = run_tests()

logging.info("Stop probes")
for thread in threads:
    stop[0] = True
    thread.join()

logging.info("Shut down")
docker.compose.down(remove_orphans=True)
