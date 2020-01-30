#!/usr/bin/python

import os
import time
import logging

from threading import Event

from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily, REGISTRY
from prometheus_client import start_http_server


# load last 5 minutes results on start
last_timestamp = time.time() - 300.0


# Generator of new metric values
# yields (time in seconds, speed in byes/second)
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

                    # convert from milliseconds to seconds
                    timestamp = float(line_separated[0]) / 1000.0

                    if timestamp > last_timestamp:
                        metric_time = float(line_separated[1])

                        # convert from megabytes to bytes
                        metric_speed = float(line_separated[2]) * 1024.0 * 1024.0

                        yield metric_time, metric_speed
                        last_timestamp = timestamp
    except Exception as ex:
        logging.error("prometeus reporter: failed to update: {}".format(ex))
        raise ex


class SpeedCollector(object):
    def _download_time_metric(self, value=None):
        return GaugeMetricFamily('speedtest_last_downloading_time',
                                 'File downloading time spent', unit='seconds', value=value)

    def _speed_metric(self, value=None):
        return GaugeMetricFamily('speedtest_last_speed',
                                 'Downloading speed in Megabytes', unit='bytes', value=value)

    def describe(self):
        yield self._download_time_metric()
        yield self._speed_metric()

    def collect(self):
        for time, speed in cycle_over_last_speeds():
            yield self._download_time_metric(value=time)
            yield self._speed_metric(value=speed)


REGISTRY.register(SpeedCollector())


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)-15s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    start_http_server(9999)
    Event().wait()
