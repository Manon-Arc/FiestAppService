def to_units(total: dict) -> dict:
    return {
        "biere": int(round(total["biere"])),  # 1 unité = 1 canette/bouteille
        "bouteille_softs": int(round(total["soft"] / 5)),
        "pizza_entieres": int(round(total["pizza"] / 8))
    }
