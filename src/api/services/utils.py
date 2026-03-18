import math


def to_units(total: dict) -> dict:
    return {
        "beer": math.ceil(total["beer"]),
        "softBottle": math.ceil(total["soft"] / 5),
        "pizza": math.ceil(total["pizza"] / 8),
    }
