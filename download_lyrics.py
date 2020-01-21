# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 14:14:48 2019
@author: zotov
"""
#we use the library for working with Genius

import lyricsgenius 

genius = lyricsgenius.Genius("BBMypsrFRNrEd68cKEkY7hLODx1wAOZ-1GfV8lOpKEdad4guY1Svo-1oB86T0fbE") #here goes your API key from Genius

#make a list of groups and artists whose songs  you want to download, in this example this is all reggeaton singers
filename = 'REGGETON_artists.txt'
with open(filename, encoding='utf-8') as f:
    reggeton_list = f.readlines()

#search for lyrics  
artist_list = []
for m in reggeton_list:
    try:
        artist = genius.search_artist(m, max_songs=None, sort="popularity")
        s = artist.songs
        artist_list.append(s)
        artist.save_lyrics(overwrite=True) #save as .json files
    except AttributeError:
        pass

#extract all songs from the artist list
song_list = []
for a in artist_list: 
    for song in a:
        song_list.append(song)
   
#artist.save_lyrics()

import pandas as pd
import json
import os

#read jsons with lyrics
songs_new = []
for filename in os.listdir('./songs'):
    if filename.endswith('.json'):
        with open(os.path.join('./songs', filename)) as f:
            song_data = json.load(f)
#            content = f.read()
            songs_new.append(song_data)

#make a dataframe with  songs 
df_songs = pd.DataFrame.from_dict(songs_new)

list_songs_df = df_songs['songs'].values.tolist()

from itertools import chain

df_songs_col = pd.DataFrame(list(chain.from_iterable(list_songs_df)))

frames = [df_songs['artist'], df_songs_col]
df = pd.concat(frames, axis=1, join='inner')
df = df.fillna('No info')

df111 = df[~df.title.str.contains('duplicada')] #exclude duplicated lyrics
df222= df111[~df111.title.str.contains('duplicado')]

df222.to_csv("all_songs.csv", sep=';', encoding='utf-8', index=False) #save the dataframe with all songs
