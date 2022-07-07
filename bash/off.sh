#!/bin/sh
sleep 1
$HOME/src/lago -s hv1 1
sleep 1
$HOME/src/lago -s hv2 1
sleep 1
$HOME/src/lago -a
sleep 15
shutdown -h now
