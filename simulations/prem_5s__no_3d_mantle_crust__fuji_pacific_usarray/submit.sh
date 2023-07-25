#!/bin/bash
#SBATCH --time=4:0:0
#SBATCH --partition=pi_korenaga
#SBATCH --nodes=2
#SBATCH --ntasks=96
#SBATCH --job-name=prem_5s__no_3d_mantle_crust__fuji_pacific_usarray

cp ../../build/axisem3d ./
mpirun -np 96 ./axisem3d
