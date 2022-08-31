'''
Author: Paul Bloom
Date: 1/18/2021

Sets up csv files for each of the 3 music/memory sessions based on prescreen
and counterbalancing info
'''

import pandas as pd
import os
import sys
import numpy as np

# take participant id
subid = sys.argv[1]

# read in participant list of event responses
events = pd.read_csv(f'../raw_data/{subid}/{subid}_events.csv')

# only prompts participant said yes for
events = events[events.resp == 1]

# cleanup
events.drop(columns = ['resp'], inplace = True)
events.rename(columns = {'EVENT': 'event'}, inplace = True)


'''
Function to parse counterbalance code:

First 3 characters: time period blocks
C: child
T: adol (teen)
A: adult

Last 3 characters: music condition
F: familiar
U: unfamiliar
C: control (no music)
'''
def use_cb_code(subid):
	# pull participant counterbalance code from key
	cb_codes = pd.read_csv('counterbalance_2021-01-14.csv')
	#print(cb_codes)
	cb = cb_codes.cb[cb_codes.subid == subid]
	cb = cb.iloc[0]

	# generate list with time period orders
	time_period_order = list(cb[0:3])
	for i in range(len(time_period_order)):
		if time_period_order[i] == 'C':
			time_period_order[i] = 'child'
		elif time_period_order[i] == 'A':
			time_period_order[i] = 'adult'
		elif time_period_order[i] == 'T':
			time_period_order[i] = 'adol'

	# music condition orders
	music_condition_order = cb[3:6]

	return({'music_order': music_condition_order,
			'time_period_order': time_period_order})

# get orderings from parsed counterbalance code
ordering = use_cb_code(subid)

# break up into child/adol/adult events, shuffle each one
# block order is consistent across sessions
block1_events=events[events.time==ordering['time_period_order'][0]].sample(frac = 1)
block2_events=events[events.time==ordering['time_period_order'][1]].sample(frac = 1)
block3_events=events[events.time==ordering['time_period_order'][2]].sample(frac = 1)

# split events across sessions, keeping block order consistent
ses1=pd.concat([block1_events.iloc[0:5,:],
	block2_events.iloc[0:5,:],
	block3_events.iloc[0:5,:]])

ses2=pd.concat([block1_events.iloc[5:10,:],
	block2_events.iloc[5:10,:],
	block3_events.iloc[5:10,:]])

ses3=pd.concat([block1_events.iloc[10:15,:],
	block2_events.iloc[10:15,:],
	block3_events.iloc[10:15,:]])

# add music condition labels for each of the sessions
ses1['condition'] = ordering['music_order'][0]
ses2['condition'] = ordering['music_order'][1]
ses3['condition'] = ordering['music_order'][2]


# for each session, pull info on clips in
# something a little different happens depending on which condition it is
ses_list = [ses1, ses2, ses3]
for i in range(3):
	session_frame = ses_list[i]
	session_frame.reset_index(inplace = True, drop = True)

	# if familiar, pull familair music in
	if session_frame.condition[1] == 'F':
		familiar_songs = pd.read_csv(f'../raw_data/{subid}/{subid}_familiar_songs.csv')

		# reorder songs by time period, shuffling within time period
		block1_songs = familiar_songs[familiar_songs.time == ordering['time_period_order'][0]].sample(frac = 1)
		block2_songs = familiar_songs[familiar_songs.time == ordering['time_period_order'][1]].sample(frac = 1)
		block3_songs = familiar_songs[familiar_songs.time == ordering['time_period_order'][2]].sample(frac = 1)
		familiar_songs_ordered = pd.concat([block1_songs, block2_songs, block3_songs]).reset_index(drop=True)
		familiar_songs_ordered.rename(columns = {'time':'time_songs'}, inplace = True)
		familiar_songs_ordered.drop(columns = ['condition'], inplace = True)
		session_frame = pd.concat([session_frame, familiar_songs_ordered], axis = 1).reindex()

	# if unfamiliar, pull unfamiliar music in
	elif session_frame.condition[1] == 'U':
		# get participant-specific unfamilar songs, merge in data from unfamiliar database
		unfamiliar_songs = pd.read_csv(f'../raw_data/{subid}/{subid}_unfamiliar_songs.csv')
		unfamiliar_songs.drop(columns = ['id', 'uri', 'duration_ms', 'time_signature', 'streams', 'genre'],
			inplace = True)

		# shuffle unfamiliar songs
		unfamiliar_songs = unfamiliar_songs.sample(frac = 1).reset_index(drop = True)

		# add unfamiliar songs to events
		session_frame = pd.concat([session_frame, unfamiliar_songs], axis = 1)

	# if no music condition ('C'), make ordering for non-music clips
	elif session_frame.condition[1] == 'C':
		clip_order = np.arange(15) + 1
		np.random.shuffle(clip_order)
		session_frame['title'] = clip_order
		session_frame['artist'] = 'no music'
		session_frame['start_time'] = 0

	# add trial and session info to csv
	session_frame['trial'] = np.arange(15) + 1
	session_frame['session'] = i + 1

	# each iteration of loop -- save to csv
	session_frame.to_csv(f'../raw_data/{subid}/{subid}_ses{i+1}.csv', index = False, float_format="%.2f")
