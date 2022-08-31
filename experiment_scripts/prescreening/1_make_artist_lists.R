# This script makes a list of about 100-200 artists per participant
# It takes 4 command line arguments: subid (in the ### format, eg. 001), age (years) at time of study, and current year
# Author: Paul A. Bloom
# Date: 11/19/2018


packagesToLoad = c('plyr', 'dplyr', 'tidyr')
suppressWarnings(suppressMessages(lapply(packagesToLoad, library, character.only = TRUE)))

# Take Command Line Args --------------------------------------------------
args = commandArgs(trailingOnly=TRUE)

#Basic error handling ----------------------------------------------------
if (length(args)!=3) {
  stop("Improper call to script! Call should be 'Rscript 1_makeArtistLists.R [subid] [age] [current year]'", call.=FALSE)
}


subid = args[1]
age = as.numeric(args[2])
currentYear = as.numeric(args[3])

print(c('subid', subid))
print(c('age', age))
print(c('current year', currentYear))


# Pull in song dataframe
songFrame = read.csv('../music_databases/familiar_music_database.csv', stringsAsFactors = FALSE)


# Function to pick music based on age/current year ------------------------
pickMusic = function(age, currentYear){

  # Define key ages
  ageBirth = currentYear - age
  age5 = ageBirth + 5
  age9 = ageBirth + 9
  age14 = ageBirth + 14
  age18 = ageBirth + 18
  age20 = ageBirth + 20
  age24 = ageBirth + 24

  # To pick artists:
  # 1) Filter by year for each time period
  # 2) Group by artists, and get the total # of songs on the chart in that time period, plus the rank of the top-ranking song
  # 3) Form an 'order' variable, which first ranks artists by the number of songs, then resolves ties with the rank of the top-ranking song for each artist
  # 4) Select the top 30 in each time period. For adol/child (in that order), first check overlapping artists with previous time periods, then get the top 30 UNIQUE artists after overlaps

  # ADULT
  adultArtists = dplyr::filter(songFrame, year >= age20 & year <= age24) %>%
    dplyr::group_by(artist) %>%
    dplyr::summarize(n = n(), top_rank=min(rank)) %>%
    dplyr::mutate(order = n + (1-top_rank/1000)) %>%
    dplyr::top_n(30, wt = order) %>%
    dplyr::mutate(., time = 'adult')

  # ADOL
  adolArtists = dplyr::filter(songFrame, year >= age14 & year <= age18) %>%
    dplyr::group_by(artist) %>%
    dplyr::summarize(n = n(), top_rank=min(rank)) %>%
    dplyr::mutate(order = n + (1-top_rank/1000)) %>%
    dplyr::top_n(30, wt = order) %>%
    dplyr::mutate(., time = 'adol')

  # if there is overlap between adol / adult artists, add more adol artists so there are 30 unique
  adol_overlap_artists = adolArtists$artist[adolArtists$artist %in% adultArtists$artist]
  if (length(adol_overlap_artists) > 0){
    adolArtists = dplyr::filter(songFrame, year >= age14 & year <= age18) %>%
      dplyr::group_by(artist) %>%
      dplyr::summarize(n = n(), top_rank=min(rank)) %>%
      dplyr::mutate(order = n + (1-top_rank/1000)) %>%
      dplyr::top_n(length(adol_overlap_artists) + 30, wt = order) %>%
      dplyr::mutate(., time = 'adol')
  }

  # CHILD
  childArtists = dplyr::filter(songFrame, year >= age5 & year <= age9) %>%
    dplyr::group_by(artist) %>%
    dplyr::summarize(n = n(), top_rank=min(rank)) %>%
    dplyr::mutate(order = n + (1-top_rank/1000)) %>%
    dplyr::top_n(30, wt = order) %>%
    dplyr::mutate(., time = 'child')

  # if there is overlap between adol / adult artists, add more adol artists so there are 30 unique
  child_overlap_artists = childArtists$artist[childArtists$artist %in% adultArtists$artist | childArtists$artist %in% adolArtists$artist]
  if (length(child_overlap_artists) > 0){
    childArtists = dplyr::filter(songFrame, year >= age5 & year <= age9) %>%
      dplyr::group_by(artist) %>%
      dplyr::summarize(n = n(), top_rank=min(rank)) %>%
      dplyr::mutate(order = n + (1-top_rank/1000)) %>%
      dplyr::top_n(length(adol_overlap_artists) + 30, wt = order) %>%
      dplyr::mutate(., time = 'child')
  }

  # put artist from all three time periods together
  artists = rbind(childArtists, adolArtists, adultArtists) %>%
    group_by(time) %>%
    dplyr::mutate(read_rank = rank(1-order, ties.method = 'first')) %>%
    dplyr::arrange(read_rank, .groups = time) %>%
    dplyr::select(-order)

  artists = mutate(artists, 
                   age = age,
                   current_year = currentYear)

  return(artists)
}


output = pickMusic(age, currentYear)
# Try to force proper utf8 encoding
outfile = file(paste0('../raw_data/', subid, '/', subid,'_artists.csv'),
               encoding="UTF-8")

# Write to csv
write.csv(output, file = outfile, row.names = FALSE)
