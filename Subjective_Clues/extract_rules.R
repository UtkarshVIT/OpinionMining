  #param =("lift","support","confidence")
  #exclude- categories to exclude out of 186 categories present in general inquirer
  #load exclude and param using input()
  exclude=exclude_tags()
  param=readline("param-->")
  #load libraries for apriori
  library("arules")
  library("arulesViz")
  #Read from General Inquirer
  word_database=read.csv("Data/csv/inquireraugmented.csv")
  #Convert toupper to match general Inquirer Input
  word_database$Entry=toupper(word_database$Entry)
  #Delete source col
  word_database=word_database[,c(-2,-185,-186)]
  #Add extra col for storing filled tags associated with words
  word_database$tags=0
  #Don't forget to exclude # words
  #Read sentences file from news articles
  type_file=readline("type-->")
  name_subj=paste("Data/csv/","SubjectiveNews_",type_file,".csv",sep="")
  name_obj=paste("Data/csv/","ObjectiveNews_",type_file,".csv",sep="")
  sentences_subj=read.csv(name_subj,header= F)
  sentences_obj=read.csv(name_obj,header= F)
  #Give name to col containing words
  colnames(sentences_subj)="words"
  colnames(sentences_obj)="words"
  #Convert toupper to match inquirer dataset
  sentences_subj$words=toupper(sentences_subj$words)
  sentences_obj$words=toupper(sentences_obj$words)
  #Find common words
  common_words_subj=intersect(sentences_subj$words,word_database$Entry)
  common_words_obj=intersect(sentences_obj$words,word_database$Entry)
  #del words with tags in exclude
  del_words=c()
  for (i in 1:length(exclude))
  {
    del_words=append(del_words,word_database[word_database[exclude[i]]!="",]$Entry)
  }
  del_words=del_words[complete.cases(del_words)]
  print (del_words)
  common_words_subj=setdiff(common_words_subj,del_words)
  common_words_obj=setdiff(common_words_obj,del_words)
  print("common words_subj")
  print (common_words_subj)
  print("common words_obj")
  print (common_words_subj)
  
  #Create a temp data frame to store tags related to each word
  temp_subj=word_database[1,]
  #loop to get tags of words present in news articles(sentences)
  for (i in 2:length(common_words_subj))
  {
    tags=c()
    temp_subj[i,]=word_database[word_database$Entry==common_words_subj[i],]
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
  for (i in 2:length(common_words_obj))
  {
    tags=c()
    temp_obj[i,]=word_database[word_database$Entry==common_words_obj[i],]
    for(j in 2:(ncol(temp_obj)-1) )
    { 
      if(temp_obj[i,j]!="")
      {
        tags=append(tags,colnames(temp_obj)[j])
      }
      
    }
    tags=append(tags,"Objective")
    temp_obj[i,]$tags=list(tags)
    #print (temp[i,]$tags)
  }
  temp=rbind(temp_subj,temp_obj)
  View(temp)
  apriori_report(temp,param,type_file)
  
#   