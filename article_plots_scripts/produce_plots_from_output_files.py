# Custom libraries
from sacanalysis import plotRankedSaccades
# Python libraries
import pandas as pd
import numpy as np
import tqdm
import os
import matplotlib.backends.backend_pdf
import matplotlib.pyplot as plt
import matplotlib as mpl

import warnings
warnings.filterwarnings("ignore")


def GetCorrectTransformationToUseInAnalysis(score_column:str) -> str:
    """
        Get the correct eye movement position for a given score. 
        Output:
            str: Is either mean normalized upwards saccade or z-score tranformed of the a mean normalized upwards saccade
    """
    if any(map(lambda x: x in  score_column,["main", "velocity","x_norm_up","velocity","dip","entropy","kurtosis","skew","bfvalue"])):
        transformation_column = "x_norm_up"
    elif any(map(lambda x: x in  score_column,["x_z_trans", "flatness"])):
        transformation_column = "x_z_trans"
    return transformation_column    

def MakeFolderToSaveScoreIn(save_dir_sub:str,score_name:str):
    """
    Makes a folder if a folder doesn't exist for the subfolders.
    Output:
        str: directory for a subfolder
    """
    save_dir_sub_sub = os.path.join(save_dir_sub,score_name)
    if not os.path.isdir(save_dir_sub_sub):
        os.makedirs(save_dir_sub_sub)         
    return save_dir_sub_sub
 
def plotRankedSaccadesTest(saccades,average_saccade,ranked_residual,save_dir_sub,saccade_pos_col="",
                       sup_title="",_nrow=8,_ncol=3,_figsize=(6,15)):
        if not os.path.isdir(save_dir_sub):
            os.makedirs(save_dir_sub)
        ii = 0
        plt.ioff()
        mpl.use('Agg')
        fig_list = []
        y_min = saccades[saccade_pos_col].min()
        y_max = saccades[saccade_pos_col].max()
        # - 1 to nrow and ncol because we add the average saccade on each page
        number_of_pages = np.arange(int(np.ceil(len(ranked_residual)/(_nrow*_ncol-1))))
        for page in tqdm.tqdm(number_of_pages,leave=False,position=0,desc="Producing plots"):
            fig, ax = plt.subplots(nrows=_nrow, ncols=_ncol,figsize=_figsize)
            fig.suptitle(sup_title + " page: " + str(page+1) + ' of '+str(len(number_of_pages)), fontsize=18)
            for ir,row in enumerate(ax):
                for ic,col in enumerate(row):
                    if (ir==0) & (ic==0):
                        col.plot(average_saccade.index,average_saccade,linestyle='-', marker='o')
                        col.set_title("Average saccade")
                        col.set_ylim([y_min, y_max])
                    else:
                        if ii>=len(ranked_residual):
                            col.axis('off')
                        else:
                            sub_df = saccades[saccades["unique_saccade_number"]==ranked_residual["unique_saccade_number"].iloc[ii]]
                            col.plot(sub_df["norm_time"],sub_df[saccade_pos_col],linestyle='-', marker='o')    
                            subtitle = "Rank " + str(ii+1) + " of " + str(len(ranked_residual)) +"\n"+"Sac no. " +str(sub_df["unique_saccade_number"].iloc[0]) + "\n" +str(np.round(ranked_residual[sup_title].iloc[ii],5))
                            col.set_title(subtitle)
                            col.set_ylim([y_min, y_max])
                            ii = ii +1
            plt.tight_layout(rect=[0, 0.03, 1, 0.95])
            #plt.savefig(os.path.join(save_dir_sub,"saccade_rank_page_"+str(page+1)+".pdf"))
            #plt.close() 
            fig_list.append(fig)
        return fig_list
    
