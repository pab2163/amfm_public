#   This script will be used to see what events the participant has or has not 
#   personally resp. It will take the events from the lists made for the 
#   three time periods (child, adol, adult), display them on the screen, and thus
#   record what events the participant says yes to, storing them in a place where
#   one can easily access it later. 

#   This script takes from template1.py that Paul Bloom made earlier this semester. 

#   Broken down (in English), this script does the following:
#       1 Inputs the dataframe of events from childhood
#       2 Displays the first event on the screen 
#       3 If the Researcher presses n, display the second event
#       4 If the Researcher presses y, store that event in a data frame; display the 
#         second event
#       5 Iterate through all the events in the childhood list
#       6 When the participant gets 5 "y"s, stop. 
#       7 Do steps 1-6 with adol list
#       8 Do steps 1-6 with adult list
#       9 Store this data frame with all the events in a file near the program so 
#         it can be easily accessed. 

#These first few steps are copied from template1.py (refered to earlier in script)
import sys
import pandas as pd
import numpy as np
import os
from sys import platform

#get command line input of participant
subid = sys.argv[1]

# specify output filename
out_file = f'../raw_data/{subid}/{subid}_events.csv'
assert(not os.path.isfile(out_file)), f'Error! Event selection has already been run for {subid}'


#function for displaying the text info of one Event on the screen
def showOneEvent(trialNum, yesCount, eventData, time_period):
	eventText = eventData.loc[trialNum, 'EVENT']
	print('\n\n')
	print(f'{time_period} yes count: ' + str(yesCount))
	print(f'Can you recall a specific memory of: \n\t{eventText}')
	yesCount = getResponse(trialNum, yesCount, eventData)
	return(yesCount)


#function for getting response on the keyboard
def getResponse(trialNum, yesCount, eventData):
	# take user response in while loop until valid
	while True:
		resp = input('')
		if resp in ['0','1']:
			break
		else:
			print('invalid answer option! should be 1 (for yes) or 0 (for no)')
	

	# once loop is broken with a valid response, update info
	resp = int(resp)
	if resp == 1:
		yesCount += 1
	#log info from that trial to output dataframe
	eventData.loc[trialNum,'trialNum'] = trialNum + 1
	eventData.loc[trialNum,'resp'] = resp

	return(yesCount)

def run_events_one_time_period(eventData, time_period):
	eventData['trialNum'] = np.nan
	eventData['resp'] = np.nan
	yesCount = 0
	for trial in range(0,eventData.shape[0]): #specifies number of events
		yesCount = showOneEvent(trial,yesCount, eventData, time_period)
		if yesCount == 15:
			break
	eventData['time'] = time_period
	return(eventData)

# print instructions for event selection
def event_selection_instructions():
	if platform=="darwin":
  		os.system('cat event_selection_instructions.txt')
	else: 
   		os.system('type event_selection_instructions.txt')

	input('(press any key to continue)')


def get_bio_response():
	print('Before the next part, I have 3 quick yes-or-no questions for you')
	while True:
		college_resp = input('Have you attended college? (y/n) ')
		if college_resp in ['y', 'n']:
			break
		else:
			print('invalid answer option! should be y (for yes) or n (for no)')
	while True:
		married_resp = input('Have you ever been married? (y/n) ')
		if married_resp in ['y', 'n']:
			break
		else:
			print('invalid answer option! should be y (for yes) or n (for no)')
	while True:
		children_resp = input('Have you ever had children? (y/n) ')
		if children_resp in ['y', 'n']:
			break
		else:
			print('invalid answer option! should be y (for yes) or n (for no)')
	
	# read in full adult event list
	eventListAdult = pd.read_csv('event_lists/eventListOnlyAdultYyy.csv')
	
	# filter based on marriage/college/children
	if college_resp == 'n':
		eventListAdult = eventListAdult[eventListAdult.CATEGORY != 'U']
	if married_resp == 'n':
		eventListAdult = eventListAdult[eventListAdult.CATEGORY != 'M']
	if children_resp == 'n':
		eventListAdult = eventListAdult[eventListAdult.CATEGORY != 'C']
	
	# have to reset indices here since df is later indexed numerically
	eventListAdult.reset_index(inplace = True)
	return(eventListAdult)



def get_event_responses():
	# check for childhood events, then adol, then adult. If for any time period, less than 15, exclude. 
	child_events = run_events_one_time_period(eventData = eventListChild, time_period = 'child')
	if child_events.resp.sum() >= 15:
		adol_events = run_events_one_time_period(eventData = eventListAdol, time_period = 'adol')
		if adol_events.resp.sum() >= 15:
			adult_events = run_events_one_time_period(eventData = eventListAdult, time_period = 'adult')
			all_events = pd.concat([child_events, adol_events, adult_events])
			all_events.drop(columns = ['trialNum', 'KEY:', 'CATEGORY', 'index'], inplace=True)
			if adult_events.resp.sum() >= 15:
				print('Include! Confirmed memory of enough events')
			else:
				print('EXCLUDE: NOT ENOUGH ADULT EVENTS')
		else:
			all_events = pd.concat([child_events, adol_events])
			print('EXCLUDE: NOT ENOUGH ADOLESCENT EVENTS')
	else:
		all_events = child_events
		print('EXCLUDE: NOT ENOUGH CHILD EVENTS')
	# regardles of what happens, save event data
	all_events.to_csv(out_file, index = False)



eventListAdult = get_bio_response()
event_selection_instructions()
eventListChild = pd.read_csv('event_lists/eventListOnlyChild.csv')
eventListAdol = pd.read_csv('event_lists/eventListOnlyAdol.csv')
get_event_responses()


