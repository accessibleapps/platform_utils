from setuptools import setup, find_packages

__version__ = 0.25


install_requires = []
import platform
if platform.system() == 'Windows':
 install_requires.append('winpaths')


setup(
 name = 'platform_utils',
 version = __version__,
 description = """Cross-platform utilities for accomplishing some tasks that the stdlib isn't equipped to provide""",
 install_requires = install_requires,
 packages = find_packages(),
 classifiers = [
  'Development Status :: 3 - Alpha',
  'Intended Audience :: Developers',
  'Programming Language :: Python',
  'License :: OSI Approved :: MIT License',
  'Topic :: Software Development :: Libraries'
 ],
)
