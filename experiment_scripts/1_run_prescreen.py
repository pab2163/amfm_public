'''
Consolidated script for AMFM prescreening call!
Paul A. Bloom
March 2021

Takes 3 command line args: [subid] [age] [year]
-subid: must be AMFM###
-age: must be 65-80
year: must be 2021 or 2022

Does the following:
-Asks pre-questions (within this script)
-Makes artist lists (1)
-Runs artist selection (2a)
-Runs event selection (2b)
-Runs MoCA (2c)
'''


import sys
import pandas as pd 
import numpy as np 
from random import shuffle
import os
from sys import platform
import re

# get command line input of participant ID
subid = sys.argv[1]
year = int(sys.argv[2])

def check_prescreen_inputs(subid, year):
	# Check that subid is in the format AMFM###
	subid_format = 'AMFM[0-9][0-9][0-9]'
	matched = re.match(subid_format, subid)
	is_match = bool(matched)
	assert(is_match==True), 'Error, subid must be in format AMFM###!'
	assert(year == 2021 or year == 2022), 'Error, year should be 2021 or 2022!'

	if platform=="darwin":
  		output_dir = f'../raw_data/{subid}'
	else: 
		output_dir = f'..\\raw_data\\{subid}'
	assert(not os.path.isdir(output_dir)), f'Output directory already exists for {subid}, has prescreening already been run?'
	# if it doesn't exist, make it
	os.system(f'mkdir {output_dir}')


def validate_response(question, possible_responses):
	while True:
		participant_response = input(question)
		# if valid response
		if participant_response in possible_responses:
			break
		else:
			print(f'Invalid response! Response should be in {possible_responses}')
	return(participant_response)

def pre_questions():
	print('Okay! First I just want to ask you a few quick questions:')

	q_english = '\nAre you a fluent English speaker? '
	q_schedule = "\nWe have the opportunity to invite some participants to conduct 3 more videocalls with us. \
		\nIf selected, in these calls you would get to listen to a variety of audio clips and we’d discuss \
		\nmemories from various points in your life. If selected, would you be interested in scheduling \
		\nthese 3 sessions? "

	q_internet = "\nDo you have consistent access to a computer, reliable internet connection, \
		\nand a quiet space to conduct video calls? "

	q_neuro = "\nAs far as you are aware, do you have any neurological condition, or any history of post-traumatic stress disorder, music-induced trauma, or music-induced seizures? "
		
	q_hearing = "\nAs far as you are aware, do you have any hearing impairment? "
	q_race = '\nWhat is your race? '
	q_ethnicity = '\nWhat is your ethnicity? '
	q_gender = '\nWhat is your gender? '
	q_age = '\nWhat is your age in years? '
	education_options = {'No Schooling Completed':'a',
						 'Nursery school to 8th grade':'b',
						 'Some high school, no diploma': 'c',
						 'High school diploma or equivalent':'d',
						 'Some college credit, no degree': 'e',
						 'Trade/technical/vocational training': 'f',
						 'Associate degree': 'g',
						 "Bachelor's degree": 'h',
						 "Master's degree": 'i',
						 'Professional Degree': 'j',
						 'Doctorate Degree': 'k'}

	income_options = {'Less than $25,000':'a',
						 '$25,000 to $35,000':'b',
						 '$35,000 to $50,000': 'c',
						 '$50,000 to $75,000':'d',
						 '$75,000 to $100,000': 'e',
						 '$100,000 to $150,000': 'f',
						 'More than $150,000': 'g'}                 

	# open-response question on where participant is located
	q_location = '\nFrom what location in the world are you joining this call today? '

	pre_q_answers = {}
	pre_q_answers['english_speaker'] = [validate_response(question = q_english, possible_responses = ['y', 'n'])]
	pre_q_answers['internet'] = [validate_response(question = q_internet, possible_responses = ['y', 'n'])]
	pre_q_answers['neuro_condition'] = [validate_response(question = q_neuro, possible_responses = ['y', 'n'])]
	pre_q_answers['hearing_impairment'] = [validate_response(question = q_hearing, possible_responses = ['y', 'n'])]
	pre_q_answers['schedule'] = [validate_response(question = q_schedule, possible_responses = ['y', 'n'])]
	pre_q_answers['age'] = [validate_response(question = q_age, possible_responses = list(map(str, list(np.arange(18,150)))))]
	os.system('python prescreening/prescreen_demog.py')
	pre_q_answers['race'] = [input(q_race)]
	pre_q_answers['ethnicity'] = [input(q_ethnicity)]
	pre_q_answers['gender'] = [input(q_gender)]
	pre_q_answers['location'] = [input(q_location)]
	pre_q_answers['demog_exclude'] = [validate_response(question = 'Exclude this participant based on demographic responses (y for EXCLUDE)? ', possible_responses = ['y', 'n'])]



	# Education/Income Questions
	print('Which of the following best describes your level of education?')
	for i in education_options.keys():
		print(f'{education_options[i]}: {i}')
	pre_q_answers['eduation'] = [validate_response(question = 'Enter education code:', possible_responses = list(education_options.values()))]

	print('Which of the following best describes your annual household income from the past 12 months?')
	for i in income_options.keys():
		print(f'{income_options[i]}: {i}')
	pre_q_answers['income'] = [validate_response(question = 'Enter income code:', possible_responses = list(income_options.values()))]

	pre_q_df = pd.DataFrame(pre_q_answers)
	pre_q_df.to_csv(f'../raw_data/{subid}/{subid}_prescreen_responses.csv', index = False)

	# check whether to stop session and exclude participant
	if pre_q_answers['english_speaker'] == ['n'] or pre_q_answers['internet'] == ['n'] or \
		pre_q_answers['schedule'] == ['n'] or pre_q_answers['neuro_condition'] == ['y'] or \
		pre_q_answers['hearing_impairment'] == ['y'] or pre_q_answers['demog_exclude'] == ['y'] or \
			(not pre_q_answers['age'][0] in list(map(str, list(np.arange(65,81))))):
		
		print('Exclude based on pre-questions')
		sys.exit('')
	else:
		print('Include based on pre-questions')

	# return age -- needed for next scripts
	return(pre_q_answers['age'][0])


