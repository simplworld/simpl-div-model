# simpl-div-model - example multi player simulation model service.

## Python Setup (assumes Python >= 3.6 and simpl-games-api server running)

    git clone git@github.com:simplworld/simpl-div-model.git
    cd simpl-div-model
    mkvirtualenv simpl-div-model
    add2virtualenv .
    
    PIP_PROCESS_DEPENDENCY_LINKS=1 pip install -r requirements.txt

## Run model service

    export DJANGO_SETTINGS_MODULE=simpl_div_model.settings
    ./manage.py run_modelservice

If you need some serious debugging help, the model_service includes the ability to do

    ./manage.py run_modelservice --loglevel=debug

Which will turn on verbose debugging of the Autobahn/Crossbar daemon to help debug interactions between the browser and model service backend.

## Run unit tests

    export DJANGO_SETTINGS_MODULE=simpl_div_model.settings
    py.test

## Development commands:

### 1 - To setup up database for simpl-div development use:

1. Creates the simpl-div game with two phases (Play and Debrief) and two roles ("Dividend" and "Divisor").
1. Adds a 'default' run..
1. Adds 1 leader ('leader@div.edu'/'leader') to the run.
1. Adds 2 players to the run ('s#@div.edu'/'s#' where # is between 1..2. Each player has a private scenario and period 1.
1. The run is set to 'Play' phase

execute:

    ./manage.py create_default_env

To make it easier to recreate the default run you can pass the `--reset` option to delete the
default run and recreate it from scratch like this:

    ./manage.py create_default_env --reset


