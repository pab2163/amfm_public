'''
Author: Paul Bloom
Date: 1/18/2021

-Runs music/memory sessions
-Imports countdown.py for multithreading

Link to google slides for running session: https://docs.google.com/presentation/d/1wBSUd-9QQxjFHZkhtv_LR9f3JiX8bivUUIZ04TP7WdA/edit#slide=id.gbd07a58e7f_0_0
'''

import pandas as pd
import os
import sys
import time
import threading
from countdown import *
import numpy as np


subid = sys.argv[1]
session = int(sys.argv[2])

# define file for this session's data
session_data = pd.read_csv(f'../raw_data/{subid}/{subid}_ses{session}.csv')


def check_correct_session(session):
	# check that the particular session hasn't been run
	assert('music_evoked_affect' not in session_data.columns), f'Error! Session {session} has already ben run for {subid}'

	# if 2 or 3 are entered for session, make sure previous session has been run
	if session != 1:
		session_prev_data = pd.read_csv(f'../raw_data/{subid}/{subid}_ses{session-1}.csv')
		assert('music_evoked_affect' in session_prev_data.columns), f'Error! Tried to run session {session}, but it seems that session {session-1} has not yet been run for {subid}'


check_correct_session(session)


def introduce_music_session():
	print('\nWelcome! Today we will be listening to some audio clips and talking about some of your memories')
	print('The session will probably take around 1 hour. If you need to take a break at any point, please just let me know!')
	print('Just as a reminder, I will be recording the video from the whole session. We will only keep the audio and delete the video after,')
	print('but you are also welcome to keep your camera off if you would rather')
	input('Any questions before we begin?\n')
	print('Okay! Before we officially get started I want to test to make sure the sound and visuals are working.')
	print('I want to remind you that at any point if you would be more comfortable, it is fine to turn your camera off')
	print('I will play a song from my computer now, and I would like you to let me know if it sounds clear to you')
	print('Feel free to adjust your volume so that you can hear the music at a comfortable volume!')
	print('[play a bit of spotify clip for participant, then share slides]')
	input('Also, can you see the screen I am sharing here?')
	print("\nGreat! I also want to let you know that when you are talking about your memories today, this will be less like a conversation\
		and more like an audio journal of your memories. I will try not to respond too much to what you are saying so I don't influence you\
			but I will be listening and paying attention. Do you have any questions about this?\
			Finally, I would like to remind you that everything I ask you to do today is completely voluntary.\
			You can opt out of any part, including if any memories I ask you about are uncomfortable for you to recall.")


def outro():
	print('\nExcellent! We are all set for today!')
	if session < 3:
		print('Thank you so much! Before we finish up I just want to confirm the time of our next session...')



# function set up likert question, validate response and return
def get_likert_input(min, max, question):
    while True:
        try:
            resp  = int(input(question))
            if resp <= max and resp >= min:
                break
            else:
                print(f'invalid answer option! should be from {min}-{max}')
        except:
            print('invalid input type!')
    return(resp)

# song instructions before playing each song
def song_instructions(trial_num):
	title = session_data.title[trial_num]
	artist = session_data.artist[trial_num]
	timing = session_data.start_time[trial_num]
	print(f'Current song: {title} - {artist}\t\nStart Time: {timing}')
	input('Ready for me to play another sound clip?\n')


def next_song_prep(trial_num):
	title = session_data.title[trial_num+1]
	artist = session_data.artist[trial_num+1]
	timing = session_data.start_time[trial_num+1]
	print(f'Next song: {title} - {artist}\t\tStart Time: {timing}')


# music emotion question to be asked after each song
def music_emotion_questions(trial_num):
	music_q = 'How did the clip you just heard make you feel, \n\ton a scale from 1 (meaning very negative) to 7 (meaning very positive) '
	session_data.at[trial_num, 'music_evoked_affect'] = get_likert_input(min = 0, max = 7, question = music_q)

def event_prompt(trial_num):
	# Print out age range before memory prompt
	event = session_data.event[trial_num]
	if session_data.time[trial_num] == 'adult':
		age_range = '20-25 years'
	elif session_data.time[trial_num] == 'adol':
		age_range = '14-18 years'
	elif session_data.time[trial_num] == 'child':
		age_range = '5-9 years'
	print(f'\nThank you! Now, in our initial phone call you told me you remembered:\n{event.upper()}')
	print(f"\nAnd we would like this memory to be between ages: {age_range}")
	input('Could you please tell me all you can remember about this specific event, focusing on \n-what happened \n-where you were\n-who was there\n-and what you thought and felt?')
	# if not the last trial, give info on prepping the next song
	if trial_num < 14:
		next_song_prep(trial_num)

	# start the countdown timer for the AI recall period
	countdown_timer(240)

# questions to be asked following the prompted recall
def post_event_questions(trial_num):
	event = session_data.event[trial_num]
	mem_positive_q = '\nThank you for sharing that memory! On a scale from 1-7, how positive was that memory? '
	mem_vivid_q = 'On a scale from 1-7, how vivid was that memory? '
	mem_coincidence_q = f'How closely related was that memory to {event.upper()} on a scale from 1 (completely different) to 5 (the same memory)? '

	session_data.at[trial_num, 'mem_positive'] = get_likert_input(min = 0, max = 7, question = mem_positive_q)
	session_data.at[trial_num, 'mem_vivid'] = get_likert_input(min = 0, max = 7, question = mem_vivid_q)
	while True:
		spont_memory = input('Now, thinking back to the clip you heard right before this, did any memories come to mind spontaneously while you were listening? (y/n) ')
		if spont_memory in ['y', 'n', '0']:
			break
		else:
			print('Invalid input! Should be either "y" or "n"')
	
	session_data.at[trial_num, 'spont_memory'] = spont_memory
	if spont_memory == 'y':
		session_data.at[trial_num, 'mem_coincidence'] = get_likert_input(min = 0, max = 5, question = mem_coincidence_q)

# initialize new df columns
session_data['music_evoked_affect'] = np.nan
session_data['mem_positive'] = np.nan
session_data['mem_vivid'] = np.nan
session_data['spont_memory'] = ''
session_data['mem_coincidence'] = np.nan

# set up!
introduce_music_session()


# macro loop -- what to do for each trial!
for trial in range(15):
	print(f'\nTrial {trial + 1}')
	song_instructions(trial)
	music_emotion_questions(trial)
	event_prompt(trial)
	post_event_questions(trial)

# write out data to same file
session_data.to_csv(f'../raw_data/{subid}/{subid}_ses{session}.csv', index = False)

# run post-questions only if session 3
if session in [1,2]:
	# give outro
	outro()
elif session == 3:
	os.system(f'python 4_run_post_question.py {subid}')