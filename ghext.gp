folder = system("echo $FOLDER")
if (strlen(folder) == 0) {
    folder = "data"
}
set xlabel "Time"
set ylabel "External Field [A/m]"
set grid
set key bottom right
set terminal png

# Infinite loop to keep updating the plot
while (1) {
	set output "plt_hext.png"
    plot folder."/log.dat" using 1:8 with lines title "H_x", \
         folder."/log.dat" using 1:9 with lines title "H_y", \
         folder."/log.dat" using 1:10 with lines title "H_z"
    pause 5
    replot
}
