#!/bin/sh
sleep 30
touch MASTER
sleep 1
cat $HOME/lago_v1_2.bit > /dev/xdevcfg
sleep 1
$HOME/src/lago -a
sleep 1
$HOME/src/lago -s t1 170
sleep 1
$HOME/src/lago -s t2 9000
sleep 1
$HOME/src/lago -s hv1 1800
sleep 1
$HOME/src/lago -s hv2 0
sleep 1
$HOME/src/lago -a
sleep 10
cd $HOME/src
screen -d -m $HOME/src/lago -f spnk
