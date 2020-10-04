import re
import pandas as pd

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
	
	speech_ts = check_verb(df_verb,'Twilight Sparkle')
	speech_aj = check_verb(df_verb,'Applejack')
	speech_rr = check_verb(df_verb,'Rarity')
	speech_pp = check_verb(df_verb,'Pinkie Pie')
	speech_rd = check_verb(df_verb,'Rainbow Dash')
	speech_fs = check_verb(df_verb,'Fluttershy')
		
	speech_sum = speech_ts + speech_aj + speech_rr + speech_pp + speech_rd + speech_fs
	
	# get ratio
	speech_ts = round(speech_ts/speech_sum,2)
	speech_aj = round(speech_aj/speech_sum,2)
	speech_rr = round(speech_rr/speech_sum,2)
	speech_pp = round(speech_pp/speech_sum,2)
	speech_rd = round(speech_rd/speech_sum,2)
	speech_fs = round(speech_fs/speech_sum,2)

	# create dictionary to store speech acts
	verbosity = dict(twilight=speech_ts,applejack=speech_aj,rarity=speech_rr,pinkie=speech_pp,rainbow=speech_rd,fluttershy=speech_fs) 	
	return(verbosity)


def check_verb(df,pony_speaker):
	# true if pony column content is speaker (case insensitive comparison)
	x = df['pony'].str.lower() == pony_speaker.lower()
	# get all true
	speech_pony = x.values.sum()
	return(speech_pony)


def mention(df):
	# how many times a pony mentions other ponies (wrt rows)
	df_mt = df.copy()

	mention_ts = lookup(df_mt,'Twilight Sparkle','twilight')
	mention_aj = lookup(df_mt,'Applejack','applejack')
	mention_rr = lookup(df_mt,'Rarity','rarity')
	mention_pp = lookup(df_mt,'Pinkie Pie','pinkie')
	mention_rd = lookup(df_mt,'Rainbow Dash','rainbow')
	mention_fs = lookup(df_mt,'Fluttershy','fluttershy')

	mention = dict(twilight=mention_ts,applejack=mention_aj,rarity=mention_rr,pinkie=mention_pp,rainbow=mention_rd,fluttershy=mention_fs)
	return mention


def lookup (df, pony_speaker,pony_speaker_abbr):
	# this function takes a speaker and a pony, outputs dict of speaker mention pony
	
	pony_str_abbr = ['twilight','applejack','rarity','pinkie','rainbow','fluttershy']
	pony_key_abbr = pony_str_abbr[:]
	pony_key_abbr.remove(pony_speaker_abbr)

	# remove speaker from pony_str
	pony_str = ['Twilight Sparkle','Applejack','Rarity','Pinkie Pie','Rainbow Dash','Fluttershy'] 
	pony_key = pony_str[:]
	pony_key.remove(pony_speaker)
	 
	pony_count = []
	for i in pony_key:
		
		# determine keywords based on pony
		if i == 'Twilight Sparkle':
			keywords = ['Twilight','Sparkle']
			n = 2
		if i == 'Applejack':
			keywords = ['Applejack']
			n = 1
		if i == 'Rarity':
			keywords = ['Rarity']
			n = 1
		if i == 'Pinkie Pie':
			keywords = ['Pinkie','Pie']
			n = 2
		if i == 'Rainbow Dash':
			keywords = ['Rainbow','Dash']
			n = 2
		if i == 'Fluttershy':
			keywords = ['Fluttershy']
			n = 1

		# filtered_df = dataframe where pony column has only pony_speaker
		filtered_df = df[(df['pony'].str.lower()==pony_speaker.lower())]	
		
		# loop through keywords of a pony, get number of mentions(speaker,pony[i])
		mention_count = filtered_df.dialog.str.count('|'.join(keywords)).sum()
	
		if n == 2:
			mention_count = mention_count - filtered_df.dialog.str.count(i).sum()
		pony_count.append(mention_count)
		
	pony_count_ratio = []
	
	if sum(pony_count) == 0:
		pony_count_ratio = [0,0,0,0,0]
	else:
		for q in pony_count:
			pony_count_ratio.append(round(q/sum(pony_count),2)) 	
	# zip
	pony_dict = dict(zip(pony_key_abbr,pony_count_ratio)) 
	return pony_dict
	

