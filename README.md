# Information-Retreival-Assignments

## Process:
    - Create folders and subfolders ./text/TaggedTrainingAP/ in root dir
    - preprocess.py: Just for preprocessing any line of text.
    - run grab_text.sh (creates only text out of files)
    (-) run create_processed_data.ipynb: output:- data.csv
    - run create_processed_data.py: input:- folder with files containing only <TEXT> tags files, output:- data.csv
    - run create_posting_list.py: output:- posting_list.json, which is dictionary of inverted index
    - tfidf.py: Helper library to parse json dump of listing and calculate tfidf for any query(word, docid)
    - query_search.py: 
        - Input: posting_list.json, data.csv(containing only texts field of all files in all docs)
        - Output: tfidf of most relevant doc
## Things to remember:
    - <TEXT></TEXT> might be empty. No need to index those files.
    - Merge sequence of same tags such as <NAME>.
    - Queries file: topics.51-100. Contains 50 individual topics. Choose text from only <title> tag.
## To-Do:
    - Create virtual environment at last.
    - Remove stopwords, do lemmetization
    - Do encoding and compress the processes data set time execution
    - Remove more frequent words
