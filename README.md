# MagnumNP Field Scan init-scripts

Welcome to the MagnumNP Field Scan repository! This repository contains some useful helper scripts for running simulations using the MagnumNP simulation framework. This is my personal setup for running simulations, feel free to branch and improve this code and workflow!

## Getting Started

To run a new simulation, you need to copy the scripts from this repository into your new simulation directory.

#### Prerequisites

Make sure you have magnumnp on your system. If you don't, you can download it from [magnumNP repo](https://pypi.org/project/magnumnp/).
Clone this repository into your current directory:
```bash
git clone https://github.com/joshuamsalazar/magnumnp-field-scan.git .
```

## My personal workflow
The way I run simulations here is: 
 - Pulling the scripts from the repo.
 - Set up the structure geometry inside `m2.py` and material parameters.
 - Run a sample simulation with $H_\text{ext}=0 \text{ mT}$:  `$ python3 m2.py 0`.
 - Check the generated .vti file and data to see if it agrees with the desired structure.
 - Run simulation in series for every external field amplitude: `$ ./xsweep.sh m2.py -10 10 1`
 - Generate the dataset with the results, `datsweep.dat`, by calling `$ ./xdatsweep.sh` at any time.
  
## Helper scripts included:
The repository contains the following essential scripts:
  - g* files for plotting with `gnuplot`.
  - x* files as `bash` scripts.

### [Sweeper: `xsweep.sh`](https://github.com/joshuamsalazar/magnumnp_scripts/tree/main/h_ext-sweeps/xsweep)
Runs simulations in series, changing the external field amplitude per simulation. Example usage: This command runs the m2.py file, variying the field amplitude from -10 mT to 10 mT. 
```bash
./xsweep m2.py -10 10 1 
```
### [Updater: `xdatsweep.sh`](https://github.com/joshuamsalazar/magnumnp_scripts/tree/main/h_ext-sweeps/xdatsweep)
Reads all the simulations for different field amplitudes and generates a datsweep.dat file with the relaxed magnetization directions at that state. Then, plots the generated dataset
```bash
./xdatsweep.dat
```
### [Plotter: `xplot.sh`](https://github.com/joshuamsalazar/magnumnp_scripts/tree/main/h_ext-sweeps/xdatsweep/xplot)
Generates and shows desired plot (SOT fields, Hext, or magnetization). If you want to see the magnetization state of, the simulation at $H_\text{ext}=3$ mT:
```bash
./xplot gmrx.py 3
```


### Extra scripts in this [repo](https://github.com/joshuamsalazar/magnumnp_scripts)

### Keeping Your Scripts Updated

 To ensure you have the latest version of the scripts, you can pull updates from the repository:
  ```bash
  git pull origin main

