#!/bin/sh

#SBATCH --account=psych
#SBATCH --job_name=music_sample_calc_lmer
#SBATCH -c 1
#SBATCH --time=0:55:00
#SBATCH --mem-per-cpu=4gb

input_dir=$1
dataset_num=$2
outdir=$3

# activate conda env
conda activate r_brms_tidyverse

# run one simulated model
Rscript run_maximal_sim_lmer.R $input_dir $dataset_num $outdir