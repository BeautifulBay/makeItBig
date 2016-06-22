#!/bin/bash

function _completeFunc()
{
	COMPREPLY=()
	local cur="${COMP_WORDS[COMP_CWORD]}"

	if [ ${COMP_CWORD} -eq $2 ]
	then
		COMPREPLY=($(compgen -W "$1" -- $cur))
		return 0
	fi
}

function _cAndroid()
{
	local opts="android kernel bootable device system vendor frameworks packages hardware out build dts dts64 power lk obj modem"
	_completeFunc "$opts" 1
}

function Cd()
{
	local option first last

	local currentDir=`pwd`
	if [[ ! $currentDir =~ "android" && ! $currentDir =~ "modem" ]]
	then
		for var in `ls`
		do
			if [[ $var =~ "android" ]]
			then
				var=$currentDir
				break
			else
				continue
			fi
		done
		if [ $var == $currentDir ]
		then
			currentDir=$currentDir/android
		else
			echo "You are not in an android product dir, Please check"
			return 0
		fi
	fi

	if [[ $currentDir =~ "android" ]]
	then
		first=${currentDir%%android*}android
		last=${currentDir%android*}android
	elif [[ $currentDir =~ "modem" ]]
	then
		first=${currentDir%%modem*}android
		last=${currentDir%modem*}android
	fi 

	if [ ${first} != ${last} ]
	then
		read option
		if [ -z "${option}" ]
		then 
			:
		else
			first=${last}
		fi
	fi
	
	case $1 in
	"modem")
		first=${first}/../$1
		;;
	"dts")
		first=${first}/kernel/arch/arm/boot/$1
		;;
	"dts64")
		first=${first}/kernel/arch/arm64/boot/dts
		;;
	"power")
		first=${first}/kernel/drivers/$1
		;;
	"lk")
		first=${first}/bootable/bootloader/$1
		;;
	"obj")
		first=${first}/out/target/product/*/$1
		;;
	"android")
		;;
	*)
		first=${first}/$1
		;;
	esac

	cd ${first}
}

complete -F _cAndroid Cd
