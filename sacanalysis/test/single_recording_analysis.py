from sacanalysis import Load_gazecom, Preproccesing, SaccadeAnalysis, CalculateEventDurationClass, plotRankedSaccades, GetVelocity
from scipy.io import arff
import numpy as np
import pandas as pd
if __name__=="__main__":
    data, meta = arff.loadarff("AAF_beach.arff")
    df_single_rec = pd.DataFrame(data)  
    df_single_rec[df_single_rec["confidence"]==0] = np.nan

    df_single_rec = df_single_rec[["time","x","y","handlabeller_final"]]
    df_single_rec = df_single_rec.rename(columns = {"handlabeller_final":"labels"})
    
    df_single_rec = GetVelocity(df_single_rec, "time")
    events = CalculateEventDurationClass.calculateBasicEventStatistics(df_single_rec,label_col="labels")
    events = events.dropna()
    duration = events["event_duration"].value_counts().index.values[0] # most frequent duration
    
    sub_event_df = events[events["event_duration"]==duration]
    extracted_saccades = CalculateEventDurationClass.extractEventsToDdf(df_single_rec,
                                                                        sub_event_df,
                                                                        event_label = Load_gazecom.class_event_gazecom["Saccade"],
                                                                        label_col = "labels")
    #extracted_saccades = extracted_saccades.groupby(by=["unique_saccade_number"]).apply(lambda x: x.dropna()) # check for nans

    preproces = Preproccesing(extracted_saccades,Hz = 250, time_unit="micro")
    
    #extracted_saccades["x_norm"] = extracted_saccades.groupby("unique_saccade_number")["x"].transform(
    #    lambda x: x-x.mean() 
    #    )
    processed_saccades = preproces.GetPreprocessedSaccades()
    average_saccade = preproces.GetAverageSaccade()
    histogram_vector = preproces.GetHistogramVectors()    
    #preprocessed_saccades = preproces.GetPreprocessedSaccades()
    """
    sub_event_df = event_df[event_df["event_duration"]==duration]
    all_saccades = CEvents.extractEventsToDdf(df,sub_event_df,event_label = load_gazecom.class_event_gazecom["Saccade"],verbose=0)
    
    # Make the processing of the saccades and store results
    data = Preproccesing(all_saccades)
    processed_saccades = data.GetPreprocessedSaccades()
    average_saccade = data.GetAverageSaccade()
    histogram_vector = data.GetHistogramVectors()
    """