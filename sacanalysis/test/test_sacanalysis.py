from sacanalysis import Preproccesing, SaccadeAnalysis
import pandas as pd

if __name__ == "__main__":
    test_df = pd.read_csv("test_data.csv")
    #test_df = test_df.drop(columns = ["source"])
    Preprocess = Preproccesing(test_df)
    processed_saccades = Preprocess.GetPreprocessedSaccades()
    average_saccade = Preprocess.GetAverageSaccade()
    histogram_velocity_vector = Preprocess.GetHistogramVectors()    
    _SaccadeAnalysis = SaccadeAnalysis(processed_saccades,average_saccade,histogram_velocity_vector)
    print("sacanalysis installed correctly")