def followon(df):
	df_fol = df.copy()
	pony_str = ['Twilight Sparkle','Applejack','Rarity','Pinkie Pie','Rainbow Dash','Fluttershy']
	
	# fol_list stores T/F of is_follow column (first elem is not follow-up)
	fol_list = [False]
	
	# iterate through rows, if episode same, speaker is pony, prev speaker is different pony, then is_follow = true
	for i in range(1,len(df_fol)):
		if df_fol['title'][i-1] == df_fol['title'][i] and df_fol['pony'][i-1] != df['pony'][i] and df_fol['pony'][i] in pony_str:
			# record who the pony follows
			if df_fol['pony'][i-1] in pony_str:
				# if is a pony, is_follow = prev pony
				fol_list.append(df_fol['pony'][i-1])
			else:
				# if not a pony, is_follow = other
				fol_list.append('other')
		else: 
			fol_list.append(False)

	df_fol['is_follow'] = fol_list
		
	# count number of follow-ups
	df_fol = df_fol.loc[df_fol['is_follow'] != False]
	
	pony_str_abbr = ['twilight','applejack','rarity','pinkie','rainbow','fluttershy','other']
	 
	# compute each dictionary
	ts =follow_dict('Twilight Sparkle','twilight',df_fol,pony_str,pony_str_abbr)
	aj =follow_dict('Applejack','applejack',df_fol,pony_str,pony_str_abbr)
	rr =follow_dict('Rarity','rarity',df_fol,pony_str,pony_str_abbr)
	pp =follow_dict('Pinkie Pie','pinkie',df_fol,pony_str,pony_str_abbr)
	rd =follow_dict('Rainbow Dash','rainbow',df_fol,pony_str,pony_str_abbr)
	fs =follow_dict('Fluttershy','fluttershy',df_fol,pony_str,pony_str_abbr)
	
	followon_comment = dict(twilight=ts,applejack=aj,rarity=rr,pinky=pp,rainbow=rd,fluttershy=fs)
	return followon_comment


	# a function takes a pony and a df as input and outputs a dictionary
def follow_dict (pony_speaker,pony_speaker_abbr,df,pony_str,pony_str_abbr):

	# pony_key = name of all ponies except speaker + other
	# pony_key_abbr = actual key (abbreviated version)
	pony_key = pony_str[:]
	pony_key.remove(pony_speaker)
	pony_key.append('other')

	pony_key_abbr = pony_str_abbr[:]
	pony_key_abbr.remove(pony_speaker_abbr)
	
	pony_value =[]

	for p in pony_key:
		# filter pony = pony_speaker and is_follow = p
		filtered_df = df[(df['pony'].str.lower()==pony_speaker.lower()) & (df['is_follow']==p)]
		# get the count
		p_count = len(filtered_df.index) 
		pony_value.append(p_count)
	
	pony_value_ratio = []
	if sum(pony_value) == 0:
		pony_value_ratio = [0,0,0,0,0,0]	
	else:
		for q in pony_value:
			# get ratio
			pony_value_ratio.append(round(q/sum(pony_value),2))
	
	# create dictionary
	pony_dict = dict(zip(pony_key_abbr,pony_value_ratio))
	return pony_dict

def non_dict(df,dict_word):
	df_nd = df.copy()

	nd_ts = gen_nd(df_nd,'Twilight Sparkle',dict_word)
	nd_aj = gen_nd(df_nd,'Applejack',dict_word)
	nd_rr = gen_nd(df_nd,'Rarity',dict_word)
	nd_pp = gen_nd(df_nd,'Pinkie Pie',dict_word)
	nd_rd = gen_nd(df_nd,'Rainbow Dash',dict_word)
	nd_fs = gen_nd(df_nd,'Fluttershy',dict_word)
	
	nd_dict = dict(twilight=nd_ts,applejack=nd_aj,rarity=nd_rr,pinkie=nd_pp,rainbow=nd_rd,fluttershy=nd_fs)
	return nd_dict

def gen_nd(df,pony_speaker,dict_word):
	# outputs a LIST of 5 top non-dict word the pony speaker uses

	# filter rows where speaker is pony_speaker
	#filtered_df = df[df['pony'].str.lower()==pony_speaker.lower()]
	
	tot_list = []
	nd_list = []

	for i in range(0,len(df)):	
		if df['pony'][i].lower()==pony_speaker.lower():
			
			# split dialog into lst
			lst = re.split('\W',df['dialog'][i])
			
			# filter out ''
			new_lst = list(filter(lambda x: x != '',lst))
		
			# append to total list
			tot_list.extend(new_lst)
	
	# filter out the dictionary words
	for i in range(len(tot_list)):
		if tot_list[i].lower() not in dict_word:
			# remove if is dictionary word
			nd_list.append(tot_list[i].lower())
	
	if len(nd_list) > 0:	
		nd_series = pd.Series(nd_list)
	
		# count the occurence of non-dict words
		count = nd_series.value_counts()
	
		# get list of non-dict words (descending by count)
		nd_list = list(count.index)
	
		if len(nd_list) <=5:
			# number of non-dict word <= 5
			return nd_list
		else:
			# number of non-dict word > 5
			return nd_list[0:5]
	else: return []
