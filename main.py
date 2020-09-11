# Custom libraries
#import load_gazecom_class
#import calculateEvents as cEvents
#from saccade_plots import* 
#import preprocessing
from sacanalysis import Load_gazecom, Preproccesing, SaccadeAnalysis, CalculateEventDurationClass, plotRankedSaccades

# Python libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import random
import tqdm
import os
import winsound
import copy
beep_duration = 1000  # millisecond
freq = 440  # Hz

def GetScoreListToLoopThrough(scores:dict) -> list:
    """
        Get only the score column names by looping through a list of known columns to drop from the dataframe
    """
    residual_columns = [*scores.keys()]#["x_norm_up","x_z_trans"]
    residual_exlude_comuns = ['unique_saccade_number',
                             'source',
                             'subject',
                             'stimuli',
                             'start_time',
                             'end_time',
                             'residual_main_sequence',
                             'ranked_residual_main_sequence',
                             'vector']
    residual_list = list(set(residual_columns) - set(residual_exlude_comuns))
    residual_list = [x for x in residual_list if "ranked" not in x ] #Dropped the ranked cols from the loop.
    return residual_list
    

def GetCorrectTransformationToUseInAnalysis(score_column:str) -> str:
    """
        Get the correct eye movement position for a given score. 
        Output:
            str: Is either mean normalized upwards saccade or z-score tranformed of the a mean normalized upwards saccade
    """
    if any(map(lambda x: x in  score_column,["main", "speed_1","x_norm_up","velocity","dip","entropy","kurtosis","skew","bfvalue"])):
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

def SaveResultsAsCsv(df:pd.DataFrame,directory:str,name:str,ms:str) -> None:
    print(os.path.join(directory,name+"_"+ms+".csv"))
    df.to_csv(os.path.join(directory,name+"_"+ms+".csv"),index=False)
    df.to_json(os.path.join(directory,name+"_"+ms+".json"))

def AddSaccadeSamplesToScore(scores:pd.DataFrame,processed_saccades:pd.DataFrame) -> pd.DataFrame:
    """
    Add the saccade samples as columns samp_0...samp_n to each row of the score df.
    """
    horizontal_df = processed_saccades[["unique_saccade_number","x"]]
    horizontal_df["samp"] = horizontal_df.groupby("unique_saccade_number")["x"].transform(lambda x:np.arange(0,len(x)))
    horizontal_df["samp"] = horizontal_df["samp"].apply(lambda x: "samp_"+str(int(x)))
    horizontal_df_wide = horizontal_df.pivot(index="unique_saccade_number",columns="samp",values="x")
    return pd.merge(scores,horizontal_df_wide,on="unique_saccade_number")    
    
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
    random.seed(10)
    # Load GazeCom and calculate events
    if 'df' not in locals():
        load_gazecom = Load_gazecom(r"C:\Users\FQ73OO\OneDrive - Aalborg Universitet\Eye_tracking\GazeCom_sample_data\all_features")
        df = load_gazecom.load_all_data(unit_for_time="Milli")
    
    CEvents = CalculateEventDurationClass()
    if 'event_df' not in locals():
        event_df = CEvents.calculateBasicEventStatistics(df)

    ### Variables
    start_dur = 20
    end_dur = 24
    eye_tracker_frequency = 250
    save_dir = "output"
    produce_plots_bool = False # Produce pdf of all ranked saccades
    one_sample_duration = int(1000/eye_tracker_frequency)
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)    
    
    
    ### Setting arrays    
    durations = np.arange(start_dur,end_dur,one_sample_duration)
    average_saccade_list = []
    residual_df_list = []    

    for duration in tqdm.tqdm(durations,position=0,leave=False,desc = "Analysing saccades"):
        sub = str(duration)+"ms"
        save_dir_sub = os.path.join(save_dir,sub)
        
        sub_event_df = event_df[event_df["event_duration"]==duration]
        # Make the analysis op the saccades and store results
        extracted_saccades = CEvents.extractEventsToDdf(df,sub_event_df,event_label = load_gazecom.class_event_gazecom["Saccade"],verbose=0)
        
        Preprocess = Preproccesing(extracted_saccades)
        processed_saccades = Preprocess.GetPreprocessedSaccades()
        average_saccade = Preprocess.GetAverageSaccade()
        histogram_velocity_vector = Preprocess.GetHistogramVectors()     
        
        _SaccadeAnalysis = SaccadeAnalysis(processed_saccades,average_saccade,histogram_velocity_vector)
        scores = _SaccadeAnalysis.GetResidualScore()        
        scores_column_list = GetScoreListToLoopThrough(scores)
        if produce_plots_bool==True:
            for score_column in scores_column_list:
                sub_score = scores[["unique_saccade_number",
                                    "ranked_"+score_column,
                                    score_column]]            
                sub_score = sub_score.sort_values(by="ranked_"+score_column)#Sort after rank
            
                transformation_colum = GetCorrectTransformationToUseInAnalysis(score_column)
                sub_average_saccade = average_saccade[transformation_colum]    
                save_dir_sub_sub = MakeFolderToSaveScoreIn(save_dir_sub,score_column)
                
                plotRankedSaccades(processed_saccades,sub_average_saccade,sub_score.dropna(),
                                       save_dir_sub_sub,saccade_pos_col=transformation_colum,
                                       sup_title=score_column,_nrow=8,_ncol=3,_figsize=(6,15))
                    
                # Add duration as a column to the data that is saved
                sub_average_saccade = pd.DataFrame({"average_saccade_"+transformation_colum:sub_average_saccade,
                                                    "duration":np.full(len(sub_average_saccade),duration)})
                processed_saccades["duration"] = np.full(len(processed_saccades),duration)
                sub_score["duration"] = np.full(len(sub_score),duration)
                
                # Save results in sub sub folder
                SaveResultsAsCsv(sub_average_saccade,save_dir_sub_sub,"average_saccades",sub)
                SaveResultsAsCsv(sub_score,save_dir_sub_sub,"saccades_"+score_column+"_score_ranked",sub)
            
        # Save results in sub folder        
        SaveResultsAsCsv(processed_saccades,save_dir,"horizontal_saccades_with_score",sub)
        SaveResultsAsCsv(average_saccade,save_dir,"average_saccade",sub)
        SaveResultsAsCsv(histogram_velocity_vector,save_dir,"velocity_vectors",sub)
        scores_with_samp = AddSaccadeSamplesToScore(scores,processed_saccades) # Add the saccade samples as columns samp_0...samp_n to each row                
        SaveResultsAsCsv(scores_with_samp,save_dir,"scores",sub)  

    winsound.Beep(freq+10, beep_duration)
