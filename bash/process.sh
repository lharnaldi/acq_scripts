#!/bin/sh
cd $HOME/src
find . -maxdepth 1 -type f -name "*.dat" -mmin +60 -exec mv {} dat \;
[ -f MASTER ] && f=s12 || f=s34
cat *.dat | tail -2000005 | head -2000000 > $f.tmp && mv -f $f.tmp $f.in
