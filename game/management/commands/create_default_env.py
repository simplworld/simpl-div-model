import djclick as click

from modelservice.simpl.sync import games_client


def echo(text, value):
    click.echo(
        click.style(text, fg='green') + '{0}'.format(value)
    )


def delete_default_run(games_client):
    """ Delete default Run """
    echo('Resetting the Simpl Div game default run...', ' done')
    runs = games_client.runs.filter(game_slug='simpl-div')
    for run in runs:
        if run.name == 'default':
            games_client.runs.delete(run.id)


@click.command()
@click.option('--reset', default=False, is_flag=True,
              help="Delete default game run and recreate it from scratch")
def command(reset):
    """
    Create and initialize Simpl Div game.
    Create a "default" Simpl Div run.
    Set the run phase to "Play".
    Add 2 worlds to the run.
    Add a scenario and period 1 for each world.
    Add 1 leader ("leader") to the run
    Add 4 players ("s1", "s2", "s3", "s4") to the run
    splitting the players between the 2 worlds and assigning all roles.
    """

    # Create a Game
    game = games_client.games.get_or_create(
        name='Simpl Div',
        slug='simpl-div'
    )
    echo('getting or creating game: ', game.name)

    # Handle resetting the game
    if reset:
        if click.confirm(
                'Are you sure you want to delete the default game run and recreate from scratch?'):
            delete_default_run(games_client)

    # Create required Roles ("Dividend" and "Divisor")
    dividend_role = games_client.roles.get_or_create(
        game=game.id,
        name='Dividend',
    )
    echo('getting or creating role: ', dividend_role.name)

    divisor_role = games_client.roles.get_or_create(
        game=game.id,
        name='Divisor',
    )
    echo('getting or creating role: ', divisor_role.name)

    # Create game Phases ("Play" and "Debrief")
    play_phase = games_client.phases.get_or_create(
        game=game.id,
        name='Play',
        order=1,
    )
    echo('getting or creating phase: ', play_phase.name)

    debrief_phase = games_client.phases.get_or_create(
        game=game.id,
        name='Debrief',
        order=2,
    )
    echo('getting or creating phase: ', debrief_phase.name)

    # Add run with 2 fully populated worlds ready to play
    run = add_run(game, 'default', 2, 1,
                        dividend_role, divisor_role,
                        play_phase, games_client)

    # echo('Completed setting up run: id=', run.id)


def add_run(game, run_name, world_count, first_user_number,
                  dividend_role, divisor_role,
                  phase, games_client):
    # Create or get a Run
    run = games_client.runs.get_or_create(
        game=game.id,
        name=run_name,
    )
    echo('getting or creating run: ', run.name)

    # Set run to phase
    run.phase = phase.id
    run.save()
    echo('setting run to phase: ', phase.name)

    user_name_root = "s"
    if run_name is not 'default':
        user_name_root = run_name
    for n in range(0, world_count):
        world_num = n + 1
        world = add_world(run, world_num, games_client)

        # Add users to run
        add_world_users(run, world, user_name_root,
                              first_user_number + n * 2,
                              dividend_role, divisor_role, games_client)

    return run


def add_world(run, number, games_client):
    """
        Add a world to the run with a scenario and period 1.
        The world's name is based on number.
    """
    name = 'World {0}'.format(number)
    world = games_client.worlds.get_or_create(
        run=run.id,
        name=name,
    )
    echo('getting or creating world: ', world.name)

    scenario = games_client.scenarios.create({
        'world': world.id,
        'name': 'World Scenario 1'
    })
    period1 = games_client.periods.create({
        'scenario': scenario.id,
        'order': 1
    })

    return world


def add_world_users(run, world, user_name_root,
                          first_number,
                          dividend_role, divisor_role, games_client):
    """
        Add 1 leader ("leader") to the run with a test scenario
        Add players to the run with names based on user_name_root and first_number
        Add players to world assigning all required roles
    """
    fac_user = games_client.users.get_or_create(
        password='leader',
        first_name='Div',
        last_name='Leader',
        email='leader@div.edu',
    )
    echo('getting or creating user: ', fac_user.email)

    games_client.runusers.get_or_create(
        user=fac_user.id,
        run=run.id,
        leader=True,
    )
    echo('getting or creating leader runuser for user: ', fac_user.email)

    roles = [dividend_role, divisor_role]
    for n in range(len(roles)):
        user_number = n + first_number
        add_player(user_name_root, user_number, run, world, roles[n],
                         games_client)


def add_player(user_name_root, user_number, run, world, role,
                     games_client):
    """Add player with name based on user_name_root and user_number to world in role"""

    username = '{}{}'.format(user_name_root, user_number)
    first_name = 'Student{0}'.format(user_number)
    if user_name_root == 's':  # assume original default namings
        last_name = 'User'
    else:
        last_name = user_name_root[:1].upper() + user_name_root[1:]
    email = '{0}@div.edu'.format(username)

    user = games_client.users.get_or_create(
        password=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
    )
    echo('getting or creating user: ', user.email)

    games_client.runusers.get_or_create(
        user=user.id,
        run=run.id,
        world=world.id,
        role=role.id,
    )
    echo('getting or creating runuser for user: ', user.email)

