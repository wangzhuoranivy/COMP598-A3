import sys
import pandas as pd
import argparse
import json
import os.path as osp
import numpy as np
import re 

script_dir = osp.dirname(__file__)

def main():
	parser = argparse.ArgumentParser()
	
	parser.add_argument('src_file',help='need src file for analysis')

	parser.add_argument('-o', nargs='?', type=argparse.FileType('w'), help='output file, in JSON format')

	args = parser.parse_args()

	src_file = osp.join(script_dir,'..','data',f'{args.src_file}')
	df = pd.read_csv(src_file)
	
	dict_1 = verbosity(df)
	dict_3 = followon(df)

def verbosity(df):	
	# create a copy of dataframe for verbosity	
	df_verb = df.copy()

	# create columns last_title and last_pony
	df_verb['last_title'] = df_verb['title'].shift(1)
	df_verb['last_pony'] = df_verb['pony'].shift(1)
	
	# handle NaN in row 1
	df_verb.last_title.fillna('Null', inplace = True)
	df_verb.last_pony.fillna('Null',inplace = True)
	
	# filter episode same,speaker same -> not speech act 
	df_verb.loc[((df_verb['last_title'] == df_verb['title'])&(df_verb['last_pony'] == df_verb['pony'])),'speech_act'] = False
	
	# get all rows that are speech acts
	df_verb = df_verb[df_verb.speech_act != False]
	
	speech_ts = check_verb(df,'Twilight Sparkle')
	speech_aj = check_verb(df,'Applejack')
	speech_rr = check_verb(df,'Rarity')
	speech_pp = check_verb(df,'Pinkie Pie')
	speech_rd = check_verb(df,'Rainbow Dash')
	speech_fs = check_verb(df,'Fluttershy')
		
	# create dictionary to store speech acts
	verbosity = dict(twilight=speech_ts,applejack=speech_aj,rarity=speech_rr,pinky=speech_pp,rainbow=speech_rd,fluttershy=speech_fs) 	
	
	print(verbosity)
	return(verbosity)


def check_verb(df,pony_speaker):
	x = df['pony'].str.contains(pony_speaker,flags=re.IGNORECASE,regex = True)
	
	# get all true
	speech_pony = x.values.sum()
	# sum of all rows where speaker is pony_speaker
	speech_sum = len(df.index)
	# ratio
	speech_pony = round(speech_pony/speech_sum,2)
	return(speech_pony)

"""
def mention(df):
	
			
	return mention

def lookup (df, pony_speaker):
	# get all rows where speaker is ...
	filtered_df = df[(df['pony']==pony_speaker)]
	
	# loop through all those rows
	for i in range(len(df_fol)):
		for word in 
"""


def followon(df):

	# iterate through rows, if episode same, speaker is pony, prev speaker is different pony, then add is_follow = true

	df_fol = df.copy()
	pony_str = ['Twilight Sparkle','Applejack','Rarity','Pinkie Pie','Rainbow Dash','Fluttershy']
	
	# first elem is not follow-up
	fol_list = [False]

	for i in range(1,len(df_fol)):
		if df_fol['title'][i-1] == df_fol['title'][i] and df_fol['pony'][i-1] != df['pony'][i] and df_fol['pony'][i-1] in pony_str and df_fol['pony'][i] in pony_str:
			# record who the pony follows (prev pony)
			fol_list.append(df_fol['pony'][i-1])
		else: 
			fol_list.append(False)

	df_fol['is_follow'] = fol_list
		
	# count number of follow-ups
	df_fol = df_fol.loc[df_fol['is_follow'] != False]
	
	pony_str_abbr = ['twilight','applejack','rarity','pinky','rainbow','fluttershy']
	
	# compute each dictionary
	ts =follow_dict('Twilight Sparkle','twilight',df_fol,pony_str,pony_str_abbr)
	aj =follow_dict('Applejack','applejack',df_fol,pony_str,pony_str_abbr)
	rr =follow_dict('Rarity','rarity',df_fol,pony_str,pony_str_abbr)
	pp =follow_dict('Pinkie Pie','pinky',df_fol,pony_str,pony_str_abbr)
	rd =follow_dict('Rainbow Dash','rainbow',df_fol,pony_str,pony_str_abbr)
	fs =follow_dict('Fluttershy','fluttershy',df_fol,pony_str,pony_str_abbr)
	
	followon_comment = dict(twilight=ts,applejack=aj,rarity=rr,pinky=pp,rainbow=rd,fluttershy=fs)
	print(followon_comment)
	return followon_comment


	# a function takes a pony and a df as input and outputs a dictionary
def follow_dict (pony_speaker,pony_speaker_abbr,df,pony_str,pony_str_abbr):

	# pony_key = name of all ponies except speaker
	# pony_key_abbr = actual key (abbreviated version)
	pony_key = pony_str[:]
	pony_key.remove(pony_speaker)
	pony_value = []

	pony_key_abbr = pony_str_abbr[:]
	pony_key_abbr.remove(pony_speaker_abbr)
	for p in pony_key:
		# filter pony = pony_speaker and is_follow = p
		filtered_df = df[(df['pony']==pony_speaker) & (df['is_follow']==p)]
		# get the count
		p_count = len(filtered_df.index) 
		pony_value.append(p_count)
	
	pony_value_ratio = []
	for q in pony_value:
		# get ratio
		pony_value_ratio.append(round(q/sum(pony_value),2))
	
	# create dictionary
	pony_dict = dict(zip(pony_key_abbr,pony_value_ratio))
	return pony_dict
	
	#df['content_length'] = df.apply(lambda row: len(row['content']),axis = 1)

if __name__ == '__main__':
	main()
