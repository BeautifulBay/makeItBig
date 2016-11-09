#!/bin/bash

function check_input()
{
	if [ $# -ne 5 ]; then
		echo "$1 subtitle_dir type[ass/srt] name txt_dir"
		exit
	fi
}

function init()
{
	SUBTITLEDIR=$2
	TITLETYPE=$3
	TXTNAME=${4//\./\\\.}
	TXTDIR=$5
	if [ ! -d $SUBTITLEDIR ]; then
		echo "Error $2 is not a directory"
		exit
	fi

	if [ ! -d $TXTDIR ]; then
		echo "Creat $TXTDIR"
		mkdir $TXTDIR
	fi
}

function parse_subtitle()
{
	local name
	for var in `ls $SUBTITLEDIR/*.$TITLETYPE | sed -n "/.*\(${TXTNAME}[sSeE0-9][sSeE0-9]*\).*$/p"`
	do
		#echo $var
		#continue
		name=$(echo ${var} | sed -n "s/.*\(${TXTNAME}[sSeE0-9][sSeE0-9]*\).*$/\1.txt/p")
		echo $name
		#echo ${var} ${TXTDIR}/$name
		./parseSubtitle.py ${var} ${TXTDIR}/$name
	done
}

function main()
{
	check_input $@
	init $@
	parse_subtitle
	
}

main $0 $@
