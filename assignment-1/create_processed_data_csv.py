from tqdm import tqdm
from preprocess_lib import PreProcess
import os
from os import listdir
from os.path import isfile, join
import pandas as pd

data_dir = './assignment1/TaggedTrainingAP'
all_files = [f for f in listdir(data_dir) if isfile(join(data_dir, f))]
processObj = PreProcess()
text_dict = {}

for file in tqdm(all_files):
	fd = open(join(data_dir, file))
	doc_no = ''
	text_in_next = False
	for line in fd:
		if('<DOCNO>' in line):
			doc_no = line.split('<DOCNO>')[-1].split('</DOCNO>')[0].strip()
		elif ('<TEXT>' in line):
			text_in_next = True
		elif (text_in_next):
			text_in_next = False
			line = processObj.run_on(line)
			text_dict[doc_no] = line
	fd.close()

df = pd.DataFrame.from_dict(text_dict,orient='index')
df.to_csv('./data.csv')
del df