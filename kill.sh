#!/bin/bash

main_pid=$(ps aux | grep "python3 main.py" | grep -v grep | awk '{print $2}')
web_pid=$(ps aux | grep "python3 webAccess.py" | grep -v grep | awk '{print $2}')

if [[ -n "$main_pid" ]]; then
    kill "$main_pid"
fi

if [[ -n "$web_pid" ]]; then
    kill "$web_pid"
fi
