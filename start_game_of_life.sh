#! /bin/bash
set START_FILE='src/game_of_life.py'

# check the start up file
if [ -f $START_FILE ]; then
    exec python3 src/game_of_life.py
else
    echo "There is no source file to execute."
fi