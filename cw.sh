#!/bin/bash

BASE_PATH=/home/richard/develop/crossword_printer

source $BASE_PATH/.venv/bin/activate
cd $BASE_PATH

python $BASE_PATH/cw.py "$@"