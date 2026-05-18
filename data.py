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
            {"name": "rat1", "x": 2, "y": 0, "marker": "\033[91mM\033[0m", "hp": 15, "dmg": 5},
            {"name": "rat2", "x": 5, "y": 0, "marker": "\033[91mM\033[0m", "hp": 15, "dmg": 5},
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
            {"name": "Ghoul", "x": 1, "y": 2, "marker": "G", "hp": 25, "dmg": 10},
            {"name": "Goblin", "x": 4, "y": 0, "marker": "M", "hp": 25, "dmg": 5},
            {"name": "Goblin", "x": 0, "y": 2, "marker": "S", "hp": 25, "dmg": 5}
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
        "x": 1,
        "y": 1,
        "current_map": 1,
        "hp": 100,
        "gp": 0,
        "marker": "\033[94mP\033[0m",
        "max_hp": 200
}

