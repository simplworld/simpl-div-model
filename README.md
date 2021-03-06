# simpl-div-model - example multi player simulation model service.

## Python Setup (assumes Python 3.6 and simpl-games-api server running)

## Install simpl-div-model

```shell
$ git clone https://github.com/simplworld/simpl-div-model.git
$ cd simpl-div-model
```
## Local Docker Setup

The Simpl API server needs to be started first to create the `simpl` bridge network.

Install [simpl-games-api master](https://github.com/simplworld/simpl-games-api) and run it in 
docker-compose so that it exposes itself as hostname `api` on port `8100`. 

You also need to have a `is_staff=True` user in the simpl-games-api database that
corresponds to the `SIMPL_GAMES_AUTH` setting used here.

After you clone the repo, run:

```bash
$ docker-compose up
```

this will create the Docker image and run it.  The first time you run it it will error
as it can't find the simpl-div game in the API.

In a separate terminal, create a shell into the simpl-div-model container by running:

```bash
$ docker-compose run --rm model.backend bash
```

Once you are in the container shell, run this command:

```shell
$ ./manage.py create_default_env
```

You should see this create the 'simpl-div' game, phases, users, etc.

Exit from the shell then stop and restart the docker container by running these commands: 

```bash
$ docker-compose down
$ docker-compose up
```

You should now see a startup log message to the effect of:

```
Game `simpl-div` installed in 2.063s.
```

This means the simpl-div-model is able to successfully communicate with the API.

## Local Setup Without Docker

### Create a virtual environment and install Python dependencies

```bash
$ mkvirtualenv simpl-div-model
$ pip install -r requirements.txt
```
### Run model service

```shell
$ export DJANGO_SETTINGS_MODULE=simpl_div_model.settings
$ ./manage.py run_modelservice
```
If you need some serious debugging help, the model_service includes the ability to do

```shell
$ ./manage.py run_modelservice --loglevel=debug
```

Which will turn on verbose debugging of the Autobahn/Crossbar daemon to help debug interactions between the browser and model service backend.

### Run model service as 2 processes

1. Get a copy of the currently in use crossbar configuration by running
    `./manage.py run_modelservice --print-config > config.json`
1. Edit `config.json` to remove the entire {"type": "guest", ...} stanza and final line
1. Run crossbar service:    
    `./manage.py run_modelservice --config=./config.json --loglevel info --settings=simpl_div_model.settings`
1. In a separate terminal, run guest service:    
    `HOSTNAME=localhost PORT=8080 ./manage.py run_guest --settings=simpl_div_model.settings`
   
## Run unit tests

```shell
$ export DJANGO_SETTINGS_MODULE=simpl_div_model.settings
$ py.test
```

## Development commands:

### 1 - To setup up database for simpl-div development use:

1. Creates the simpl-div game with two phases (Play and Debrief) and two roles ("Dividend" and "Divisor").
1. Adds a 'default' run..
1. Adds 1 leader ('leader@div.edu'/'leader') to the run.
1. Adds 2 players to the run ('s#@div.edu'/'s#' where # is between 1..2. Each player has a private scenario and period 1.
1. The run is set to 'Play' phase

execute:

```shell
$ ./manage.py create_default_env
```

To make it easier to recreate the default run you can pass the `--reset` option to delete the
default run and recreate it from scratch like this:

```shell
$ ./manage.py create_default_env --reset
```

Copyright © 2018 The Wharton School,  The University of Pennsylvania 

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

