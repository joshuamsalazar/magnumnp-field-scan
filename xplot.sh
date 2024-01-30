#!/bin/bash

# Check if an argument is provided
if [ $# -eq 0 ]; then
	echo -e "\t\n This script is an interface to the gnuplotscripts for each subfolder. To generate your plot choose the template.
       	Templates avaiable: 	gmrx.gp  -- m vs. t
				gsot.gp  -- H_sot vs. t
				ghext.gp -- H_ext vs. t
				"
    echo -e "Usage: \t\t $0 <template> <field_in_mT>\n"
    echo -e "Example: \n $0 gmrx.gp 0  -->> Generates a m vs. t plot for the data at H_ext=-1 mT"
    exit 1
fi

# Pad the input number with zeros up to 4 digits
folder_num=$(printf "%04d" $2)
FOLDER="data_H${folder_num}" gnuplot $1 $2

