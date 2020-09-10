import setuptools
'''
from setuptools.command.install import install as InstallCommand

class Install(InstallCommand):
    """ Customized setuptools install command which uses pip. """

    def run(self, *args, **kwargs):
        import pip
        pip.main(['install', '.'])
        InstallCommand.run(self, *args, **kwargs)
'''  
setuptools.setup(
    author="Shagen Djanian",
    author_email="s.d@hotmail.dk",
    license="MIT",
    description='chocobo is a python package for delicious chocobo recipes.',
    version='v0.0.1',
    url='https://github.com/Kongskrald/GazeComCritique',
    python_requires=">=3.6",
    install_requires = ['modality>=1.0'],
    dependency_links = ['https://github.com/kjohnsson/modality/archive/master.zip#egg=modality-1.1'],
    )

#https://github.com/kjohnsson/modality/blob/master/dist/modality-1.0.tar.gz?raw=true