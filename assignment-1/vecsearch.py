import pandas as pd
import numpy as np 
from tqdm import tqdm
from nltk.tag.stanford import StanfordNERTagger
from nltk.stem import SnowballStemmer
from preprocess_lib import PreProcess
from query_search import QuerySearch
from tqdm import tqdm
import os

tags = {'PERSON': 'P:', 'LOCATION': 'L:','ORGANIZATION': 'O:'}
punc = ['.',',',':',';','"','!','?','%','(',')']

def solve(file_path, sno, ner_tagger, processObj, queryObj, num_docs_retrieval=2):
	'''
		1. Lemmetize query and add * at the end. much more efficient than doing it for whole corpus of training
		2. dont merge same tags in queries, rather add * at the end of each. Ex org_cbs* org_news*
	'''

	fd = open(file_path, 'r')
	try:
		os.system('rm resultfile')
	except:
		pass
	
	out = open("resultfile", "a")
	
	cnt = 0
	qid=''
	for line in tqdm(fd):
		if line.startswith('<num>'):
			# qid = line.split('<num> Number:')[-1].strip()
			qid = line.split('<num>')[-1].strip().split('Number:')[-1].strip()
		if line.startswith('<title>'):
			query_line = line.split(': ')[-1].strip()
			
			tokenized_text = processObj.run_on(query_line,return_tokens=True, case_senstivity=True)
			classified_text = ner_tagger.tag(tokenized_text)
			
			res = []
			for j in classified_text:
				if j[1] in tags:
					res.append(tags[j[1]]+j[0].lower()+'*')
				elif (j[0] not in punc):
					res.append(sno.stem(j[0].lower())+'*')
			best_k_docs = queryObj.search_queries(res, num_docs_retrieval=num_docs_retrieval)
			for i in range(num_docs_retrieval):
				out.write(str(qid)+' Q0 '+str(best_k_docs[i][0])+' 1 '+str(int(best_k_docs[i][1])+(num_docs_retrieval)-i)+' STANDARD\n')
	out.close()
	fd.close()			


if __name__=='__main__':
	jar = './stanford-ner-4.0.0/stanford-ner.jar'
	model = './stanford-ner-4.0.0/classifiers/english.all.3class.distsim.crf.ser.gz'

	ner_tagger = StanfordNERTagger(model, jar, encoding='utf8')
	sno = SnowballStemmer('english')

	queryObj = QuerySearch('./posting_list.json', './data.csv')
	
	query_file_path = './assignment1/topics.51-100'
	preprocessObj = PreProcess()
	k = 10
	solve(query_file_path, sno, ner_tagger, preprocessObj, queryObj, num_docs_retrieval=k)