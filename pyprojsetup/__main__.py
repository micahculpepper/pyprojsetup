#!/usr/bin/env python

"""
Main module of pyprojsetup. Provides command-line entry point and main logic.
"""

from __future__ import print_function
import datetime
import json
import os
import pkg_resources
import re
import stat
import subprocess
import sys
import urllib2
from time import sleep

try:
    import sphinx_rtd_theme
except Exception:
    print(
        "WARNING: sphinx_rtd_theme is not installed. "
        "You will not be able to build HTML with that theme.",
        file=sys.stderr
        )

MYDIR = os.path.dirname(os.path.realpath(__file__))


def chmod_plus_x(uri):
    # Get file's current permissions
    st = os.stat(uri)
    # Use binary OR to add the new permissions
    os.chmod(uri, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def copy(src, dst_dir, dst, fmt=[]):
    """Copy files from data/ to the project and insert
    project-specific data."""
    s = os.path.join(MYDIR, 'data', src)
    d = os.path.join(dst_dir, dst)
    with open(s) as f1:
        c = f1.read()
    with open(d, 'w') as f2:
        print(c.format(*fmt), file=f2, end='')


def overwrite_sphinx_conf(confdir):
    """Sphinx-quickstart does not take input for the Man page title,
    and instead assumes '<your project> Documentation'
    To fix that, we have to rewrite the file. Also, set the default
    html theme to sphinx_rtd_theme. Also also, we have to tell
    sphinx autodoc where to find the project."""
    tempfile = os.path.join(confdir, 'setup_sphinx.tmp')
    conf = os.path.join(confdir, 'conf.py')
    section = False
    import_done = False

    with open(tempfile, 'w') as t:
        with open(conf) as c:
            while True:
                line = c.readline()
                if line == '':
                    break
                if (not import_done) and line.startswith('import'):
                    line = (
                        line + ("import sphinx_rtd_theme\n") +
                        "sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath('.'))))"
                        )
                    import_done = True
                if line.startswith('html_theme ='):
                    line = "html_theme = \"sphinx_rtd_theme\""
                if line.startswith('#html_theme_path'):
                    line = (
                        "html_theme_path = "
                        "[sphinx_rtd_theme.get_html_theme_path()]")
                if line.startswith('man_pages'):
                    section = True
                if section:
                    args = line.split(',')
                    for index, arg in enumerate(args):
                        if 'Documentation' in arg:
                            args[index] = "''"
                            section = False
                    line = ','.join(args)
                t.write(line)
    os.rename(tempfile, conf)


def git_init(root, project_name, short_description, gh_token,
             git_repo_creation_url, gh_pages_dir, author, author_email):
    subprocess.call('git init', cwd=root, shell=True)
    subprocess.call(
        'git config user.name {}'.format(author), cwd=root, shell=True)
    subprocess.call(
        'git config user.email "{}"'.format(author_email), cwd=root,
        shell=True)
    subprocess.call('git add --all', cwd=root, shell=True)
    subprocess.call(
        'git commit --all -m "initial commit"',
        cwd=root, shell=True)
    data = json.dumps({
        'name': project_name,
        'description': short_description
        })
    auth_header = {'Authorization': "token {}".format(gh_token)}
    req = urllib2.Request(git_repo_creation_url, data, headers=auth_header)
    response = urllib2.urlopen(req)
    j = json.load(response)
    subprocess.call(
        'git remote add origin {}'.format(j['ssh_url']), cwd=root, shell=True)
    subprocess.call('git push origin master', cwd=root, shell=True)
    subprocess.call(
        "git subtree push --prefix {} origin gh-pages".format(gh_pages_dir),
        cwd=root, shell=True)


def main(args=None):
    """CLI entry point"""
    if not args:
        import parsers
        parser = parsers.main()
        args = parser.parse_args()
    project_name = args.name
    author = args.author
    author_email = args.email
    short_description = args.description
    version = args.startingversion
    if 'Legacy' in str(type(pkg_resources.parse_version(version))):
        print(
            "{} is not a PEP 440 compliant version number."
            "".format(version), file=sys.stderr)
        sys.exit(2)
    if not os.path.isdir(args.path):
        print(
            "{} is not a directory.\n"
            "For 'path', please provide the directory where the project root "
            "should be created.\n$HOME/projects would create "
            "$new_project at $HOME/projects/$new_project"
            "".format(args.path),
            file=sys.stderr)
        sys.exit(2)
    root = os.path.join(args.path, project_name)
    if os.path.isdir(root):
        print(
            "{} already exists; aborting.".format(root)
            )
        sys.exit(1)
    github_data = (
        g for g in args.githubconfig if g['hostname'] == args.github
        ).next()
    git_org = args.organization
    git_url = github_data['project_url'].format(
        user=git_org, name=project_name)
    git_host = github_data['hostname']
    git_repo_creation_url = github_data['repo_creation_url']
    api_release_url = github_data['api_release_url']
    gh_pages_url = github_data['gh_pages_url'].format(
        user=git_org, name=project_name)
    print(
        "Requesting token for {} at {} from keychain."
        "".format(git_org, git_host),
        file=sys.stderr)
    try:
        gh_token = subprocess.check_output(
            "security find-generic-password -a {} -s {} -w"
            "".format(git_org, git_host), shell=True).strip()
    except:
        print(
            "Failed to retrieve password. This setup script and the associated"
            " build system use the OS Keychain to access your github token. "
            "Please add your personal access token to your keychain like this:"
            "\nsecurity add-generic-password -a {} -s {} -l [label] "
            "-w [token]".format(git_org, git_host)
            )
        sys.exit(1)

    # Create Directory Structure
    os.mkdir(root)
    doc_dir = os.path.join(root, 'docs')
    os.mkdir(doc_dir)
    doc_src_dir = os.path.join(doc_dir, 'src')
    os.mkdir(doc_src_dir)
    doc_man_dir = os.path.join(doc_dir, 'man')
    os.mkdir(doc_man_dir)
    apidoc_dir = os.path.join(doc_dir, 'apidocs')
    os.mkdir(apidoc_dir)
    doctest_dir = os.path.join(doc_dir, 'doctests')
    os.mkdir(doctest_dir)
    gh_pages_dir = os.path.join(doc_dir, 'gh-pages')
    os.mkdir(gh_pages_dir)
    metadata_dir = os.path.join(root, 'metadata')
    os.mkdir(metadata_dir)
    project_dir = os.path.join(root, project_name)
    os.mkdir(project_dir)
    tests_dir = os.path.join(project_dir, "tests")
    os.mkdir(tests_dir)

    # Create VirtualEnv
    subprocess.call('virtualenv .', cwd=root, shell=True)

    # Write Project Python Files
    copy('project.init.py', project_dir, '__init__.py',
         fmt=[short_description, version])
    copy('project.main.py', project_dir, '__main__.py',
         fmt=[project_name])
    chmod_plus_x(os.path.join(project_dir, '__main__.py'))
    copy('project.parsers.py', project_dir, 'parsers.py')

    # Write Test Suite Files
    copy('project.tests.init.py', tests_dir, '__init__.py')
    copy('project.tests.tests.py', tests_dir, 'tests.py')

    # Write Documentation
    copy('API.rst', doc_src_dir, 'API.rst',
         fmt=[git_url])
    copy('Bugs.rst', doc_src_dir, 'Bugs.rst')
    copy('Contributing.rst', doc_src_dir, 'Contributing.rst')
    copy('Description.rst', doc_src_dir, 'Description.rst')
    copy('Example.rst', doc_src_dir, 'Example.rst')
    copy('Exit_Codes.rst', doc_src_dir, 'Exit_Codes.rst')
    copy('help_output', doc_src_dir, 'help_output')
    copy('Installation.rst', doc_src_dir, 'Installation.rst',
         fmt=[project_name, git_url])
    copy('Options.rst', doc_src_dir, 'Options.rst')
    copy('Synopsis.rst', doc_src_dir, 'Synopsis.rst')
    copy('README.rst', root, 'README.rst',
         fmt=[project_name, gh_pages_url])
    subprocess.call(
        "sphinx-quickstart -q -p '{0}' -a '{1}' -v '{2}' "
        "--ext-autodoc --ext-doctest --ext-viewcode "
        "--no-batchfile --no-makefile {3}"
        "".format(project_name, author, version, doc_src_dir),
        cwd=root, shell=True
        )
    overwrite_sphinx_conf(doc_src_dir)
    copy('index.rst', doc_src_dir, 'index.rst',
         fmt=[project_name, datetime.date.today().isoformat()])
    copy('nojekyll', gh_pages_dir, '.nojekyll')

    # Write Miscellaneous Files
    project_name_file = os.path.join(root, 'metadata', 'project_name')
    with open(project_name_file, 'w') as f:
        f.write(project_name)
    version_file = os.path.join(root, 'metadata', 'version')
    with open(version_file, 'w') as f:
        f.write(version)
    desc_file = os.path.join(root, 'metadata', 'short_description')
    with open(desc_file, 'w') as f:
        f.write(short_description)
    copy(
        'setup.py', root, 'setup.py',
        fmt=[
            author, author_email,
            re.sub(project_name, "{}", git_url)
            ]
        )
    copy('MANIFEST.in', root, 'MANIFEST.in')
    copy('sublime-project', root, "{}.sublime-project".format(project_name))
    copy('env', root, '.env')
    copy('Makefile', root, 'Makefile',
         fmt=[
            re.sub(project_name, "$(proj)", api_release_url)
            ])
    copy('gitignore', root, '.gitignore')
    copy('editorconfig', root, '.editorconfig')
    copy('LICENSE.txt', root, 'LICENSE.txt',
         fmt=[datetime.date.today().year, author])

    # Install User-requested packages
    if args.packages:
        subprocess.call(
            './bin/pip install {}'.format(' '.join(args.packages)),
            cwd=root, shell=True)

    if args.django:
        subprocess.call(
            'django-admin startproject {}'.format(project_name),
            cwd=os.path.dirname(root), shell=True)

    # Create docs
    os.environ['SKIPEDIT'] = '1'
    os.environ['AUTOYES'] = '1'
    subprocess.call("make docs", shell=True, cwd=root)

    # Setup Git
    git_init(root, project_name, short_description, gh_token,
             git_repo_creation_url, os.path.relpath(gh_pages_dir, root),
             author, author_email)

    # Welcome to your project
    subprocess.call("open {}".format(git_url), shell=True)
    print("Welcome to the new {} repository!\n".format(project_name))
    print(
        "Support is included for a man.1 page. "
        "To add other man pages, create the RST documentation and "
        "update the following:\n"
        "{0}/Makefile 'docs'\n"
        "{1}/conf.py 'man_pages'\n"
        "{0}/setup.py 'DATA_FILES'\n".format(root, doc_src_dir)
        )
    print(
        "To get started, cd {0}\n"
        "subl {0}.sublime-project".format(project_name)
        )


if __name__ == '__main__':
    main()
