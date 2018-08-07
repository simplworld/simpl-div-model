import asyncio

from modelservice.games import Period, Game
from modelservice.games import subscribe, register

from .runmodel import divide, save_decision


class SimplDivPeriod(Period):
    @register
    async def submit_decision(self, operand, **kwargs):
        """
        Receives the operand played and saves as a ``Decision``.
        If decisions for both roles have been saved,
        runs the model saving the ``Result``.
        """
        # Call will prefix the ROOT_TOPIC
        # "world.simpl.sims.simpl-div.model.period.1.submit_decision"

        for k in kwargs:
            self.session.log.info("submit_decision: Key: {}".format(k))

        user = kwargs['user']
        runuser = self.game.get_scope('runuser', user.runuser.pk)
        role = runuser.role

        role_name = role.json["name"]
        if role_name == "Divisor" and float(operand) == 0:
            return "Cannot divide by zero"

        await save_decision(self.pk, role.pk, operand)
        self.session.log.info(
            "submit_decision: saved decision for role {}".format(role_name))

        #pause while the scopes update
        await asyncio.sleep(0.01)

        if len(self.decisions) == 2:
            await divide(self.scenario.pk, )
            self.session.log.info("submit_decision: saved result")

        return 'ok'


Game.register('simpl-div', [
    SimplDivPeriod,
])
