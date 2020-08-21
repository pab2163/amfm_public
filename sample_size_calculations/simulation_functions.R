# function to convert correlation matrix to covariance by matrix multiplication with standard deviation of each variable
cor2cov <- function(cor_matrix,sds){
  diag(sds) %*% cor_matrix %*% diag(sds)
}

# this function simulates one dataset for a given number of subjects (and a set seed)
simulate_one_dataset= function(seed, n_subs, outfile,
                               familiar_external_mean, familiar_external_sd, 
                               familiar_internal_mean, familiar_internal_sd, 
                               music_internal_mean, music_internal_sd, 
                               music_external_mean, music_external_sd){
  # set the seed
  set.seed(seed)
  
  cond = c('unfamiliar', 'noMusic','familiar')
  time = c('child', 'adol', 'adult')
  
  # set up trial structure for each participant
  frame = expand.grid(id = 1:n_subs, cond = cond, time = time, trial = 1:5)
  
  # using the pilot data parameters and chosen 'ground truth effects', simulate internal and external details
  frame = frame %>%
    # This first part simulates the participant-level parameters
    dplyr::group_by(id) %>%
    mutate(pilot_ind = sample(nrow(pilot_params), size =1),
           # Step1 -- each simulated participant gets parameters from one of the pilot participants (sampled with replacement)
           intercept_internal = pilot_params$internal_intercept[pilot_ind],
           intercept_external = pilot_params$external_intercept[pilot_ind],
           subject_sd_internal= pilot_params$internalSD[pilot_ind],
           subject_sd_external= pilot_params$externalSD[pilot_ind],
           child_effect_internal= pilot_params$internal_time_c[pilot_ind],
           adol_effect_internal = pilot_params$internal_time_t[pilot_ind],
           child_effect_external= pilot_params$external_time_c[pilot_ind],
           adol_effect_external = pilot_params$external_time_t[pilot_ind],
           # covariance matrix for internal/external details based on pilot data
           cor_internal_external = pilot_params$cor_internal_external[pilot_ind],
           cov_mat = list(cor2cov(cor_matrix = matrix(c(1, cor_internal_external[1], cor_internal_external[1], 1), nrow = 2, ncol = 2),
                                  sds = c(subject_sd_internal[1], subject_sd_external[1]))),
           
           # Step 2: Participant specific music effects are drawn from 'ground truth' distributions
           familiar_effect_internal= rnorm(1, familiar_internal_mean, familiar_internal_sd),
           familiar_effect_external= rnorm(1, familiar_external_mean, familiar_external_sd),
           music_effect_internal= rnorm(1, music_internal_mean, music_internal_sd),
           music_effect_external= rnorm(1, music_external_mean, music_external_sd)
    ) %>%
    ungroup() %>%
    # This part uses the participant level parameters to define the distributions (multivariate normal) from which to draw 
    # From these distributions, draw internal and external details for each trial
    mutate(., 
           mu_internal = intercept_internal +
             #effects of familiarity and music more generally
             ifelse(cond == 'familiar', familiar_effect_internal + music_effect_internal, 0) + 
             ifelse(cond == 'unfamiliar', music_effect_internal, 0) +
             # developmental effects
             ifelse(time == 'child', child_effect_internal, 0) +
             ifelse(time == 'adol', adol_effect_internal, 0), 
           mu_external = intercept_external +
             #effects of familiarity and music more generally
             ifelse(cond == 'familiar', familiar_effect_external + music_effect_external, 0) + 
             ifelse(cond == 'unfamiliar', music_effect_external, 0) +
             # developmental effects
             ifelse(time == 'child', child_effect_external, 0) +
             ifelse(time == 'adol', adol_effect_external, 0)) %>%
    group_by(id, cond, time, trial) %>%
    # internal and external details are drawn from multivariate normal based on the pilot participants' data
    mutate(dets = list(mvrnorm(n = 1, Sigma = cov_mat[[1]], mu = c(mu_internal, mu_external)))) %>% 
    ungroup() %>%
    tidyr::unnest_wider(dets) 
  
  # tidy the column names  
  frame = frame %>% dplyr::select(everything(), internal = `...1`, external = `...2`)
  
  
  # pivot to long format
  frame_long = frame %>% 
    tidyr::pivot_longer(cols = c(internal, external), names_to = 'type', values_to = 'num_details') %>%
    mutate(type = ifelse(type == 'internal', '0', '1')) %>%
    dplyr::select(id, cond, time, trial, type, num_details)
  
  # write out to csv
  write.csv(frame_long, row.names = FALSE, file = outfile)
}


simulate_many_datasets = function(n_sims, n_subs, outdir,
                                  familiar_external_mean, familiar_external_sd, 
                                  familiar_internal_mean, familiar_internal_sd, 
                                  music_internal_mean, music_internal_sd, 
                                  music_external_mean, music_external_sd){
  
  # set up output directory for datasets
  system(paste0('mkdir ', outdir))
  
  # make datasets in a loop
  for (i in 1:n_sims){
    simulate_one_dataset(n_subs = n_subs, seed = i, outfile = paste0(outdir, '/dataset_', i, '.csv'),
                         familiar_external_mean = familiar_external_mean, 
                         familiar_external_sd = familiar_external_sd, 
                         familiar_internal_mean = familiar_internal_mean,
                         familiar_internal_sd = familiar_internal_sd, 
                         music_internal_mean = music_internal_mean, 
                         music_internal_sd = music_internal_sd, 
                         music_external_mean = music_external_mean, 
                         music_external_sd = music_external_sd)
  }
}
