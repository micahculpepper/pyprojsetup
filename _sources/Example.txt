#######
Example
#######

.. highlight:: none

Create a new project named "my_project" in the current directory, and create the remote repo on github.com::

    pyprojsetup my_project --author <author name(s)> --email <author e-mail address> --organization <github username> --description "This is what my_project does."

As above, but create "my_project" on COMPANY's enterprise github (requires updating a config file, see :doc:`Customization`)::

    pyprojsetup my_project --author <author name(s)> --email <author e-mail address> --organization <github username> --description "This is what my_project does." --github github.COMPANY.com