# for checking whether to go on after running artist selection	
def check_inclusion_artist():
	artist_df = pd.read_csv(str('../raw_data/' + str(subid) + '/' + str(subid) + '_artists.csv'))
	familiar_child = sum(artist_df.resp[artist_df.time == 'child'] >= 3)
	familiar_adol = sum(artist_df.resp[artist_df.time == 'adol'] >= 3)
	familiar_adult = sum(artist_df.resp[artist_df.time == 'adult'] >= 3)
	assert(familiar_child >= 5 and familiar_adol >=5 and familiar_adult >= 5), 'Exclude based on artist selection'

# for checking whether to go on after running event selection
def check_inclusion_events():
	events_file = pd.read_csv(f'../raw_data/{subid}/{subid}_events.csv')
	events_child = sum(events_file.resp[events_file.time == 'child'] == 1)
	events_adol = sum(events_file.resp[events_file.time == 'adol'] ==1 )
	events_adult = sum(events_file.resp[events_file.time == 'adult'] == 1)
	assert(events_child >= 15 and events_adol >= 15 and events_adult >= 15), 'Exclude based on event selection'


######### NOW RUN THINGS ##################


# Validate the inputs
check_prescreen_inputs(subid, year)

# print file out depending on windows vs. maca
if platform=="darwin":
  os.system('cat prescreen_intro.txt')
else: 
   os.system('type prescreen_intro.txt')
input('\npress any key + enter to continue')


# Ask 'pre-questions on elegibility/demographics)
age = pre_questions()

# Run setup R script 1 to make artist lists
os.system(f'Rscript prescreening/1_make_artist_lists.R {subid} {age} {year}')

# Pull Input Dataframe of artists from Subject's Folder
artist_df = pd.read_csv(str('../raw_data/' + str(subid) + '/' + str(subid) + '_artists.csv'))

# check that we don't already have artists selected for this participant
# throw error if 'resp' column is already in artist_df, indicating we already have participant response
assert('resp' not in artist_df.columns), f'Error! Prescreening has already ben run for {subid}'


# Run artist selection
os.system(f'python prescreening/2a_select_artists.py {subid}')

# Check that artist selection was run!
# Pull Input Dataframe of artists from Subject's Folder
artist_df = pd.read_csv(str('../raw_data/' + str(subid) + '/' + str(subid) + '_artists.csv'))

# check that we don't already have artists selected for this participant
# throw error if 'resp' column is already in artist_df, indicating we already have participant response
assert('resp' in artist_df.columns), f'Exclude participant {subid}'

# before running event selection, check whether participant had exposure to enough musical artists
check_inclusion_artist()

# Run event selection
os.system(f'python prescreening/2b_select_events.py {subid}')

# Check that event selection was run!
out_file = f'../raw_data/{subid}/{subid}_events.csv'
assert(os.path.isfile(out_file)), f'Error! No event selection file exists for participant {subid}'

# before running t-moca, check whether participant had memory of enough events
check_inclusion_events()

# Run t-moca
os.system(f'python prescreening/2c_moca.py {subid}')