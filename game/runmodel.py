from modelservice.simpl import games_client
from .model import Model


async def save_decision(period_id, role_id, operand):
    # add/update role's decision for period
    async with games_client as api_session:
        decision = await api_session.decisions.get_or_create(
            period=period_id,
            name='decision',
            role=role_id
        )
        decision.data["operand"] = float(operand)
        await decision.save()
        return decision


async def divide(period_id):
    """
    (Re)calculates the result of the period's Dividend and Divisor decisions.
    """
    async with games_client as api_session:
        period = await api_session.periods.get(scenario=period_id)
        period_decisions = await api_session.decisions.filter(period=period.id)

        dividend, divisor = None, None
        for decision in period_decisions:
            role = await api_session.roles.get(id=decision.role)
            if role.name == 'Dividend':
                dividend = decision.data["operand"]
            else:
                divisor = decision.data["operand"]

        if dividend is None or divisor is None:
            return None

        # run model
        model = Model()
        quotient = model.step(dividend, divisor)

        result = await api_session.results.get_or_create(
            period=period.id,
            name="result",
            defaults={"role": None}
        )
        result.data["quotient"] = quotient
        await result.save()

        return quotient
