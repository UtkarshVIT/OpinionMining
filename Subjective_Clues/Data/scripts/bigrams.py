<<<<<<< HEAD
# _*_ coding:utf-8 _*_
=======
>>>>>>> 17db5338a74e41ab93db59d688a35465d9182831
import nltk
import json
import re
import csv
unicodeToAsciiMap = {u'\u2019':"'", u'\u2018':"`", }

"""
from nltk.collocations import *
bigram_measures = nltk.collocations.BigramAssocMeasures()
finder = BigramCollocationFinder.from_words(nltk.corpus.genesis.words('rawArticle-argentina.txt'))
finder.nbest(bigram_measures.pmi, 10)
"""

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


f = file('../json/SubjectiveNews(sent_rule)')
string = f.read()
object1 = json.loads(string)
<<<<<<< HEAD
print object1[0]['value']
=======
>>>>>>> 17db5338a74e41ab93db59d688a35465d9182831
string = unicodeToAscii(object1[0]['value'])
print string
