# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages
import python_netsuite as app

setup(
    name="python_netsuite",
    version=app.__version__,
    description='Netsuite Python Toolkit for WS API (SuiteTalk SOAP, Restlet)',
    long_description=open('README.rst').read(),
    license='BSD License',
    platforms=['OS Independent'],
    keywords=['Netsuite','Python','SuiteTalk','RESTLET'],
    author='David Durst',
    author_email='ddurst@mrosupply.com',
    url="https://github.com/ddurs555/python-netsuite",
    packages=find_packages(),
    include_package_data=True,
    install_requires=['zeep'],
)
