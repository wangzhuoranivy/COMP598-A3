import sys
import pandas as pd
import argparse
import json
import os.path as osp
import numpy as np
import re

from hw3.pony_functions import *

script_dir = osp.dirname(__file__)

def main():
	parser = argparse.ArgumentParser()

	parser.add_argument('src_file',help='need src file for analysis')

	parser.add_argument('-o',metavar='file_name', help='output file, in JSON format')

	args = parser.parse_args()

	src_file = osp.join(script_dir,'..','data',f'{args.src_file}')
	df = pd.read_csv(src_file)
		
	# open dictionary word file and save all as a list
	dict_word_path = osp.join(script_dir,'..','data','words_alpha.txt')
	with open(dict_word_path, 'r') as f:
		dict_word = [line.strip() for line in f]
	dict_word = set(dict_word)

	# replace unicode char w/ space
	df['dialog'] = df['dialog'].str.replace('<U\+.*>', ' ', regex=True)
	
	dict_1 = verbosity(df)
	dict_2 = mention(df)
	dict_3 = followon(df)
	dict_4 = non_dict(df,dict_word)
	
	dict_all = dict(verbosity=dict_1,mentions=dict_2,follow_on_comments=dict_3,non_dictionary_words=dict_4)

	if args.o == None:
		dict_json = json.dumps(dict_all)
		sys.stdout.write(dict_json)
        # if -o save to file
	else:
		with open(args.o, 'w') as output:
			json.dump(dict_all, output)

if __name__ == '__main__':
	main()
