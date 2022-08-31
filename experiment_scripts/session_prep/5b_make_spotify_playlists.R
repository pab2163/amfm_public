# Makes a spotify playlist for a given participant ID for both familiar/unfamiliar songs
# Requires auth access to Paul's spotify account to run 
# Date: 2/14/2021
# Author: Paul A. Bloom

library(spotifyr)
library(dplyr)
library(tidyverse)


# Take Command Line Args --------------------------------------------------
args = commandArgs(trailingOnly=TRUE)

#Basic error handling ----------------------------------------------------
if (length(args)!=1) {
  stop("Improper call to script! Call should be 'Rscript 5b_make_spotify_playlist.R [subid]'", call.=FALSE)
}

# subid is first command line arg
subid = args[1]

# Set up spotify api access
keys = read_csv('spotify_keys/spotify_api_keys.csv')

# import autho token
load('spotify_keys/spotify_auth_code.rda')
Sys.setenv(SPOTIFY_CLIENT_ID = keys$client[1])
Sys.setenv(SPOTIFY_CLIENT_SECRET = keys$secret[1])
# shouldn't need to be run - but if new token needs to be set up
#auth_code = spotifyr::get_spotify_authorization_code(scope = 'playlist-modify-public')
access_token = get_spotify_access_token()


# read in familiar and unfamiliar playlist files
familiar_playlist_path = paste0('../raw_data/', subid, '/', subid,  '_familiar_songs.csv')
unfamiliar_playlist_path = paste0('../raw_data/', subid, '/', subid,  '_unfamiliar_songs.csv')
familiar = read_csv(familiar_playlist_path)
unfamiliar = read_csv(unfamiliar_playlist_path)

# a set of spotify uniform resource identifiers (URIs) for familiar songs + unfamiliar songs
uri_set = c(familiar$uri, unfamiliar$uri)

# create playlist for participant
new_playlist = spotifyr::create_playlist(name = subid, 
                          user_id = 'paulbloomusic', 
                          public = TRUE,
                          authorization =  auth_code)


# add tracks to participant playlist
spotifyr::add_tracks_to_playlist(playlist_id = new_playlist$id, 
                                 uris = uri_set, 
                                 authorization = auth_code)
