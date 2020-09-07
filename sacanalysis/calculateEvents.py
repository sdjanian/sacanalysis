import pandas as pd
import numpy as np
import tqdm
import copy
import itertools

class CalculateEventDurationClass:

    def __init__(self,rater_col_name="handlabeller_final"):
        self._rater_col_name=rater_col_name
        
       
    def calculateBasicEventStatistics(self,df=None,remove_outliers = False,rater_col_name='handlabeller_final'):            
        if remove_outliers is True:
            print("Removing outliers")
            
        event_type_list = []
        event_duration_list=[]
        source_list = []
        event_peak_velocity_list = []
        event_amplitude_list = []
        event_start_list = []
        event_end_list = []
        
        video_start_flag = df['source'].ne(df['source'].shift().bfill()).astype(int) # Indication of where the start of a recoding is
        # hacky way to the the indices of where recording starts
        ix = np.isin(video_start_flag,1)
        ix2 = np.where(ix)
        ix3 = list(sum(ix2))
        ix3.insert(0,0) # insert start of the first recording
        for ii in tqdm.tqdm(np.arange(0,len(ix3)),position=0,leave=True,desc = "Calculating event features"):
            if any(ix):
                #Hacky way to get the correct length length of recording 
                if ii != len(ix3)-1:
                    df_sub = df.iloc[ix3[ii]:ix3[ii+1]] # Recording between two flags    
                else:
                    df_sub = df.iloc[ix3[ii]:len(video_start_flag)] # Last recording
            else:
                df_sub = df
                
            labelled_event = df_sub[rater_col_name]
            event_start = np.where(np.roll(labelled_event,1)!=labelled_event)[0]
            if event_start.size == 0:
              print("There was only detected 1 event")
              return
            if event_start[0] != 0:
                event_start = np.insert(event_start,0,0) # Add start of the first event in the case where the first and alst even are the same
            event_end = np.roll(event_start,-1)
            event_end[-1] = len(labelled_event) # Add the end of the last event (0 indexing should get yeeted) (threw away -1)
            event_end = event_end-1 # shift everything down 1 index then an event ends right before another starts
            # Calculate event durations
            times = df_sub["time"]
            start_times = times.iloc[event_start]
            end_times = times.iloc[event_end]        
            event_duration = end_times.values-start_times.values
            #event_duration[-1] = times.iloc[-1]-start_times.iloc[-1] # Calculate the last sample correctly.
            #event_duration /= 1000
    
            # Calculate event amplitudes
            position = df_sub[["x","y"]]
            position_start = position.iloc[event_start].values
            position_end = position.iloc[event_end].values
            event_amplitude = position_end-position_start
            #event_amplitude_list[-1] =position.iloc[-1]-position_start[-1]  # calcultae the last sample correctly (last sample of position - last sample of start position)
            event_amplitude = np.sqrt((event_amplitude[:,0]**2)+(event_amplitude[:,1]**2)) # Calculate euclidian distance between event starts and ends
            
            # Calculate the peak velocities of events
            velocity = df_sub["speed_1"]       
            event_peak_velocity = []
            for start,end in (zip(event_start,event_end)):
                event_peak_velocity.append(np.amax(velocity.iloc[start:end]))
            event_peak_velocity = np.array(event_peak_velocity)
                
            # Record the source of the events
            event_source = df_sub["source"].iloc[event_start]        
            event_type = labelled_event.iloc[event_start].values
            
            
            if remove_outliers:
                without_outliers = self.is_outlier(event_duration)
                event_type = event_type[~without_outliers]
                event_duration = event_duration[~without_outliers]
                event_source = event_source[~without_outliers]
                event_amplitude=event_amplitude_list[~without_outliers]
                event_peak_velocity = event_peak_velocity[~without_outliers]
                event_start = event_start[~without_outliers]
                event_end = event_end[~without_outliers]
    
            event_duration_list = np.hstack((event_duration_list,event_duration))
            source_list = np.hstack((source_list,event_source))
            event_type_list = np.hstack((event_type_list,event_type))
            event_peak_velocity_list = np.hstack((event_peak_velocity_list,event_peak_velocity))
            event_amplitude_list = np.hstack((event_amplitude_list,event_amplitude))        
            event_start_list =np.hstack((event_start_list,event_start.astype(int)))
            event_end_list =np.hstack((event_end_list,event_end.astype(int))) 
            
            #if any(x > 6000 for x in event_duration):
            #    print("Sub set staring at idx:",ix3[ii],"at idx:",event_duration[event_duration>6000],)
            
        df_event = pd.DataFrame({"event_type":event_type_list,"event_duration":event_duration_list,
                                 "event_source":source_list,"event_peak_velocity":event_peak_velocity_list,
                                 "event_amplitude":event_amplitude_list,"event_starts":event_start_list,"event_ends":event_end_list})
        df_event['event_starts']= df_event['event_starts'].astype('int32')
        df_event['event_ends']=df_event['event_ends'].astype('int32')
        return df_event  
    @staticmethod
    def is_outlier(points, thresh=3.5):
        """
        Returns a boolean array with True if points are outliers and False 
        otherwise.
    
        Parameters:
        -----------
            points : An numobservations by numdimensions array of observations
            thresh : The modified z-score to use as a threshold. Observations with
                a modified z-score (based on the median absolute deviation) greater
                than this value will be classified as outliers.
    
        Returns:
        --------
            mask : A numobservations-length boolean array.
    
        References:
        ----------
            Boris Iglewicz and David Hoaglin (1993), "Volume 16: How to Detect and
            Handle Outliers", The ASQC Basic References in Quality Control:
            Statistical Techniques, Edward F. Mykytka, Ph.D., Editor. 
        """
        if len(points.shape) == 1:
            points = points[:,None]
        median = np.median(points, axis=0)
        diff = np.sum((points - median)**2, axis=-1)
        diff = np.sqrt(diff)
        med_abs_deviation = np.median(diff)
    
        modified_z_score = 0.6745 * diff / med_abs_deviation
    
        return modified_z_score > thresh
    
    @staticmethod
    def extractEventsToDdf(df:pd.core.frame.DataFrame,
                           event_df:pd.core.frame.DataFrame,
                           event_label:int,verbose = 1)->pd.core.frame.DataFrame:
            event_list = []
            event_numbers =[]
            unique_saccade_counter = 1
            df = df.reset_index()
            groups = [grp for di, grp in df.groupby('source')] # Faster too loop through the list then get extract each subset during the loop.
            for sub_df in tqdm.tqdm(groups,total=len(groups),position=1,leave=True,desc="Extracting all samples of events"):
                recording = sub_df["source"].unique()
                events = event_df[(event_df["event_type"]==event_label) &(event_df["event_source"]==recording[0])] # recording[0] because it's a list with 1 element
                for i,(index, row) in enumerate(events.iterrows()):
                    event = copy.deepcopy(sub_df.iloc[row["event_starts"]:row["event_ends"]+1]) # +1 is because of weird Python indexing. Easier to +1 then figure out the cause.
                    event_numbers.append(list(np.full(len(event),i)))
                    event["norm_time"] = event["time"]-event["time"].iloc[0]
                    event["unique_saccade_number"] = np.full(len(event),unique_saccade_counter)
                    event["start_time"] = np.full(len(event),row["event_starts"])
                    event["end_time"] = np.full(len(event),row["event_ends"])
                    unique_saccade_counter = unique_saccade_counter+1
                    event_list.append(event)
            event_numbers_flat = list(itertools.chain.from_iterable(event_numbers))
            event_samples_df = pd.concat(event_list)
            event_samples_df["event_number"] = event_numbers_flat
            if verbose == 1:
                print("Event",event_label,"samples selected:", len(event_samples_df),
                      "\nEvent",event_label,"samples total:",len(df[df["handlabeller_final"]==event_label]),
                      "\nNumber of difference:",len(df[df["handlabeller_final"]==event_label])-len(event_samples_df),
                      "\nDifferent indices:",df[df["handlabeller_final"]==event_label].index.difference(event_samples_df.index),
                      "\nPercentage of event in samples from all events:", np.round(len(df[df["handlabeller_final"]==event_label])/len(df),4))
            return event_samples_df

