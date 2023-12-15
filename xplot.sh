#!/bin/bash

# Check if an argument is provided
if [ $# -eq 0 ]; then
	echo -e "\t This script is an interface to the gnuplotscripts for each subfolder. To plot your type=(m_relax, sot, hext) use:"
    echo -e"\t\t: $0 <type> <field_in_mT>"
    exit 1
fi

# Pad the input number with zeros up to 4 digits
folder_num=$(printf "%04d" $2)
FOLDER="data_H${folder_num}" gnuplot $1 $2

