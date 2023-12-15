#!/bin/bash

# Check if an argument is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <number>"
    exit 1
fi

# Pad the input number with zeros up to 4 digits
folder_num=$(printf "%04d" $1)
cd "data_H${folder_num}"
