from urllib2 import Request, urlopen, URLError
import json
import re
from bs4 import BeautifulSoup
import sys
reload(sys)

#set deafult encoding to utf-8 for file writing
sys.setdefaultencoding('utf-8')

patt = re.compile("[^\t]+")

#function to remove articles having sports tags(subjectivity filter)
def sportsFilter(tagList):
	patt = r"[a-z, ]?sport"
	for tag in tagList:
		if re.match(patt, tag, re.IGNORECASE):
			return True
	return False

#class to define json format for writing news articles
class NewsObject:
	def __init__(self, title, date, content):
		self.title = title
		self.date = date
		self.content = content
		self.tags = []

#query parameters
head = "http://content.guardianapis.com/search?"
queryList = ["antarctica", "belarus"]
apiKey = "&api-key=" + "ed0d3545-4b8f-4bbf-862a-5098ac74c2c0"

for country in queryList:
	query = "q="+country
	request = Request(head + query + apiKey)

	# check if we the api reuturns any result
	try:
		#request the API
	    response = urlopen(request)

	    #decode the returned links in json format
	    jsonObject = json.loads(response.read())

	except URLError, e:
	    print 'Got an error code:', e

	#results list contains the links to the news articles and their meta data
	results = jsonObject['response']['results']
	
	print "The Number of objects in " + country + " list are " + str(len(results))
	
	ls = []
	jsonToWrite=""
	
	for obj in results:
			try:
				#fetch the url if it exists
				html = BeautifulSoup(urlopen(Request(obj['webUrl'])).read(),'lxml')
				print obj['webUrl']
				
			except URLError, e:
				print "Problem with the url or with tags"
				continue

			#check if the keywords of the article are present in the source code 
			if (html.find(attrs={"name":"keywords"})):
				articleTags = html.find(attrs={"name":"keywords"})['content'].split(',')
			else:
				continue

			#skip if its a sports article	
			if sportsFilter(articleTags):
				continue

			#get the html content in the main article 
			contentOfMainArticle = html.find('div', itemprop='articleBody')
			completeTextInMainArticle = ""

			#condition to skip if the page does not contain the specified div tag
			if contentOfMainArticle == None:
				continue

			#find the contents of the <p> tag in main article 
			for paraInMainArticle in contentOfMainArticle.findAll('p'):
				#get only pure text in main article(remove content of other tags)
				for textFragmentInMainArticle in paraInMainArticle.findAll(text=True):
					completeTextInMainArticle +=  textFragmentInMainArticle

			#create a dictionary object of the article content 
			dictionaryObject = NewsObject(obj["webTitle"], obj["webPublicationDate"], completeTextInMainArticle)
			dictionaryObject.tags = articleTags
			dictionaryObject = dictionaryObject.__dict__
			
			#write a json object with the dictionary object
			jsonToWrite += json.dumps(dictionaryObject)+","
			
			#write data to a file
			dataFile = open('RawNewsArticles.txt', 'a')
			dataFile.write(jsonToWrite)
			dataFile.close()