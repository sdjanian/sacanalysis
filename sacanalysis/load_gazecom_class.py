import glob
import pandas as pd
from scipy.io import arff
import timeit
import tqdm
import math
import warnings
import os


class Load_gazecom:
    _CLEAN_TIME_LIMIT = 21 * 1e6
    class_label_gazecom = {0: 'Unknown',
                     1: 'Fixation',
                     2: 'Saccade',
                     3: 'Smooth Pursuit',
                     4: 'Noise'}
    
    class_event_gazecom = {'Unknown':0,
                    'Fixation':1,
                    'Saccade':2,
                    'Smooth Pursuit':3,
                    'Noise':4}
       
    def __init__(self, GAZECOM_PATH = 'GazeCom_Data\\all_features'):
        """
        :param GAZECOM_PATH: Path where the GazeCom dataset is located. By default set to '\GazeCom_Data\all_features'
        """
        self.GAZECOM_PATH = GAZECOM_PATH
      
    #@profile  
    def load_all_data(self,keys = None,unit_for_time = "micro"):
        """
        Prepares the data by parsing throught the GazeCom database sequentially and splitting each session into windows.
        prints the time it takes. You can download the GazeCom dataset at http://michaeldorr.de/smoothpursuit/deep_eye_movement_classification_package.zip
        and is located in:
            deep_eye_movement_classification_package -> data -> inputs -> GazeCom_all_features.zip
        x
        :return: processed_data_seq which is a list of the processed data in the form of
        [window_list_session1,label_list_session1,session_1_path,...] repeating. This needs to be unpacked by unpackProcessedData()
                      
        """  
        if not glob.glob(self.GAZECOM_PATH):
            print("Folder not found:",self.GAZECOM_PATH)
            return
        df = pd.DataFrame()
        start_time = timeit.default_timer()
        temp_list = []
        for video in tqdm.tqdm(glob.glob(self.GAZECOM_PATH+'/*'),position=1,leave=True,desc = "Loading GazeCom"):
            for session in glob.glob(video+'/*'):
                data, meta = arff.loadarff(session)
                # Resamples SSK to 250 Hz from 500 Hz
                if "SSK_" in session:
                    data = data[::2]
                else:
                    #data = data[data['time'] <= CLEAN_TIME_LIMIT]
                    None
                ppd_f = self._calculate_ppd()
                normalize_keys = [             
                     "x",
                     "y",
                     "speed_1",            
                     "acceleration_1",
                     "speed_2",
                     "acceleration_2",
                     "speed_4",
                     "acceleration_4",
                     "speed_8",
                     "acceleration_8",
                     "speed_16",
                     "acceleration_16"
                     ]
                #data = arff_obj["data"]
                for k in normalize_keys:
                    data[k] /= ppd_f
                
                if (data["speed_1"] > 20000).any():
                    #print(i)
                    None
                df_temp = pd.DataFrame(data)
                if unit_for_time == "milli":
                    df_temp["time"] = df_temp["time"]/1000.0 # Convert from micro seconds to milli seconds
                df_temp["source"] =[session]*len(df_temp)
                
                def getStimuliStr(x):
                    stimuli_str = x.split("\\")[-1].split(".")[0].split("_")[1:]
                    
                    if type(stimuli_str) is list:
                        stimuli_str = "_".join(stimuli_str)
                    return stimuli_str
                
                df_temp["subject"] = df_temp["source"].apply(lambda x :x.split("\\")[-1].split(".")[0].split("_")[0])
                df_temp["stimuli"] = df_temp["source"].apply(lambda x :getStimuliStr(x))   
                #df = df.append(df_temp)
                #print("List:", temp_list)
                temp_list.append(df_temp)
                #i = i + 1
        df = pd.concat(temp_list)    
        self.df = df        
        print("Sequence time: ",timeit.default_timer() - start_time)     
        return df    
    
    def saveRecordingsAsIndividualFiles(self,df=None,path=None,columns = ['subject','stimuli','time', 'x', 'y', 'speed_1', 'handlabeller_final']):
        
        #Either pass a dataframe or use the default df
        if df==None:
            df = self.df
        else:
            None
        if path==None:
            current_dir = os.getcwd()
            save_dir = os.path.join(current_dir, 'GazeComIndiviualFiles')
        else:
            save_dir =path
        if not os.path.isdir(save_dir):
            os.makedirs(save_dir)
        #df_recordings = df.groupby(["subject","stimuli"])
        df_recordings = [grp for di, grp in df.groupby(["subject","stimuli"])]
        for df_recording in tqdm.tqdm(df_recordings,desc="Saving individual recordings",position=0,leave=True):
            df_to_save = df_recording[columns]
            df_to_save.to_csv(os.path.join(save_dir,"_".join([df_recording["subject"].iloc[0],df_recording["stimuli"].iloc[1]])+".csv"))
            
        
    
    @staticmethod
    def _calculate_ppd(skip_consistency_check=False):
        """
        Original code from https://github.com/MikhailStartsev/sp_tool/blob/master/util.py and has been rewritten to fit this code.
        Documentation copy pasted from original code:
            
        Pixel-per-degree value is computed as an average of pixel-per-degree values for each dimension (X and Y).
    
        :param arff_object: arff object, i.e. a dictionary that includes the 'metadata' key.
                    @METADATA in arff object must include "width_px", "height_px", "distance_mm", "width_mm" and
                    "height_mm" keys for successful ppd computation.
        :param skip_consistency_check: if True, will not check that the PPD value for the X axis resembles that of
                                       the Y axis
        :return: pixel per degree.
    
        """
        """
        # Previous version of @METADATA keys, now obsolete
        calculate_ppd.OBSOLETE_METADATA_KEYS_MAPPING = {
            'PIXELX': ('width_px', lambda val: val),
            'PIXELY': ('height_px', lambda val: val),
            'DIMENSIONX': ('width_mm', lambda val: val * 1e3),
            'DIMENSIONY': ('height_mm', lambda val: val * 1e3),
            'DISTANCE': ('distance_mm', lambda val: val * 1e3)
        }
    
        for obsolete_key, (new_key, value_modifier) in calculate_ppd.OBSOLETE_METADATA_KEYS_MAPPING.iteritems():
            if obsolete_key in arff_object['metadata'] and new_key not in arff_object['metadata']:
                warnings.warn('Keys {} are obsolete and will not necessarily be supported in future. '
                              'Consider using their more explicit alternatives: {}'
                              .format(calculate_ppd.OBSOLETE_METADATA_KEYS_MAPPING.keys(),
                                      [val[0] for val in calculate_ppd.OBSOLETE_METADATA_KEYS_MAPPING.values()]))
                # replace the key
                arff_object['metadata'][new_key] = value_modifier(arff_object['metadata'].pop(obsolete_key))
        
    
        """
        width_px = 1280.0
        height_px = 720.0
        width_mm = 400.0
        height_mm = 225.0
        distance_mm = 450.0
        theta_w = 2 * math.atan(width_mm /
                                (2 * distance_mm)) * 180. / math.pi
        theta_h = 2 * math.atan(height_mm /
                                (2 * distance_mm)) * 180. / math.pi
    
        ppdx = width_px / theta_w
        ppdy = height_px / theta_h
    
        ppd_relative_diff_thd = 0.2
        if not skip_consistency_check and abs(ppdx - ppdy) > ppd_relative_diff_thd * (ppdx + ppdy) / 2:
            warnings.warn('Pixel-per-degree values for x-axis and y-axis differ '
                          'by more than {}% in source file {}! '
                          'PPD-x = {}, PPD-y = {}.'.format(ppd_relative_diff_thd * 100,
                                                           "temp",
                                                           ppdx, ppdy))
        return (ppdx + ppdy) / 2
          
if __name__ == "__main__":
    load_gazecom = Load_gazecom(GAZECOM_PATH = '..\GazeCom_Data\\all_features')
    df = load_gazecom.load_all_data()
    load_gazecom.saveRecordingsAsIndividualFiles(path=r"\output")
