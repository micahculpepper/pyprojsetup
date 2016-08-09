#######
Options
#######

Command-line Help
=================

.. highlight:: none
.. include:: help_output
   :code:

Details
=======

author
^^^^^^

The author will be configured as the git user in the new repo, and will be referenced in documentation and package metadata. To modify the git user, :code:`git config user.name <name>`

email
^^^^^

The e-mail address will be configured as the git email in the new repo, and will be referenced in documentation and package metadata. To modify the git email, :code:`git config user.email <address>`

github
^^^^^^

The options available to --github are defined in a config file. See :doc:`Customization` for more details.

description
^^^^^^^^^^^

The description is designed to be modifiable. To update the description after the project has been created, update :code:`__init__.py`, :code:`metadata/short_description`, and the description on the github repo, then :code:`make docs`.
