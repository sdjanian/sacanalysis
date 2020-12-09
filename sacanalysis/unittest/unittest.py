import unittest
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
pd.options.mode.chained_assignment = None
from pandas.testing import assert_frame_equal
from pandas.testing import assert_series_equal
from sacanalysis import Load_gazecom, Preproccesing, SaccadeAnalysis, CalculateEventDurationClass, plotRankedSaccades

class TestPreprocess(unittest.TestCase):   
    
    @classmethod
    def setUpClass(cls):
        cls.manual_calculated_average_saccade = pd.read_csv("20_ms_average_saccade_manual_calculation.csv")
        cls.four_saccades_for_input = pd.read_csv("four_20_ms_saccades.csv")
        cls.four_saccades_correct_output = pd.read_csv("four_20_ms_saccades_preprocessed_output.csv")
        cls.four_saccade_correct_vectors = pd.read_json("four_20_ms_saccade_vectors.json")
        cls.Preprocess = Preproccesing(cls.four_saccades_for_input)
        cls.processed_saccades = cls.Preprocess.GetPreprocessedSaccades()
        cls.processed_average_saccade = cls.Preprocess.GetAverageSaccade()
        cls.processed_saccade_vectors = cls.Preprocess.GetHistogramVectors()
        
    def test_x_norm(self):
        assert_series_equal(self.four_saccades_correct_output["x_norm"].reset_index(drop=True),
                            self.processed_saccades["x_norm"].reset_index(drop=True),check_less_precise = True)
    def test_y_norm(self):
        assert_series_equal(self.four_saccades_correct_output["y_norm"].reset_index(drop=True),
                            self.processed_saccades["y_norm"].reset_index(drop=True),check_less_precise = True)

    def test_x_norm_up(self):
        assert_series_equal(self.four_saccades_correct_output["x_norm_up"].reset_index(drop=True),
                            self.processed_saccades["x_norm_up"].reset_index(drop=True),check_less_precise = True)    
        
    def test_velocity_norm(self):
        assert_series_equal(self.four_saccades_correct_output["velocity_norm"].reset_index(drop=True),
                            self.processed_saccades["velocity_norm"].reset_index(drop=True),check_less_precise = True)        

    def test_z_score_norm_up(self):
        assert_series_equal(self.four_saccades_correct_output["x_z_trans"].reset_index(drop=True),
                            self.processed_saccades["x_z_trans"].reset_index(drop=True),check_less_precise = True)                
    
    def test_average_saccade_x_norm_up(self):
        assert_series_equal(self.manual_calculated_average_saccade["x_norm_up"].reset_index(drop=True),
                            self.processed_average_saccade["x_norm_up"].reset_index(drop=True),
                            check_names=False, check_index_type=False,check_less_precise = True)

    def test_average_saccade_x_z_trans(self):
        assert_series_equal(self.manual_calculated_average_saccade["x_z_trans"].reset_index(drop=True),
                            self.processed_average_saccade["x_z_trans"].reset_index(drop=True),
                            check_names=False, check_index_type=False,check_less_precise = True)
        
    def test_average_saccade_velocity_norm(self):
        assert_series_equal(self.manual_calculated_average_saccade["velocity_norm"].reset_index(drop=True),
                            self.processed_average_saccade["velocity_norm"].reset_index(drop=True),
                            check_names=False, check_index_type=False,check_less_precise = True)        

    def test_vector(self):
        assert_series_equal(self.four_saccade_correct_vectors["vector"].reset_index(drop=True),
                            self.processed_saccade_vectors["vector"].reset_index(drop=True),
                            check_names=False, check_index_type=False,check_less_precise = True)     
        
