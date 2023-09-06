#!/bin/bash
#SBATCH --time=1-00:00:00
#SBATCH --partition=
#SBATCH --ntasks=10000
#SBATCH --job-name=prem_2s__no_3d_mantle_crust__hetero_fuji_pacific_usarray

cp ../../build/axisem3d ./
module load foss/2018b
module load METIS/5.1.0-GCCcore-7.3.0-32bit
module load netCDF/4.6.1-foss-2018b

mpirun -np 10000 ./axisem3d
