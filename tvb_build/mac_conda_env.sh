#!/bin/bash

#Install dependencies
conda update -n base -c defaults conda
conda create -y --name mac-distribution python=3.7 nomkl numba scipy numpy networkx scikit-learn cython pip numexpr psutil
conda install -y --name mac-distribution pytest pytest-cov pytest-benchmark pytest-mock matplotlib-base
conda install -y --name mac-distribution psycopg2 pytables scikit-image==0.14.2 simplejson cherrypy docutils werkzeug==0.16.1
conda install -y --name mac-distribution -c conda-forge jupyterlab flask gevent pillow

/WORK/anaconda3/anaconda3/envs/mac-distribution/bin/pip install --upgrade pip
/WORK/anaconda3/anaconda3/envs/mac-distribution/bin/pip install h5py>=2.10 formencode cfflib jinja2 nibabel sqlalchemy==1.1.14 sqlalchemy-migrate==0.11.0 allensdk
/WORK/anaconda3/anaconda3/envs/mac-distribution/bin/pip install tvb-gdist typing BeautifulSoup4 subprocess32 flask-restplus python-keycloak mako
/WORK/anaconda3/anaconda3/envs/mac-distribution/bin/pip install py2app docutils apscheduler pyobjc
/WORK/anaconda3/anaconda3/envs/mac-distribution/bin/pip install --upgrade setuptools
/WORK/anaconda3/anaconda3/envs/mac-distribution/bin/pip install --upgrade distribute

# Add an empty __init__.py in conda_env/python3.7/site-packages/PyObjCTools/ folder or else py2app won't be able to process this module
echo "" > /WORK/anaconda3/anaconda3/envs/mac-distribution/lib/python3.7/site-packages/PyObjCTools/__init__.py
ln -s /WORK/anaconda3/anaconda3/envs/mac-distribution/lib/libpython3.7m.dylib /WORK/anaconda3/anaconda3/envs/mac-distribution/lib/libpython3.7.dylib
rm -rf /WORK/anaconda3/anaconda3/envs/mac-distribution/lib/python3.7/site-packages/migrate/__init__.py
echo -e "from migrate.versioning import *\nfrom migrate.changeset import *\n__version__ = '0.11.0'" > /WORK/anaconda3/anaconda3/envs/mac-distribution/lib/python3.7/site-packages/migrate/__init__.py
ln -s /WORK/anaconda3/anaconda3/envs/mac-distribution/lib/libtiff.5.dylib /usr/local/lib/libtiff.5.dylib
# Install TVB
cd ../framework_tvb
/WORK/anaconda3/anaconda3/envs/mac-distribution/bin/python setup.py develop --no-deps

cd ../scientific_library
/WORK/anaconda3/anaconda3/envs/mac-distribution/bin/python setup.py develop

cd ../scientific_library/contrib
/WORK/anaconda3/anaconda3/envs/mac-distribution/bin/python setup.py develop --no-deps

cd ../../tvb_bin
/WORK/anaconda3/anaconda3/envs/mac-distribution/bin/python setup.py develop

cd ../tvb_build
/WORK/anaconda3/anaconda3/envs/mac-distribution/bin/python setup.py develop --no-deps
