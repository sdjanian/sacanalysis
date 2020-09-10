# Python libraries
import pandas as pd
import numpy as np
import random
from scipy.stats import entropy
from scipy.stats import kurtosis, skew
import modality
from .rjmcmc import rjmcmc_output

class SaccadeAnalysis:
    """
    A class to analyse saccades and caculate different scores and rank them.
    
    Usage example with GazeCom:
    
    # Load GazeCom
    load_gazecom = load_gazecom_class.Load_gazecom()
    df = load_gazecom.load_all_data(unit_for_time="Milli")
    CEvents = cEvents.CalculateEventDurationClass()
    event_df = CEvents.calculateBasicEventStatistics(df)
    duration = 20
    sub_event_df = event_df[event_df["event_duration"]==duration]
    all_saccades = CEvents.extractEventsToDdf(df,sub_event_df,event_label = load_gazecom.class_event_gazecom["Saccade"],verbose=0)
    
    # Make the processing of the saccades and store results
    preprocess = preprocessing.Preproccesing(all_saccades)
    processed_saccades = preprocess.GetPreprocessedSaccades()
    average_saccade = preprocess.GetAverageSaccade()
    histogram_vector = preprocess.GetHistogramVectors()
    
    # Analyse the results
    saccadeAnalysis = SaccadeAnalysis(processed_saccades,average_saccade,histogram_vector)
    residuals = saccadeAnalysis.GetResidualScore()
    
    Functions:
        GetResidualScore : 
            Returns a dataframe with all the preproccesed data added as
            ['residual_sum_x_z_trans'       : Residual sum of the horizontal signal from average saccade in z-score transformation , 
            'residual_sum_x_norm_up'        : Residual sum of the horizontal signal from average saccade in mean normalized transformation,
            'residual_sum_velocity'         : Residual sum of the velocity from average saccade in degrees pr second,
            'flatness_score'                : The flatness of a saccade by measuring the lowest dispersion with a rolling window,
            'ranked_residual_sum_x_z_trans' : Rankings of each saccade by residual_sum_x_z_trans with 1 being best ranked,
            'ranked_residual_sum_x_norm_up' : Rankings of each saccade by residual_sum_x_norm_up with 1 being best ranked,
            'ranked_residual_sum_velocity'  : Rankings of each saccade by residual_sum_velocity with 1 being best ranked,
            'ranked_flatness_score'         : Rankings of each saccade by flatness_score with 1 being best ranked]
            and each row is a timestamp sample of a saccade.
            'dipvalue_score'                : Hartigans Diptest value for a histogram of the velocity 
            'entropy_score'                 : Shanons entropy for a histogram of the velocity
            'kurtosis_score'                : Kurtosis for a histogram of the velocity
            'skew'                          : Skew for a histogram of the velocity
            'bfvalue_score'                 : Bayesian Factor for a histogram of the velocity calculated using Reversible Jump Markov Chain Monte Carlo 
                                              for https://pdfs.semanticscholar.org/29a4/f9cd5faa12593ac13d0349ba842d48eb792a.pdf

        
    """    

    def __init__(self,saccades:pd.DataFrame, average_saccade:pd.DataFrame,histogram_velocity_vector:pd.DataFrame):
        self.__saccades = saccades
        self.__average_saccade = average_saccade
        self.__histogram_velocity_vector = histogram_velocity_vector
        self.__one_sample_duration = 1000/250 
    
    
    def __CalcuateResiduals(self):
        
        # Create residual dataframe
        self.__scores = self.__saccades.groupby("unique_saccade_number").apply(
                lambda x: x[["unique_saccade_number","source","subject","stimuli","start_time","end_time"]].iloc[0]
                )

        self.__ResidualZScoreSaccade()
        self.__ResidualUpwardsSaccade()
        self.__ResidualVelocity()
        self.__FlatnessScore()
        
        #Vector analyses
        self.__AddHistogramVectorToScore()       
        self.__CalulateHartigansDiptest()
        self.__CalculateEntropy()
        self.__CalculateKurtosis()
        self.__CalculateSkew()
        self.__CalculateBFValue()

        # REMEMBER TO ADD MAIN SEQUENCE ANALYSIS
        self.__RankScores()
        
    def __ResidualZScoreSaccade(self) -> None:
        """Calculate the residual for each saccade from the average saccade. The norm is applied to ensure all values are positive."""
        self.__saccades["residual_x_z_trans"] = self.__saccades.groupby("unique_saccade_number")["x_z_trans"].transform(
                lambda x: abs(x-self.__average_saccade["x_z_trans"].values)
                )   
        
        self.__scores["residual_sum_x_z_trans"] = self.__saccades.groupby("unique_saccade_number")["residual_x_z_trans"].apply(
                lambda x:np.sum(x)
                )
    def __ResidualUpwardsSaccade(self) -> None:
        """Calculate the residual for each saccade from the average saccade. The norm is applied to ensure all values are positive."""
        self.__saccades["residual_x_norm_up"] = self.__saccades.groupby("unique_saccade_number")["x_norm_up"].transform(
                lambda x:  abs(x-self.__average_saccade["x_norm_up"].values)
                ) 
        # Calculate the sum of the residuals
        self.__scores["residual_sum_x_norm_up"] = self.__saccades.groupby("unique_saccade_number")["residual_x_norm_up"].apply(
                lambda x:np.sum(x)
                )        
    
    def __ResidualVelocity(self) -> None:
        """
        Calculate the residualof the velocity for each saccade from the average saccade.
        The norm is applied to ensure all values are positive.
        """
        self.__saccades["residual_velocity"] = self.__saccades.groupby("unique_saccade_number")["velocity_norm"].transform(
                lambda x:  abs(x-self.__average_saccade["velocity_norm"].values)
                )
        # Calculate the sum of the residuals
        self.__scores["residual_sum_velocity"] = self.__saccades.groupby("unique_saccade_number")["residual_velocity"].apply(
                    lambda x:np.sum(x)
                    )

    def __FlatnessScore(self,windows_size:int=3) -> None:
        """ 
        Calculate the flatness of a z score transofrmed saccade by using the dispertion of a rolling window. 
        The score is lowest value found in that saccade because the lower the score, the flatter a parter of the saccade is.
        Input:
            windows_size: The size of the rolling window. By default 3 samples. 
            
        """
        self.__scores["flatness_score"] = self.__saccades.groupby("unique_saccade_number").apply(
                lambda x: min(x["x_z_trans"].rolling(windows_size).apply(self.minmaxdiff).dropna())
                )      
        
    def __CalulateHartigansDiptest(self) -> None:
       self.__scores["dipvalue_score"] = self.__scores["vector"].apply(
               lambda x: modality.diptest.getDip(x)
               )
    def __CalculateEntropy(self) -> None:
        self.__scores["entropy_score"] = self.__scores["vector"].apply(
               lambda x: entropy(x)
               )       

    def __CalculateBFValue(self) -> None:
       self.__scores["bfvalue_score"] = self.__scores["vector"].apply(
               lambda x: rjmcmc_output(np.expand_dims(np.array(x),axis=1))
               )        

    def __CalculateSkew(self) -> None:
       self.__scores["skew_score"] = self.__scores["vector"].apply(
               lambda x: skew(x)
               )  
       
    def __CalculateKurtosis(self) -> None:
       self.__scores["kurtosis_score"] = self.__scores["vector"].apply(
               lambda x: kurtosis(x)
               )         
    def __AddHistogramVectorToScore(self) -> None:
        
        self.__scores = self.__scores.sort_values(by=["unique_saccade_number"])
        self.__histogram_velocity_vector = self.__histogram_velocity_vector.sort_values(by=["unique_saccade_number"])
        self.__scores["vector"] = self.__histogram_velocity_vector["vector"].values
        #self.__scores = self.__scores.merge(self.__histogram_velocity_vector[["unique_saccade_number","vector"]],on="unique_saccade_number")
        
    def __RankScores(self) -> None:
        """
        Created a ranking column for each score.
        """
        
        def HelperFun(variable):
            score_col = ["residual", "score"]
            if   any(x in variable for x in score_col):
                return True
            else:
                return False
        # Normalize scores to be in range 0-1
        def normalizeRanks(rank):
            rank = rank+1
            return (rank)/max(rank)
            
        residual_cols = list(filter(HelperFun,self.__scores.columns))
        for residual_col in residual_cols:
            if any(x in residual_col for x in ["residual_main_sequence_negative","flatness_score","dipvalue_score"]):
                # Scores in decending order of value
                self.__scores = self.__scores.sort_values(by=[residual_col],ascending=False).reset_index(drop=True)
                self.__scores["ranked_"+residual_col] = normalizeRanks(self.__scores.index)
            else:
                # Scores in ascending order of value
                self.__scores = self.__scores.sort_values(by=[residual_col]).reset_index(drop=True)
                self.__scores["ranked_"+residual_col] = normalizeRanks(self.__scores.index)
            self.__scores["ranked_"+residual_col][self.__scores[residual_col].isna()==True]=np.nan     
            
    def GetResidualScore(self) -> pd.DataFrame:
        """
            Returns a dataframe with all the preproccesed data added as
            ['residual_sum_x_z_trans'       : Residual sum of the horizontal signal from average saccade in z-score transformation , 
            'residual_sum_x_norm_up'        : Residual sum of the horizontal signal from average saccade in mean normalized transformation,
            'residual_sum_velocity'         : Residual sum of the velocity from average saccade in degrees pr second,
            'flatness_score'                : The flatness of a saccade by measuring the lowest dispersion with a rolling window,
            'ranked_residual_sum_x_z_trans' : Rankings of each saccade by residual_sum_x_z_trans with 1 being best ranked,
            'ranked_residual_sum_x_norm_up' : Rankings of each saccade by residual_sum_x_norm_up with 1 being best ranked,
            'ranked_residual_sum_velocity'  : Rankings of each saccade by residual_sum_velocity with 1 being best ranked,
            'ranked_flatness_score'         : Rankings of each saccade by flatness_score with 1 being best ranked]
            and each row is a timestamp sample of a saccade.
            'dipvalue_score'                : Hartigans Diptest value for a histogram of the velocity 
            'entropy_score'                 : Shanons entropy for a histogram of the velocity
            'kurtosis_score'                : Kurtosis for a histogram of the velocity
            'skew'                          : Skew for a histogram of the velocity
            'bfvalue_score']                : Bayesian Factor for a histogram of the velocity calculated using Reversible Jump Markov Chain Monte Carlo 
                                              for https://pdfs.semanticscholar.org/29a4/f9cd5faa12593ac13d0349ba842d48eb792a.pdf
            and each row is a timestamp sample of a saccade.
        """
        self.__CalcuateResiduals()
        return self.__scores
        
    
    @staticmethod            
    def minmaxdiff(x):
        return max(x)-min(x)     

