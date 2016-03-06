pre_process=function()
{
exclude=exclude_tags()
word_database=read.csv("Data/csv/inquireraugmented.csv")
#Convert toupper to match general Inquirer Input
word_database$Entry=toupper(word_database$Entry)
#Delete source col
word_database=word_database[-1,c(-2,-185,-186)]
#Add extra col for storing filled tags associated with words
word_database[]=lapply(word_database,as.character)
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
common_words_subj=setdiff(common_words_subj,del_words)
common_words_obj=setdiff(common_words_obj,del_words)
# print("common words_subj")
# print (common_words_subj)
# print("common words_obj")
# print (common_words_subj)

#Create a temp data frame to store tags related to each word
temp_subj=word_database[1,]
temp_subj$type=0
#loop to get tags of words present in news articles(sentences)

for (i in 1:length(common_words_subj))
{
  
  temp_subj[i,]=word_database[word_database$Entry==common_words_subj[i],]
 
  for(j in 2:(ncol(temp_subj)-1) )
  { 
    
    if(temp_subj[i,j]!=""){temp_subj[i,j]="yes"}
    else
    {temp_subj[i,j]="no"
      }

  }
  
  temp_subj[i,]$type="Subjective"
  
}
temp_obj=word_database[1,]
temp_obj$type=0
View(temp_subj)
for (i in 1:length(common_words_obj))
{

  temp_obj[i,]=word_database[word_database$Entry==common_words_obj[i],]
  for(j in 2:(ncol(temp_obj)-1) )
  { temp_obj[,j]=as.character(temp_obj[,j])
    if(temp_obj[i,j]!=""){temp_obj[i,j]="yes"}else{temp_obj[i,j]="no"}
   
    
  }
  
  temp_obj[i,]$type="Objective"
  
}
temp=rbind(temp_subj,temp_obj)
temp=temp[,-1]
temp[]=lapply(temp,as.factor)
temp
}
