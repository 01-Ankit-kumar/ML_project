from setuptools import find_packages,setup
from typing import List

HYPEN_E_DOT = '-e .' ## this is used in requirements.txt to map setup.py as soon as requirements.txt is read
## as an indication that there is a setp.py file
def get_requirements(file_path:str)->List[str]:
    
    """
    this function will return the list of requirements
    """
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace('\n','') for req in requirements]
        
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    return requirements

setup(
    name="ML_projects",
    version = '0.0.1',
    author='Ankit',
    author_email='ankit27560@gmail.com',
    packages=find_packages(), ## this will atuomatically search for floder having __int__py file and install the src as package
    requires= get_requirements('requirements.txt')
)