from decimal import ROUND_HALF_UP, Decimal


def round_up_two_places(item: Decimal) -> Decimal:
    return item.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