if __name__ == "__main__":
    import load_gazecom_class
    import seaborn as sns
    import matplotlib.pyplot as plt
    from matplotlib.ticker import ScalarFormatter
    import plotting_class


    if 'df' not in locals():
        load_gazecom = load_gazecom_class.Load_gazecom()
        df = load_gazecom.load_all_data(unit_for_time="Mirco")
    calculateBasicEventStatisticsClass = CalculateEventDurationClass()
    plotting_class = plotting_class.Plotting_class(colors="GazeCom")

    
    event_df = calculateBasicEventStatisticsClass.calculateBasicEventStatistics(df)
    for items in load_gazecom.class_event_gazecom.items():
        print(items)
        
    # Print the frequency
    print("Fequency of each event\n",
          event_df["event_type"].groupby(event_df["event_type"]).count())
    label_list = []
    label_name_list = []
    for key,val in load_gazecom.class_label_gazecom.items():
        if val!="Unknown":
            label_name_list.append(val)
            label_list.append(key)
    # Get saccade and fixation with only 1 sample, get smooth pursuits above 1 sec        
    sample_1_time = 4000
    one_second_in_micro = 1000000
    print("Saccade shorther than 1 sample",
          event_df[(event_df["event_type"]==load_gazecom.class_event_gazecom["Saccade"]) &
                   (event_df["event_duration"]<sample_1_time)].count())
    print("Fixations shorther than 1 sample",
          event_df[(event_df["event_type"]==load_gazecom.class_event_gazecom["Fixation"]) &
                   (event_df["event_duration"]<sample_1_time)].count()) 
    print("Smooth Pursuit longer than 1 second",
      event_df[(event_df["event_type"]==load_gazecom.class_event_gazecom["Smooth Pursuit"]) &
               (event_df["event_duration"]>=one_second_in_micro)].count())
    # Plot event duration
    bins_event_duration = np.arange(event_df["event_duration"][event_df["event_type"]==2].min(),event_df["event_duration"][event_df["event_type"]==2].max(),10)
    fig,ax = plotting_class.plotDistributions(df=event_df,feature="None",xlabel_="Duration (ms)",ylabel_="Frequency (log)",labels=label_list,titles=label_name_list,plotType="event duration",
                               bins = None, sup_title="Event duration")
    
    # Print the bar heights for event duration
    event_duration_hist_dict = {}
    for _ax in ax:
        for __ax in _ax:
            barX = [h.get_height() for h in __ax.patches]
            barY = [h.get_width() for h in __ax.patches]
            print(__ax.get_title(),": sum of bar heights: ",sum(barX),"mean width of bars: ",np.mean(barY))
            event_duration_hist_dict[__ax.get_title()] = {"barX":barX,"barY":barY}
    fig.savefig("event_duration.pdf",bbox_inches='tight')
    
    # Plot the event amplitudes
    bins_event_ampltitude = np.arange(event_df["event_amplitude"][event_df["event_type"]==2].min(),event_df["event_amplitude"][event_df["event_type"]==2].max(),0.5)

    fig2,ax2 = plotting_class.plotDistributions(df=event_df,feature="None",xlabel_="Amplitude (deg/s)",ylabel_="Frequency(log)",labels=label_list,titles=label_name_list,plotType="event amplitude",
                                 bins = bins_event_ampltitude, sup_title= "Event amplitude")
    fig2.savefig("event_amplitude.pdf",bbox_inches='tight')
    
    # Extract th events to a dataframe with all the samples for the events and save it.
    #df["subject"] = df["source"].apply(lambda x :x.split("\\")[-1].split(".")[0].split("_")[0])
    #df["stimuli"] = df["source"].apply(lambda x :x.split("\\")[-1].split(".")[0].split("_")[1])    
    event_sample_dfs = []
    for event_label in label_list:
        event_sample_dfs.append(calculateBasicEventStatisticsClass.extractEventsToDdf(df,event_df,event_label))
    
    for idx,event_label in tqdm.tqdm(enumerate(label_list),desc="Saving samples to csv"):
        df_sample = event_sample_dfs[idx]

        df_sample_to_save = df_sample[["subject","stimuli","time","x","y","handlabeller_final","event_number"]]
        df_sample_to_save.to_csv(load_gazecom.class_label_gazecom[event_label]+"_event_samples.csv",index=False)


    #..\GazeCom_Data\all_features\beach\AAF_beach.arff this dataset has bad sampling rate



