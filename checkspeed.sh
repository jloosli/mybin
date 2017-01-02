#!/bin/bash

TESTRESULTS=`speedtest --simple --share `
FILE="$HOME/storage/Dropbox/downtown_issues/speedtest.csv"
IP=`ifconfig | grep eno -n2 | sed -n '/inet /s/  */|/gp' | cut -d'|' -f3 | cut -d':' -f1`
IPVSIX=`ifconfig | grep eno -n2 | sed -n '/inet6/s/  */|/gp' | cut -d'|' -f4`
DATE=`date`

EXPORTSTRING="$DATE,"

if [[ $TESTRESULTS == Ping* ]]; then
    echo "Test worked"
    TESTRESULTS=$(echo $TESTRESULTS | cut -d' ' -f2,5,8,12 --output-delimiter=',')
else
    echo "Test didn't work"
    TESTRESULTS="$TESTRESULTS,,"
fi
EXPORTSTRING="$EXPORTSTRING$TESTRESULTS,$IP,$IPVSIX"
echo $EXPORTSTRING | tee -a ${FILE}
