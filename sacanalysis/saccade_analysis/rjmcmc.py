import rpy2.robjects.packages as rpackages
import rpy2.robjects as robjects
import numpy as np
import rpy2.robjects.numpy2ri
from rpy2.rinterface import RRuntimeError

def importr_tryhard(packname):
    try:
        rpack = rpackages.importr(packname)
    except RRuntimeError:
        print("Installing R package ",packname)
        utils.install_packages(packname)
        rpack = rpackages.importr(packname)
    return rpack

rpy2.robjects.numpy2ri.activate()
utils = rpackages.importr('utils')
utils.chooseCRANmirror(ind=1)
list_of_packages = ["madness","mixAK","dplyr"]

for package in list_of_packages:
    importr_tryhard(package)
    

rjmcmc = robjects.r('''
mcmc_func <- function(y){
keep=2000
Floor<-floor(min(y))
Ceiling<-ceiling(max(y))
a=min(y); b=max(y); ra=b-a; a=a-ra/4; b=b+ra/4
gp=100; x=seq(a,b,(b-a)/(gp-1)); d=x
xi=0.5*(a+b)
ra_squared=ra^2
ce=1/ra^2
d=rep(0,gp); modes=rep(0,keep)
r=NMixMCMC(y,scale=list(shift=0,scale=1),
           prior=list(priorK="tpoisson",Kmax=5,lambda=1,xi=0.5*(a+b),ce=1/ra^2),
           nMCMC=c(burn=200,keep=keep,thin=10,info=100),keep.chains=TRUE)
i=0
for(j in 1:keep){
  kt=r$K[j]; w=r$w[(i+1):(i+kt)]; mu=r$mu[(i+1):(i+kt)]; si=sqrt(r$Sigma[(i+1):(i+kt)])
  for(k in 1:gp){d[k]=sum(w*dnorm(x[k],mu,si))}
  for(k in 3:gp){if(d[k-2]<d[k-1]){if(d[k-1]>d[k]){modes[j]=modes[j]+1}}}
  i=i+kt; if(modes[j]==0){modes[j]=1}
}
ktot=max(r$K); mc=matrix(0,ncol=2,nrow=ktot)
for(k in 1:ktot){mc[k,1]=sum(r$K==k)/keep; mc[k,2]=sum(modes==k)/keep}
rownames(mc)=1:max(r$K); colnames(mc)=c("P(comps)","P(modes)")
BF_for_GT_1_mode<-(19/(sum(modes==1)/(keep-sum(modes==1))))
return(BF_for_GT_1_mode)
}
'''
)

def rjmcmc_output(y):
    try:
        BF_value = rpy2.robjects.numpy2ri.ri2py(rjmcmc(y))[0]
    except:
        BF_value = None
    return BF_value

if __name__ == "__main__":
    working = [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3
    ,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3
    ,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,5
    ,5,5,5,5,5,5,5,5,5,5,5,5]
    
    not_working = [0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3
    ,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4
    ,4,4,5,5,5,5,5,5,5,5,5,5]
    y = np.expand_dims(np.array(working),axis=(1))
    y1 =  np.expand_dims(np.array(not_working),axis=(1))
    print(rjmcmc(y))      
    #print(rjmcmc(y1))      
