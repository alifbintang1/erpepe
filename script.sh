#!/bin/bash

FOLDER="aim"

for FILE in "$FOLDER"/*.cnf; do
    echo "Processing $FILE..."
    python solver.py -f "$FILE"
    # python solver.py -f aim-100-1_6-no-1.cnf
done
