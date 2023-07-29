#!/bin/bash
#SBATCH --time=01:00:00
#SBATCH --partition=pi_korenaga
#SBATCH --nodes=1
#SBATCH --ntasks=48
#SBATCH --job-name=prem_5s__no_3d_mantle_crust__no_hetero

cp ../../build/axisem3d ./
module load foss/2018b
module load METIS/5.1.0-GCCcore-7.3.0-32bit
module load netCDF/4.6.1-foss-2018b

mpirun -np 48 ./axisem3d
