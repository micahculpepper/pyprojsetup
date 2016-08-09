############
Contributing
############

.. highlight:: none

If you would like to contribute to this project, here's how you can get started. Instructions written for OS X.

Prerequisites
=============

* Make sure your github account is set up, git is installed on your machine, and your SSH keys are uploaded to your account. `Git Bootcamp <https://help.github.com/articles/set-up-git/>`_.

* Have an editor that supports `editorconfig <http://editorconfig.org/>`_. Also have $EDITOR exported.

* Have these installed on your system (doesn't have to be in this project's env):

    * pylint

    * coverage

    * sphinx

    * sphinx-rtd-theme

    * virtualenv


Repository Setup
================

1. `Make your own fork <https://help.github.com/enterprise/2.4/user/articles/fork-a-repo/>`_ (version) of the github repo, then clone (copy) it onto your machine. N.B.: The guide shows you how to clone over HTTPS, but due to the way OAUTH HTTPS authentication is set up, I recommend cloning with SSH via the SSH clone link on the repo's page. If you want to use HTTPS, check out `this article <https://github.com/blog/1270-easier-builds-and-deployments-using-git-over-https-and-oauth>`_ on getting it to work.

2. Set up a `virtualenv <https://virtualenv.pypa.io/en/stable/>`_ in the root of the repo. Example::

    # cd to the folder that contains setup.py and README.rst
    virtualenv .

3. When working in the project directory, configure your environment by typing "source .env". Alternatively, install `autoenv <https://github.com/kennethreitz/autoenv>`_ to take care of this step for you when you cd into the project directory.

4. Install any project dependencies into the virtual environment::

    pip install requirements.txt -r


Making a Contribution
=====================

1. Make a new `branch <https://git-scm.com/docs/git-checkout>`_ for the feature or bugfix you are working on. Example::

    git checkout -b mybugfix

2. Make your code revisions.

3. Write test cases for your new code.

4. Verify that your tests are passing and that you have updated documentation, setup scripts, etc. by running::

    make dryrun

5. Commit your changes and push them to your fork. Then create a pull request to merge your new branch into the project.

