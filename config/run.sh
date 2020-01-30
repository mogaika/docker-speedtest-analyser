#!/usr/bin/env bash
echo "Starting run.sh"

cat /var/www/html/config/crontab.default > /var/www/html/config/crontab

if [[ ${CRONJOB_ITERATION} && ${CRONJOB_ITERATION-x} ]]; then
    sed -i -e "s/0/*\/${CRONJOB_ITERATION}/g" /var/www/html/config/crontab
fi
crontab /var/www/html/config/crontab

echo "Starting Cronjob"
crond -l 2 -f &

echo "starting nginx"
nginx -g "daemon off;" &
P1=$!

echo "starting prometeus reporter"
python /var/www/html/scripts/reporter.py &
P2=$!

wait $P1 $P2
