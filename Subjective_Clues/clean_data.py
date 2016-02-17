import nltk
import json
import pandas as pd
import re
import csv
from nltk.corpus import stopwords
with open('ObjectiveNews1.json') as data_file:    
     data = json.load(data_file)

# sentences = pd.read_csv("SubjectiveNews1.json", sep="\t")
# print sentences

unicodeToAsciiMap = {u'\u2019':"'", u'\u2018':"`", }

def unicodeToAscii(inStr):
    try:
        return str(inStr)
    except:
        pass
    outStr = ""
    for i in inStr:
        try:
            outStr = outStr + str(i)
        except:
            if unicodeToAsciiMap.has_key(i):
                outStr = outStr + unicodeToAsciiMap[i]
            else:
                outStr = outStr + "_"
    return outStr



def clean_data():
	content_all=""
	for i in range(1,len(data)):
		content_all=content_all + " " + data[i]['value']
	content_all=unicodeToAscii(content_all)
	tokens=nltk.word_tokenize(content_all)
	#--------- remove stopwords----------#
	letters_only = re.sub("[^a-zA-Z]", " ", content_all) 
	words = letters_only.lower().split() 
	stops = set(stopwords.words("english"))
	meaningful_words = [w for w in words if not w in stops]
	meaningful_words = [w for w in meaningful_words if len(w)>2]
	print meaningful_words
	with open('ObjectiveNews.csv', 'wb') as f:
		writer = csv.writer(f)
		for val in meaningful_words:
			writer.writerow([val])



clean_data()
