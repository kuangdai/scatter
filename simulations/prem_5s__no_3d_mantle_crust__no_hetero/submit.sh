#!/bin/bash
#SBATCH --time=01:00:00
#SBATCH --partition=pi_korenaga
#SBATCH --nodes=1
#SBATCH --ntasks=48
#SBATCH --job-name=prem_5s__no_3d_mantle_crust__no_hetero

cp ../../build/axisem3d ./
mpirun -np 48 ./axisem3d
