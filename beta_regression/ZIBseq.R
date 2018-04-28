ZIBseq=function(data,outcome,levels,transform=F,alpha=1) {

    library(gamlss)
    library(gamlss.dist)
    library(MASS)
    source("/home/leelab/PycharmProjects/BioInfoPipeLine/BetaRegression/calc_qvalues_new.R")

    genodata=data     ## data is a matrix with size n*p, where n is the samoke size and p is the number of features

    ## must contain the column names
    Y=outcome        ## Y is a vector with length n

    useF=which(colSums(genodata)>2*dim(genodata)[1])    ## remove features with totle counts less than 2 times sample size

    X=genodata[,useF]

    ST=rowSums(X)   ## calculation the sample total

    P=dim(X)[2]


    ##-------------------------------------------------------------------------------------


    beta=matrix(data=NA,P,2)
    propMat = matrix(data=NA,dim(X)[1], dim(X)[2])

    for (i in 1:P)

    {x.prop=X[,i]/ST

    if (transform==T)

    {x.prop=sqrt(x.prop) }

    propMat[,i] = x.prop
    bereg=gamlss(x.prop~Y,family=BEZI(sigma.link="identity"),sigma.fo=~(ST-1),trace=FALSE,control = gamlss.control(n.cyc = 100))

    out=summary(bereg)

    beta[i,]=out[2,c(1,4)]}      ## get all the coefficients and P values in beta regression

    pvalues=beta[,2]

    qvalues=calc_qvalues(pvalues)

    sig=which(qvalues<=alpha)

    sigFeature=colnames(X)[sig]

    return(list(sigFeature=sigFeature,useFeature=P,qvalues=qvalues, pvalues=pvalues, propMat = propMat,levels = c(levels)))
}

