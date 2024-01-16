#!/bin/bash

if ! command -v pvpython &> /dev/null; then
    echo -e "\n Paraview-python-interface 'pvpython' command not found."
    echo -e "\n Please, provide the full path of the paraview python interface\n" 
    echo -e "\t Example: /datadisk/programs/paraview_x.x/bin/pvpython \n Your path: "
    read -p "" pvpython_path
    # You can now use "$pvpython_path" as the path to the pvpython command
else
    pvpython_path=$(which pvpython)
fi

if [ $# -lt 1 ]; then
    echo "Not enough arguments."
    echo -e "\t Usage: $ ./xscreenshot.sh [field_value_in_mT] (optional, by default: 0 mT)"
    exit 1
fi

#Transform the number input to zero padded value
hampl=$(printf "%04d" $1)
file_path="data_H$hampl/m_relaxed.vti"

if [ ! -f "$file_path" ]; then
    echo "File $file_path not found. Searching for file with highest cnt..."

    # Find the file with the highest cnt value
    highest_cnt_file=$(find . -type f -name "m_relax_H${hampl}_*.vti" | sort -V | tail -n 1)

    if [ -n "$highest_cnt_file" ]; then
        echo "Using file: $highest_cnt_file"
        file_path=$highest_cnt_file
    else
        echo "No suitable file found."
        exit 1
    fi
fi

$pvpython_path top_screenshot.py $file_path
