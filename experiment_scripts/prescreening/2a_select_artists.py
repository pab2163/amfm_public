
import sys
import pandas as pd 
import numpy as np 
from random import shuffle
import os
from sys import platform

# get command line input of participant ID
subid = sys.argv[1]

# Pull Input Dataframe of artists from Subject's Folder
artist_df = pd.read_csv(str('../raw_data/' + str(subid) + '/' + str(subid) + '_artists.csv'))

# check that we don't already have artists selected for this participant
# throw error if 'resp' column is already in artist_df, indicating we already have participant response
assert('resp' not in artist_df.columns), f'Error! Artist selection has already ben run for {subid}'


artist_df['resp'] = np.nan
unique_artists = artist_df['artist'].unique()

familiar = [0,0,0]
numSongs = 5
min_familiarity = 3

def validate_response(question, possible_responses):
	while True:
		participant_response = input(question)
		# if valid response
		if participant_response in possible_responses:
			break
		else:
			print(f'Invalid response! Response should be in {possible_responses}')
	return(participant_response)


def artist_selection_setup():
    print('\nNow, I will read you a list of many musical artists that have been popular in the US. \n\
        For each one, please rate how much you were exposed to that artists music before age 25\n\
        Please answer "Zero", or "Never", if you have never heard of an artist I mention.\n\
        Otherwise, you can rate the artist on a scale from 1 (meaning hardly ever exposed to) to \n\
        5 (meaning exposed to a lot). We do not expect you to be familiar with all of the artists I read, \n\
        so please do not worry if you have never heard of some of these artists.')
    print('')
    input('Are these instructions clear? Any questions?')


# function for displaying the text info for one song on the screen
def showOneSong(trialNum, unique_artists):
    artistText = unique_artists[trialNum]

    print('Child Familiar: ' + str(familiar[0]))
    print('Adol Familiar: ' + str(familiar[1]))
    print('Adult Familiar: ' + str(familiar[2]))
    print('artistNum: ' + str(trialNum) + '\n\n')
    response = getResponse(artistText)

    # Update numbers
    artist_df.loc[artist_df['artist'] == unique_artists[trialNum], 'resp'] = int(response)

    # calculate number of songs familiar enough so far in each time period
    familiar[0] = (artist_df[(artist_df['resp'] >= min_familiarity) & (artist_df['time'] == 'child')]).shape[0]
    familiar[1] = (artist_df[(artist_df['resp'] >= min_familiarity) & (artist_df['time'] == 'adol')]).shape[0]
    familiar[2] = (artist_df[(artist_df['resp'] >= min_familiarity) & (artist_df['time'] == 'adult')]).shape[0]


# function for getting participant response yes/no
def getResponse(artist_name):
    while True:
        try:
            resp  = int(input(f'On a scale from 0-5, how much were you exposed to {artist_name.upper()} before age 25? '))
            if resp <= 5 and resp >= 0:
                break
            else:
                print('invalid answer option! should be from 0-5')
        except:
            print('invalid input type!')
    return(resp)


# set background, control macro structure
def start(unique_artists):
    # trials loop
    # Ask about 60 artist to start
    firstPassartistNum = 60

    # go through first 60 artists
    for trial in range(0,firstPassartistNum):
        showOneSong(trial, unique_artists)

    # if one of the categories is still below 5
    if min(familiar) < 5:
        for trial in range(firstPassartistNum, len(unique_artists)):
            # if the artist was included for childhood
            if unique_artists[trial] in (artist_df['artist'][artist_df['time'] == 'child']).tolist():
                # if childhood artists still needed, then ask about the artist
                if familiar[0] < 5:
                    showOneSong(trial, unique_artists)
            # else, if the artist was included for adolescence
            elif unique_artists[trial] in (artist_df['artist'][artist_df['time'] == 'adol']).tolist():
                # if adol artists still needed, then ask about the artist
                if familiar[1] < 5:
                    showOneSong(trial, unique_artists)
            # if the artist was included for adulthood, 
            elif unique_artists[trial] in (artist_df['artist'][artist_df['time'] == 'adult']).tolist():
                # if adult artists still needed, then ask about the artist
                if familiar[2] < 5:
                    showOneSong(trial, unique_artists)

            # check if enough songs in each category now
            if min(familiar) >= 5:
                end()

# save output csv
def end():
    artist_df['participantID'] = subid
    artist_df.to_csv(str('../raw_data/' + str(subid) + '/' + str(subid) + '_artists.csv'), index = False)
    if min(familiar) < 5:
        print('\nExclude based on artist selection')
    else:
        print('\nInclude based on artist selection')
    sys.exit('')


# actually run everything!
artist_selection_setup()
start(unique_artists)
end()
