proj := $(shell python ./setup.py --name)
$(info Makefile for $(proj))
branch = $(git rev-parse --abbrev-ref HEAD)
versionfile = metadata/version
version = $(shell cat $(versionfile))
sources_file = $(proj).egg-info/SOURCES.txt
sources = $(shell grep ".*\.py$$" $(sources_file))
gituser = $(shell git remote get-url --push origin | cut -d ':' -f 2 | cut -d '/' -f 1)
githostname = $(shell git remote get-url --push origin | grep -o -e 'github.*\.com')
githubtoken = $(shell security find-generic-password -a $(gituser) -s $(githostname) -w)
api_release_url = "https://api.github.com/repos/micahculpepper/$(proj)/releases"
linter = pylint
sdistdir = dist
# Minimum required test coverage percentage
coverage_min = 0
# To see curl output when uploading to github, export VERBOSE=1
ifeq ($(VERBOSE), 1)
	ttydev = $$(tty)
	curl_verbosity = -v
	curl_output = cat
else
	ttydev = /dev/null
	curl_verbosity = -s
	curl_output = cat > /dev/null
endif

# To avoid all the editor-opening, export SKIPEDIT=1
ifeq ($(SKIPEDIT), 1)
	EDITOR = echo
	OPEN = cat
# man -P cat doesn't keep all the nice formatting from the man page, but
# it's better than looking at raw troff
	MAN = man -P cat
else
	OPEN = open
	MAN = man
endif

# To avoid all the pausing, export AUTOYES=1
ifeq ($(AUTOYES), 1)
define continue
@echo
endef
else
define continue
@read -rsp "Press any key to continue, or CTRL-C to exit." -n1 _
@echo
endef
endif

.PHONY: all clean install egginfo requirements test coverage lint docs sdist release commit dryrun

all: newversion dryrun commit release

dryrun: test coverage lint docs sdist

clean:
	rm -rf $(sdistdir)
	rm -rf $(proj).egg-info
	rm -rf .tox
	rm -rf $$(find . -name .doctrees)
	rm -rf docs/src/apidocs/*

install:
	pip install pip --upgrade
	pip install setuptools --upgrade
	pip install -r requirements.txt --upgrade
	pip install . --upgrade

newversion:
	$(shell read -rp "New version, cannot be an existing tag: $$(echo $$(git tag)) : " version;\
		printf "$$version" > $(versionfile))
	@echo "Testing new version number for PEP 440 compliance"
	python -c "import pkg_resources, sys;sys.exit(bool('Legacy' in str(type(pkg_resources.parse_version('$(version)')))))"
	@echo "Writing new version"
	sed -i '' "s/^__version__ =.*/__version__ = \"$(version)\"/" ./$(proj)/__init__.py

egginfo:
	python setup.py egg_info

lint: egginfo
	-$(linter) $(sources)
	@echo "Please address any linter errors before proceeding."
	$(continue)

requirements: egginfo
	@echo
	@echo "#######################################"
	@echo "||  FINDING DEPENDENCIES IN PROJECT  ||"
	@echo "#######################################"
	@echo
	@echo === DEPENDENCIES SPECIFIED IN SETUP.PY ===
	-@cat $(proj).egg-info/requires.txt
	@echo
	@echo === PIP INSTALLED PACKAGES IN ENVIRONMENT ===
	@pip freeze
	@echo
	@echo === IMPORT STATEMENTS FOUND IN PROJECT ===
	@grep -r --include "*.py" --exclude-dir './dist' --exclude-dir './build' --exclude-dir "./lib" --exclude-dir "./bin" --exclude-dir "./.tox" --exclude-dir "./pyprojsetup_test_repo" import .
	@echo
	@echo === DEPENDENCIES REPORTED BY PYLINT ===
	-pylint --disable=all --disable=RP0001 --disable=RP0002 --disable=RP0003 --disable=RP0004 --disable=RP0101 --disable=RP0701 --disable=RP0801 --enable=imports persistent=n ./$(proj)
	@echo
	@echo "#######################################"
	@echo "||   FINDING DEPENDENCIES COMPLETE   ||"
	@echo "#######################################"
	@echo "Please ensure that you have updated requirements.txt and setup.py 'install_requires' to account for all dependencies."
	$(EDITOR) requirements.txt setup.py
	$(continue)

