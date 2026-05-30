PLAYER = {
        "name": "Hero",
        "x": 1,
        "y": 1,
        "current_map": 1,
        "hp": 50,
        "gp": 0,
        "xp": 0,
        "level": 1,
        "stat_points": 0,
        "marker": "\033[94mP\033[0m",
        "max_hp": 50,
        "max_sanity": 100,
        "sanity": 100,
        "stats": {
            "dread": 0, #Todo Maybe Like Kreig from borderlands
            "instinct": 0, #Todo Migi from parasyte natural hardwired reaction
            "vigor": 0, #Todo Tank like ability with regeneration Zorro from One Piece
            "cunning": 0, #Todo Sora from no game no life achieving goal through decit or manipulation
            "bastion": 0
        },
        "equipment":{
            "Helmet": None,
            "Chestplate": None,
            "Sword": None,
            "Leggings": None,
            "Boots": None,
        },
        "inventory": {
            "Health Potion": 2,
            "Bread": 1,
            "Hair": 6,
            "Sword": 3,
            "Water": 4,
            "Gold": 5,
            "XP Pot": 13,
            "Iron Helmet": 1,
            "Steel Helmet": 2,
        }
}
visited_levels = {}

DUNGEON = {
    1: {
        "map": [
            [".", ".", ".",".", ".", ".","W", "G", "G"],
            [".", ".", ".","W", ".", "W","W", "G", "G"],
            ["$", ".", ".","W", ".", ".",".", ".", "S"]
        ],
        "stairs":{
            (2,8): {"target_map": 2, "target_x": 4, "target_y": 4},
        },
        "monsters":[
            {"name": "Rat", "x": 2, "y": 0, "marker": "\033[91mM\033[0m", "hp": 15, "dmg": 5},
            {"name": "Rat", "x": 5, "y": 0, "marker": "\033[91mM\033[0m", "hp": 15, "dmg": 5}
        ],
        "shop":{
            "Small Health Potion": 10,
            "Bread": 5,
            "Iron Helmet": 50,
        },
    },

    2: {
        "map": [
            [".",".",".",".","W",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".","."],
            [".",".",".",".","W",".",".",".",".",".",".",".",".",".","W",".",".",".",".",".","."],
            [".",".",".",".","W","W","W",".","W","W","W","W","W","W","W",".",".",".",".",".","."],
            ["W",".","W","W","W",".",".",".",".","W",".",".",".",".","W",".",".",".",".",".","."],
            [".",".",".",".","S",".",".",".",".","W",".","W",".",".",".",".",".",".",".",".","."],
            [".",".",".",".",".",".",".",".",".","W",".","W",".",".","W",".",".",".",".",".","."],
            [".",".",".",".",".",".",".",".",".","W",".","W",".",".","W","W","W","W","W","W","W"],
            [".",".",".","W",".","W","W","W","W","W",".","W",".",".",".",".",".",".",".",".","."],
            [".",".",".","W",".",".",".",".",".","W",".","W",".",".",".",".",".",".",".",".","."],
            [".",".",".","W",".",".",".",".",".","W",".","W","W","W","W","W","W","W","W","W","."],
            [".",".",".","W",".",".",".",".",".","W",".",".",".",".",".",".","W",".",".",".","."],
        ],
        "stairs":{(4,4): {"target_map": 1, "target_x": 8, "target_y": 2},
                  },
        "monsters": [
            {"name": "Ghoul", "x": 1, "y": 2, "marker": "\033[91mM\033[0m", "hp": 25, "dmg": 10},
            {"name": "Goblin", "x": 4, "y": 0, "marker": "\033[91mM\033[0m", "hp": 25, "dmg": 5},
            {"name": "Goblin", "x": 0, "y": 2, "marker": "\033[91mM\033[0m", "hp": 25, "dmg": 5}
        ]
    }
}


TILE_EFFECTS = {
        "T": {"msg": "TRAP! -10 HP", "hp": -10, "consume": "."},
        "G": {"msg": "GOLD! +15 GP", "gp": 15, "consume": "."},
        "H": {"msg": "HEALED! HP to 100", "hp": 100, "consume": "."},
        "W": {"msg": "A solid wall.", "block": True},
        "S": {"msg": "You begin to travel to another floor.", "teleport": True},
        "$": {"msg": "Welcome {name}, come and see my wares", "shop": True},
    }

MONSTERS = {
    "Ghoul": {
            "name": "Ghoul",
            "hp": 20,
            "dmg": 15,
            "madness": 4,
            "intro":["The Ghouls wispy form appears before you, wretched and torn."],
            "cry":["The Ghoul swipes through you with it's clawlike hand. Hitting your soul."],
            "loot_weights": {
                "common": 90,
                "rare": 10,
                "epic": 0,
                "legendary": 0
            },
    },
    "Rat": {
        "name": "Rat",
        "hp": 15,
        "dmg": 5,
        "madness": 2,
        "intro":["The rat looks hideously deformed.", "It starts oozing yellowish thick liquid from it's pours"],
        "cry":["The oily rat lunges at you", "and starts gnawing on your flesh."],
        "loot_weights": {
            "common": 90,
            "rare": 10,
            "epic": 0,
            "legendary": 0
        }
    },
    "Goblin": {
        "name": "Goblin",
        "hp": 20,
        "dmg": 15,
        "madness": 3,
        "intro":["The Goblin takes it jagged club and licks the blood off it before attacking you."],
        "cry":["The crooked Goblin raises it's club and strikes!"],
        "loot_weights": {
            "common": 90,
            "rare": 10,
            "epic": 0,
            "legendary": 0
        }

    },
    "Dragon": {
        "hp": 500,
        "dmg": 50,
        "madness_yield": 50,
        "loot_weights": {
            "common": 20,
            "rare": 50,
            "legendary": 30
        }
    }
}


LOOT_DATA = {
    "common": ["Rusty Sword", "Small Health Potion", "Leather Scraps"],
    "rare": ["Steel Longsword", "Large Health Potion", "Iron Shield"],
    "epic": [],
    "legendary": ["Excalibur", "Dragon Scale Armor"]
}
ITEMS = {
    #///CONSUMABLES///
    "Small Health Potion": {
        "type": "consumable",
        "value": 100
    },
    "Bread":{
        "type": "consumable",
        "value": 50,
    },





    #///EQUIPMENT///
    "Iron Helmet": {
        "value": 200,
        "type": "equipment",
        "slot": "Helmet",
        "stats": {"accuracy": 5, "crit_chance": 4, "regen": 3, "max_hp": 2, "armor": 7, "dread": 404, "vigor": 2},
    },
    "Iron Leggings": {
            "value": 200,
            "type": "equipment",
            "slot": "Leggings",
            "stats": {"accuracy": 5, "vigor": 2},
        },
    "Iron Boots": {
            "value": 200,
            "type": "equipment",
            "slot": "Boots",
            "stats": {"accuracy": 5, "vigor": 2},
        },
    "Iron Chestplate": {
            "value": 200,
            "type": "equipment",
            "slot": "Chestplate",
            "stats": {"accuracy": 5, "vigor": 2},
        },
    "Iron Sword": {
            "value": 200,
            "type": "equipment",
            "slot": "Sword",
            "stats": {"accuracy": 5, "vigor": 2},
        },
    "Steel Helmet": {
            "value": 200,
            "type": "equipment",
            "slot": "Helmet",
            "stats": {"accuracy": 5, "vigor": 2},
        },
}
