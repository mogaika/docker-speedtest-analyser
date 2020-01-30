#!/usr/bin/python

import os
import time
from threading import Event

from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily, REGISTRY
from prometheus_client import start_http_server


# load last 5 minutes results on start
last_timestamp = time.time() - 300.0


def cycle_over_last_speeds():
    global last_timestamp

    file_path = os.path.dirname(os.path.abspath(__file__)) + '/../data/result.csv'
    try:
        with open(file_path, 'r') as f:
            # skip csv header
            f.readline()

            while True:
                line = f.readline()
                if len(line) < 5:
                    return
                else:
                    line_separated = line.split(",")
                    timestamp = float(line_separated[0]) / 1000.0
                    if timestamp > last_timestamp:
                        metric_time = line_separated[1]
                        metric_speed = line_separated[2]
                        yield metric_time, metric_speed
                        last_timestamp = timestamp
    except Exception as ex:
        print("prometeus reporter: failed to update: {}".format(ex))
        raise ex


class SpeedCollector(object):
    def describe(self):
        yield GaugeMetricFamily('speedtest_last_downloading_time', 'File downloading time spent')
        yield GaugeMetricFamily('speedtest_last_speed', 'Downloading speed in Megabytes')

    def collect(self):
        for time, speed in cycle_over_last_speeds():
            yield GaugeMetricFamily('speedtest_last_downloading_time', 'File downloading time spent', value=time)
            yield GaugeMetricFamily('speedtest_last_speed', 'Downloading speed in Megabytes', value=speed)


REGISTRY.register(SpeedCollector())

if __name__ == "__main__":
    start_http_server(9999)
    Event().wait()
