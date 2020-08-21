# Launches all simulation models on high computing cluster in parallel for slurm scheduling
# Author: Paul A. Bloom

# launch 100 jobs for each level of effect
for (details in c(1,1.5,2, 2.5, 3)){
  direc75 = paste0('mkdir data/sim_models/effect_', details, '_detail_75_subs')
  direc100 = paste0('mkdir data/sim_models/effect_', details, '_detail_100_subs')
  system(paste0('mkdir ', direc75))
  system(paste0('mkdir ', direc100))
  
  # lanch 100 jobs for both sample sizes for each level of details
  for (num in 1:100){
    command75 = paste0('sbatch launch_one_model.sh ', 'data/sim_', details, '_detail_effect_75_subs ', num, ' data/sim_models/effect_', details, '_detail_detail_75_subs')
    command100 = paste0('sbatch launch_one_model.sh ', 'data/sim_', details, '_detail_effect_100_subs ', num, ' data/sim_models/effect_', details, '_detail_detail_100_subs')
    system(command75)
    system(command100)
  }
}

