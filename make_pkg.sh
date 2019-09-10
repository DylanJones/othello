#!/bin/zsh

if [ -z "$1" ]; then
    FOLDER=other_strategy
else
    FOLDER="$1"
fi

rm -rf "$FOLDER"
mkdir "$FOLDER"
cp *.py "$FOLDER"
for f in "$FOLDER"/*.py; do
    #sed -i "s/(?(?<=from )[A-Za-z_]*|(?<=import )[A-Za-z_]*\s*$)/\.&/g" $f
    for mod in ai heuristics machine_code strategy helpers Othello_Core cfunc_caller; do
        #sed -i "s/(?(?<=from )$mod|(?<=import )$mod\s*$)/\.&/g" $f
        sed -i "s/from $mod/from .$mod/g" $f
        sed -i "s/import $mod/from . import $mod/g" $f
    done
done
echo "
from .strategy import *
" > "$FOLDER"/__init__.py
