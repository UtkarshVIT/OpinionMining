  #param =("lift","support","confidence")
  #exclude- categories to exclude out of 186 categories present in general inquirer
  #load libraries for apriori
  library("arules")
  library("arulesViz")
  #Read from General Inquirer
  word_database=read.csv("inquireraugmented.csv")
  #Convert toupper to match general Inquirer Input
  word_database$Entry=toupper(word_database$Entry)
  #Delete source col
  word_database=word_database[,c(-2,-185,-186)]
  #Add extra col for storing filled tags associated with words
  word_database$tags=0
  #Don't forget to exclude # words
  #Read sentences file from news articles
  sentences=read.csv("SubjectiveNews.csv",header= F)
  #Give name to col containing words
  colnames(sentences)="words"
  #Convert toupper to match inquirer dataset
  sentences$words=toupper(sentences$words)
  #Find common words
  common_words=intersect(sentences$words,word_database$Entry)
  #del words with tags in exclude
  del_words=c()
  for (i in 1:length(exclude))
  {
    del_words=append(del_words,word_database[word_database[exclude[i]]!="",]$Entry)
  }
  del_words=del_words[complete.cases(del_words)]
  print (del_words)
  common_words=setdiff(common_words,del_words)
  print("common words")
  print (common_words)
  #Create a temp data frame to store tags related to each word
  temp_subj=word_database[1,]
  #loop to get tags of words present in news articles(sentences)
  for (i in 2:length(common_words))
  {
    tags=c()
    temp_subj[i,]=word_database[word_database$Entry==common_words[i],]
    for(j in 2:(ncol(temp_subj)-1) )
    { 
      if(temp_subj[i,j]!="")
      {
        tags=append(tags,colnames(temp_subj)[j])
      }
      
    }
    tags=append(tags,"Subjective")
    temp_subj[i,]$tags=list(tags)
    #print (temp[i,]$tags)
  }
  View(temp_subj)
#   convert tags into transactions
  trans=as(temp$tags,"transactions")
  #extract apriori rules
  rules = apriori(trans, parameter=list(support=0.01, confidence=0.5))
  #display apriori rules by param - "lift", "support", "confidence"
  inspect(head(sort(rules, by=param),50))
#   