# Effects of familiar music exposure on deliberate retrieval of remote episodic and semantic memories in healthy aging adults [Code Capsule]

This Code Ocean capsule contains containerized code & data necessary to reproduce all main analyses & figures in the manuscript. A Reproducible Run will reproduce all main figures and analyses with one click in this cloud-based environment. 

Protocols, more information, and materials can be found in the [Open Science Framework respository](https://osf.io/kjnwd/) associated with this study.  

## Results

### Stats

All statistics reported in the results section of the manuscript can be found in the html files (knitted R markdowns) in `/results/stats`. As with code, stats are separated into files for manipulation checks, primary analyses, secondary analyses, and exploratory analyses. 

* `0_manipulation_checks_stats.html`
* `1_primary_analysis_stats.html`
* `2_secondary_analysis_stats.html`
* `3_exploratory_developmental_analysis_stats.html`

### Figures

Figures 2-6 in the manuscript are labeled numerically and output to the `/results` folder. 

### Supplemental Figures

Supplemental figures 5-15 are labeled numerically and output to the `/results/supplemental_figs` folder. 

### Model objects

The `/results/models` folder contains four `.rda` files with model fit objects. These can be opened in R.

*   `manipulation_check_models.rda` -- all `brms` fit model objects in manipulation check analyses
*   `primary_analysis_models.rda` -- all `brms` fit model objects in primary analyses
*   `secondary_models.rda` -- all `brms` fit model objects in secondary analyses
*   `prompt_model.rda` -- `brms` fit model object used in exploratory analyses of prompts

## Code:

All R analysis code is in the `/code` folder. Within this, subfolders contain `.Rmd` files for:

0. Manipulation checks (`0_manipulation_checks`)
1. Primary analyses (`1_primary_analyses`)
2. Secondary analyses (`2_secondary_analyses`)
3. Exploratory analyses (`3_exploratory_analyses`)
4. Making supplemental figures (`4_make_supplemental figures`)

All code runs in numerical / alphabetical order (i.e. *0..1..2..3..4* and *a..b..c* within subfolders). For the manipulation checks, primary, and secondary analyses, typically the first markdown ('a') runs the Bayesian models, the second one ('b') creates the figures, and the third one ('c') calculates and outputs the statistical report into the `/results/stats` folder. I have done my best to modularize and comment code in hopes of making it readible, but please reach out if you have any questions!

## Data

All datasets live in the `/data` folder. This contains

* `data_dictionary_code_ocean.csv`: data dictionary with information on all columns contained in the other data files
* `sesson_data.csv`: trialwise data for the full study, *not* containing scores for prompted autobiographical recall
* `autobio_interview_scores.csv`: trialwise scores of prompted autobiographical recall for the full study 
* `power_sim_params.csv`: parameters derrived from the pilot data used for sample size calculations

Additional data collected in the study not used in this manuscript can be found in the [Open Science Framework respository](https://osf.io/kjnwd/) associated with this project.  

*Note:* specification curve analyses included in the manuscript are not included in this capsule for computational feasibility, but code & materials for these can be found on Github [here](https://github.com/pab2163/amfm_public)


### Contact

paul.bloom@columbia.edu

