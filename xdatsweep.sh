#!/bin/bash
cnt=0
for dir in data_H*; do
    # Check if it's a directory
    if [ -d "$dir" ]; then
        # Extract the number from the directory name
        num=$(echo $dir | sed 's/data_H//')

        # Check if log.dat exists
        if [ -f "$dir/log.dat" ]; then
            last_val=$(tail -n 1 "$dir/log.dat")
            
            if [ $cnt -eq 0 ]; then #if its the first iteration, the header is cloned
                first_val=$(head -n 1 "$dir/log.dat")
                echo -e "Hext_x [A/m]\t$first_val" > output.dat  
            fi

            cnt=$((cnt + 1))  # Increment the counter
        else
            echo "Warning: $dir/log.dat does not exist."
            last_val=0
        fi

        # Write to output.dat
        echo -e "$num\t$last_val" >> output.dat
    fi
done

# Sort the output file
sort -n -k1 output.dat -o datsweep.dat

gnuplot gbsweep.gp

