# Run all code for this study

# set up output subfolders
mkdir ../results/stats
mkdir ../results/models
mkdir ../results/supplemental_figs
mkdir ../results/knit_markdowns

# Manipulation Checks
Rscript -e "library(rmarkdown); rmarkdown::render('0_manipulation_checks/0a_manipulation_checks_models.Rmd',  output_file = '../../results/knit_markdowns/0a_manipulation_checks_models.html')" 
Rscript -e "library(rmarkdown); rmarkdown::render('0_manipulation_checks/0b_manipulation_checks_plots.Rmd',     output_file = '../../results/knit_markdowns/0b_manipulation_checks_plots.html')" 
Rscript -e "library(rmarkdown); rmarkdown::render('0_manipulation_checks/0c_manipulation_checks_stats.Rmd', output_file = '../../results/stats/0_manipulation_checks_stats.html')" 

# Primary Analyses
Rscript -e "library(rmarkdown); rmarkdown::render('1_primary_analyses/1a_primary_models.Rmd', output_file = '../../results/knit_markdowns/1a_primary_models.html')" 
Rscript -e "library(rmarkdown); rmarkdown::render('1_primary_analyses/1b_primary_graphs.Rmd', output_file = '../../results/knit_markdowns/1b_primary_graphs.html')" 
Rscript -e "library(rmarkdown); rmarkdown::render('1_primary_analyses/1c_primary_stats.Rmd', output_file = '../../results/stats/1_primary_analysis_stats.html')"

# Secondary Analyses
Rscript -e "library(rmarkdown); rmarkdown::render('2_secondary_analyses/2a_secondary_models.Rmd', output_file = '../../results/knit_markdowns/2a_secondary_models.html')" 
Rscript -e "library(rmarkdown); rmarkdown::render('2_secondary_analyses/2b_secondary_graphs.Rmd', output_file = '../../results/knit_markdowns/2b_secondary_graphs.html')" 
Rscript -e "library(rmarkdown); rmarkdown::render('2_secondary_analyses/2c_secondary_stats.Rmd', output_file = '../../results/stats/2_secondary_analysis_stats.html')"

# Exploratory Analyses
Rscript -e "library(rmarkdown); rmarkdown::render('3_exploratory_analyses/developmental.Rmd', output_file = '../../results/stats/3_exploratory_developmental_analysis_stats.html')"
Rscript -e "library(rmarkdown); rmarkdown::render('3_exploratory_analyses/prompt.Rmd')"


# # Supplemental Figures
Rscript -e "library(rmarkdown); rmarkdown::render('4_make_supplemental_figures/make_sfig10.Rmd')"
Rscript -e "library(rmarkdown); rmarkdown::render('4_make_supplemental_figures/make_sfig13.Rmd')"
Rscript -e "library(rmarkdown); rmarkdown::render('4_make_supplemental_figures/make_sfig15.Rmd')"
Rscript -e "library(rmarkdown); rmarkdown::render('4_make_supplemental_figures/make_more_sfigs.Rmd')"

