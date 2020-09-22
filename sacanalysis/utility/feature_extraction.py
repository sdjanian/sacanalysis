import pandas as pd
import numpy as np
import tqdm
from .time_units import getTimeinSec
from .error_handling import sourceCheck, xyCheck

def GetVelocity(eye_movement_signal:pd.DataFrame,timestamp_col:str,windowWidth:int = 1, time_unit:str = "micro"):    
    """   
    Description
    ---------- 
    Calculates the velocity of an eye tracking signal. Modified GazeCom feature extraction from Matlab to python:
    https://github.com/MikhailStartsev/deep_em_classifier/blob/master/feature_extraction/arff_utils/GetVelocity.m
    
    Parameters
    ----------
    eye_movement_signal : pd.DataFrame
        dataframe containting horizontal and vertical eye tracking signal.
    timestamp_col : str
        Name of the column in the dataframe that contains the timestamps. Must be in milliseconds
        The default is None.
    time_unit : str
        Unit that timestamp_col is in. Valid arguments are "micro", "milli", "second".
        The default is "micro".        
    windowsWidth : int, optional
        window width used to calculate velocity. Window is centered around the sample being calculated.
        The default is 1 which is instantanious velocity.

    Returns
    -------
    eye_movement_signal : TYPE
        The original dataframe with velocity appended

    """
    

    xyCheck(eye_movement_signal) # sanity check
    if timestamp_col != None:
        None
    else:
        raise Exception("timestamp_col not defined")    
        
    if "source" in eye_movement_signal.columns:
        print("Source on col")
        eye_movement_signal = __CalculateVelocityOnMultipleRecordings(eye_movement_signal,timestamp_col,windowWidth, time_unit)
        

    else:                
        eye_movement_signal = sourceCheck(eye_movement_signal)
        x = eye_movement_signal["x"]
        y = eye_movement_signal["y"]
        timestamp = eye_movement_signal[timestamp_col]
        #velocity_list = np.zeros(len(eye_movement_signal))
        eye_movement_signal["velocity"] = __CalcateVelocity(x,y,timestamp,windowWidth,time_unit)

    
     #= velocity_list
    return eye_movement_signal

def __CalculateVelocityOnMultipleRecordings(eye_movement_signal:pd.DataFrame,timestamp_col:str,windowWidth:int = 1, time_unit:str = "micro"):
    recording_list =[]
    groups = [grp for di, grp in eye_movement_signal.groupby('source')] # Faster too loop through the list then get extract each subset during the loop.
    for recording in tqdm.tqdm(groups,total=len(groups),position=1,leave=True,desc="Calculating velocity on multple recordings"):
        x = recording["x"]
        y = recording["y"]
        timestamp = recording[timestamp_col]
        #velocity_list = np.zeros(len(eye_movement_signal))
        recording["velocity"] = __CalcateVelocity(x,y,timestamp,windowWidth,time_unit)
        recording_list.append(recording)
    eye_movement_signal = pd.concat(recording_list)
    return eye_movement_signal

def __CalcateVelocity(x,y,timestamp,windowWidth:int = 1, time_unit:str = "micro"):
    step = int(np.ceil(windowWidth/2))
    data_size = len(x)
    velocity_list = np.zeros(data_size)
    for i in range(data_size):
    
        # get initial interval
        if (step == windowWidth):
            startPos = i - step
            endPos = i
        else:
            startPos = i -step
            endPos = i + step
        
        # fine tune intervals
        if (startPos < 0 ):
            startPos = i;
        
        if (endPos > data_size):
            endPos = i
        
        if (x.iloc[endPos] is np.nan or x.iloc[startPos] is np.nan or
            y.iloc[endPos] is np.nan or y.iloc[startPos] is np.nan):
            velocity = np.nan
            continue
        
        ampl = np.sqrt(((x.iloc[endPos]-x.iloc[startPos])**2+(y.iloc[endPos]-y.iloc[startPos])**2))
        delta_t =(timestamp.iloc[endPos]-timestamp.iloc[startPos])
        time = __safe_div(delta_t,getTimeinSec(time_unit))   

             
        velocity = np.round(__safe_div(ampl,time),2)
        velocity_list[i] = velocity
    return velocity_list

def __safe_div(x,y):
    if y == 0:
        return 0
    return x / y

if __name__=="__main__":

    from scipy.io import arff
    from pandas.testing import assert_series_equal
    from sacanalysis import Load_gazecom
    # check multple recordings
    load_gazecom = Load_gazecom("C:/sacanalysis/gazecom_small/all_features")
    df_multiple_rec = load_gazecom.load_all_data(unit_for_time="Milli")
    list_of_rec = df_multiple_rec["source"].unique()
    rec_1 = df_multiple_rec[df_multiple_rec["source"]==list_of_rec[0]].drop(columns=(["source"]))
    rec_2 = df_multiple_rec[df_multiple_rec["source"]==list_of_rec[1]].drop(columns=(["source"]))
    rec_3 = df_multiple_rec[df_multiple_rec["source"]==list_of_rec[2]].drop(columns=(["source"]))
    
    df_multiple_rec_vel = GetVelocity(df_multiple_rec,timestamp_col="time")
    rec_1_vel = GetVelocity(rec_1,timestamp_col="time")
    rec_2_vel = GetVelocity(rec_2,timestamp_col="time")
    rec_3_vel = GetVelocity(rec_3,timestamp_col="time")  
    assert_series_equal(df_multiple_rec_vel["velocity"][df_multiple_rec["source"]==list_of_rec[0]],
                        rec_1_vel["velocity"],check_less_precise=True,check_names=False)
    assert_series_equal(df_multiple_rec_vel["velocity"][df_multiple_rec["source"]==list_of_rec[1]],
                        rec_2_vel["velocity"],check_less_precise=True,check_names=False)
    assert_series_equal(df_multiple_rec_vel["velocity"][df_multiple_rec["source"]==list_of_rec[2]],
                        rec_3_vel["velocity"],check_less_precise=True,check_names=False)
    
    subdf = df_multiple_rec_vel[df_multiple_rec["source"]==list_of_rec[1]]
    
    # Check single recording
    data, meta = arff.loadarff(r"C:/sacanalysis/gazecom_small/all_features/beach/AAF_beach.arff")
    df_original = pd.DataFrame(data)       
    df_original[df_original["confidence"]==0] = np.nan
    vel_df = GetVelocity(df_original,timestamp_col="time")
    vel_df = vel_df.dropna()
    original = vel_df["velocity"]
    mine = vel_df["velocity"]
    test2 = original!=mine
    test = original.equals(mine)
    diff = original-mine
    test3 = assert_series_equal(original,mine,check_less_precise=True,check_names=False)
    errors = vel_df[["time","x","y","speed_1","velocity"]][test2]
    
