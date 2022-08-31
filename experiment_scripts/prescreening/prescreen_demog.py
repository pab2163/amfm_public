import pandas as pd 
import glob
import os
import numpy as np

# find all participant files
files = glob.glob('../raw_data/*/*prescreen_responses.csv')
files.sort()

# put together combined dataframe
df_list = []
for file in files:
	participant_df = pd.read_csv(file)
	participant_df['subid'] = file.split('/')[-2]
	df_list.append(participant_df)


comb_df = pd.concat(df_list)

comb_df['include'] = np.nan
comb_df.reset_index(inplace=True)


# mark inclusions (if 'ses11 file exists)
for index, row in comb_df.iterrows():
	ses1path = f"../raw_data/{row['subid']}/{row['subid']}_participant_song_familiarity_ratings.csv"
	if os.path.isfile(ses1path):
		comb_df.at[index, 'include'] = 1
	else:
		comb_df.at[index, 'include'] = 0


comb_df.to_csv('prescreening/prescreen_responses_combined.csv', index = False)
comb_df[comb_df.include == 1].to_csv('prescreening/prescreen_responses_included.csv', index = False)


included = comb_df.loc[comb_df.include == 1, ]

included.gender = included.gender.str.lower()
included.race = included.race.str.lower()
included.race = included.race.str.strip()
included.race_white = included.race.replace({'caucasian':'white', 'causacian': 'white', 'mediterranean': 'white'}) 

print(included.gender.value_counts())
print('Max participants of either gender = 45')

print(included.race_white.value_counts())
print('Max participants identifying as white = 55')
