###########
Credentials
###########

pyprojsetup itself uses your credentials for one thing: creating the remote origin repo via an API call.

pyprojsetup also creates a Makefile for you, and you can use the Makefile to create releases and upload files to releases on github via API calls, which will also use the same credentials.

In both cases, the credential used is a `Personal Access Token <https://help.github.com/articles/creating-an-access-token-for-command-line-use/>`_.
pyprojsetup looks for a token in your OS X Keychain [1]_ with the following parameters:

* "account" matches the organization set via the :code:`--organization` command-line flag
* "service" or "where" matches the github hostname set via the :code:`--github` command-line flag
* "type" is "application password"


.. [1] I am planning to add options for integration with other password managers like lastpass, but for now, OS X is required.
