# Manualy labelled saccade analysis
This repository contains Python code that performs the analysis for a recently submitted manuscript entitled ” A Method for the Detection of Poorly-Formed or Misclassified Saccades: A case study using the GazeCom Dataset.” The authors on the paper are Lee Friedman, Shagen Djanian and Oleg V. Komogortsev. The author of the code is Shagen Djanian. The manuscript is currently under review by the journal Behavior Research Methods. 

## Abstract for "A Method for the Detection of Poorly-Formed or Misclassified Saccades: A case study using the GazeCom Dataset"
There are many automatic methods for the detection of eye movement types like fixation and saccades. Evaluating the accuracy of these methods can be a difficult and time-consuming process. We present a method to detect misclassified or poorly formed saccades, regardless of how they were classified. We developed and tested our method on saccades from the very large and publicly available GazeCom dataset. We started out by creating a total of 9 metrics (velocity shape, velocity shape amplitude, position shape, position shape amplitude, flatness, entropy, kurtosis, skewness, and the Dip Test statistic of multimodality) which will be explained below. We applied these metrics to horizontal saccades of 20, 40 and 60 ms duration. For each duration, we performed a data reduction step with factor analysis to see how these 9 metrics were naturally grouped. For every duration, there were 2 factors, one which was dominated by our velocity shape metric and one which was dominated by our entropy metric. We determined that the entropy metric was the single most valuable metric for detecting misclassified saccades. We illustrate the types of saccades that our entropy metric indicates were misclassified.

## Dataset
Our analysis is based on the GazeCom dataset. The scripts in this repository use the GazeCom dataset but another dataset can be used as long as the dataframe used is in the correct format. The GazeCom dataset can be found [here](http://michaeldorr.de/smoothpursuit/deep_eye_movement_classification_package.zip). The correct folder can be found at deep_eye_movement_classification_package --> data --> inputs --> GazeCom_all_features.zip. If default pathing is wanted, place the GazeCom_all_features folder in the same folder as ```main.py```.

This is an example of how the data should be formated with corresponding column names. It contains the time of the recording in milliseconds, and the and x and y coordinates of the eye movements.  The column labelled “handlabeller_final” is the eye movement class, unknown as code 0, with fixation as code 1, saccades as code 2, smooth pursuit as code 3, and noise as code 4. “Velocity” is self-explanatory. In the GazeCom dataset they have multiple velocities named speed_1, speed_2 ... speed_16. We use speed_1 and rename it to velocity. “Source” is the file name and “subject” is the subject identifier.

% - 0 is UNKNOWN
% - 1 is FIX (fixation)
% - 2 is SACCADE
% - 3 is SP (smooth pursuit)
% - 4 is NOISE

| time  | x | y | handlabeller_final | velocity | source | subject |
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |------------- |
| 1  | 22.57  | 0.19  | 4  | 0  | GazeCom_Data\all_features\beach\AAF_beach.arff  |AAF  |
| 5  | 22.57  | 0.19  | 4  | 0  | GazeCom_Data\all_features\beach\AAF_beach.arff  |AAF  |
| 9   | 22.56  | 0.19  | 4  | 3.44  | GazeCom_Data\all_features\beach\AAF_beach.arff  |AAF  |
| 13  | 22.55  | 0.19  | 4  | 1.90  | GazeCom_Data\all_features\beach\AAF_beach.arff  |AAF  |
| 17  | 22.53  | 0.19  | 4  | 6.03  | GazeCom_Data\all_features\beach\AAF_beach.arff  |AAF  |
| 21  | 22.53  | 0.19  | 4  | 2.13  | GazeCom_Data\all_features\beach\AAF_beach.arff  |AAF  |
| 25  | 22.54  | 0.18  | 4  | 2.70  | GazeCom_Data\all_features\beach\AAF_beach.arff  |AAF  |
| 29  | 22.58  | 0.17  | 4  | 11.17  | GazeCom_Data\all_features\beach\AAF_beach.arff  |AAF  |
| 33  | 22.58  | 0.0  | 4  | 42.98  | GazeCom_Data\all_features\beach\AAF_beach.arff  |AAF  |
| 37  | 22.67  | 0.49  | 4  | 126.07  | GazeCom_Data\all_features\beach\AAF_beach.arff  |AAF  |

## Content

The module contains the following:
1.	```load_gazecom_class.py``` is responsible for loading the GazeCom dataset into a dataframe in correct format.
2.	```caculateEvents.py``` generates an additional dataframe by using the output of ```load_gazecom_class.py``` that contains information on the event level. 
3.	```preprocessing.py``` prepares the GazeCom dataframe for analysis. An average composite saccade for each duration is computed as are various transformations and selection of saccades.
4.	```saccade_analysis.py``` performs the calculation of the various metrics for each saccade described in the paper. 
5.	```saccade_plots.py``` contains the code for producing the pages of saccades (as pdf files) ranked according to their metrics. 
6.	Lastly ```test_sacanalysis.py``` is a script written to test that the module has been installed correctly.


## Dependencies

* `Python 3.6` and packages specificed in `setup.py`. Currently only compatible with `pandas 0.23.4`.

There are one dependencies to be aware of:
* `modality` 
Is used to perform [Hartigan's Diptest for Unimodality](https://github.com/alimuldal/diptest). It requries you to have OpenMPI installed which can be found [here](https://www.microsoft.com/en-us/download/details.aspx?id=57467). Only OpenMPI 10.0 has been checked to work.


## Installation

### Windows
1. Download installation at `https://github.com/sdjanian/sacanalysis/archive/master.zip` and unzip.

2. Recommended to create a conda environment first: `conda create --name saccade_analysis python=3.6`.

3. In the console change the diretory to where the master was unpanked and run. 
4. Recommended to use:
    ```python
    cd PATH
    pip install .
    ```

Alternatively it can also be installed with using `setup.py` install instead.
```python
cd PATH
python setup.py install
```
### Quick Windows install
In conda promt copy paste this snippet and change ```python PATH``` to the master directory:
```python
cd PATH
conda create --name saccade_analysis_test python=3.6 -y
conda activate saccade_analysis_test
conda install -c r rpy2 -y
pip install .
```
### Test if installed correctly
Run `test/test_sacanalysis.py`. If there are no errors it is installed correctly.
### Common bugs

* `from mpi4py import MPI : error: ImportError: DLL load failed:` OpenMPI not found. Most likely it is not installed.

* `pandas` errors are caused by a wrong pandas version. The correct version is 0.23.4. To check run
```python
import pandas as pd
print(pd.__version__)
```
## Usage
To perform the whole analysis run `main.py`. In conda prompt write
```
conda activate saccade_analysis
spyder
```
Before running `main.py` make sure:
* In `main.py` set the path argument in `Load_gazecom(GAZECOM_PATH=YOURPATH)` in `main.py` to be your path to the GazeCom data leading to the feature e.g. `../GazeCom_Data/all_features`. Alternativly place the GazeCom folder in the same folder as `main.py` as that is it's default pathing.
* In `main.py` set `produce_plots_bool` to `False` if plots for all saccades for all metrics is not wanted. By default it is `True`.
and then run `main.py`


## Citation
How to cite ...

## Author
Shagen Djanian \
Department of Computer Science \
Aalborg University \
Selma Lagerløfs Vej 300 \
Aalborg East, 9220, Denmark \
email: shagendj@cs.aau.dk \
2022-02-28 


