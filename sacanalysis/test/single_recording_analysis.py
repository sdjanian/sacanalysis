from sacanalysis import Load_gazecom, Preproccesing, SaccadeAnalysis, CalculateEventDurationClass, plotRankedSaccades, GetVelocity
from scipy.io import arff
import numpy as np
import pandas as pd
if __name__=="__main__":
    #data, meta = arff.loadarff("AAF_beach.arff")
    #df = pd.DataFrame(data)  
    
    load_gazecom = Load_gazecom("C:/sacanalysis/gazecom_small/all_features")
    df = load_gazecom.load_all_data(unit_for_time="milli")
    df[df["confidence"]==0] = np.nan

    df = df[["time","x","y","handlabeller_final","source","speed_1"]]
    df = df.rename(columns = {"handlabeller_final":"labels","speed_1":"velocity"})
    
    #df = GetVelocity(df, "time",time_unit="milli")
    events = CalculateEventDurationClass.calculateBasicEventStatistics(df,label_col="labels")
    events = events.dropna()
    duration = events["event_duration"].value_counts().index.values[0] # most frequent duration
    
    sub_event_df = events[events["event_duration"]==duration]
    extracted_saccades = CalculateEventDurationClass.extractEventsToDdf(df,
                                                                        sub_event_df,
                                                                        event_label = Load_gazecom.class_event_gazecom["Saccade"],
                                                                        label_col = "labels",verbose=0)
    #extracted_saccades = extracted_saccades.groupby(by=["unique_saccade_number"]).apply(lambda x: x.dropna()) # check for nans
    
    preproces = Preproccesing(extracted_saccades,Hz = 250, time_unit="milli")
    
    
    #processed_saccades = preproces.GetPreprocessedSaccades(None)
    #average_saccade = preproces.GetAverageSaccade()
    #histogram_vector = preproces.GetHistogramVectors()   
    #_SaccadeAnalysis = SaccadeAnalysis(processed_saccades,average_saccade,histogram_vector)
    #scores = _SaccadeAnalysis.GetScores()
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