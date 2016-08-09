########
Makefile
########

Projects created by pyprojsetup will include a Makefile in their root directory. This Makefile exists to automate common development workflows.

Targets
=======

A make target, supplied as a command-line argument following the :code:`make` command, describes an objective that :code:`make` should work towards. For more information on make, see the `official docs <https://www.gnu.org/software/make/manual/make.html>`_. The following targets are defined in the Makefile that pyprojsetup creates:

make clean
^^^^^^^^^^
Delete temporary files in the repo.

make install
^^^^^^^^^^^^
Install the project on your system using pip. Meant as a convenience function for end-users who are comfortable with installing things via :code:`make`.

make test
^^^^^^^^^
Run the test suite and `tox <https://tox.readthedocs.io/en/latest/>`_.

make newversion
^^^^^^^^^^^^^^^
Prompt for a new version number, check it for PEP 440 compliance, then write the new version to :code:`metadata/version` and :code:`__init__.py`

make egginfo
^^^^^^^^^^^^
Populate :code:`<project_name>.egg-info/` by running :code:`python setup.py egginfo`, which creates some useful metadata.

make lint
^^^^^^^^^
Run :code:`make egginfo`, then lint the project. Default linter is pylint. The linted files are the .py files included in :code:`setup.py`'s :code:`packages`.

make coverage
^^^^^^^^^^^^^
Evaluate the percentage of code that is covered by a test case. Set a value for :code:`coverage_min` in :code:`Makefile` to enforce a minimum coverage percentage requirement.

make requirements
^^^^^^^^^^^^^^^^^
Run :code:`make egginfo`, then compare the dependencies declared by the project with those mentioned in imports, those used by the project, and those installed in the virtual environment. This tool helps you keep your :code:`setup.py`'s :code:`install_requires` up-to-date.

make docs
^^^^^^^^^
Run :code:`make requirements`, then dynamically build updated documentation using a combination of the documents under :code:`docs/src`, CLI help output, docstrings, and actual code. Open the sources for review prior to building. Build a man page and an HTML page.

make commit
^^^^^^^^^^^
Git tag the current version number. Add, commit, and push all files to the new tag. Push :code:`docs/gh-pages` to the :code:`gh-pages` branch of the remote repo, which publishes the HTML documentation made by :code:`make docs` as a `GitHub Page <https://pages.github.com/>`_.

make sdist
^^^^^^^^^^
Creates a source distribution by running :code:`python setup.py sdist`.

make release
^^^^^^^^^^^^
Run :code:`make sdist`, then create a new `release <https://help.github.com/articles/about-releases/>`_ in draft status on github via an API call, and upload the sdist tarball to the release page. The API call uses your :doc:`Credentials`.

make dryrun
^^^^^^^^^^^
Run :code:`make test coverage lint docs sdist`.

make all
^^^^^^^^
Run :code:`make newversion dryrun commit release`.

.. note:: :code:`make` with no other arguments will run :code:`make all`.

Environment
===========

To modify the behavior of the Makefile, export environment variables before running make.

* To see curl output when uploading to github, :code:`export VERBOSE=1`
* To avoid opening files in the editor, :code:`export SKIPEDIT=1`
* To avoid pausing for user input, :code:`export AUTOYES=1`

.. tip:: If you are not sure if your code is ready to release, run :code:`make dryrun` to *check all the things*. 
    If you are ready to mark a new version and publish a release, :code:`make`.

