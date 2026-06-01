import random


PLAYER = {
        "name": "Hero",
        "hp": 50,
        "gp": 0,
        "xp": 0,
        "xp_curve": 50,
        "level": 1,
        "stat_points": 0,
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
GAME_STATE = {
        "x": 1,
        "y": 1,
        "current_map": 2,
        "marker": "\033[94mP\033[0m",
        "fog_map": []

}
visited_levels = {}

DUNGEON = {
    1: {
        "map": [
            ["$", ".", ".",".", ".", ".","W", "G", "G"],
            ["T", ".", ".","W", ".", "W","W", "G", "G"],
            ["T", ".", ".","W", ".", ".",".", ".", "S"]
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
            ["E",".",".","G","W",".",".",".",".",".",".",".",".",".",".",".",".",".",".",".","."],
            [".",".",".","G","W",".",".",".",".",".",".",".",".",".","W",".",".",".",".",".","."],
            [".",".",".",".","W","W","W",".","W","W","W","W","W","W","W",".",".",".",".",".","."],
            ["W","E","W","W","W",".",".",".",".","W",".",".",".",".","W",".",".",".",".",".","."],
            [".",".",".",".","S",".",".",".",".","W",".","W",".",".",".",".",".",".",".",".","."],
            [".",".",".",".",".",".",".",".",".","W",".","W",".",".","W",".",".",".",".",".","."],
            [".",".",".",".",".",".",".",".",".","W",".","W",".",".","W","W","W","W","W","W","W"],
            [".",".",".","W","T","W","W","W","W","W",".","W",".",".",".",".",".",".",".",".","."],
            [".",".",".","W","E",".",".","W","E","W",".","W",".",".",".",".",".",".",".",".","."],
            ["T",".",".","W",".",".",".","W",".","W",".","W","W","W","W","W","W","W","W","W","."],
            ["G","T",".","W",".",".",".",".",".","W",".",".",".",".",".",".","W",".",".",".","."],
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
        "$": {"msg": "", "shop": True},
        "E": {"event": True,"consume": "."},
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
    "Crooked Blade": {
                "value": 50,
                "type": "equipment",
                "slot": "Sword",
                "stats": {"atk": 3},
            },
}


DIALOGUE_NODES = {

    (0, 0, 0): {
        "speaker": "Master Copy",
        "text": [""],
        "options": {
            "1": {
                "text": "[Dread]",
                "skill_required": "",
                "difficulty": 0,
                "success_node": "",
                "failure_node": ""
            },
            "2": {
                "text": "[Instinct]",
                "skill_required": "",
                "difficulty": 0,
                "success_node": "",
                "failure_node": ""
            },
        },
        },
    #///Physical Triggers///
    (2, 1, 3): {
        "speaker": "Cracked Wall",
        "text": ["The wall looks cracked, it has been degrading here over centuries.",
        "You feel a slight breeze coming from the other side."],
        "options": {
            "1": {
                "text": "[Dread] Bash the wall in with your head.",
                "skill_required": "dread",
                "difficulty": 12,
                "success_node": "m2:cracked_wall:busted",
                "failure_node": "m2:cracked_wall:hurt"
            },
            "2": {
                "text": "[Instinct] Look for the weakest point and use your shoulder to bust in",
                "skill_required": "instinct",
                "difficulty": 12,
                "success_node": "m2:cracked_wall:busted",
                "failure_node": "m2:cracked_wall:hurt"
            },
        },
        },
    (2, 0, 0): {
            "speaker": "Chest",
            "text": ["You see a chest full of gold and potions.",
                     "Your eyes grow big as you decide to take the whole stash",
                     "You see an old note stuck to the top of the lid",
                     "Choose One: Take a potion or gold"],
            "options": {
                "1": {
                    "text": "You take some of the gold and obey the solemn note",
                    "effect":{"gp": random.randint(25, 75)},
                    "next_node": "end",
                },
                "2": {
                    "text": "Gold is worthless to you. You take a potion and close the chest lid.",
                    "effect":{"inventory": "Small Health Potion" },
                    "next_node": "end",
                },
                "3": {
                    "text": "[Cunning]You take the note crumple it up and eat it. All the treasure is yours!",
                    "skill_required": "cunning",
                    "difficulty": 20,
                    "success_node": "m2:chest:treasure",
                    "failure_node": "m2:chest:sanity"
                },
            },
    },

    (2, 4, 8): {
            "text": ["The room looks crude. Grime lines the walls.",
                     "Makeshift crooked cupboards cover a portion of",
                     "the wall. It appears to be made out of bone and",
                     "some type of sinew holding everything together.",
                     "Utensils are scattered over the countertops.",
                     "You hear a noise coming from the corner of the",
                     "room. It sounds like a small creature is in",
                     "pain. The heavy labored breathing and pungent",
                     "stench that wafts through the room seems to say",
                     "the creature is near death."],
            "next_node": "end",
            },

    (2, 8, 8): {
            "speaker": "Goblin",
            "text": ["As you draw near you can see the shelves held up by bones",
                     "in this small room. On the shelves are a number of jars",
                     "with different concoctions of body parts. There are strange",
                     "spices in the air. That are all repugnant. in the corner",
                     "there lies a small goblin, wounded it's thick ichor is",
                     "draining from the crude knife that's stuck in its stomach.",
                     "It looks up at you, sensing that you are the predator and",
                     "it is the prey. It wallows its final cry, defeated. 'Ick rak",
                     "grald nkree.' its hand shakes as it goes for the knife stuck",
                     "in its belly, about to finish the job."],
            "options": {
                "1": {
                    "text": "[Instinct] Stop the goblin from killing itself.",
                    "skill_required": "instinct",
                    "difficulty": 12,
                    "success_node": "m2:goblin:alive",
                    "failure_node": "m2:goblin:dead",
                },
                "2": {
                    "text": "You are the preditor. Take the knife and finish the job.",
                    "next_node": "m2:goblin:dead",
                    "effect":{"inventory": "Crooked Blade" },
                },
            },
            },


        #///The Story Branches///
        "master": {
            "speaker": "",
            "text": [""],
            "options": {"1": {"text": "Continue", "next_node": "end"}},
            "effect": {"inventory": "" },
            "next_node": "end",
        },
        "m2:cracked_wall:busted": {
            "speaker": "Cracked Wall",
            "text": ["The wall crumbles away and a new path lies before you."],
            "options": {"1": {"text": "Continue", "next_node": "end"}},
        },

        "m2:cracked_wall:hurt": {
            "speaker": "Cracked Wall",
            "text": ["You decided to bash in the wall with your skull.",
                     "Your head rings in protest as the wall crumbles away.",
                     "You feel your health drain."],
            "options": {"1": {"text": "Regret everything", "next_node": "end"}},
            "effect": {"hp": -10},
        },

        "m2:chest:treasure": {
            "speaker": "Chest",
            "text": ["Your greed pays off. You snatch the gold and potions before the chest can shut on you.",
                     "The chest shuts tight, never to be opened again."],
            "next_node": "end",
            "effect": {"gp": random.randint(25, 75), "inventory": "Small Health Potion", "sanity": -10},
        },

        "m2:chest:sanity": {
            "speaker": "Chest",
            "text": ["You try and dart your hand into the chest. Too late.",
                     "The chest shuts tight, your arm still in it.",
                     "You writhe in pain as you manage to pull your",
                     "arm out. The chest is locked with your blood",
                     "staining the gold, never to be seen again.",
                     "You stand back in horror and walk away from"
                     "the chest."],
            "next_node": "end",
            "effect": {"hp": -10, "sanity": -15}
        },
        "m2:goblin:alive": {
            "speaker": "Goblin",
            "text": [""],
            "options": {
                "1": {
                    "text": "Continue",
                    "next_node": "end"
                },
                "2": {
                    "text": "[Bread] give the goblin a loaf of bread",
                    "item_required": {"Bread": 1},
                    "next_node": "end"

                }
            },
            "effect": {"sanity": 20,"inventory": "" },
        },
        "m2:goblin:dead": {
            "speaker": "Goblin",
            "text": ["The goblin groans in pain.",
                     "It lets out its final cry",
                     "and then it is listless on",
                     "the floor. You walk away",
                     "with nothing more to do"],
            "options": {"1": {"text": "Continue", "next_node": "end"}},
            "effect": {"sanity": -10, "inventory": "" },
        },
}










