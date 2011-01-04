from setuptools import setup, find_packages

setup(
 name = 'platform_utils',
 version = '0.1.1',
 description = 'Cross-platform utilities for accomplishing basic tasks',
 package_dir = {'platform_utils': 'platform_utils'},
 packages = find_packages(),
 classifiers = [
  'Development Status :: 3 - Alpha',
  'Intended Audience :: Developers',
  'Programming Language :: Python',
  'License :: OSI Approved :: MIT License',
'Topic :: Software Development :: Libraries'
],
)
