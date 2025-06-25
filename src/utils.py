def to_units(total: dict) -> dict:
    return {
        "biere": round(total["biere"]),  # 1 unité = 1 canette/bouteille
        "soft_bouteilles": round(total["soft"] / 5),
        "pizza_entieres": round(total["pizza"] / 8)
    }
