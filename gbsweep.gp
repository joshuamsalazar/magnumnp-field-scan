folder = system("echo $FOLDER")
if (strlen(folder) == 0) {
    folder = "data"
}

set xlabel "Field [mT]"
#set xlabel "$\\mu h_{\\text{ext,z}}$ [mT]"
set ylabel "M_z"
set grid
set key bottom right
set terminal png

# Infinite loop to keep updating the plot
#while (1) {
    set output "plt_bzsweep.png"
    plot "datsweep.dat" u 1:5 w l lw 2title "m_z signal (full mm: magnumnp)", \
	 "1dmin_bxsweep_M2_1nm.dat" u 1:2 w p lw 2 title "m_z signal (single spin: PDE)", \
	 "expt_bxsweep_M2_1nm.dat" u 1:2 w p lw 2 title "m_z signal (expt.)"
set terminal x11 
    plot "datsweep.dat" u 1:5 w l lw 2title "m_z signal (full mm: magnumnp)", \
	 "1dmin_bxsweep_M2_1nm.dat" u 1:2 w p lw 2 title "m_z signal (single spin: PDE)", \
	 "expt_bxsweep_M2_1nm.dat" u 1:2 w p lw 2 title "m_z signal (expt.)"
pause -1
