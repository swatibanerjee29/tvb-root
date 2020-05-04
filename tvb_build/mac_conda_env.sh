#!/bin/bash

#Install dependencies
conda create -y --name mac-distribution python=3 nomkl numba scipy numpy networkx scikit-learn cython pip numexpr psutil
conda install -y --name mac-distribution pytest pytest-cov pytest-benchmark pytest-mock matplotlib-base
conda install -y --name mac-distribution psycopg2 pytables scikit-image==0.14.2 simplejson cherrypy docutils werkzeug==0.16.1
conda install -y --name mac-distribution -c conda-forge jupyterlab flask gevent
source activate mac-distribution
pip install --upgrade pip
pip install h5py>=2.10 formencode cfflib jinja2 nibabel sqlalchemy==1.1.14 sqlalchemy-migrate==0.11.0 allensdk
pip install tvb-gdist typing BeautifulSoup4 subprocess32 flask-restplus python-keycloak mako
pip install py2app docutils apscheduler pyobjc
pip install --upgrade setuptools
pip install --upgrade distribute

# Install TVB
cd ../framework_tvb
python setup.py develop --no-deps

cd ../scientific_library
python setup.py develop

cd ../scientific_library/contrib
python setup.py develop --no-deps

cd ../../tvb_bin
python setup.py develop

cd ../tvb_build
python setup.py develop --no-deps
