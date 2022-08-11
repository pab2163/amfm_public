## Code:

All R analysis code is in the `code` folder. Within this, subfolders contain `.Rmd` files for:

0. Manipulation checks (`0_manipulation_checks`)
1. Primary analyses (`1_primary_analyses`)
2. Secondary analyses (`2_secondary_analyses`)
3. Exploratory analyses (`3_exploratory_analyses`)
4. Making supplemental figures (`4_make_supplemental figures`)

All code runs in numerical / alphabetical order (i.e. *0..1..2..3..4* and *a..b..c* within subfolders). For the manipulation checks, primary, and secondary analyses, typically the first markdown ('a') runs the Bayesian models, the second one ('b') creates the figures, and the third one ('c') calculates and outputs the statistical report into. I have done my best to modularize and comment code in hopes of making it readible, but please reach out if you have any questions!

## Data

All datasets live in the `data` folder. This contains

* `sesson_data.csv`: trialwise data for the full study, *not* containing scores for prompted autobiographical recall
* `autobio_interview_scores.csv`: trialwise scores of prompted autobiographical recall for the full study 
* `power_sim_params.csv`: parameters derrived from the pilot data used for sample size calculations