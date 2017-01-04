#!/bin/bash

TESTRESULTS=`speedtest --simple --share `
FILE="$HOME/storage/Dropbox/downtown_issues/speedtest.csv"
IP=`ifconfig | grep -A 3 eno1 | awk '/inet addr/{print substr($2,6)}'`
IPVSIX=`ifconfig | grep -A 2 eno1 | awk '/inet6 addr/{print substr($3,6)}'`
DATE=`date`
MESSAGE=''
EXPORTSTRING="$DATE,"

if [[ $TESTRESULTS == Ping* ]]; then
    echo "Test worked"
    TESTRESULTS=$(echo $TESTRESULTS | cut -d' ' -f2,5,8,12 --output-delimiter=',')
else
    echo "Test didn't work"
    MESSAGE="$TESTRESULTS"
    TESTRESULTS=",,,,"
fi
EXPORTSTRING="$EXPORTSTRING$TESTRESULTS,$IP,$IPVSIX,$MESSAGE"
echo $EXPORTSTRING | tee -a ${FILE}
