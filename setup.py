from setuptools import setup, find_packages

setup(
    author="Shagen Djanian",
    author_email="s.d@hotmail.dk",
    name='sacanalysis',
    license="MIT",
    description='chocobo is a python package for delicious chocobo recipes.',
    version='v0.0.1',
    url='https://github.com/Kongskrald/GazeComCritique',
    packages=find_packages(),
    py_modules=['load_gazecom_class','saccade_plot','saccade_analysis'],
    python_requires=">=3.6",
    install_requires=['matplotlib','numpy>=1.15','tqdm','scipy','seaborn','modality>=1.1','pandas==0.23.4'],
    dependency_links =['https://github.com/kjohnsson/modality/archive/master.zip#egg=modality-1.1'],
)