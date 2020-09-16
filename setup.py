from setuptools import setup, find_packages

print(find_packages())
setup(
    author="Shagen Djanian",
    author_email="s.d@hotmail.dk",
    name='sacanalysis',
    license="MIT",
    description='sacanalysis is a package to analyse the quality of saccade and find potentially incorrect saccades.',
    version='v0.0.2',
    url='https://github.com/Kongskrald/sacanalysis',
    packages=find_packages(),
    py_modules=['load_gazecom_class','saccade_plot','saccade_analysis'],
    python_requires=">=3.6",
    install_requires=['matplotlib','numpy>=1.15','tqdm','scipy','seaborn','pandas>=0.23.4',
    'modality @ https://github.com/kjohnsson/modality/archive/master.zip#egg=modality-1.1'],
    include_package_data=True,
    package_data={'': ['test/*.csv']}
)