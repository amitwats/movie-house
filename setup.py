from setuptools import setup, find_packages 
NAME = "movie-house" 

VERSION = "0.1" 

REQUIRES = [ 
    "numpy", 
    "pandas"
] 

 

setup( 
    name=NAME, 
    version=VERSION, 
    install_requires=REQUIRES, 
    packages=find_packages(), 
    python_requires=">=3.5.3", 
    include_package_data=True, 
    entry_points={"console_scripts": ["start = start:main"]}, 

) 