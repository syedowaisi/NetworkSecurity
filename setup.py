from setuptools import find_packages,setup
from typing import List

hypen_dot="-e ."
def get_requirements(file_path:str)->List[str]:
    '''
    returns list of requirements
    '''
    requirements=[]
    try:
        with open(file_path,encoding="utf-8") as file_obj:
            requirements=file_obj.readlines()
            requirements=[req.replace('\n',"") for req in requirements]
            
            if hypen_dot in requirements:
                requirements.remove(hypen_dot)
    except FileNotFoundError:
        print("file is not available")
        
    return requirements

setup(
    name='Network Security project',
    version='0.0.1',
    author='Syed Owais',
    author_email='osyed8452@gmail.com',
    packages=find_packages(),
    install_req=get_requirements('requirements.txt')
)

# print(get_requirements('requirements.txt'))