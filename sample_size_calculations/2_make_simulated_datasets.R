library(tidyverse)
library(MASS)
source('simulation_functions.R')
pilot_params= read_csv('data/power_sim_params.csv')



# 75 participants ---------------------------------------------------------
for (details in c(1, 1.5, 2, 2.5, 3)){
  simulate_many_datasets(n_subs = 75, n_sims = 100,
                     familiar_internal_mean = details, familiar_internal_sd = 1,
                     familiar_external_mean = 0, familiar_external_sd = 1,
                     music_internal_mean = 1, music_internal_sd = 1, music_external_mean = 1,
                     music_external_sd =1, outdir = paste0('data/sim_', details, '_detail_effect_75_subs'))
}


# 100 participants ---------------------------------------------------------
for (details in c(1, 1.5, 2, 2.5, 3)){
  simulate_many_datasets(n_subs = 100, n_sims = 100,
                         familiar_internal_mean = details, familiar_internal_sd = 1,
                         familiar_external_mean = 0, familiar_external_sd = 1,
                         music_internal_mean = 1, music_internal_sd = 1, music_external_mean = 1,
                         music_external_sd =1, outdir = paste0('data/sim_', details, '_detail_effect_100_subs'))
  print('break before next sims')
  Sys.sleep(10)
}
