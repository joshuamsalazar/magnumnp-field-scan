folder = system("echo $FOLDER")
if (strlen(folder) == 0) {
    folder = "data"
}
set xlabel "Time"
set ylabel "Magnetization"
set grid

# Infinite loop to keep updating the plot
while (1) {
    plot folder."/log.dat" using 1:2 with lines title "MX", \
         folder."/log.dat" using 1:3 with lines title "MY", \
         folder."/log.dat" using 1:4 with lines title "MZ"
    pause 5
    replot
}

