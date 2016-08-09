############
Installation
############

Supported Platforms
===================

* Mac OS X
* Linux
* Cygwin

.. tip:: Mac OS X users,
    avoid using the system's Python library `(why?) <https://hackercodex.com/guide/python-development-environment-on-mac-osx/#python>`_, and install your own Python library via `homebrew <http://brew.sh/>`_.

pip
===

|package| is designed for installation with `pip <https://pip.pypa.io/en/stable/>`_. If you do not have pip, you can get it `here <https://pip.pypa.io/en/stable/installing/>`_.

Make sure your pip installation is up to date by running::

    sudo pip install pip --upgrade

Dependencies
============

The following Python packages must be installed on your system:

.. highlight:: none
.. include:: ../../{0}.egg-info/requires.txt
   :literal:

If they are not, pip will attempt to download and install them before installing |package|.
However, this feature of pip is unreliable if the dependencies are hosted somewhere besides `pypi <https://pypi.python.org/pypi>`_.
Therefore, you may want to install any dependencies before attempting to install |package|.


Instructions
============

1. `Download the latest release here <{1}/releases/latest>`_.
2. Install the downloaded tarball using pip. If upgrading from a previous version, use the --upgrade flag. For example:

    .. parsed-literal::

        sudo pip install |package|-|version|.tar.gz [--upgrade]

3. If you are having difficulty with the previous step, try the following alternate installation method:

    .. parsed-literal::

        # Extract the tarball
        tar -zxvf |package|-|version|.tar.gz
        # Change to the extracted directory
        cd |package|-|version|
        # Run the installation routine
        sudo make install

4. When done, you can delete |package|-|version|.tar.gz and the |package|-|version| directory (if present).


Verification
============

Verify the installed version:

.. parsed-literal::

    |package| --version

The current version as of |today| is |version|.

