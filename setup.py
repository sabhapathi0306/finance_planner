"""Setup file to install/build the required python packages collectively"""

from setuptools import find_packages,setup
from typing import List

# -e triggers the setup file whenever  install requirments
HYPEN_E_DOT='-e .'


def get_requirements(file_path:str)->List[str]:
    '''
    Function will return the list of requirements
    '''
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace("\n","") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    
    return requirements

setup(
name='financeproject',
version='0.0.1',
author='Adithya Sabhapathi',
author_email='adithyasabhapathi03@gmail.com',
packages=find_packages(),
install_requires=get_requirements('requirements.txt')

)