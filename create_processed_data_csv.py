from tqdm import tqdm
from preprocess_lib import PreProcess
import os
from os import listdir
from os.path import isfile, join
import pandas as pd

text_dir = './text/TaggedTrainingAP/'

processObj = PreProcess()

all_text_files = [f for f in listdir(text_dir) if isfile(join(text_dir, f))]

files_dict = {} 
for file in tqdm(all_text_files):
    fd = open(join(text_dir,file))
    cnt=0
    for index,line in enumerate(fd):
        if(line=='<TEXT>\n'):
            continue
        if(line=='</TEXT>\n'):
            cnt+=1
        line = processObj.run_on(line)
        files_dict[file.upper().split('_')[0]+'-'+str(cnt)]=line
    fd.close()

df = pd.DataFrame.from_dict(files_dict,orient='index')
df.to_csv('./data.csv')