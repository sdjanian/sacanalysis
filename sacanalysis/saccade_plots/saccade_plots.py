import numpy as np
from .plotting_class import Plotting_class
import matplotlib.pyplot as plt
import matplotlib as mpl
import tqdm
import os


Plotting_class = Plotting_class(colors="GazeCom")

def plotRankedSaccades(saccades,average_saccade,ranked_residual,save_dir_sub,saccade_pos_col="",
                       sup_title="",_nrow=8,_ncol=3,_figsize=(6,15)):
        if not os.path.isdir(save_dir_sub):
            os.makedirs(save_dir_sub)
        ii = 0
        plt.ioff()
        mpl.use('Agg')

        # - 1 to nrow and ncol because we add the average saccade on each page
        number_of_pages = np.arange(int(np.ceil(len(ranked_residual)/(_nrow*_ncol-1))))
        for page in tqdm.tqdm(number_of_pages,leave=False,position=0,desc="Producing plots"):
            fig, ax = plt.subplots(nrows=_nrow, ncols=_ncol,figsize=_figsize)
            fig.suptitle(sup_title + " page: " + str(page+1) + ' of '+str(len(number_of_pages)), fontsize=18)
            for ir,row in enumerate(ax):
                for ic,col in enumerate(row):
                    if (ir==0) & (ic==0):
                        col.plot(average_saccade.index,average_saccade)
                        col.set_title("Average saccade")
                    else:
                        if ii>=len(ranked_residual):
                            col.axis('off')
                        else:
                            sub_df = saccades[saccades["unique_saccade_number"]==ranked_residual["unique_saccade_number"].iloc[ii]]
                            col.plot(sub_df["norm_time"],sub_df[saccade_pos_col])    
                            subtitle = "Rank " + str(ii+1) + " of " + str(len(ranked_residual)) +"\n"+str(np.round(ranked_residual[sup_title].iloc[ii],5))
                            col.set_title(subtitle)
                            ii = ii +1
            plt.tight_layout(rect=[0, 0.03, 1, 0.95])
            plt.savefig(os.path.join(save_dir_sub,"saccade_rank_page_"+str(page+1)+".pdf"))
            plt.close() 

def plotRankedSaccadesArticle(saccades,average_saccade,ranked_residual,save_dir_sub,saccade_pos_col="",
                       sup_title="",metric="",_nrow=8,_ncol=3,_figsize=(6,15),num_of_ranks=0,list_of_ranks_to_plot=[]):

        ii = 0
        plt.ioff()
        mpl.use('Agg')

        # - 1 to nrow and ncol because we add the average saccade on each page

        fig, ax = plt.subplots(nrows=_nrow, ncols=_ncol,figsize=_figsize)
        fig.suptitle(sup_title, fontsize=18)
        for ir,row in enumerate(ax):
            for ic,col in enumerate(row):
                if (ir==0) & (ic==0):
                    col.plot(average_saccade.index,average_saccade)
                    col.set_title("Average saccade")
                else:
                    if ii>=len(ranked_residual):
                        col.axis('off')
                    else:
                        sub_df = saccades[saccades["unique_saccade_number"]==ranked_residual["unique_saccade_number"].iloc[ii]]
                        col.plot(sub_df["norm_time"],sub_df[saccade_pos_col])    
                        subtitle = "Rank " + str(list_of_ranks_to_plot[ii]) + " of " + str(num_of_ranks) +"\n"+str(np.round(ranked_residual[metric].iloc[ii],2))
                        col.set_title(subtitle)
                        ii = ii +1
        fig.text(0.5, -0.01, 'Duration (ms)', ha='center',fontsize=12)
        fig.text(-0.01, 0.5, 'Position (deg)', va='center', rotation='vertical',fontsize=12)
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        #plt.close()         
        
def plotRankedSaccadesAndDistributionsArticle(saccades,average_saccade,ranked_residual,save_dir_sub,saccade_pos_col="",
                       sup_title="",metric="",_nrow=8,_ncol=3,_figsize=(6,15),num_of_ranks=0,list_of_ranks_to_plot=[]):

        ii = 0
        plt.ioff()
        mpl.use('Agg')

        # - 1 to nrow and ncol because we add the average saccade on each page
        fig = plt.figure(figsize=_figsize)
        fig.suptitle(sup_title, fontsize=18)
        
        grid_size = (_nrow,_ncol)
        axlist = []
        axlist.append(plt.subplot2grid(grid_size,(0,0)))
        axlist[0].plot(average_saccade.index,average_saccade)
        axlist[0].set_title("Average saccade")
        
        axlist.append(plt.subplot2grid(grid_size,(0,1),colspan=3))
        axlist[-1].set_title("Score histogram")

        for row in np.arange(1,_nrow):
            for col in np.arange(0,_ncol):
                axlist.append(plt.subplot2grid(grid_size,(row,col)))
                sub_df = saccades[saccades["unique_saccade_number"]==ranked_residual["unique_saccade_number"].iloc[ii]]
                axlist[-1].plot(sub_df["norm_time"],sub_df[saccade_pos_col])                
                subtitle = "Rank " + str(list_of_ranks_to_plot[ii]) + " of " + str(num_of_ranks) +"\n"+str(np.round(ranked_residual[metric].iloc[ii],2))
                axlist[-1].set_title(subtitle)
                ii = ii +1
        
        fig.text(0.5, -0.01, 'Duration (ms)', ha='center',fontsize=12)
        fig.text(-0.01, 0.5, 'Position (deg)', va='center', rotation='vertical',fontsize=12)
        plt.tight_layout(rect=[0, 0.03, 1, 0.95]) 
        return axlist              
        

if __name__ == "__main__":
    None            