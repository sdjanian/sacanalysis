import pandas as pd
import numpy as np
from sacanalysis import Load_gazecom, Preproccesing, SaccadeAnalysis, CalculateEventDurationClass, plotRankedSaccades
from scipy import stats

if __name__ == '__main__':
    #unittest.main()
    
    df = pd.read_csv("test_saccades.csv") 
    preprocess_class = Preproccesing(df,time_unit="milli")
    #get1 = preprocess_class.GetPreprocessedSaccades()
    # saccade 1
    x_1 = df["x"].iloc[0:6].values
    x_1_mean = x_1.mean()
    x_1_norm = x_1-x_1_mean
    
    y_1 = df["y"].iloc[0:6].values
    y_1_mean = y_1.mean()
    y_1_norm = y_1-y_1_mean

    velocity_1 = df["velocity"].iloc[0:6].values
    velocity_1_mean = velocity_1.mean()
    velocity_1_norm = velocity_1-velocity_1_mean    
    
    ampl_1 = x_1[0]-x_1[-1] # ampl_1 is <0 so it is not flipped
    
    x_1_norm_up = x_1_norm
    z_score_1 = stats.zscore(x_1_norm_up)

    # saccade 2
    x_2 = df["x"].iloc[6:12].values
    x_2_mean = x_2.mean()
    x_2_norm = x_2-x_2_mean
    
    y_2 = df["y"].iloc[6:12].values
    y_2_mean = y_2.mean()
    y_2_norm = y_2-y_2_mean

    velocity_2 = df["velocity"].iloc[6:12].values
    velocity_2_mean = velocity_2.mean()
    velocity_2_norm = velocity_2-velocity_2_mean    
    
    ampl_2 = x_2[0]-x_2[-1] 
    x_2_norm_up = x_2_norm # ampl_2 is <0 so it is not flipped
    z_score_2 = stats.zscore(x_2_norm_up)
    
    # saccade 3
    x_3 = df["x"].iloc[12:18].values
    x_3_mean = x_3.mean()
    x_3_norm = x_3-x_3_mean
    
    y_3 = df["y"].iloc[12:18].values
    y_3_mean = y_3.mean()
    y_3_norm = y_3-y_3_mean

    velocity_3 = df["velocity"].iloc[12:18].values
    velocity_3_mean = velocity_3.mean()
    velocity_3_norm = velocity_3-velocity_3_mean    
    
    ampl_3 = x_3[0]-x_3[-1] # ampl_3 is <0 so it is not flipped
    
    x_3_norm_up = x_3_norm
    z_score_3 = stats.zscore(x_3_norm_up)
    
    # saccade 4
    x_4 = df["x"].iloc[18:24].values
    x_4_mean = x_4.mean()
    x_4_norm = x_4-x_4_mean
    
    y_4 = df["y"].iloc[18:24].values
    y_4_mean = y_4.mean()
    y_4_norm = y_4-y_4_mean

    velocity_4 = df["velocity"].iloc[18:24].values
    velocity_4_mean = velocity_4.mean()
    velocity_4_norm = velocity_4-velocity_4_mean    
    
    ampl_4 = x_4[0]-x_4[-1] # ampl_4 is >0 so it is not flipped
    
    x_4_norm_up = x_4_norm*-1
    z_score_4 = stats.zscore(x_4_norm_up)
    
    
    mean_sac_x = [None]*6
    mean_sac_x_norm_up = [None]*6
    mean_sac_vel = [None]*6
    for i in np.arange(0,6): 
        mean_sac_x[i] = np.mean([x_1[i],x_2[i],x_3[i],x_4[i]])
        mean_sac_x_norm_up[i] = np.mean([x_1_norm_up[i],x_2_norm_up[i],x_3_norm_up[i],x_4_norm_up[i]])
        mean_sac_vel[i] = np.mean([velocity_1_norm[i],velocity_2_norm[i],velocity_3_norm[i],velocity_4_norm[i]])
    
    mean_sac_z = stats.zscore(mean_sac_x_norm_up)
    df_mean_sac = pd.DataFrame({"x_z_trans":mean_sac_z,"x_norm_up":mean_sac_x_norm_up,"velocity_norm":mean_sac_vel})
    df_mean_sac.to_csv("20_ms_average_saccade_manual_calculation.csv")
    
    df_four_saccades = df.iloc[0:24]
    df_four_saccades.to_csv("four_20_ms_saccades.csv")
    df_four_saccades["x_norm"] = np.concatenate((x_1_norm,x_2_norm,x_3_norm,x_4_norm),axis=None)
    df_four_saccades["y_norm"] = np.concatenate((y_1_norm,y_2_norm,y_3_norm,y_4_norm),axis=None)
    df_four_saccades["velocity_norm"] = np.concatenate((velocity_1_norm,velocity_2_norm,velocity_3_norm,velocity_4_norm),axis=None)
    df_four_saccades["x_norm_up"] = np.concatenate((x_1_norm_up,x_2_norm_up,x_3_norm_up,x_4_norm_up),axis=None)
    df_four_saccades["x_z_trans"] = np.concatenate((z_score_1,z_score_2,z_score_3,z_score_4),axis=None)
    df_four_saccades.to_csv("four_20_ms_saccades_preprocessed_output.csv")
    
    #preprocess_class = Preproccesing(df_four_saccades,time_unit="milli")
    #get1 = preprocess_class.GetPreprocessedSaccades() 
