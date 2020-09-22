import unittest
import pandas as pd
from pandas.testing import assert_frame_equal
from pandas.testing import assert_series_equal
from sacanalysis import Load_gazecom, Preproccesing, SaccadeAnalysis, CalculateEventDurationClass, plotRankedSaccades

class TestPreprocess(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manual_calculated_average_saccade = pd.read_csv("20_ms_average_saccade_manual_calculation.csv")
        cls.two_saccades_for_input = pd.read_csv("two_20_ms_saccades.csv")
        cls.two_saccades_correct_output = pd.read_csv("two_20_ms_saccades_preprocessed_output.csv")
        cls.Preprocess = Preproccesing(cls.two_saccades_for_input)
        cls.processed_saccades = cls.Preprocess.GetPreprocessedSaccades()
        cls.processed_average_saccade = cls.Preprocess.GetAverageSaccade()
        
    def test_x_norm(self):
        assert_series_equal(self.two_saccades_correct_output["x_norm"].reset_index(drop=True),
                            self.processed_saccades["x_norm"].reset_index(drop=True),check_less_precise = True)
    def test_y_norm(self):
        assert_series_equal(self.two_saccades_correct_output["y_norm"].reset_index(drop=True),
                            self.processed_saccades["y_norm"].reset_index(drop=True),check_less_precise = True)

    def test_x_norm_up(self):
        assert_series_equal(self.two_saccades_correct_output["x_norm_up"].reset_index(drop=True),
                            self.processed_saccades["x_norm_up"].reset_index(drop=True),check_less_precise = True)    
        
    def test_velocity_norm(self):
        assert_series_equal(self.two_saccades_correct_output["velocity_norm"].reset_index(drop=True),
                            self.processed_saccades["velocity_norm"].reset_index(drop=True),check_less_precise = True)        

    def test_z_score_norm_up(self):
        assert_series_equal(self.two_saccades_correct_output["x_z_trans"].reset_index(drop=True),
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


if __name__ == '__main__':
    unittest.main()
    """
    manual_calculated_average_saccade = pd.read_csv("20_ms_average_saccade_manual_calculation.csv")
    two_saccades_for_input = pd.read_csv("two_20_ms_saccades.csv")
    two_saccades_correct_output = pd.read_csv("two_20_ms_saccades_preprocessed_output.csv")
    Preprocess = Preproccesing(two_saccades_for_input)
    processed_saccades = Preprocess.GetPreprocessedSaccades()
    processed_average_saccade = Preprocess.GetAverageSaccade()
    """
