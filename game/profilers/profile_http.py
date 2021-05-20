import asyncio

from django.conf import settings

from modelservice.profiler import ProfileCase
from modelservice.simpl import games_client_factory


class ProfileHttpTestCase(ProfileCase):
    """
    Profile HTTP calls from the modelservice to simpl-games-api.
    """

    async def profile_submit_decision(self):
        email = self.user_email
        if email is not None:
            # print('profile_submit_decision: email=', email)

            # email format is <char><int>@ where <int> is 1..78
            # delay = int(email[1:email.find('@')])
            # await asyncio.sleep(delay * 0.5)

            coro_client = games_client_factory()

            async with coro_client as coro_session:
                try:
                    # Determine Run and Runuser based on player email
                    run_name = email[0]  # assumes run name is a single letter
                    run = await coro_session.runs.get(
                        game_slug=settings.GAME_SLUG,
                        name=run_name,
                    )
                    user = await coro_session.users.get(email=email)
                    runuser = await coro_session.runusers.get(
                        run=run.id,
                        user=user.id
                    )

                    # From here down, pull data from modelservice via WAMP
                    # emulating the calls made by the simpl-react simpl decorator

                    world_topic = 'world.simpl.sims.simpl-div.model.world.' + str(runuser.world)

                    #  getRunUsers(world_topic)
                    get_active_runusers_uri = world_topic + '.get_active_runusers'
                    get_active_runusers_result = await self.call(get_active_runusers_uri)
                    # print(get_active_runusers_uri, '->')
                    # print(get_active_runusers_result)

                    # getCurrentRunPhase(world_topic)
                    get_current_run_and_phase_uri = world_topic + '.get_current_run_and_phase'
                    get_current_run_and_phase_result = await self.call(get_current_run_and_phase_uri)
                    # print(get_current_run_and_phase_uri, '->')
                    # print(get_current_run_and_phase_result)

                    # getDataTree(world_topic)
                    get_scope_tree_uri = world_topic + '.get_scope_tree'
                    get_scope_tree_result = await self.call(get_scope_tree_uri)
                    # print(get_scope_tree_uri, '->')
                    # print(get_scope_tree_result)

                    runuser_topic = 'world.simpl.sims.simpl-div.model.runuser.' + str(runuser.id)

                    #  getRunUsers(world_topic)
                    await self.call(runuser_topic + '.get_active_runusers')  # ignore results

                    # getCurrentRunPhase(world_topic)
                    await self.call(runuser_topic + '.get_current_run_and_phase')  # ignore results

                    # getDataTree(world_topic)
                    await self.call(runuser_topic + '.get_scope_tree')  # ignore results

                    # getRunUserScenarios(runuser_topic)
                    get_scenarios_uri = runuser_topic + '.get_scenarios'
                    get_scenarios_result = await self.call(get_scenarios_uri)
                    # print(get_scenarios_uri, '->')
                    # print(get_scenarios_result)

                    # getPhases('model:model.game')
                    get_phases_uri = 'world.simpl.sims.simpl-div.model.game.get_phases'
                    get_phases_ = await self.call(get_phases_uri)
                    # print(get_phases_uri, '->')
                    # print(get_phases_)

                    # getRoles('model:model.game')
                    get_roles_uri = 'world.simpl.sims.simpl-div.model.game.get_roles'
                    get_roles_result = await self.call(get_roles_uri)
                    # print(get_roles_uri, '->')
                    # print(get_roles_result)

                    for role in get_roles_result:
                        name = role['name']
                        id = role['id']
                        if name == "Dividend":
                            dividend_role = id
                        elif name == "Divisor":
                            divisor_role = id
                        else:
                            raise Exception("ERROR: unexpected role '" + name + "'")

                    # debug simpl-div-ops#37
                    run_phase_name = get_current_run_and_phase_result['phase']['data']['name']
                    if run_phase_name != 'Play':
                        raise Exception("ERROR: Run must be in Play phase")

                    # get id of first period of first scenario of player's world
                    first_period_id = get_scope_tree_result['children'][0]['children'][0]['pk']
                    # print('first_period_id: ', first_period_id)

                except Exception as e:
                    print(e)
                    return

                # submit player's decision
                uri = 'world.simpl.sims.simpl-div.model.period.' + \
                      str(first_period_id) + '.submit_decision'
                if runuser.role is dividend_role:
                    decision = 5
                elif runuser.role is divisor_role:
                    decision = 2
                else:
                    decision = None

                if decision is not None:
                    status = await self.call_as(email, uri, decision)
                    if status != 'ok':
                        raise ValueError(
                            "submit_decision: status=" + status)
