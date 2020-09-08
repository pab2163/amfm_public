"""
Script to generate lists of songs matching the already-generated familiar music
Uses OptMatch() function written by Matt Siegelman
Each participant will get the following outputs:
- selected.csv: familiar songs and matching unfamiliar songlist
- match_summary.csv: summary of the matched sets
- matched_pairplot.png: comparing distributions of familiar vs. matches


Paul A. Bloom & Matt Siegelman
March 2020
"""
import pandas as pd
import seaborn as sns
import sklearn.preprocessing
import scipy
import numpy as np
import scipy.stats
from scipy.special import softmax
from statsmodels.stats import weightstats
import os

# Define OptMatch function
def OptMatch(target_feature_mat, select_feature_mat, do_std, weights):
    #initialize list indices
    select_list=[i for i in range(len(select_feature_mat))]
    matched_list_inds=[]

    #get length of of possible selections
    len_select=len(select_feature_mat)


    for i in range(len(target_feature_mat)):

        #initialize probability
        feat_probs_sum=np.zeros([len_select-i])

        for j in range(len(target_feature_mat[0])):

            #get features
            target_feats=target_feature_mat[:,j]
            select_feats=select_feature_mat[:,j]

            #get distribution of current matched list once ≥2 items are includes
            if i > 1:
                matched_feats=matched_feature_mat[:,j]
                #print(i, j)
                #print(matched_feature_mat)
                matched_feat_dist=scipy.stats.gaussian_kde(matched_feats)

            #updated mean and sd
            target_feat_mean=np.mean(target_feats)
            target_feat_sd=np.std(target_feats)

            #get feature weight
            weight=weights[j]

            #get probability that each item comes from the target distribution
            select_feat_z=np.abs(select_feats-target_feat_mean)/target_feat_sd
            feat_prob_target = scipy.stats.norm.sf(select_feat_z)

            #get overall probability of item
            if i > 1 and do_std==1:
                feat_prob_current = matched_feat_dist.evaluate(select_feats)
                feat_probs = weight * np.log(feat_prob_target/feat_prob_current)
            else:
                feat_probs = weight * np.log(feat_prob_target)

            #softmax and add to sum
            feat_probs_soft=softmax(feat_probs)
            feat_probs_sum+=feat_probs_soft

        #find best song and add to matched song list and feature list
        top_ind=np.argmax(feat_probs_sum)
        matched_list_inds.append(select_list[top_ind])

        if i==0:
            matched_feature_mat=select_feature_mat[top_ind,:]
        else:
            matched_feature_mat=np.vstack((matched_feature_mat,select_feature_mat[top_ind,:]))

        #remove from original song list and feature list
        select_list=select_list[:top_ind] + select_list[top_ind+1:]
        select_feature_mat=np.concatenate((select_feature_mat[:top_ind,:],select_feature_mat[top_ind+1:,:]),axis=0)



    return matched_list_inds, matched_feature_mat

def find_participant_matches(combined_data, subid):
    print(f'Working on finding matches for {subid}')
    os.system(f'mkdir {subid}')
    # Make a dataframe of familiar songs for the current subject, plus all unfamiliar
    sub = combined_data[(combined_data.participantID == subid) |
        (combined_data.participantID == 'all')]

    sub.drop(columns =['participantID', 'key', 'instrumentalness',
        'liveness', 'speechiness', 'duration_ms', 'time_signature'], inplace = True)

    sub.dropna(inplace = True)

    # vectors to indicate familiar/unfamiliar indices
    sub_familiar = sub.familiar == 1
    sub_unfamiliar = sub.familiar == 0

    # make a dataframe of features to use for OptMatch
    sub_feature_frame = sub.drop(columns = ['Artist', 'Title',
        'familiar']).copy()

    # Add small gaussian noise to categorical columns to prevent singular matrices
    sub_feature_frame['mode'] = sub_feature_frame['mode'] + \
        np.random.normal(0,.01,len(sub_feature_frame))

    # Make a tempo-valence interaction term to also be matched on
    sub_feature_frame['tempo_valence_int'] = sub_feature_frame.tempo * \
        sub_feature_frame.valence

    # Convert to numpy arrays
    sub_feature_array = sub_feature_frame.to_numpy()
    familiar_array = sub_feature_array[sub_familiar,]
    unfamiliar_array = sub_feature_array[sub_unfamiliar,]

    # Weights vector for OptMatch
    weightVec = np.ones(familiar_array.shape[1])

    # Run OptMatch
    matched_list_inds, matched_feature_mat = OptMatch(target_feature_mat=familiar_array,
        select_feature_mat = unfamiliar_array,
        do_std = 1,
        weights = weightVec)

    # Make a dataframe of all features of selected songs (familiar + matches)
    subselect = pd.concat([sub[sub.familiar == 1],
        sub[sub.familiar == 0].iloc[matched_list_inds,]])

    # Round numbers and export selected songs to csv
    subselect.round(2).to_csv(f'{subid}/selected.csv', index = False)

    # Calculate means and sds for all features for the matched sets
    sub_means = subselect.groupby('familiar').mean()
    sub_sds = subselect.groupby('familiar').std()
    sub_means['stat'] = 'mean'
    sub_sds['stat'] = 'sd'
    groupstats = pd.concat([sub_means, sub_sds])

    # Calculate t-stats for each variable used for matching
    t, p, freedom = weightstats.ttest_ind(subselect[:int(len(subselect)/2)].drop(columns = ['Title',
        'Artist', 'familiar']),
        subselect[int(len(subselect)/2):].drop(columns = ['Title', 'Artist', 'familiar']))

    # Concatenate a summary with means, sds, and t-stats for each feature
    t_stats = pd.DataFrame(t).transpose()
    t_stats['stat'] = 'tstat'
    t_stats.columns = groupstats.columns
    sub_match_summary = groupstats.append(t_stats)
    sub_match_summary['familiar'] = sub_match_summary.index
    sub_match_summary.familiar[sub_match_summary.stat == 'tstat'] = 'NA'

    # Save summary to csv
    sub_match_summary.to_csv(f'{subid}/match_summary.csv', index = False)

    # Make a pairplot between familiar songs and selected MATCHES
    matched_pairplot = sns.pairplot(data = subselect, hue = 'familiar',\
        vars = ['acousticness','danceability','energy',
                'loudness', 'tempo','valence'],height = 2.5)

    # Save pairplot
    matched_pairplot.savefig(f'{subid}/matched_pairplot.png')


###### PULL IN DATA AND FIND SUBJECT MATCHES #####

# Pull in data
all_pilots_familiar = pd.read_csv('pilot_familiar_songs_with_spotify.csv')
unfamiliar = pd.read_csv('unfamiliar_songs_with_spotify.csv')
unfamiliar['participantID'] = 'all'

# Concat unfamiliar and familiar song
opt = pd.concat([all_pilots_familiar, unfamiliar])

# make a list of all pilot participants
sublist = all_pilots_familiar.participantID.unique()

# loop through subjects and run matching!
for subject in sublist:
    find_participant_matches(combined_data = opt, subid = subject)
