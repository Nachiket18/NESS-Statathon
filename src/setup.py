'''
Created on 28-Mar-2021

@author: Nachiket Deo
'''

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy
import scipy
ext_modules = [Extension("anomaly_detection", ["anomaly_detection.pyx"])]

setup(
    package_dir={'src': ''},
    cmdclass = {'build_ext': build_ext},
    include_dirs=[numpy.get_include(),scipy.get_include()],
    ext_modules = ext_modules
    
)
