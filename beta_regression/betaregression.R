source('/home/leelab/PycharmProjects/BioInfoPipeLine/BetaRegression/ZIBseq.R')
args = commandArgs(trailingOnly = TRUE)
d = read.csv(args[1])
num_features = dim(d)[2]
d_split = split(d,d$group)
result = c()

for(i in seq(1:length(d_split))){
    for(j in seq(1:length(d_split))){
        if(i<j){
            df = rbind(d_split[[i]], d_split[[j]])
            data = df[,c(2:num_features)]
            outcome = (df[,c(1:1)])
            levels = levels(factor(df$group))
            data
            outcome
            result = cbind(result, ZIBseq(data = data, levels = levels, outcome = outcome, transform = T))
        }
    }
}

final_result = data.frame()

for(i in seq(1:length(result[1,]))){
    sigFeatures = result[,i]$sigFeature
    groups = result[,i]$levels
    pValues = result[,i]$pvalues
    qValues = result[,i]$qvalues
    final_result = rbind(final_result, data.frame(groups=toString(groups), sigFeatures=toString(sigFeatures),pValues=toString(pValues), qValues= toString(qValues)))
}

write.csv(final_result, args[2])

