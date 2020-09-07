#import os
#os.environ["R_HOME"] = r"C:\Users\FQ73OO\AppData\Local\Continuum\anaconda3\envs\generel\lib\R"
import rpy2.robjects.packages as rpackages
import rpy2.robjects as robjects
import numpy as np
import pandas as pd
import rpy2.robjects.numpy2ri
rpy2.robjects.numpy2ri.activate()
utils = rpackages.importr('utils')
#r_lib_path = "C:/Users/FQ73OO/AppData/Local/Continuum/anaconda3/envs/generel/lib/R/library" # AAU laptop
r_lib_path = "C:/Users/Shaggy/Anaconda3/envs/generel/Lib/R/library" # Home computer

madness = rpackages.importr('madness',lib_loc=r_lib_path)
mixAK = rpackages.importr('mixAK',lib_loc=r_lib_path)
dplyr = rpackages.importr('dplyr',lib_loc=r_lib_path)

# Needs to be installed before this function can run.
#utils.install_packages('madness',contriburl="https://cran.r-project.org/web/packages/madness/index.html")
#utils.install_packages('mixAK')
#utils.install_packages('dplyr')

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
    print(rjmcmc(y))      
    
    
    df  = pd.read_json("F:/OneDrive - Aalborg Universitet/Eye_tracking/GazeComCritique.git/output2/scores_40ms.json")
    vectors = df["vector"]
    vector = np.expand_dims(np.array(vectors.iloc[14]),axis=1)
    #print(rjmcmc(vector))      
    print(rjmcmc_output(vector)) 
    print(rjmcmc_output(not_working)) 
    df_sub = df.iloc[0:5]
    bf_values = df_sub["vector"].apply(lambda x: rjmcmc_output(np.expand_dims(np.array(x),axis=1)))

    from scipy.stats import kurtosis, skew
    skew_values = df_sub["vector"].apply(lambda x: skew(x))
    kurtosis_values = df_sub["vector"].apply(lambda x: kurtosis(x))
    