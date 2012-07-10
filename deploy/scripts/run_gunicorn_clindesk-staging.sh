#!/bin/bash
set -e
LOGFILE=/var/log/gunicorn-clindesk-staging/clindesk-staging.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=1
USER=clindesk-staging
GROUP=clindesk-staging
WORKER_CLASS="gevent"
BIND="127.0.0.1:8001"
cd /home/clindesk-staging/
source bin/activate
test -d $LOGDIR || mkdir -p $LOGDIR
chown $USER:$GROUP $LOGDIR
cd clindesk/
exec ../bin/gunicorn --bind $BIND --debug --workers $NUM_WORKERS --worker-class $WORKER_CLASS \
    --user=$USER --group=$GROUP --log-level=debug \
    --log-file=$LOGFILE clindesk:app 2>>$LOGFILE