class TestSaccadeAnalysis(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.four_saccades_for_input = pd.read_csv("four_20_ms_saccades.csv")        
        cls.Preprocess = Preproccesing(cls.four_saccades_for_input)
        cls.processed_saccades = cls.Preprocess.GetPreprocessedSaccades()
        cls.processed_average_saccade = cls.Preprocess.GetAverageSaccade()
        cls.histogram_vectors = cls.Preprocess.GetHistogramVectors()
        cls.SacAnalysis = SaccadeAnalysis(cls.processed_saccades,
                                          cls.processed_average_saccade,
                                          cls.histogram_vectors)
        cls.scores = cls.SacAnalysis.GetScores()
        cls.scores = cls.scores.sort_values(by="unique_saccade_number")
        cls.scores_manually_calculated = pd.read_json("scores_four_saccades_manually_calculated.json")
        cls.scores_manually_calculated = cls.scores_manually_calculated.sort_values(by="unique_saccade_number")

        
   
    def test_residual_sum_x_z_trans(self):
        assert_series_equal(self.scores_manually_calculated["residual_sum_x_z_trans"].reset_index(drop=True),
                            self.scores["residual_sum_x_z_trans"].reset_index(drop=True),check_less_precise = True)

    def test_residual_sum_x_norm_up(self):
        assert_series_equal(self.scores_manually_calculated["residual_sum_x_norm_up"].reset_index(drop=True),
                            self.scores["residual_sum_x_norm_up"].reset_index(drop=True),check_less_precise = True)

    def test_residual_sum_velocity(self):
        assert_series_equal(self.scores_manually_calculated["residual_sum_velocity"].reset_index(drop=True),
                            self.scores["residual_sum_velocity"].reset_index(drop=True),check_less_precise = True)
        
     
        
    def test_vector(self):
        assert_series_equal(self.scores_manually_calculated["vector"].reset_index(drop=True),
                            self.scores["vector"].reset_index(drop=True),check_less_precise = True)       
        
    def test_entropy_score(self):
        assert_series_equal(self.scores_manually_calculated["entropy_score"].reset_index(drop=True),
                            self.scores["entropy_score"].reset_index(drop=True),check_less_precise = True) 
        
    def test_kurtosis_score(self):
        assert_series_equal(self.scores_manually_calculated["kurtosis_score"].reset_index(drop=True),
                            self.scores["kurtosis_score"].reset_index(drop=True),check_less_precise = True) 
        
    def test_skew_score(self):
        assert_series_equal(self.scores_manually_calculated["skew_score"].reset_index(drop=True),
                            self.scores["skew_score"].reset_index(drop=True),check_less_precise = True)  
        
    def test_flatness_score(self):
        assert_series_equal(self.scores_manually_calculated["flatness_score"].reset_index(drop=True),
                            self.scores["flatness_score"].reset_index(drop=True),check_less_precise = True)      
        
    def test_residual_sum_velocity_z_trans(self):
        assert_series_equal(self.scores_manually_calculated["residual_sum_velocity_z_trans"].reset_index(drop=True),
                            self.scores["residual_sum_velocity_z_trans"].reset_index(drop=True),check_less_precise = True)           
if __name__ == '__main__':
    unittest.main()
    
    """
    manual_calculated_average_saccade = pd.read_csv("20_ms_average_saccade_manual_calculation.csv")
    four_saccades_for_input = pd.read_csv("four_20_ms_saccades.csv")
    four_saccades_correct_output = pd.read_csv("four_20_ms_saccades_preprocessed_output.csv")
    scores_correct_output = pd.read_json("scores_four_saccades_manually_calculated.json")
    four_saccade_correct_vectors = pd.read_json("four_20_ms_saccade_vectors.json")

    Preprocess = Preproccesing(four_saccades_for_input)
    processed_saccades = Preprocess.GetPreprocessedSaccades()
    processed_average_saccade = Preprocess.GetAverageSaccade()
    histogram_vectors = Preprocess.GetHistogramVectors()
    SacAnalysis = SaccadeAnalysis(processed_saccades,
                                      processed_average_saccade,
                                      histogram_vectors)
    scores = SacAnalysis.GetScores() 
    """
    
    
    
