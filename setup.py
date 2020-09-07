import setuptools

setuptools.setup(
    author="Shagen Djanian",
    author_email="s.d@hotmail.dk",
    name='sacanalysis',
    license="MIT",
    description='chocobo is a python package for delicious chocobo recipes.',
    version='v0.0.1',
    url='https://github.com/Kongskrald/GazeComCritique',
    packages=["sacanalysis"],
    py_modules=['load_gazecom_class'],
    python_requires=">=3.6",
    install_requires=['pandas','matplotlib','numpy','tqdm',"scipy"],
)