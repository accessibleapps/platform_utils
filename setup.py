from setuptools import setup, find_packages
import io

__version__ = 0.41


setup(
    name="platform_utils",
    author = "Christopher Toth",
    author_email = "q@q-continuum.net",
    version=__version__,
    description="""Cross-platform utilities for accomplishing some tasks that the stdlib isn't equipped to provide""",
    long_description=io.open("README.rst", encoding="UTF8").read(),
    packages=find_packages(),
    zip_safe=False,
    extras_require={
        ':sys_platform == "win32"': [
            'pywin32',
            'winpaths',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries",
    ],
)
