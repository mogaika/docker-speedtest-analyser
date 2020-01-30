#!/usr/bin/python

import time
import os
import csv
import requests
import logging


def run_speedtest():
    readed_bytes = 0
    time_start = time.time()

    url = os.environ['SPEED_DOWNLOAD_URL']
    logging.info("Starting download speed measure for url {}".format(url))

    with requests.get(url, stream=True) as reader:
        reader.raise_for_status()
        for chunk in reader.iter_content(chunk_size=1024*1024):
            if chunk:
                readed_bytes += len(chunk)

    time_end = time.time()

    time_amount = time_end - time_start
    download = readed_bytes / time_amount

    logging.info("Loaded {} bytes in {} seconds. Speed: {} bytes/sec ({} MBytes/sec".format(
        readed_bytes, time_amount, download, download/1024.0/1024.0))

    file_path = os.path.dirname(os.path.abspath(__file__))+'/../data/result.csv'
    file_exist = os.path.isfile(file_path)
    
    out_file = open(file_path, 'a')
    writer = csv.writer(out_file)
    
    if not file_exist:
        out_file.write("timestamp,ping,download,upload")
        out_file.write("\n")
    
    writer.writerow((time_end*1000, time_amount, (download/1024.0/1024.0), 0.0))
    out_file.close()
    
    return


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)-15s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    run_speedtest()
