# Manualy labelled saccade analysis

These are scientific scripts for how well saccades have been labelled. It uses the GazeCom dataset but another dataset can be used as long as the dataframe used is in the correct format. The GazeCom dataset can be found [here](http://michaeldorr.de/smoothpursuit/deep_eye_movement_classification_package.zip). The correct folder can be found at deep_eye_movement_classification_package --> data --> inputs --> GazeCom_all_features.zip. If default pathing is wanted place the GazeCom_all_features folder in the same folder as ```python main.py```.

This is an example of how the data should be formated with corresponding column names. It contains the time of the recording in miliseconds, the and x and y coordinates of the eye movements, handlabeller_final is the eye movement class, the velocity and source is the file name and subject is the subjects identifier.
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
The module contains the following.```python load_gazecom_class.py``` is responsible for loading the GazeCom dataset into a dataframe in correct format. ```python caculateEvents.py``` generates an additional dataframe by using the output of ```python load_gazecom_class.py``` that contains information on the event level. ```python preprocessing.py``` prepares the GazeCom dataframe for analysis. An average composite saccade for each duration is computed as is various transformation and selection of saccades. ```python saccade_analysis.py``` performs the calculation of the various metrics for each saccade described in the paper. ```python saccade_plots.py``` contains the code for producing the pages of saccades ranked according to their metrics. Lastly ```python test_sacanalysis.py``` is a script written to test that the module has been installed correctly.

## Dependencies

* `Python 3.6` and packages specificed in `setup.py`. Currently only compatible with `pandas 0.23.4`.

There are one dependencies to be aware of:
* `modality` 
Is used to perform [Hartigan's Diptest for Unimodality](https://github.com/alimuldal/diptest). It requries you to have OpenMPI installed which can be found [here](https://www.microsoft.com/en-us/download/details.aspx?id=57467). Only OpenMPI 10.0 has been checked to work.


## Installation

### Windows
Download installation at `https://github.com/sdjanian/sacanalysis/archive/master.zip` and unzip.

Recommended to create a conda environment first `conda create --name saccade_analysis python=3.6`.

In the terminal change the diretory to where the master was unpanked and run. Recommended to use
```python
cd PATH
pip install .
```

Alternatively it can also be installed with using setup.py install instead.
```python
cd PATH
python setup.py install
```
### Quick Windows install
In conda promt copy paste this snippit and change PATH to the master directory:
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
* In `main.py` set `produce_plots_bool` to `False` if plots for all saccades for all metrics is wanted is not wanted. By default it is `True`.
and then run `main.py`


## Citation
How to cite ...

## Author
Shagen Djanian
2020-09-11

