#!/bin/sh
FILENAME="sputnik"
HV1=1500
HV2=0
T1=70
T2=70
ST1=1000
ST2=1000
DIR=${HOME}/src/
# do not modify below this line
BIN=${DIR}lago
RUN="$BIN -f $FILENAME"
cd $DIR
#setup
$BIN -s hv1 $HV1
$BIN -s hv2 $HV2
$BIN -s t1 $T1
$BIN -s t2 $T2
$BIN -s st1 $ST1
$BIN -s st2 $ST2
# start
while true
do $RUN
done
