import nltk
import json
import pandas as pd
import re
import csv
from nltk.corpus import stopwords

#Read input json file for cleaning
input_file=raw_input("input file--->")
#Setting path for input file
input_file="Data/json/" + input_file
with open(input_file) as data_file:    
     data = json.load(data_file)



#-----------Resolve encoding problem------------------------------------------#
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


#-------------Clean data-tokenize-filter--------------------------------------#
def clean_data():
	content_all=""
	#---------extract text of news articles from given JSON and merge all-----#
	for i in range(1,len(data)):
		content_all=content_all + " " + data[i]['value']
	content_all=unicodeToAscii(content_all)
	print content_all
	tokens=nltk.word_tokenize(content_all)
	#---------remove stopwords-----------------------------------------------#
	letters_only = re.sub("[^a-zA-Z]", " ", content_all) 
	words = letters_only.lower().split() 
	stops = set(stopwords.words("english"))
	meaningful_words = [w for w in words if not w in stops]
	#exclude one letter or two letter words that occur due to parsing issues
	meaningful_words = [w for w in meaningful_words if len(w)>2]
	print meaningful_words
	#Name of csv file for output
	output_file=raw_input("output_file--->")
	#Setting path for output file
	output_file="Data/csv/" + output_file + ".csv"
	with open(output_file, 'wb') as f:
		writer = csv.writer(f)
		for val in meaningful_words:
			writer.writerow([val])



clean_data()

