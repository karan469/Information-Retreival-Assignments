import pandas as pd
import numpy as np 
from tqdm import tqdm
import nltk
from nltk.tag.stanford import StanfordNERTagger
import os
from preprocess_lib import PreProcess

def solve(file_path, ner_tagger):
	# os.system("grep -E '(<title>)' "+file_path+" > "+file_path+'_title_only')
	# print('created file')
	# fd = open(file_path+'_title_only','r')
	fd = open(file_path, 'r')
	for line in fd:
		if line.startswith('<title>'):
			query_line = line.split(': ')[-1]
			# preprocess(query_line)
			tokenized_text = nltk.word_tokenize(query_line)
			classified_text = ner_tagger.tag(tokenized_text)
			print(classified_text)


if __name__=='__main__':
	jar = './stanford-ner-4.0.0/stanford-ner.jar'
	model = './stanford-ner-4.0.0/classifiers/english.all.3class.distsim.crf.ser.gz'

	ner_tagger = StanfordNERTagger(model, jar, encoding='utf8')
	tags = ['PERSON', 'LOCATION','ORGANIZATION']
	punc = ['.',',',':',';','"','!','?','%']

	query_file_path = './assignment1/topics.51-100'
	
	solve(query_file_path, ner_tagger)