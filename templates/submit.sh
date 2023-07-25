#!/bin/bash
__HEAD__
#SBATCH --job-name=__NAME__

cp ../../build/axisem3d ./
mpirun -np __NP__ ./axisem3d
