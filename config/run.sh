#!/usr/bin/env bash

set -m

echo "Starting run.sh"

cat /var/www/html/config/crontab.default > /var/www/html/config/crontab

if [[ ${CRONJOB_ITERATION} && ${CRONJOB_ITERATION-x} ]]; then
    sed -i -e "s/0/*\/${CRONJOB_ITERATION}/g" /var/www/html/config/crontab
fi
crontab /var/www/html/config/crontab

echo "Starting Cronjob"
crond -l 2 -f &
P1=$!

echo "starting nginx"
nginx -g "daemon off;" &
P2=$!

echo "starting prometeus reporter"
python /var/www/html/scripts/reporter.py &
P3=$!

fg %1
