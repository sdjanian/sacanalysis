import pandas as pd
import numpy as np
from .time_units import getTimeinSec

def GetVelocity(eye_movement_signal:pd.DataFrame,timestamp_col:str,windowsWidth:int = 1, time_unit:str = "micro"):    
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
    
    try:
        x = eye_movement_signal["x"]
        y = eye_movement_signal["y"]
    except KeyError:
        print("Either column x or y is missing from eye_movement_signal")
    
    if "velocity" in eye_movement_signal:
        raise Exception("Velocity already exists")

    x = eye_movement_signal["x"]
    y = eye_movement_signal["y"]
    velocity_list = np.zeros(len(eye_movement_signal))
    windowWidth = 1
    step = int(np.ceil(windowWidth/2))
    data_size = len(eye_movement_signal)
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
        
        if (x[endPos] is np.nan or x[startPos] is np.nan or
            y[endPos] is np.nan or y[startPos] is np.nan):
            velocity = np.nan
            continue
        
        # invalid interval
        #if (startPos == endPos):
        #    break;
        ampl = np.sqrt(((x[endPos]-x[startPos])**2+(y[endPos]-y[startPos])**2))
        if timestamp_col != None:
            delta_t =(eye_movement_signal[timestamp_col].iloc[endPos]-eye_movement_signal[timestamp_col].iloc[startPos])
            time = __safe_div(delta_t,getTimeinSec(time_unit))   
        else:
            raise Exception("timestamp_col not defined")
             
        velocity = np.round(__safe_div(ampl,time),2)
        velocity_list[i] = velocity
    
    eye_movement_signal["velocity"] = velocity_list
    return eye_movement_signal

def __safe_div(x,y):
    if y == 0:
        return 0
    return x / y

if __name__=="__main__":
    """
    df = pd.DataFrame({"x":[1,1,1,1,1,1,2,2,2,2,2,3,3,3,3,6,7,8,8,9,9,9,9,9,7,7,7,5,5,4,3,22,2],
                       "y":[5,5,5,6,6,6,30,30,7,7,7,24,25,24,23,50,30,50,8,9,5,3,7,10,11,23,24,52,54,52,56,52,32]})
    
    test =shift(df["x"],4,cval=np.NaN)


    x1 = 590.9
    y1 = 5.2
    
    x2 = 590.6
    y2 = 5.0
    """
    from scipy.io import arff

    data, meta = arff.loadarff(r"C:\GazeCom_Data\all_features\beach\AAF_beach.arff")
    df_original = pd.DataFrame(data)   
    #example = (np.sqrt((x2-x1)**2)+np.sqrt((y2-y1)**2))/(4000/1000000)
    df_original[df_original["confidence"]==0] = np.nan
    vel_df = GetVelocity(df_original,timestamp_col="time")
    vel_df = vel_df.dropna()
    from pandas.testing import assert_series_equal
    original = vel_df["speed_1"]
    mine = vel_df["velocity"]
    test2 = original!=mine
    test = original.equals(mine)
    diff = original-mine
    test3 = assert_series_equal(original,mine,check_less_precise=True,check_names=False)
    errors = vel_df[["time","x","y","speed_1","velocity"]][test2]
    
