#!/bin/zsh

if [ -z "$1" ] || [ -z "$(echo $1 | grep '\.c' )" ] ; then
    echo "Usage: $0 <function.c>"
    exit 1
fi

if [ -z "$2"  ]; then
    OPTLEVEL=0
else
    OPTLEVEL="$2"
fi

g++ "-O$OPTLEVEL" -S "$1" -o tmp.s -masm=intel
as tmp.s -o func
HEX=$(objdump -d func -M intel | grep -oP '(?<=\t).*(?=\t)' | tr -d ' ' | tr -d '\n')
PYHEX=b\'$(echo $HEX | sed 's/.\{2\}/\\\\x&/g')\'
echo $PYHEX
