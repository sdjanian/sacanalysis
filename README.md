# Manualy labelled saccade analysis

These are scientific scripts for how well saccades have been labelled. It uses the GazeCom dataset but another dataset can be used as long as the dataframe used is in the correct format.

## Dependencies

* `Python 3.6` and packages specificed in `setup.py`. Currently only compatible with `pandas 0.23.4`.

There are three dependencies to be aware of:
* `modality` 
Is used to perform [Hartigan's Diptest for Unimodality](https://github.com/alimuldal/diptest). It requries you to have OpenMPI installed which can be found [here](https://www.microsoft.com/en-us/download/details.aspx?id=57467). Only OpenMPI 10.0 has been checked to work.

* `rpy2`
Is used as an interface R. It requires R to be installed. This can be done with `conda install -c r rpy2` or `pip install rpy2`. When using conda it will also install a separate version of R in the environment while pip will only install `rpy2`. 

* ```madness, mixAK, dplyr```
R packages used for rjmcmc.py. They will automatically be installed if missing. They can also be manually installed through R or Rstudio if needed.


## Installation

### Windows
Download installation at `https://github.com/Kongskrald/sacanalysis/archive/master.zip` and unzip.

Recommended to create a conda environment first `conda create --name saccade_analysis python=3.6`.

Install ´rpy2´. It is recommended to use conda.
`conda install -c r rpy2`

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

### Test if installed correctly
Run `test/test_sacanalysis.py`. If there are no errors it is installed correctly.
### Common bugs

* `OSError: cannot load library 'C:\Program Files\R\R-4.0.2\bin\x64\R.dll': error 0x7e` R is not installed. Look under `rpy2` in installation guide.

* `rpy2` bugs are caused by wrong pathing. To check if pathing it is a pathing error run
```python
import rpy2.situation as situation
for row in situation.iter_info():
    print(row)
```
and look for `R_HOME`. The path to the R folder can be manually set with 
```python
import os
os.environ["R_HOME"] = PATH_TO_R
```

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
* In `main.py` set the path argument in `Load_gazecom(GAZECOM_PATH=YOURPATH)` in `main.py` to be your path to the GazeCom data leading to the feature e.g. `../GazeCom_Data/all_features`. Alternativly place the GazeCom folder at the level before this `main.py` as that is it's default pathing.
* In `main.py` set `produce_plots_bool` to `True` if plots for all saccades for all metrics is wanted. By default it is `False`.
and then run `main.py`


## Citation
How to cite ...

## Author
Shagen Djanian
2020-09-11
