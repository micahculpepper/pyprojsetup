"""
Setup script. Used to distribute and install this project.
See setuptools documentation at setuptools.readthedocs.io
"""

import setuptools


def read(fname):
    """Return contents of fname"""
    txt = None
    with open(fname) as ftoken:
        txt = ftoken.read()
    return txt

PROJECT_NAME = read("metadata/project_name")
VERSION = read("metadata/version")
DESCRIPTION = read("metadata/short_description")
LONG_DESCRIPTION = read("README.rst")
PACKAGES = setuptools.find_packages(exclude=("dist"))
DATA_FILES = [("share/man/man1", ["docs/man/{}.1.gz".format(PROJECT_NAME)])]

setuptools.setup(
    author="Micah Culpepper",
    author_email="micahculpepper@gmail.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: Apache License",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    data_files=DATA_FILES,
    description=DESCRIPTION,
    entry_points={
        "console_scripts": [
            "{0} = {0}.__main__:main".format(PROJECT_NAME)
            ]
        },
    install_requires=[
        "sphinx",
        "sphinx-rtd-theme",
        "tox",
        "coverage",
        "pylint"
    ],
    license="Apache License",
    long_description=LONG_DESCRIPTION,
    name=PROJECT_NAME,
    packages=PACKAGES,
    package_data={
        PROJECT_NAME: ['data/*'],
    },
    test_suite="{}.tests".format(PROJECT_NAME),
    url="https://github.com/micahculpepper/{}".format(PROJECT_NAME),
    version=VERSION,
    zip_safe=False
    )
