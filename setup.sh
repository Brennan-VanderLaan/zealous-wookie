#!/bin/bash

pid=/var/run/pythonApp.pid
name=pythonApp
prog=./python main.py

case $1 in
    start)
        /sbin/start-stop-daemon --start -b --oknodo --name "$name" -m --pidfile "$pid" --startas "$prog" --daemon
        ;;
    stop)
        /sbin/start-stop-daemon --stop --oknodo --name "$name" --pidfile "$pid" --retry=TERM/5/KILL/1
        ;;
    restart)
        ;;
    *)
        ;;
esac