#!/bin/bash
#SBATCH --time=02:00:00
#SBATCH --partition=pi_korenaga
#SBATCH --nodes=2
#SBATCH --ntasks=96
#SBATCH --job-name=prem_5s__no_3d_mantle_crust__no_hetero

cp ../../build/axisem3d ./
mpirun -np 96 ./axisem3d
