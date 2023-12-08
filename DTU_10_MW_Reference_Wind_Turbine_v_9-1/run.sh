#!/bin/bash

# Set the number of cores to be used
N_CORES=16  # Change this to the desired number of cores

# Set the path to the simulation program
SIMULATION_PROGRAM="../HAWC2/HAWC2MB.exe"

# Set the path to the folder containing input files
INPUT_FOLDER="htc"

# Find all input files in the specified folder
find "$INPUT_FOLDER" -type f -name "*.htc" | \
  # Use xargs to execute the simulation program in parallel
  xargs -P "$N_CORES" -I {} sh -c "$SIMULATION_PROGRAM {}"
