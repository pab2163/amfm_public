paths = .libPaths()
paths = c(paths[2], paths[1])
.libPaths(paths)

library(dplyr)
library(lme4)
library(broom.mixed)
library(brms)

args = commandArgs(trailingOnly=TRUE)

# input directory 
input_dir = args[1]

# dataset #
dataset_num = args[2]

# output directory
outdir = args[3]

# read in data
data_long = read.csv(paste0(input_dir, '/dataset_', dataset_num, '.csv'))

# define output files
proportion_out_file = paste0(outdir, '/model_proportion_draws_', dataset_num, '.csv')
model_summary_out_file = paste0(outdir, '/model_summary_', dataset_num, '.csv')

# fit model
mod = lmer(data = data_long, num_details ~ cond*type + time*type + (cond*type + time*type|id))

# tidy model outputs
model_summary = broom.mixed::tidy(mod) %>%
  dplyr::filter(effect == 'fixed') %>%
  mutate(dataset_num = dataset_num)

# save summary
write.csv(model_summary, file = model_summary_out_file, row.names = FALSE)
