'''
Author: Paul Bloom & Michaelle DiMaggio-Potter
Date: 3/9/2021

1. Go through all songs and ask participants to rate familiarity and early-life listening for each one
2. Music experiences questionairre
'''


# pandas is how we work with dataframes in python
import pandas as pd
import os
import sys
import time
import numpy as np

######## SETUP ###################################

# subid is command line argument 1
subid = sys.argv[1]

# filepaths for familiar/unfamiliar songs
familiar_path = f'../raw_data/{subid}/{subid}_familiar_songs.csv'
unfamiliar_path = f'../raw_data/{subid}/{subid}_unfamiliar_songs.csv'

# import data files
df_familiar = pd.read_csv(familiar_path)
df_unfamiliar = pd.read_csv(unfamiliar_path)

# drop unneceesary columns
df_familiar = df_familiar[['title', 'artist', 'start_time']]
df_unfamiliar = df_unfamiliar[['title', 'artist', 'start_time']]

df_combined = pd.concat([df_familiar, df_unfamiliar])

# shuffle dataframe rows
df_combined = df_combined.sample(frac=1).reset_index(drop=True)

# set up blank column to be filled in with participant responses
df_combined['familiarity'] = np.nan
df_combined['childhood_exposure'] = np.nan
df_combined['adolescence_exposure'] = np.nan
df_combined['young_adult_exposure'] = np.nan
df_combined['adult_present_exposure'] = np.nan
df_combined['clip_liking'] = np.nan


#### DEFINE FUNCTIONS #############

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

# general function for validating responses
def validate_response(question, possible_responses):
    while True:
        participant_response = input(question)
        # if valid response
        if participant_response in possible_responses:
            break
        else:
            print(f'Invalid response! Response should be in {possible_responses}')
    return(participant_response)

# Function for printing info about a song
def print_song_info(row_number):
    print("")
    print(f"Title: {df_combined.title[row_number]}")
    print(f"Artist: {df_combined.artist[row_number]}\n")
    print(f"Start Time: {df_combined.start_time[row_number]}\n")

# ask the participant how familiar they are with the song
def ask_familiarity(row_number):
    df_combined.at[row_number, 'familiarity'] = get_likert_input(min = 1, max = 5, question = "On a scale of 1 (not familiar at all) to 5 (extremely familiar), how familiar is the song you just heard?")
def ask_childhood_exposure(row_number):
    df_combined.at[row_number, 'childhood_exposure'] = get_likert_input(min = 1, max = 5, question = "On a scale of 1 (never listened to) to 5 (listened every day), how much did you listen to the song you just heard during ages 5-9?")
def ask_adolescence_exposure(row_number):
    df_combined.at[row_number, 'adolescence_exposure'] = get_likert_input(min = 1, max = 5, question = "On a scale of 1 (never listened to) to 5 (listened every day), how much did you listen to the song you just heard during ages 14-18?")
def ask_young_adult_exposure(row_number):
    df_combined.at[row_number, 'young_adult_exposure'] = get_likert_input(min = 1, max = 5, question = "On a scale of 1 (never listened to) to 5 (listened every day), how much did you listen to the song you just heard during ages 20-25?")
def ask_adult_present_exposure(row_number):
    df_combined.at[row_number, 'adult_present_exposure'] = get_likert_input(min = 1, max = 5, question = "On a scale of 1 (have never listened to) to 5 (have listened every day), how much have you listened to this song from age 26-present?")
def ask_clip_liking(row_number):
    df_combined.at[row_number, 'clip_liking'] = get_likert_input(min = 1, max = 5, question = "On a scale of 1 (hated it) to 5 (loved it), how much did you like that clip?")


# functions for music background questions
def ask_pop_listening_childhood():
    music_background_df['pop_listening_childhood'] = get_likert_input(min = 1, max = 7, question = "On a scale of 1 (no pop listening) to 7 (listened to pop every day), what number best describes your total USA pop music listening in childhood (5-9)?")
def ask_pop_radio_childhood():
    music_background_df['pop_radio_childhood'] = get_likert_input(min = 1, max = 7, question = "On a scale of 1 (not at all) to 7 (heard a lot) how often did you hear USA pop music on the radio when you were a child (5-9)?")
def ask_pop_hours_childhood():
    music_background_df['pop_hours_childhood'] = get_likert_input(min = 1, max = 7, question = "About how many hours per month did you listen to USA pop music in childhood (5-9) years old?\nWas it 0-1 hours, 1-3 hours, 4-7 hours, 8-11 hours, 12-15 hours, or more than 16 hours?\n[Directions: input 1-7 for the followings hours reported.]\n1: NA\n2: 0-1 hr\n3: 1-3 hrs\n4: 4-7 hrs\n5: 8-11 hrs\n6: 12-15 hrs\n7: 16 + hrs\n")
def ask_pop_like_childhood():
    music_background_df['pop_like_childhood'] = get_likert_input(min = 1, max = 7, question = "On a scale of 1 (hated it) to 7 (really really liked it), how much did you like the USA pop music you heard during childhood (5-9)?")
