import djclick as click

from modelservice.simpl import games_client
from modelservice.utils.asyncio import coro

from ...runmodel import divide, save_decision


@click.command()
@click.option('--scenario_id', '-s', type=int, help='Scenario.id')
@click.option('--decision', '-d', default=0, type=float,
              help='Decision value. (defaults to 0)')
@click.option('--role_name', '-r', type=str, help='Role name (Dividend or Divisor')
@coro
async def command(scenario_id, decision, role_name):
    """
    Add decision to current scenario period, step the model and save result
    """
    if scenario_id is None:
        click.secho("ERROR: scenario_id must specified", fg='red')
        return

    async with games_client as api_session:
        game = await api_session.games.get(slug='simpl-div')

        role = await api_session.roles.get(
            game=game.id,
            name=role_name,
        )

        period = await api_session.periods.get(scenario=scenario_id)

        # add submitted decision to current period
        await save_decision(period.id, role.id, decision)

        result = None
        decisions = await api_session.decisions.filter(scenario=period.id)
        if len(decisions) == 2:
            # calculate new result
            result = await divide(scenario_id)

        click.echo("result is {}".format(result))
