#############
Customization
#############

By default, pyprojsetup creates projects on github.com. To use enterprise github, simply edit data/githubconfig.json in the source code. Then, when setting up a project, specify which github to use via the :code:`--github` flag.

.. highlight:: json

Example configuration of data/githubconfig.json for a company named COMPANY::

    [
        {
            "hostname": "github.com",
            "project_url": "https://github.com/{user}/{name}",
            "repo_creation_url": "https://api.github.com/user/repos",
            "gh_pages_url": "http://{user}.github.io/{name}",
            "api_release_url": "https://api.github.com/user/repos/{user}/{name}/releases"
        },
        {
            "hostname": "github.COMPANY.com",
            "project_url": "https://github.COMPANY.com/{user}/{name}",
            "repo_creation_url": "https://github.COMPANY.com/api/v3/user/repos",
            "gh_pages_url": "https://pages.github.COMPANY.com/{user}/{name}",
            "api_release_url": "https://github.COMPANY.com/api/v3/repos/{user}/{name}/releases"
        }
    ]

.. highlight:: none

In fact, anything under :code:`data/` is fair game for customization. For example, if you often create projects with a common set of dependencies, you may want include them in :code:`data/requirements.txt`
Bear in mind that files under :code:`data/` will be processed by :code:`.format()`, so be sure to escape any literal braces (i.e. :code:`{{` instead of :code:`{` and :code:`}}` instead of :code:`}`).
