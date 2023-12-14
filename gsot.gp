folder = system("echo $FOLDER")
if (strlen(folder) == 0) {
    folder = "data"
}

set xlabel "Time"
set ylabel "Value"
set grid

# Infinite loop to keep updating the plot
while (1) {
    plot folder."/log.dat" using 1:5 with lines title "H_sot_x", \
         folder."/log.dat" using 1:6 with lines title "H_sot_y", \
         folder."/log.dat" using 1:7 with lines title "H_sot_z"
    pause 5
    replot
}

