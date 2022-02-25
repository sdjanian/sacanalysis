from sacanalysis import Preproccesing, SaccadeAnalysis
import pandas as pd

if __name__ == "__main__":
    """
    Run this script after installation to test 
    """
    test_df = pd.read_csv("test_data.csv")
    test_df = test_df.rename(columns = {"speed_1":"velocity"})
    #test_df = test_df.drop(columns = ["source"])
    Preprocess = Preproccesing(test_df)
    processed_saccades = Preprocess.GetPreprocessedSaccades()
    average_saccade = Preprocess.GetAverageSaccade()
    histogram_velocity_vector = Preprocess.GetHistogramVectors()    
    _SaccadeAnalysis = SaccadeAnalysis(processed_saccades,average_saccade,histogram_velocity_vector)
    scores = _SaccadeAnalysis.GetScores()
    print("sacanalysis installed correctly")