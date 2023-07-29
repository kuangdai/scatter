#!/bin/bash
__HEAD__
#SBATCH --job-name=__NAME__

cp ../../build/axisem3d ./
module load foss/2018b
module load METIS/5.1.0-GCCcore-7.3.0-32bit
module load netCDF/4.6.1-foss-2018b

mpirun -np __NP__ ./axisem3d
