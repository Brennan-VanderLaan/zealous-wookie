#!/bin/bash

pid=/var/run/pythonApp.pid
name=pythonApp

case $1 in
    start)
        /sbin/start-stop-daemon --start -b -g www -u www --oknodo -m --pidfile "$pid" -d "/var/app/" --exec "/usr/bin/python" -- "main.py"
        ;;
    stop)
        /sbin/start-stop-daemon --stop --oknodo --pidfile "$pid" --retry=TERM/5/KILL/1
        ;;
    restart)
        ;;
    *)
        ;;
esac
