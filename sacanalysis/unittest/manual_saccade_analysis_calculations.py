import pandas as pd
import numpy as np
from sacanalysis import Load_gazecom, Preproccesing, SaccadeAnalysis, CalculateEventDurationClass, plotRankedSaccades
from scipy import stats

if __name__ == '__main__':
    #unittest.main()
    
    manual_calculated_average_saccade = pd.read_csv("20_ms_average_saccade_manual_calculation.csv")
    four_saccades_for_input = pd.read_csv("four_20_ms_saccades.csv")
    four_saccades_correct_output = pd.read_csv("four_20_ms_saccades_preprocessed_output.csv")
    Preprocess = Preproccesing(four_saccades_for_input)
    processed_saccades = Preprocess.GetPreprocessedSaccades()
    processed_average_saccade = Preprocess.GetAverageSaccade()
    
    sac_1 = processed_saccades.iloc[0:6]
    sac_2 = processed_saccades.iloc[6:12]    
    sac_3 = processed_saccades.iloc[12:18]
    sac_4 = processed_saccades.iloc[18:24]        
    
    scores = pd.DataFrame({"unique_saccade_number":[],
                           "source":[],
                           "residual_sum_x_z_trans":[],
                           "residual_sum_x_norm_up":[],
                           "residual_sum_velocity":[],
                           "flatness_score":[],
                           "vector":[],
                           "dipvalue_score":[],
                           "entropy_score":[],
                           "kurtosis_score":[],
                           "skew_score":[]})
    scores = scores.append(pd.Series(), ignore_index=True)
    scores = scores.append(pd.Series(), ignore_index=True)
    scores = scores.append(pd.Series(), ignore_index=True)
    scores = scores.append(pd.Series(), ignore_index=True)


    scores["unique_saccade_number"].iloc[0]= sac_1["unique_saccade_number"].iloc[0]
    scores["unique_saccade_number"].iloc[1] = sac_2["unique_saccade_number"].iloc[0]
    scores["unique_saccade_number"].iloc[2] = sac_3["unique_saccade_number"].iloc[0]
    scores["unique_saccade_number"].iloc[3] = sac_4["unique_saccade_number"].iloc[0]


    scores["residual_sum_x_z_trans"].iloc[0] = np.mean(abs(sac_1["x_z_trans"].values - manual_calculated_average_saccade["x_z_trans"].values))
    scores["residual_sum_x_z_trans"].iloc[1] = np.mean(abs(sac_2["x_z_trans"].values - manual_calculated_average_saccade["x_z_trans"].values))
    scores["residual_sum_x_z_trans"].iloc[2] = np.mean(abs(sac_3["x_z_trans"].values - manual_calculated_average_saccade["x_z_trans"].values))
    scores["residual_sum_x_z_trans"].iloc[3] = np.mean(abs(sac_4["x_z_trans"].values - manual_calculated_average_saccade["x_z_trans"].values))

    scores["residual_sum_x_norm_up"].iloc[0] =  np.mean(abs(sac_1["x_norm_up"].values - manual_calculated_average_saccade["x_norm_up"].values))
    scores["residual_sum_x_norm_up"].iloc[1] =  np.mean(abs(sac_2["x_norm_up"].values - manual_calculated_average_saccade["x_norm_up"].values))
    scores["residual_sum_x_norm_up"].iloc[2] =  np.mean(abs(sac_3["x_norm_up"].values - manual_calculated_average_saccade["x_norm_up"].values))
    scores["residual_sum_x_norm_up"].iloc[3] =  np.mean(abs(sac_4["x_norm_up"].values - manual_calculated_average_saccade["x_norm_up"].values))

    scores["residual_sum_velocity"].iloc[0] =  np.mean(abs(sac_1["velocity_norm"].values - manual_calculated_average_saccade["velocity_norm"].values))
    scores["residual_sum_velocity"].iloc[1] =  np.mean(abs(sac_2["velocity_norm"].values - manual_calculated_average_saccade["velocity_norm"].values))
    scores["residual_sum_velocity"].iloc[2] =  np.mean(abs(sac_3["velocity_norm"].values - manual_calculated_average_saccade["velocity_norm"].values))
    scores["residual_sum_velocity"].iloc[3] =  np.mean(abs(sac_4["velocity_norm"].values - manual_calculated_average_saccade["velocity_norm"].values))

    scores.to_csv("scores_four_saccades_manually_calculated.csv")

    #unique_saccade_number,source,residual_sum_x_z_trans,residual_sum_x_norm_up,residual_sum_velocity,flatness_score,vector,dipvalue_score,entropy_score,kurtosis_score,skew_score,bfvalue_score,ranked_residual_sum_x_z_trans,ranked_residual_sum_x_norm_up,ranked_residual_sum_velocity,ranked_flatness_score,ranked_dipvalue_score,ranked_entropy_score,ranked_kurtosis_score,ranked_skew_score
    
    