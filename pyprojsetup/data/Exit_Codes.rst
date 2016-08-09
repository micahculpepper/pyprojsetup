##########
Exit Codes
##########

While every effort is made to provide helpful and descriptive messages when the program ends, the meanings of the possible exit codes are documented here for reference.

===  =========    =====
No.  Meaning      Notes
===  =========    =====
0    Success      The program finished within acceptable parameters.
1    Failure      The program failed or was interrupted, and no more specific exit code applies.
2    CLI Error    The operator provided invalid input. See :doc:`options`
===  =========    =====

.. highlight:: none

.. tip:: In POSIX-standard shells, the exit status of a command will be set to the variable :code:`?`.
    To check the exit code of a program, after it has ended, you can run::

        echo $?
