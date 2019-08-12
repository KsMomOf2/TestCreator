mcprocessanswers <- function(ID,versions,answers,path=getwd()) {
 
tol <- .Machine$double.eps^0.5 
if(! is.numeric(answers)) stop("non-numeric value(s) in answers, mcprocessanswers stopped") 
if(min(answers > tol)==0) stop("non-positive value(s) in answers, mcprocessanswers stopped") 
if(min(abs(answers - round(answers)) < tol)==0) stop("non-integer value(s) in answers, mcprocessanswers stopped") 
if(! is.numeric(versions)) stop("non-numeric value(s) in versions, mcprocessanswers stopped") 
if(min(versions > tol)==0) stop("non-positive value(s) in versions, mcprocessanswers stopped") 
if(min(abs(versions - round(versions)) < tol)==0) stop("non-integer value(s) in versions, mcprocessanswers stopped") 
if(min(versions-4< tol)==0) stop("value(s) in versions too large, maximum possible value is 4, mcprocessanswers stopped") 
 
questiondictionary=list(c(2,1),c(1,2),c(2,1),c(1,2))
 
randomizedanswersdictionary=list(
