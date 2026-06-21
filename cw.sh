#!/bin/bash

BASE_PATH=/home/richard/prod/crossword-printer

source $BASE_PATH/.venv/bin/activate
cd $BASE_PATH

python $BASE_PATH/cw.py "$@"
