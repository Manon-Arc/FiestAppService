def to_units(total: dict) -> dict:
    return {
        "beer": int(round(total["beer"])),
        "softBottle": int(round(total["soft"] / 5)),
        "pizza": int(round(total["pizza"] / 8)),
    }
