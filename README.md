# ckanext-metrics_dashboard

[![GitHub Actions](https://github.com/GSA/ckanext-metrics_dashboard/actions/workflows/deploy.yml/badge.svg)](https://github.com/GSA/ckanext-metrics_dashboard/actions/workflows/publish.yml)
[![PyPI version](https://badge.fury.io/py/ckanext-metrics_dashboard.svg)](https://badge.fury.io/py/ckanext-metrics_dashboard)

A CKAN extension to display metrics about harvest sources.

## Features

-   `${CKAN_URL}/report/metrics_dashboard`
-   -   Displays a summary report of number of datasets and harvest sources for each organization

-   `${CKAN_URL}/report/metrics_dashboard/{org}`
-   -   Displays a detailed report of each harvest source in an organization, where org is the ID of your organization

-   CSV Export: A comprehensive table of all harvest sources
-   JSON Export: CSV raw data plus a second key `table_data_by_org` that includes the same data grouped by organization

Compatibility: Tested with CKAN 2.9, though it's expected to work with earlier versions compatible with ckanext-report.

## Usage

### Requirements

These extensions are required for metrics_dashboard:

-   [ckanext-report](https://github.com/ckan/ckanext-report/)

## Development

### Requirements

-   GNU Make
-   Docker Compose

### Setup

Build the docker containers. You'll want to do this anytime the dependencies
change (requirements.txt, dev-requirements.txt).

    $ make build

Start the containers.

    $ make up

CKAN will start at [localhost:5000](http://localhost:5000).

Start the containers, but don't start ckan. More debugging instructions [here](#Debugging)

    $ make debug

Open a shell to run commands in the container.

    $ docker-compose exec app bash

If you're unfamiliar with docker-compose, see our
[cheatsheet](https://github.com/GSA/datagov-deploy/wiki/Docker-Best-Practices#cheatsheet)
and the [official docs](https://docs.docker.com/compose/reference/).

Clean the containers and remove the data.

    $ make clean

For additional make targets, see the help.

    $ make help

### Testing

They follow the guidelines for [testing CKAN extensions](https://docs.ckan.org/en/2.8/extensions/testing-extensions.html#testing-extensions).

To run the extension tests:

    $ make test

Lint your code.

    $ make lint

### Debugging

We have not determined a good way for most IDE native debugging, however you can use the built in Python pdb debugger. Simply run `make debug`, which will run docker with an interactive shell. Add import pdb; pdb.set_trace() anywhere you want to start debugging, and if the code is triggered you should see a command prompt waiting in the shell. Use a pdb cheat sheet when starting to learn like this.

When you edit/add/remove code, the server is smart enough to restart. If you are editing logic that is not part of the webserver (ckan command, etc) then you should be able to run the command after edits and get the same debugger prompt.

1. Launch the containers with `make debug`
2. Start the CKAN process by running `./start_ckan_development.sh`
3. Add `import ibdb; ipdb.set_trace()` at the point you wish to debug.
4. Invoke that code to hit that breakpoint.
