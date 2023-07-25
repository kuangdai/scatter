#!/bin/bash
#SBATCH --time=1-00:00:00
#SBATCH --partition=day
#SBATCH --nodes=20
#SBATCH --ntasks=960
#SBATCH --job-name=prem_5s__no_3d_mantle_crust__hetero_fuji_pacific_usarray

cp ../../build/axisem3d ./
mpirun -np 960 ./axisem3d