def plotRankedSaccadesVelocityHistograms(saccades,average_saccade,ranked_residual,save_dir_sub,saccade_pos_col="",
                       sup_title="",_nrow=8,_ncol=3,_figsize=(6,15)):
        if not os.path.isdir(save_dir_sub):
            os.makedirs(save_dir_sub)
        ii = 0
        plt.ioff()
        mpl.use('Agg')
        fig_list = []
        y_min = saccades[saccade_pos_col].min()
        y_max = saccades[saccade_pos_col].max()
        # - 1 to nrow and ncol because we add the average saccade on each page
        number_of_pages = np.arange(int(np.ceil(len(ranked_residual)/(_nrow*_ncol-1))))
        for page in tqdm.tqdm(number_of_pages,leave=False,position=0,desc="Producing plots"):
            fig, ax = plt.subplots(nrows=_nrow, ncols=_ncol,figsize=_figsize)
            fig.suptitle(sup_title + " page: " + str(page+1) + ' of '+str(len(number_of_pages)), fontsize=18)
            for ir,row in enumerate(ax):
                for ic,col in enumerate(row):
                    if (ir==0) & (ic==0):
                        col.plot(average_saccade.index,average_saccade,linestyle='-', marker='o')
                        col.set_title("Average saccade")
                    else:
                        if ii>=len(ranked_residual):
                            col.axis('off')
                        else:
                            sub_df = saccades[saccades["unique_saccade_number"]==ranked_residual["unique_saccade_number"].iloc[ii]]
                            velocity = ranked_residual["vector"].iloc[ii]
                            bins = np.arange(-0.5,len(sub_df)+0.5)
                            col.hist(velocity,bins = bins)    
                            subtitle = "Rank " + str(ii+1) + " of " + str(len(ranked_residual)) +"\n"+"Sac no. " +str(sub_df["unique_saccade_number"].iloc[0]) +"\n"+str(np.round(ranked_residual[sup_title].iloc[ii],5))
                            col.set_title(subtitle)
                            ii = ii +1
            plt.tight_layout(rect=[0, 0.03, 1, 0.95])
            #plt.savefig(os.path.join(save_dir_sub,"saccade_rank_page_"+str(page+1)+".pdf"))
            #plt.close() 
            fig_list.append(fig)
        return fig_list    
if __name__ == "__main__":
    """
        Runs the whole analysis in these steps:
            1. Load gazecom data with the load_gamecom class. If using other dataset or loader make sure it is the same format.
            2. Calculates a dataframe with event information containing event types, starts and ends, amplitude, duration etc.
            3. Sets variables like, chosen durations for the saccades and frequncy of eye tracker.
            4. Looping through each set of saccade duration it runs the analysis.
                a. Extract saccacdes with the chosen duration
                b. Preprocess the saccades
                c. Perform saccade analysis to get scores
                d. For each score, plot a pdf of all saccades ranked in order according to the respective score
            5. Save the results as .csv and .json.
    """
    
    
    ### Setting arrays    

    durations = [20,40,60]
    produce_plots_bool = True
    output_folder = os.path.join("..","output")
    average_saccade_list = []
    residual_df_list = []   
    save_dir = "output"

    for duration in tqdm.tqdm(durations,position=0,leave=False,desc = "Looping through files"):
        sub = str(duration)+"ms"
        save_dir_sub = os.path.join(save_dir,sub)        
        processed_saccades = pd.read_json(os.path.join(output_folder,"horizontal_saccades_with_score_{0}ms.json".format(duration)))
        average_saccade = pd.read_csv(os.path.join(output_folder,"average_saccade_{0}ms.csv".format(duration)))
        histogram_velocity_vector = pd.read_json(os.path.join(output_folder,"velocity_vectors_{0}ms.json".format(duration))) 
        scores = pd.read_json(os.path.join(output_folder,"scores_{0}ms.json".format(duration)))        
        scores_column_list = ["entropy_score","residual_sum_velocity"]#GetScoreListToLoopThrough(scores)
        if produce_plots_bool==True:
            for score_column in scores_column_list:
                sub_score = scores[["unique_saccade_number",
                                    "ranked_"+score_column,
                                    score_column,"vector"]]            
                if "entropy" in score_column:
                    sub_score = sub_score.sort_values(by="ranked_"+score_column,ascending=False)#Sort after rank
                else:                        
                    sub_score = sub_score.sort_values(by="ranked_"+score_column)#Sort after rank
            
                transformation_colum = GetCorrectTransformationToUseInAnalysis(score_column)
                sub_average_saccade = average_saccade[transformation_colum]    
                save_dir_sub_sub = MakeFolderToSaveScoreIn(save_dir_sub,score_column)
                
                figs = plotRankedSaccadesTest(processed_saccades,sub_average_saccade,sub_score.dropna(),
                                       save_dir_sub_sub,saccade_pos_col=transformation_colum,
                                       sup_title=score_column,_nrow=5,_ncol=3,_figsize=(8.5, 11))
                pdf = matplotlib.backends.backend_pdf.PdfPages(os.path.join(save_dir,score_column+"_"+str(duration)+".pdf"))
                for x in figs:
                    pdf.savefig(x)
                pdf.close()
                
                if "entropy" in score_column:
                    figs = plotRankedSaccadesVelocityHistograms(processed_saccades,sub_average_saccade,sub_score.dropna(),
                                           save_dir_sub_sub,saccade_pos_col=transformation_colum,
                                           sup_title=score_column,_nrow=5,_ncol=3,_figsize=(8.5, 11))
                    pdf = matplotlib.backends.backend_pdf.PdfPages(os.path.join(save_dir,score_column+"_histogram_"+str(duration)+".pdf"))
                    for x in figs:
                        pdf.savefig(x)
                    pdf.close()                   
                    
                # Add duration as a column to the data that is saved


    #winsound.Beep(freq+10, beep_duration)