def ask_pop_mood_childhood():
    music_background_df['pop_mood_childhood'] = get_likert_input(min = 1, max = 7, question = "On a scale of 1 (worst times in my life) to 7 (best times in my life), with what mood/experiences do you associate childhood USA pop music?")
def ask_pop_listening_adolescence():
    music_background_df['pop_listening_adolescence'] = get_likert_input(min = 1, max = 7, question = "On a scale of 1 (no pop listening) to 7 (listened every day), what number best describes your total USA pop music listening when you were in adolescence (14-18 years old)?")
def ask_pop_radio_adolescence():
    music_background_df['pop_radio_adolescence'] = get_likert_input(min = 1, max = 7, question = "On a scale of 1 (not at all) to 7 (heard a lot) how often did you hear USA pop music on the radio when you were in adolescence (14-18 years old)?")
def ask_pop_hours_adolescence():
    music_background_df['pop_hours_adolescence'] = get_likert_input(min = 1, max = 7, question = "About how many hours per month did you listen to USA pop music in adolescence (14-18) years old?\nWas it 0-1 hours, 1-3 hours, 4-7 hours, 8-11 hours, 12-15 hours, or more than 16 hours?\n[Directions: input 1-7 for the followings hours reported.]\n1: NA\n2: 0-1 hr\n3: 1-3 hrs\n4: 4-7 hrs\n5: 8-11 hrs\n6: 12-15 hrs\n7: 16 + hrs\n")
def ask_pop_like_adolescence():
    music_background_df['pop_like_adolescence'] = get_likert_input(min = 1, max = 7, question = "On a scale of 1 (hated it) to 7 (really really liked it), how much did you like the USA pop music you heard during adolescence (14-18)?")
def ask_pop_mood_adolescence():
     music_background_df['pop_mood_adolescence'] = get_likert_input(min = 1, max = 7, question = "On a scale of 1 (worst times in my life) to 7 (best times in my life), with what mood/experiences do you associate adolescent USA pop music?")

########### Run questions about specific songs ##################

#Text for experimenter and printing songs
print("\nThank you for participating in the Music and Memory Study.")
print("For our final session, I'm going to replay each song you heard earlier for 10 seconds.")
print("Then I'm going to ask you how familiar you are with the songs.\n")
print("Do you have any questions?")
input()
print("Great, let's begin.\n")
input()
print("[Directions: Play each song for 10 seconds, then ask the following questions.]\n")

# i is the 'iterator' variable which is changing throughout the loop
for i in range(df_combined.shape[0]):
    print(i)
    print_song_info(row_number = i)
    print("")
    ask_familiarity(row_number = i)
    print("")
    ask_childhood_exposure(row_number = i)
    print("")
    ask_adolescence_exposure(row_number = i)
    print("")
    ask_young_adult_exposure(row_number = i)
    print("")
    ask_adult_present_exposure(row_number = i)
    print("")
    ask_clip_liking(row_number = i)
    print("")

# save the data for song famliarity / liking
df_combined.to_csv(f'../raw_data/{subid}/{subid}_participant_song_familiarity_ratings.csv')

####### RUN MUSIC BACKGROUND QUESTIONS ######

#define music background questions
print("Thank you so much. Now I am going to ask you a few more questions about your exposure to USA pop/mainstream music.")
print("“Pop” music includes “top 40” or “hot 100” Billboard songs that typically feature vocals.")
input("")

# Saving to one row data frame
music_background_df = pd.DataFrame({'subid':[subid]})

#ask music background questions
ask_pop_listening_childhood()
print("")
ask_pop_radio_childhood()
print("")
ask_pop_hours_childhood()
print("")
ask_pop_like_childhood()
print("")
ask_pop_mood_childhood()
print("")
ask_pop_listening_adolescence()
print("")
ask_pop_radio_adolescence()
print("")
ask_pop_hours_adolescence()
print("")
ask_pop_like_adolescence()
print("")
ask_pop_mood_adolescence()
print("")


#closing remarks and future updates
print("Now that the study has come to a close, we will be sending you a link to access an Amazon e-gift card.")
print("The total amount will be calculated at $20/hr for each zoom session, including our pre-screening session.")
print("We will also securely send you a debriefing form via redcap,")
print("as well as a spotify playlist or spreadsheet of the songs you listened to.")
print("Finally, if you're interested, we can keep you updated with any findings from the study.\n")


# Check about future updates
future_updates = validate_response ("Would you like us to send you updates? [Directions: input y or n]", possible_responses = ["y", "n"]) 
if future_updates == "y":
    print("\nOkay! You'll be receiving those updates.")
elif future_updates == "n":
    print("\nOkay, you will not be receiving any future updates.")

music_background_df['future_updates'] = future_updates
music_background_df.to_csv(f'../raw_data/{subid}/{subid}_participant_music_background.csv', index=False)


###### Debrief participant #####
input()
print("From this point onwards, you won't be paid for your time.")
print("However, if you have questions, I'm happy to stay on and answer them!") 
input()
print("At this time, we are still recruiting participants,")
print("so if you know anyone who might be interested,")
print("feel free to refer them to the study.")
print("We just ask that you try to refrain from mentioning any details about the study.")
print("Again, thank you so much for participating in the study! Have a wonderful day/evening/weekend!\n\n")