DUNGEON = {
    1: {
        "map": [
            [".", ".", "G"],
            [".", "W", "."],
            ["T", ".", "S"]
        ],
        "stairs":{
            (2,2): {"target_map": 2, "target_x": 4, "target_y": 3},
        },
        "monsters": [
            {"x": 2, "y": 0, "marker": "M", "name": "Rat", "dmg": 5}
        ]
    },
    2: {
        "map": [
            [".",".",".","G","G",".",".",".","G","G",],
            [".",".",".","G","G",".",".",".","G","G",],
            [".",".",".","G","G",".",".",".","G","G",],
            [".",".",".","G",".",".",".",".","G","G",],
            [".","T","T","G","S","W","W","W","G","G",],
            [".","T","T","G","G",".",".","W","G","G",],
            [".",".",".","G","G",".",".","W","G","G",],
            [".",".",".","G","G","H","H",".","G","G",],
            [".",".",".","G","G",".",".",".","G","G",],
            [".",".",".","G","G",".",".",".","G","G",],
        ],
        "monsters": [
            {"x": 1, "y": 2, "marker": "G", "name": "Ghost", "dmg": 20},
            {"x": 4, "y": 0, "marker": "M", "name": "Goblin", "dmg": 15},
            {"x": 0, "y": 2, "marker": "S", "name": "Shadow", "dmg": 25}
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
        "x": 2,
        "y": 2,
        "current_map": 1,
        "monsters": DUNGEON[1]["monsters"],
        "hp": 100,
        "gp": 0,
        "marker": "P",
        "max_hp": 200
}

