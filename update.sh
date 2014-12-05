#!/bin/sh

set -e

PREFIX=/home/jcorebiz/jcorebiz

mkdir -p $PREFIX/data
cd $PREFIX/data

wget -q -O data.html http://j-core.biz/
if [ -s data.html ]; then
	cat data.html | PYTHONIOENCODING=utf8 python ../parse.py 2> /dev/null | sort -V > new.txt
	if [ -s new.txt ]; then
		[ -e current.txt ] && mv current.txt old.txt
		mv new.txt current.txt
		[ -e old.txt ] && diff -u0 old.txt current.txt |grep '^[+-][^+-]' > diff.txt
		cat diff.txt
		sed "s/^/$(date +%s): /" diff.txt >> log.txt
	fi
fi
