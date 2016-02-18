import json
import csv
import re
import sys
reload(sys)

sys.setdefaultencoding('utf-8')

patt = re.compile("[^\t]+")

RawNewsFile = open('RawNewsArticles.txt')
rawNewsdata = RawNewsFile.read()
RawNewsFile.close()

class PolarityObject:
	def __init__(self, key, value):
		self.key = key
		self.value = value

fileSubjectiveNews = open('ObjectiveNews(sent_rule)', 'a')

with open('sent_rule.csv', 'rb') as f:
	reader = csv.reader(f)
	for row in reader:
		obj = patt.findall(row[0])
		temp = rawNewsdata[int(obj[0].split('_')[2]): int(obj[0].split('_')[3])]
		if obj[1] == "obj":
			temp = unicode(str(temp), errors='ignore')
			dictionaryObject = PolarityObject("obj",temp.encode('utf-8')).__dict__
			jsonToWrite = json.dumps(dictionaryObject)+","
			fileSubjectiveNews.write(jsonToWrite)

fileSubjectiveNews.close()