# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages
import python_netsuite as app

setup(
    name="python_netsuite",
    version=app.__version__,
    description='Netsuite Python Toolkit for SuiteTalk SOAP API',
    long_description=open('README.rst').read(),
    license='BSD License',
    platforms=['OS Independent'],
    keywords='Netsuite,Python,SuiteTalk,SOAP,API',
    author='fmalina',
    author_email='fmalina@gmail.com',
    url="https://github.com/fmalina/python-python_netsuite",
    packages=find_packages(),
    include_package_data=True,
    install_requires=['zeep'],
)
