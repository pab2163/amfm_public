import os
import sys
import re

# take subid
subid = sys.argv[1]

# check that session has not already been prepped
assert(not os.path.isfile(f'../raw_data/{subid}/{subid}_familiar_songs.csv')), f'Error, songlists already exist for {subid}'

# 4a - make familiar song list
os.system(f'Rscript session_prep/4a_make_familiar_songlist.R {subid}')

# 4b - make unfamiliar song list
os.system(f'python session_prep/4b_make_unfamiliar_songlist.py {subid}')


# 5a - set up session
os.system(f'python session_prep/5a_session_setup.py {subid}')

# 5b - make spotify playlist
os.system(f'Rscript session_prep/5b_make_spotify_playlists.R {subid}')