if __name__ == "__main__":
    # Custom libraries
    import load_gazecom_class
    import preprocessing
    import calculateEvents as cEvents  
    from colorama import init
    init()    
    
    random.seed(10)
    # Load GazeCom and calculate events
    if 'df' not in locals():
        load_gazecom = load_gazecom_class.Load_gazecom()
        df = load_gazecom.load_all_data(unit_for_time="Milli")
    
    CEvents = cEvents.CalculateEventDurationClass()
    if 'event_df' not in locals():
        event_df = CEvents.calculateBasicEventStatistics(df)
    duration = 20
    sub_event_df = event_df[event_df["event_duration"]==duration]
    all_saccades = CEvents.extractEventsToDdf(df,sub_event_df,event_label = load_gazecom.class_event_gazecom["Saccade"],verbose=0)
    
    # Make the processing of the saccades and store results
    preprocess = preprocessing.Preproccesing(all_saccades)
    processed_saccades = preprocess.GetPreprocessedSaccades()
    average_saccade = preprocess.GetAverageSaccade()
    histogram_vector = preprocess.GetHistogramVectors()
    
    # Analyse the results
    saccadeAnalysis = SaccadeAnalysis(processed_saccades,average_saccade,histogram_vector)
    residuals = saccadeAnalysis.GetResidualScore()
    




