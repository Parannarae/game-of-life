#! /bin/bash
START_FILE='src/game_of_life.py'

# check the start up file
if [ -f $START_FILE ]; then
    # exec python3 -m unittest tests.test_life
    exec python3 $START_FILE
else
    echo "There is no source file to execute."
fi