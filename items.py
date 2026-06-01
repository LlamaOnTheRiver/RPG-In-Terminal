import data


def heal_small():
    amount = 20
    data.PLAYER["hp"] = min(data.PLAYER["max_hp"], data.PLAYER["hp"] + amount)
    return {"msg":f"You eat the bread. It's dry, but you feel better (+{amount} HP)."}

def heal_large():
    amount = 50
    data.PLAYER["hp"] = min(data.PLAYER["max_hp"], data.PLAYER["hp"] + amount)
    return {"msg":f"You drink the potion. A warm glow spreads through your limbs (+{amount} HP)."}

def sanity_small():
    amount = -20
    data.PLAYER['sanity'] = min(data.PLAYER['max_sanity'], data.PLAYER['sanity'] + amount)
    return {"msg":f"You eat the hair??? It's revolting, but you swallow it whole. (-{amount} sanity)."}

def xp_boost():
    amount = +90
    data.PLAYER['xp'] += amount


def teleport_home():
    data.PLAYER["current_map"] = 1
    data.PLAYER["x"], data.PLAYER["y"] = 1, 1
    return {"msg": "The scroll vanishes in a flash of blue light! You are home."}


# This is the "Registry" that the engine will look at
ITEM_REGISTRY = {
    "Bread": heal_small,
    "Health Potion": heal_large,
    "Teleport Scroll": teleport_home,
    "Hair": sanity_small,
    "XP Pot":xp_boost,
}