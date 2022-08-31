# This script pulls the familiar songs to be played for a participant given their artist ratings
# It takes 1 command line arguments: subid
# Date: 1/13/2021

packagesToLoad = c('dplyr', 'tidyr', 'plyr')
suppressWarnings(suppressMessages(lapply(packagesToLoad, library, character.only = TRUE)))


# Take Command Line Args --------------------------------------------------
args = commandArgs(trailingOnly=TRUE)

# assign command line args to variables
subid = args[1]


# Pull in subjects artist ratings
artist_frameFile = paste0('../raw_data/', subid, '/', subid, '_artists.csv')
artist_frame = read.csv(artist_frameFile, stringsAsFactors = FALSE)


# Pull main song database
song_frame = read.csv('../music_databases/familiar_music_database.csv', stringsAsFactors = FALSE)


# Set years for time periods
age = artist_frame$age[1]
current_year = artist_frame$current_year[1]
ageBirth = current_year - age
age5 = ageBirth + 5
age9 = ageBirth + 9
age14 = ageBirth + 14
age18 = ageBirth + 18
age20 = ageBirth + 20
age24 = ageBirth + 24


pickFamiliarSongs= function(age, current_year){
  sequence = c(5,4,3,2,1)
  
  # Initialize Dataframe
  childSongs= tibble(year =as.integer(),
                      Title = as.character(),
                      artist = as.character(),
                      Genre = as.character(),
                      rank = as.integer(),
                      index = as.integer())
  
  adolSongs = childSongs
  adultSongs = childSongs
  
  # Iterate to make dataframes of familiar songs -- starting with most familiar ranking then going down
  for (rating in sequence){
    artistSelect = artist_frame %>%
      dplyr::filter(., resp == rating) 
      if (nrow(artistSelect) >= 1){
          # Child
        # Get top child songs of the current rating
          songs = song_frame %>%
            dplyr::filter(., artist %in% artistSelect$artist[artistSelect$time == 'child'], year >= age5, year <= age9) %>%
            dplyr::group_by(artist) %>%
            dplyr::top_n(., n = -1, wt = rank) %>%
            dplyr::ungroup() %>%
            dplyr::top_n(., n = -5, wt = rank)
        if (nrow(songs) >= 1){
          songs$rating = rating
        }
        # If childSongs isn't full yet, add songs at the current rating level
        if (nrow(childSongs) < 5){
          childSongs = rbind(childSongs, songs)
        }
        # Adol
        # Get top adol songs of the current rating
        songs = song_frame %>%
          dplyr::filter(., artist %in% artistSelect$artist[artistSelect$time == 'adol'], year >= age14, year <= age18) %>%
          dplyr::group_by(artist) %>%
          dplyr::top_n(., n = -1, wt = rank) %>%
          dplyr::ungroup() %>%
          dplyr::top_n(., n = -5, wt = rank)
        if (nrow(songs) >= 1){
          songs$rating = rating
        }
        # If adolSongs isn't full yet, add songs at the current rating level
        if (nrow(adolSongs) < 5){
          adolSongs = rbind(adolSongs, songs)
        }
        # Adult
        # Get top adult songs of the current rating
        songs = song_frame %>%
          dplyr::filter(., artist %in% artistSelect$artist[artistSelect$time == 'adult'], year >= age20, year <= age24) %>%
          dplyr::group_by(artist) %>%
          dplyr::top_n(., n = -1, wt = rank) %>%
          dplyr::ungroup() %>%
          dplyr::top_n(., n = -5, wt = rank)
        if (nrow(songs) >= 1){
          songs$rating = rating
        }
        # If adolSongs isn't full yet, add songs at the current rating level
        if (nrow(adultSongs) < 5){
          adultSongs = rbind(adultSongs, songs)
        }
    }
  }
  
  if (nrow(childSongs) >= 1){
      childSongs = dplyr::mutate(childSongs, indexTemp = 1:nrow(childSongs), time = 'child') %>%
        dplyr::top_n(., n = -5, wt = indexTemp) %>%
        dplyr::select(., -indexTemp)
  }
  else{
      childSongs= tibble(year =as.integer(),
                      Title = as.character(),
                      artist = as.character(),
                      Genre = as.character(),
                      rank = as.integer(),
                      index = as.integer())
  }

  if (nrow(adolSongs >= 1)){
      adolSongs = dplyr::mutate(adolSongs, indexTemp = 1:nrow(adolSongs), time = 'adol') %>%
        dplyr::top_n(., n = -5, wt = indexTemp) %>%
        dplyr::select(., -indexTemp)
  }
  else{
     adolSongs= tibble(year =as.integer(),
                  Title = as.character(),
                  artist = as.character(),
                  Genre = as.character(),
                  rank = as.integer(),
                  index = as.integer()) 
  }
  if (nrow(adultSongs >= 1)){
        adultSongs = dplyr::mutate(adultSongs, indexTemp = 1:nrow(adultSongs), time = 'adult') %>%
        dplyr::top_n(., n = -5, wt = indexTemp) %>%
        dplyr::select(., -indexTemp) 
  }
  else{
     adultSongs= tibble(year =as.integer(),
                  Title = as.character(),
                  artist = as.character(),
                  Genre = as.character(),
                  rank = as.integer(),
                  index = as.integer()) 
  }
  familiarFrame = rbind(childSongs, adolSongs, adultSongs)
  return(familiarFrame)
}

# run the function to pick familiar songs
familiar = pickFamiliarSongs(age = age, current_year = current_year) %>%
  dplyr::mutate(., condition = 'familiar')


out_file_name = paste0('../raw_data/', subid, '/', subid, '_familiar_songs.csv')
write.csv(familiar, file = out_file_name, row.names = FALSE)


