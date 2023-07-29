#!/bin/bash
#SBATCH --time=04:00:00
#SBATCH --partition=day
#SBATCH --nodes=20
#SBATCH --ntasks=960
#SBATCH --job-name=prem_5s__no_3d_mantle_crust__hetero_fuji_pacific_usarray

cp ../../build/axisem3d ./
module load foss/2018b
module load METIS/5.1.0-GCCcore-7.3.0-32bit
module load netCDF/4.6.1-foss-2018b

mpirun -np 960 ./axisem3d
