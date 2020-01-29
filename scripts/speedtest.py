#!/usr/bin/python

import time
import os
import csv
import requests


def run_speedtest():
    readed_bytes = 0
    time_start = time.time()
    with requests.get(os.environ['SPEED_DOWNLOAD_URL'], stream=True) as reader:
        reader.raise_for_status()
        for chunk in reader.iter_content(chunk_size=1024*1024):
            print("loaded part {}".format(readed_bytes/1024.0/1024.0))
            if chunk:
                readed_bytes += len(chunk)

    time_end = time.time()

    time_amount = time_end - time_start
    download = readed_bytes / time_amount

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
    run_speedtest()
