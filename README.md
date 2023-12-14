# MagnumNP Field Scan init-scripts

Welcome to the MagnumNP Field Scan repository! This repository contains essential scripts for running simulations using the MagnumNP simulation framework. 

## Getting Started

To run a new simulation, you need to copy the scripts from this repository into your new simulation directory. Here's a step-by-step guide to doing so.

### Prerequisites

- Make sure you have magnumnp on your system. If you don't, you can download it from [magnumNP repo](https://pypi.org/project/magnumnp/).

### Cloning the Repository

1. **Create a New Directory for Your Simulation:**
   - Open a terminal.
   - Navigate to where you want to create your new simulation directory.
   - Create a new directory and navigate into it:
     ```bash
     mkdir my-new-simulation
     cd my-new-simulation
     ```

2. **Clone the Repository:**
   - Now clone the MagnumNP Field Scan repository into your simulation directory:
     ```bash
     git clone https://github.com/joshuamsalazar/magnumnp-field-scan.git .
     ```
   - The `.` at the end of the command clones the repository into the current directory.

### Running the Simulation

- After cloning the scripts, you can run your simulation, modifying the `m2.py` as usual within the directory.
- The repository contains the following essential scripts:
  - g* files for plotting with `gnuplot`.
  - x* files as `bash` scripts.

### Keeping Your Scripts Updated

- To ensure you have the latest version of the scripts, you can pull updates from the repository:
  ```bash
  git pull origin main

