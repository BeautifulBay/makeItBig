#!/bin/bash

function print_info()
{
	local log="You didn't add any log here!"
	local col="35"
	if [ "$1" ]; then
		log=$1
	fi
	if [ "$2" ]; then
		col=$2
	fi
	echo -e "\e[${col}m $log \e[0m"
}

function fetch_svn_log()
{
	#:
	print_info "$FUNCNAME start"
	$(svn log -v $SVN_RANGE | grep "^   " > $PATCH_LOG)
	print_info "$FUNCNAME end"
}

function parse_svn_log()
{
	print_info "$FUNCNAME start"
	if [ -f $FILE_TXT ]; then
		rm $FILE_TXT
	fi
	$(cat $PATCH_LOG | while read line; do line=android${line#*android}; echo $line | cut -d " " -f 1 | sed 's/\(^android.*\)/\1/' | grep "^android" >> $FILE_TXT; done)
	$(cat $PATCH_LOG | while read line; do line=modem${line#*modem}; echo $line | cut -d " " -f 1 | sed 's/\(^modem.*\)/\1/' | grep "^modem" >> $FILE_TXT; done)
	sort -u $FILE_TXT > $SORT_FILE_TXT
	$(cat $SORT_FILE_TXT | while read line; do dirname $line >> $DIR_TXT; done)
	sort -u $DIR_TXT > $SORT_DIR_TXT
	print_info "$FUNCNAME end"
}

function handle_svn_log()
{
	print_info "$FUNCNAME start"
	cd $PATCH_DIR
	cat $SORT_DIR_TXT | while read line; do if [ -d $ANDROID_DIR/$line ]; then mkdir -p $line; fi; done
	#cat $SORT_DIR_TXT | while read line; do echo $line; done
	cat $SORT_FILE_TXT | while read line; do if [ -f $ANDROID_DIR/$line ]; then cp $ANDROID_DIR/$line $PATCH_DIR/$line -rf; fi; done
	#cat $SORT_FILE_TXT | while read line; do echo -e "$ANDROID_DIR/$line\n" "$PATCH_DIR/$line\n"; done
	print_info "$FUNCNAME end"
}

function usage()
{
	print_info "Usage:" "31"
	print_info "\t$0 temp svn_start:svn_end"
	print_info "\ttemp is a temp directory you want it to be the fullPatch path"
	print_info "\tsvn_start is the beginning of svn"
	print_info "\tsvn_end is the end of svn"
}

function init_project()
{
	if [ ! -d "android" ] || [ ! -d "modem" ]; then
		print_info "You are not in an android project directory" "31"
		print_info "Please cd xxx/android/../" "31"
		exit
	elif [ ${#@} -eq 3 ] || [ ${#@} -eq 2 ]; then
		[ ${2:${#2}-4:4} == "help" ] && usage && exit
	else
		usage
		exit
	fi

	print_info "$FUNCNAME start"
	ANDROID_DIR=`pwd -P`
	PATCH_DIR=$ANDROID_DIR/$2
	if [ ! -d $PATCH_DIR/log ]; then
		mkdir $PATCH_DIR/log -p
	fi
	if [ ${#@} -eq 3 ]; then
		SVN_RANGE="-r $3"
		SVN_START=${3%%:*}
		SVN_END=${3#*:}
	elif [ ${#@} -eq 2 ]; then
		SVN_RANGE=
		SVN_START=0	
		SVN_END=$(svn info | grep ^Revision | cut -d ' ' -f 2)
	fi

	PATCH_LOG=$PATCH_DIR/log/${SVN_START}_${SVN_END}_svn_log.txt
	FILE_TXT=$PATCH_DIR/log/${SVN_START}_${SVN_END}_file.txt
	SORT_FILE_TXT=$PATCH_DIR/log/${SVN_START}_${SVN_END}_sort_file.txt
	DIR_TXT=$PATCH_DIR/log/${SVN_START}_${SVN_END}_dir.txt
	SORT_DIR_TXT=$PATCH_DIR/log/${SVN_START}_${SVN_END}_sort_dir.txt
	print_info "ANDROID_DIR   = $ANDROID_DIR"
	print_info "PATCH_DIR     = $PATCH_LOG"
	print_info "FILE_TXT      = $FILE_TXT"
	print_info "SORT_DIR_TXT  = $SORT_FILE_TXT"
	print_info "DIR_TXT       = $DIR_TXT"
	print_info "SORT_FILE_TXT = $SORT_DIR_TXT"
	print_info "$FUNCNAME end"
}

function main()
{
	init_project $@
	fetch_svn_log
	parse_svn_log 
	handle_svn_log
}

main $0 $@

