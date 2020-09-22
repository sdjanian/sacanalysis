# Python libraries
import pandas as pd
import numpy as np
import copy
from scipy import stats
from .utility import getTimeinSec

class Preproccesing:
    """
    A class to preprocess the saccades before doing analysis.
    Preproccesing consists of ...:
        removes saccades with unstable timestamps.
        chooses only saccades where the horizontal component is 5 times larger than the vertical. Can be changed using __ChooseOnlyHoriztonalOrVerticalSaccades(self,ratio_threshold = 5)
        mean normalizes the horizontal (x), vertical (y) and instantanious velocity (velocity).
        flips all saccades so they point in the same direction horizontaly (upwards)
        z-score transform the upwards horizontal position (x_norm_up)
        
    Usage example with GazeCom:
        
            # Load data 
            load_gazecom = load_gazecom_class.Load_gazecom()
            df = load_gazecom.load_all_data(unit_for_time="Milli")    
            CEvents = cEvents.CalculateEventDurationClass()
            event_df = CEvents.calculateBasicEventStatistics(df)
            duration = 20
            sub_event_df = event_df[event_df["event_duration"]==duration]
            all_saccades = CEvents.extractEventsToDdf(df,sub_event_df,event_label = load_gazecom.class_event_gazecom["Saccade"],verbose=0)
            
            # Make the processing of the saccades and store results
            data = Preproccesing(all_saccades)
            processed_saccades = data.GetPreprocessedSaccades()
            average_saccade = data.GetAverageSaccade()
            histogram_vector = data.GetHistogramVectors()
    
    Functions:
        GetPreprocessedSaccades : 
            Returns a dataframe with all the preproccesed data added as
            ['norm_time', 'unique_saccade_number',
            'start_time', 'end_time', 'event_number', 'x_y_ratio', 'x_norm',
            'y_norm', 'velocity_norm', 'x_norm_up', 'x_z_trans']
            and each row is a timestamp.
            
        GetAverageSaccade : 
            Returns the average saccades in a dataframe with columns
            ['x_z_trans', 'x_norm_up', 'velocity_norm']
            and each row is a timestamp.

        GetHistogramVectors:
            Return a dataframe with the columns
            [timestamp_1,timestamp_2...Timestampe_n,vector]
            and each row is the saccade.
        
        
    """

    def __init__(self,saccades:pd.DataFrame, Hz:int=250,time_unit="milli"):
        self.__saccades = saccades
        self.__one_sample_duration = getTimeinSec(time_unit)/Hz 
            
    def __preprocessSaccades(self,ratio_threshold=5):
        self.__RemoveSaccadesWithUnstableTimestamps()
        self.__GetHorVerRatio()
        self.__ChooseOnlyHoriztonalOrVerticalSaccades(ratio_threshold)
        self.__NormalizePositionalAndVelocitySignal()
        self.__TransformSaccadesToUpwardsDirection()
        self.__ZScoreTransformPosition()
        
    def __RemoveSaccadesWithUnstableTimestamps(self) -> None:
        '''
            Select only saccades that have 4 ms between each time stamp.
        '''
        self.__stable_timestamps = self.__saccades.groupby(["source","event_number"]).filter(
                lambda x: all(x["time"].diff().dropna()==self.__one_sample_duration)==True
                )         
        
    def __GetHorVerRatio(self)-> None:
        '''
        Get the ratio between the horizontal and vertical position and add to stable_timestamps dataframe.
        Uses __X_Y_ratio() to cacluate the ratio.
        Adds "x_y_ratio" column to dataset
        '''
        x_y_ratios = self.__stable_timestamps.groupby("unique_saccade_number").apply(
                lambda x: np.full(len(x),self.__X_Y_ratio(x["x"],x["y"]))
                )
        x_y_ratios_array =[]
        for ratio in x_y_ratios:
            x_y_ratios_array.extend(ratio)     
        self.__stable_timestamps.loc[:,"x_y_ratio"] = x_y_ratios_array
                         


    
    def __ChooseOnlyHoriztonalOrVerticalSaccades(self,ratio_threshold = 5) -> None:
        '''
        Filter saccades based on threshold. With a ratio of above 5 the saccedes are mainly horizontal, 
        meaning that the horizontal position is 5 times larger then the vertical.
        '''
        if ratio_threshold == None:
            self.__saccadesToProcces = self.__stable_timestamps
        else:
            self.__saccadesToProcces = self.__stable_timestamps[self.__stable_timestamps["x_y_ratio"]>ratio_threshold]
        
    def __NormalizePositionalAndVelocitySignal(self)-> None:
        """
        Normalize the vertical and horizontal position using mean normalization.
        Adds the normalized position to dataframe as "x_norm" and "y_norm" columns respectivly.
        """
        # Normalise the horizontal position
        self.__saccadesToProcces.loc[:,"x_norm"] = self.__saccadesToProcces.groupby("unique_saccade_number")["x"].transform(
                lambda x: x-x.mean() 
                )
        # Normalise the vertical position
        self.__saccadesToProcces.loc[:,"y_norm"] = self.__saccadesToProcces.groupby("unique_saccade_number")["y"].transform(
                lambda y: y-y.mean() 
                )
        self.__saccadesToProcces.loc[:,"velocity_norm"] = self.__saccadesToProcces.groupby("unique_saccade_number")["velocity"].transform(
        lambda x: x-x.mean()
        )
        
    def __TransformSaccadesToUpwardsDirection(self) -> None:
        """
        Convert the saccades to all point upwards based on the mean normalized horitzontal position.
        Adds the upwards pointing saccades as "x_norm_up".
        """
        self.__saccadesToProcces.loc[:,"x_norm_up"] = self.__saccadesToProcces.groupby("unique_saccade_number")["x_norm"].apply(
                lambda x: x*-1 if x.iloc[0]-x.iloc[-1] > 0 else x
                ) 
        
    def __ZScoreTransformPosition(self) -> None:
        """
        Z score transforms horizontal position of the upwards pointing saccades.
        """
        # Z score transform the horizontal position
        self.__saccadesToProcces.loc[:,"x_z_trans"] = self.__saccadesToProcces.groupby("unique_saccade_number")["x_norm_up"].transform(
                lambda x: stats.zscore(x)
                )        
    def __CalcuateAvergeSaccade(self) -> pd.DataFrame:
        
        # Average saccade in normalized degrees
        average_saccade_norm_deg = self.__saccadesToProcces.groupby("norm_time")["x_norm_up"].apply(
                lambda x: np.mean(x)
                )
        
        """ Wrong way to calculate the z-scored average saccade
        # Average saccade in z transformed domain
        average_saccade_z_score = self.__saccadesToProcces.groupby("norm_time")["x_z_trans"].apply(
                lambda x: np.mean(x)
                )
        """
        
        # Average saccade in z transformed domain
        average_saccade_z_score = pd.Series(data=stats.zscore(average_saccade_norm_deg),
                                            name = "x_z_trans",
                                            index=average_saccade_norm_deg.index)
        
        average_saccade_velocity = self.__saccadesToProcces.groupby("norm_time")["velocity_norm"].apply(
                lambda x: np.mean(x)
                )
        # Average saccade dataframe
        average_saccade = pd.DataFrame([average_saccade_z_score,average_saccade_norm_deg,average_saccade_velocity]).T
    
        return average_saccade
    
    def __GenerateHistogramVector(self) -> pd.DataFrame:

        
        def vectorizeHelperFunction(x):            
            x_round = np.round(x)
            vector = []
            for enum,sample in enumerate(x_round):
                numberOfSamplesInBin = np.full((1,np.int((abs(sample)))),enum)
                vector.append(numberOfSamplesInBin)            
            return np.hstack(vector).squeeze()

        wide_form = self.__saccadesToProcces.pivot(index="unique_saccade_number",columns = "norm_time",values = "velocity")
        wide_form.loc[:,"vector"] = wide_form.apply(lambda x: vectorizeHelperFunction(x) if x.index.name!="unique_saccade_number" else None,axis=1)
        wide_form=wide_form.reset_index()
        wide_form=wide_form.rename(columns={"index":"unique_saccade_number"})
        #normalized_saccades["vector"] = normalized_saccades.groupby("unique_saccade_number")["x_norm_up"].transform(
        #        lambda x: vectorizeHelperFunction(x)
        #        )
        return wide_form

        
    def GetAverageSaccade(self) -> pd.DataFrame:
        """
        Calculates an average saccade my taking the mean of each sample and generating it from that. 
        E.g. the average of all samples at timestep 1 to create sample 1 of the average saccade, and all samples of timestep 2 to create sample 2 etc.
        
        Return:
            Returns 3 average saccades based on z transform, upwards pointing mean normalized position, and mean normalized velocity.
            Each row is a timestamp and each column are the different transforms
        """        
        return self.__CalcuateAvergeSaccade()
    
    def GetHistogramVectors(self) -> pd.DataFrame:        
        """
        Generates a vector to be used for modality analysis. Converts the velocity of saccade to a distribution where the vector is the bin height for each timestamp.
        Return:
            Returns a dataframe where each row is a saccade, the columns are the time stamps and the very last column is vectors.
        """
        return self.__GenerateHistogramVector()
    
    def GetPreprocessedSaccades(self,ratio_threshold = 5) -> pd.DataFrame:
        """
        Runs the preprocessing and returns the saccades in a df where each row is a time stamp and the columns are the different processes.
        """
        self.__preprocessSaccades(ratio_threshold=ratio_threshold)
        return self.__saccadesToProcces

    @staticmethod
    def __X_Y_ratio(x,y):
        """
        Helper function for _GetHorVerRatio() to calucalate horizontal and veritical position ratios
        """
        ratio = (np.max(x)-np.min(x))/(np.max(y)-np.min(y))
        return ratio 
    
if __name__ == "__main__":
    ### Example with GazeCom
    # Custom libraries
    import load_gazecom_class
    import calculateEvents as cEvents    
    # Load GazeCom and calculate events
    load_gazecom = load_gazecom_class.Load_gazecom()
    df = load_gazecom.load_all_data(unit_for_time="Milli")    
    CEvents = cEvents.CalculateEventDurationClass()
    event_df = CEvents.calculateBasicEventStatistics(df)
    duration = 20
    sub_event_df = event_df[event_df["event_duration"]==duration]
    all_saccades = CEvents.extractEventsToDdf(df,sub_event_df,event_label = load_gazecom.class_event_gazecom["Saccade"],verbose=0)
    
    # Make the processing of the saccades and store results
    data = Preproccesing(all_saccades)
    processed_saccades = data.GetPreprocessedSaccades()
    average_saccade = data.GetAverageSaccade()
    histogram_vector = data.GetHistogramVectors()
