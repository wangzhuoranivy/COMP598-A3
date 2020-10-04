import unittest
import pandas as pd
from pony_functions import *
import os.path as osp

class PonyTestCase(unittest.TestCase):

	script_dir = osp.dirname(__file__) 
	
	d = {'title': ['Episode A','Episode A','Episode A','Episode B','Episode B','Episode B','Episode B','Episode B'],'writer': ['LF','LF','LF','LF','LF','LF','LF','LF'],'pony':['Applejack','Rarity','Rainbow Dash','Pinkie Pie','Rainbow Dash','Narrator','Fluttershy','Twilight Sparkle'],'dialog':['test Twilight Twilight Sparkle','Hello','Hi, Spike! Hi, Rarity!','good!','rarity is not Rarity','Once upon a time..','hehehe, awwww awwww','I talk to Applejack, Rainbow and I like rainbow']}
	df = pd.DataFrame(data = d)

	dict_word_path = osp.join(script_dir,'..','..','..','data','words_alpha.txt')  
	with open(dict_word_path, 'r') as f: 
		dict_word = [line.strip() for line in f]
	dict_word = set(dict_word)
	
	# check if return type is a dictionary
	def test_verbosity(self):
		values = verbosity(self.df)
		check_dict = isinstance(values,dict)
		self.assertTrue(check_dict)
	
	# check if sum = 1 in verbosity
	def test_verbosity2(self):
		values = verbosity(self.df)
		total = sum(list(values.values()))
		check_sum = (abs(total-1)<=0.01)
		self.assertTrue(check_sum)

	# check correct value of verbosity for Twilight Sparkle
	def test_verbosity3(self):
		values = verbosity(self.df)
		ts_verb = values['twilight']
		self.assertEqual(ts_verb,round(1/7,2))
	
	# check correct dictionary size (6 ponies) and sub-dictionary size (5 ponies)
	def test_mention(self):
		values = mention(self.df)
		dict_len = len(values)
		sub_dict_len = len(values['applejack'])
		self.assertEqual([dict_len,sub_dict_len],[6,5])

	# check correct value of mentions for Pinkie Pie (edge case)
	def test_mention2(self):
		values = mention(self.df)
		pp_mentions = values['pinkie']
		correct_ans = dict(twilight=0,applejack=0,rarity=0,rainbow=0,fluttershy=0)
		self.assertEqual(pp_mentions,correct_ans)
	
	# check correct value of mentions for Twilight mention Rainbow 
	def test_mention3(self):
		values = mention(self.df)
		ts_mentions = values['twilight']['rainbow']
		self.assertEqual(ts_mentions,0.5)
	
	# check correct value of follow_on_comments for Rarity
	def test_followon(self):
		values = followon(self.df)
		rr_follow = values['rainbow']
		rr_follow_lst = list(rr_follow.values())
		self.assertEqual(rr_follow_lst,[0.0,0.0,0.5,0.5,0.0,0.0])
	
	# check correct value of follow_on_comments (edge case)
	def test_followon2(self):
		values = followon(self.df)
		aj_follow = values['applejack']
		aj_follow_lst = list(aj_follow.values())
		self.assertEqual(aj_follow_lst,[0,0,0,0,0,0])

	# check correct value of non-dictionary words
	def test_nondict(self):
		values = non_dict(self.df,self.dict_word)
		rd_nondict = values['fluttershy']
		self.assertEqual(rd_nondict,['awwww','hehehe'])

	# check edge case (non-dictionary words is empty)
	def test_nondict2(self):
		values = non_dict(self.df,self.dict_word)
		fs_nondict =  values['pinkie']
		self.assertEqual(fs_nondict,[])
	
		

	
