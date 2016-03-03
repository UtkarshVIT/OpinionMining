apriori_report=function(data,param,type_file)
{
  #   convert tags into transactions
  trans=as(temp$tags,"transactions")
  #extract apriori rules
  rules = apriori(trans, parameter=list(support=0.01, confidence=0.5))
  #display apriori rules by param - "lift", "support", "confidence"
  output_file=paste("Reports/",type_file,"_",param,sep="")
  sink(output_file)
  inspect(head(sort(rules, by=param),50))
  sink()
}