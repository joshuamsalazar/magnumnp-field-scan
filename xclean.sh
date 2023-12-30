#!/bin/bash

# Directory containing the subdirectories
root_dir=$1

# Check if root_dir is a valid directory
if [ ! -d "$root_dir" ]; then
    echo "Error: Provided path is not a valid directory."
    exit 1
fi

# Navigate through each subdirectory in the main directory
for dir in "$root_dir"/*/; do
    # Check if directory exists (to handle the case of no subdirectories)
    if [ ! -d "$dir" ]; then
        echo "No subdirectories found in $root_dir."
        break
    fi

    echo -e "\t \e[32m  Processing directory: $dir \e[0m"

    # Find the .vti file with the highest number
    latest_vti=$(ls -v "${dir}"fields_*.vti 2>/dev/null | tail -n 1)
    echo -e "\t\tThe last relaxed VTI file is: $latest_vti"

    # Check if latest_vti is not empty
    if [ -n "$latest_vti" ]; then
        # List all .vti files except the latest one
        # List all .vti files except the latest one, sorted
        files_to_remove=$(find "$dir" -maxdepth 1 -name 'fields_*.vti' ! -name "$(basename "$latest_vti")" | sort)
	if [ -n "$files_to_remove" ]; then
            echo "Files to remove:"
            echo "$files_to_remove"

            # Ask for confirmation
            read -p "Do you want to proceed with deletion? (y/n) " confirm
            if [ "$confirm" = "y" ]; then
                # If confirmed, remove the files
                echo "$files_to_remove" | xargs rm -v
            else
                echo "Deletion aborted."
            fi
        else
            echo "No .vti files to remove in $dir."
        fi
    else
        echo "No .vti files found in $dir."
    fi
done

echo "Cleanup complete."

