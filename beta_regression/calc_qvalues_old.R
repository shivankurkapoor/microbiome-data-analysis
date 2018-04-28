calc_qvalues <- function(pvalues)
{
nrows = length(pvalues);

# create lambda vector
lambdas <- seq(0,0.95,0.01);
pi0_hat <- array(0, dim=c(length(lambdas)));

# calculate pi0_hat
for (l in 1:length(lambdas)){ # for each lambda value
count = 0;
for (i in 1:nrows){ # for each p-value in order
if (pvalues[i] > lambdas[l]){
count = count + 1;
}
pi0_hat[l] = count/(nrows*(1-lambdas[l]));
}
}

f <- unclass(smooth.spline(lambdas,pi0_hat,df=3));
f_spline <- f$y;
pi0 = f_spline[length(lambdas)];   # this is the essential pi0_hat value

# order p-values
ordered_ps <- order(pvalues);
pvalues <- pvalues;
qvalues <- array(0, dim=c(nrows));
ordered_qs <- array(0, dim=c(nrows));

ordered_qs[nrows] <- min(pvalues[ordered_ps[nrows]]*pi0, 1);
for(i in (nrows-1):1) {
    p = pvalues[ordered_ps[i]];
new = p*nrows*pi0/i;

ordered_qs[i] <- min(new,ordered_qs[i+1],1);
}

# re-distribute calculated qvalues to appropriate rows
for (i in 1:nrows){
    qvalues[ordered_ps[i]] = ordered_qs[i];
}

################################
# plotting pi_hat vs. lambda
################################
plot(lambdas,pi0_hat,xlab=expression(lambda),ylab=expression(hat(pi)[0](lambda)),type="p");
lines(f);
list(pi0=pi0, qvalues=qvalues, pvalues=pvalues)

return (qvalues);
}