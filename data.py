DUNGEON = {
    1: {
        "map": [
            [".", ".", ".",".", ".", ".","W", "G", "G"],
            [".", ".", ".","W", ".", "W","W", "G", "G"],
            [".", ".", ".","W", ".", ".",".", ".", "S"]
        ],
        "stairs":{
            (2,8): {"target_map": 2, "target_x": 4, "target_y": 4},
        },
        "monsters": [
            {"name": "Rat", "x": 2, "y": 0, "marker": "\033[91mM\033[0m", "hp": 15, "dmg": 5},
            {"name": "Rat", "x": 5, "y": 0, "marker": "\033[91mM\033[0m", "hp": 15, "dmg": 5},
]
    },
    2: {
        "map": [
            [".",".",".","G","G",".",".",".","G","G",],
            [".",".",".","G","G",".",".","H","G","G",],
            [".","H",".","G","G",".",".",".","G","G",],
            [".",".",".","G",".","H",".",".","G","G",],
            [".","T","T","G","S","W","W","W","G","G",],
            [".","T","T","G","G",".",".","W","G","G",],
            [".",".",".","G","G",".",".","W","G","G",],
            [".",".",".","G","G","H","H",".","G","G",],
            [".",".",".","G","G",".",".",".","G","G",],
            [".",".",".","G","G",".",".",".","G","G",],
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
        "G": {"msg": "GOLD! +5 GP", "gp": 5, "consume": "."},
        "H": {"msg": "HEALED! HP to 100", "hp": 100, "consume": "."},
        "W": {"msg": "A solid wall.", "block": True},
        "S": {"msg": "You begin to travel to another floor.", "teleport": True},
    }

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
        "max_hp": 200,
        "max_sanity": 100,
        "sanity": 100,
        "stats": {
            "dread": 0, #Todo Maybe Like Kreig from borderlands
            "instinct": 0, #Todo Migi from parasyte natural hardwired reaction
            "vigor": 0, #Todo Tank like ability with regeneration Zorro from One Piece
            "cunning": 0, #Todo Sora from no game no life achieving goal through decit or manipulation
            "bastion": 0
        },
        "inventory": {
            "Health Potion": 2,
            "Bread": 1,
            "Hair": 6,
            "Sword": 3,
            "Water": 4,
            "Gold": 5,
            "Poop": 3
        }
}

MONSTERS = {
    "Rat": {
        "name": "Rat",
        "hp": 15,
        "dmg": 75,
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
        "hp": 20,
        "dmg": 15,
        "madness_yield": 2,
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
visited_levels = {}

LOOT_DATA = {
    "common": ["Rusty Sword", "Small Health Potion", "Leather Scraps"],
    "rare": ["Steel Longsword", "Large Health Potion", "Iron Shield"],
    "epic": [],
    "legendary": ["Excalibur", "Dragon Scale Armor"]
}

