from urllib2 import Request, urlopen, URLError
import json
import re
from bs4 import BeautifulSoup
import sys
reload(sys)

sys.setdefaultencoding('utf-8')

patt = re.compile("[^\t]+")

def sportsFilter(tagList):
	patt = r"[a-z, ]?sport"
	for tag in tagList:
		if re.match(patt, tag, re.IGNORECASE):
			return True
	return False

class NewsObject:
	def __init__(self, title, date, content):
		self.title = title
		self.date = date
		self.content = content
		self.tags = []

#keyword to add query 
keyword=raw_input("keyword-->")
head = "http://content.guardianapis.com/search?"
query = "q=" + keyword
apiKey = "&api-key=" + "ed0d3545-4b8f-4bbf-862a-5098ac74c2c0"
addLater = "&tag=politics/politics&from-date=2014-01-01&api-key=ed0d3545-4b8f-4bbf-862a-5098ac74c2c0')"
request = Request(head + query + apiKey)

try:
    response = urlopen(request)
    jsonObject = json.loads(response.read())

except URLError, e:
    print 'Got an error code:', e

results = jsonObject['response']['results']
print "The Number of objects in this list are " + str(len(results))
ls = []
jsonToWrite=""
count =1
for obj in results:
		try:
			html = BeautifulSoup(urlopen(Request(obj['webUrl'])).read())
			print obj['webUrl']
			
		except URLError, e:
			print "Problem with the url or with tags"
			continue

		if (html.find(attrs={"name":"keywords"})):
			articleTags = html.find(attrs={"name":"keywords"})['content'].split(',')
		else:
			continue

		if sportsFilter(articleTags):
			continue

		contentOfMainArticle = html.find('div', itemprop='articleBody')
		completeTextInMainArticle = ""

		for paraInMainArticle in contentOfMainArticle.findAll('p'):
			for textFragmentInMainArticle in paraInMainArticle.findAll(text=True):
				completeTextInMainArticle +=  textFragmentInMainArticle

		dictionaryObject = NewsObject(obj["webTitle"], obj["webPublicationDate"], completeTextInMainArticle)
		dictionaryObject.tags = articleTags
		dictionaryObject = dictionaryObject.__dict__
		jsonToWrite += json.dumps(dictionaryObject)+","
		
		dataFile = open('RawNewsArticles.txt', 'a')
		dataFile.write(jsonToWrite)
		dataFile.close()
			
		print "Loop executed"