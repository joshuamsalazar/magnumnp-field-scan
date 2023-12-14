#!/bin/bash

# Check if the correct number of arguments are provided
if [ "$#" -ne 4 ]; then
    echo "Usage: $0 script.py start end increment [field values in miliTesla]"
    exit 1
fi

# Assigning command line arguments to variables
script=$1
start=$2
end=$3
increment=$4

# Looping over the range and increment
for ((i=start; i<=end; i+=increment)); do
    echo "Running: python3 $script $i"
    python3 "$script" "$i"
    echo "Finished running with argument $i"
done
