#!/bin/bash

PROCESS_ALL=`screen -ls | grep -o -E "[0-9]+\.[a-z]"`
PIDS=`echo $PROCESS_ALL | grep -o -E "[0-9]+"`
screen kill $PIDS
screen -wipe