test:
	python setup.py test
	tox

coverage:
	-coverage run --source ./$(proj) setup.py test > /dev/null
	coverage report -m --fail-under=$(coverage_min)


docs: requirements
	@echo "Please review short_description and the __init__.py and save any changes. short_description and __init__.py's 'description' should match for the sake of consistency."
	$(EDITOR) metadata/short_description $(proj)/__init__.py
	$(continue)
	@echo
	@echo "Here is your current cli help output:"
	python ./$(proj)/__main__.py -h
	@echo
	@echo "Save any changes to parsers."
	$(EDITOR) ./$(proj)/parsers.py
	$(continue)
	python ./$(proj)/__main__.py -h > docs/src/help_output
	python -c "from $(proj) import parsers; parsers.main().print_usage()" | sed 's/^usage: //' > docs/src/usage
	@echo "Please review each document and save any changes: "
	$(EDITOR) docs/src/*[^.py]
	$(continue)
	sphinx-apidoc -o docs/src/apidocs -P --no-toc ./$(proj)
	sphinx-build -b doctest docs/src docs/doctests -D version="$(version)" -D release="$(version)" -D rst_epilog=".. |package| replace:: $(proj)"
	@echo
	@echo "Please review and correct any doctest errors before proceeding."
	$(continue)
	sphinx-apidoc -o docs/src/apidocs -P --no-toc ./$(proj)
	rm -rf docs/man
	sphinx-build -b man docs/src docs/man -Ea -D version="$(version)" -D release="$(version)" -D rst_epilog=".. |package| replace:: $(proj)" -D  man_show_urls=1
	gzip docs/man/*
	sphinx-build -b html docs/src docs/gh-pages -Ea -D version="$(version)" -D release="$(version)" -D html_theme=sphinx_rtd_theme -D rst_epilog=".. |package| replace:: $(proj)"
	@echo
	@echo "Please proofread the docs."
	$(OPEN) docs/gh-pages/index.html
	$(MAN) ./docs/man/*
	$(continue)

sdist:
	python setup.py sdist --dist-dir $(sdistdir)

commit:
	git status
	@echo
	@echo "Please make sure you are on the right branch, review your .gitignore, and save any changes."
	$(EDITOR) .gitignore
	$(continue)
	$(eval message := $(shell read -rp "Comment for this build: " message ; echo $$message))
	git add --all
	git commit --all -m "$(message)"
	git tag -a "$(version)" -m "$(message)"
	git push origin "$(version)"
# Copy new documentation to gh-pages branch
	git subtree push --prefix docs/gh-pages origin gh-pages

release: sdist
# Create github release and upload tarball
	$(eval prerelease := $(shell \
		read -rp "Mark build as pre-release? [Y|N]: " P ; \
		if [[ $$P =~ [Yy] ]] ;\
		then \
			P='true';\
		else \
			P='false';\
		fi ;\
		echo $$P))
	@echo
	$(eval tarball := $(shell ls -t dist/ | head -1))
	$(eval api_resp := $(shell curl $(curl_verbosity) $(api_release_url) -H "Authorization: token $(githubtoken)" --data '{"tag_name": "'"$(version)"'","target_commitish": "master","name": "'"$(version)"'","body": "'"$(message)"'","draft": true,"prerelease": '"$(prerelease)"'}' --trace-ascii $(ttydev)))
	$(eval upload_url := $(shell echo '$(api_resp)' | python -m json.tool | grep 'upload_url' | cut -d '"' -f 4 | cut -d '{' -f 1))
	$(eval html_url := $(shell echo '$(api_resp)' | python -m json.tool | grep 'html_url' | tail -1 | cut -d '"' -f 4 | cut -d '{' -f 1))
	$(eval upload_resp := $(shell curl $(curl_verbosity) $(upload_url)?name=$(tarball) -H "Authorization: token $(githubtoken)" -H "Content-Type: application/x-compressed-tar" -X POST --data-binary @dist/$(tarball)))
	@echo '$(upload_resp)' | python -m json.tool | $(curl_output)  || echo '$(upload_resp)' | $(curl_output)
	@echo
	open $(html_url)

