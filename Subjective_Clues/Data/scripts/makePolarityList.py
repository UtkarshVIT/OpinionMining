import json
import csv
import re
import sys
reload(sys)

sys.setdefaultencoding('utf-8')

patt = re.compile("[^\t]+")

class PolarityObject:
	def __init__(self, mpqatType, mpqaPolarity, word):
		self.mpqaType = mpqaType
		self.mpqaPolarity = mpqaPolarity
		self.word = word

rawNewsFile = open('RawNewsArticles.txt')
rawNewsdata = rawNewsFile.read()
rawNewsFile.close()

fileSubjectiveNews = open('ObjectivePolarityNews', 'a')

with open('subjclueslen1polar.csv', 'rb') as f:
	reader = csv.reader(f)
	for row in reader:
		obj = patt.findall(row[0]) + patt.findall(row[1])
		obj += obj[4].split(" ")
		del obj[4]
		obj.append(rawNewsdata[int(obj[1]): int(obj[2])])
		
		mpqaType = str(obj[4].split("=")[1])
		mpqaType = mpqaType[1:-1]

		mpqaPolarity = str(obj[5].split("=")[1])
		mpqaPolarity = mpqaPolarity[1:-1]
		
		dictionaryObject = PolarityObject(mpqaType, mpqaPolarity, obj[6]).__dict__
		print dictionaryObject
		jsonToWrite = json.dumps(dictionaryObject)+","
		print jsonToWrite
		fileSubjectiveNews.write(jsonToWrite)

fileSubjectiveNews.close()