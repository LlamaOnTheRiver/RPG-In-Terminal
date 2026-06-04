import random


PLAYER = {
        "name": "Hero",
        "hp": 50,
        "gp": 0,
        "xp": 0,
        "xp_curve": 50,
        "level": 20,
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
            "Goblin Emblem": 1,
        }
}
GAME_STATE = {
        "x": 10,
        "y": 1,
        "current_map": 2,
        "marker": "\033[94mP\033[0m",
        "fog_map": []

}
visited_levels = {}

DUNGEON = {
    1: {
        "map": [
            [".", ".", ".",".", ".", ".","W", "G", "G"],
            ["T", ".", ".","W", ".", "W","W", "G", "G"],
            ["T", ".", ".","W", ".", ".",".", ".", "S"]
        ],
        "stairs":{
            (2,8): {"target_map": 2, "target_x": 4, "target_y": 4},
        },
        "monsters":[
            {"name": "Rat", "x": 2, "y": 0, "marker": "\033[91mM\033[0m"},
            {"name": "Rat", "x": 5, "y": 0, "marker": "\033[91mM\033[0m"}
        ],
    },

    2: {
        "map": [
            ["E",".",".","G","W",".",".",".",".",".",".",".","T",".","E",".",".","W","W",".","G"],
            [".",".",".","G","W","$",".",".",".",".","T",".",".",".","W",".",".",".",".","T","."],
            [".",".",".",".","W","W","W","E","W","W","W","W","W","W","W",".",".",".",".","W","."],
            ["W","E","W","W","W",".",".",".",".","W",".","M",".",".","W",".",".",".",".","W","."],
            [".",".",".",".","S",".",".",".",".","W",".","W",".",".",".",".",".","W","W",".","."],
            [".",".",".",".",".",".",".",".",".","W",".","W",".",".","W",".",".","T",".",".","G"],
            [".",".",".",".",".",".",".",".",".","W",".","W",".",".","W","W","W","W","W","W","W"],
            [".",".",".","W","T","W","W","W","W","W",".","W",".",".",".",".",".",".",".",".","."],
            [".",".",".","W","E",".",".","W","E","W",".","W",".",".",".",".",".",".",".",".","."],
            ["T",".","T","W",".",".",".","W",".","W",".","W","W","W","W","W","W","W","W","W","."],
            ["G","T","G","W",".",".",".",".",".","W",".",".",".",".",".",".","W",".",".",".","."],
        ],
        "stairs":{(4,4): {"target_map": 1, "target_x": 8, "target_y": 2},
                  },
        "monsters": [
            {"name": "Ghoul", "x": 1, "y": 2, "marker": "\033[91mM\033[0m"},
            {"name": "Goblin", "x": 4, "y": 0, "marker": "\033[91mM\033[0m"},
            {"name": "Goblin", "x": 0, "y": 2, "marker": "\033[91mM\033[0m"}
        ],
        "shop":{
                    "Small Health Potion": 10,
                    "Bread": 5,
                    "Iron Helmet": 1,
                    "Iron Boots": 1,
                },
    }
}


TILE_EFFECTS = {
        "T": {"msg": "TRAP! -10 HP", "hp": -10, "consume": "."},
        "[": {"hp": -10, "consume": "."},
        "]": {"hp": -10, "consume": "."},
        "G": {"msg": "GOLD! +15 GP", "gp": 15, "consume": "."},
        "H": {"msg": "HEALED! HP to 100", "hp": 100, "consume": "."},
        "W": {"msg": "A solid wall.", "block": True},
        "S": {"msg": "You begin to travel to another floor.", "teleport": True},
        "$": {"msg": "", "shop": True},
        "E": {"event": True,"consume": "."},
        "M": {"msg": "This wall seems a little loose. Your not sure how to get past it.", "block": True},
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
        "intro":["The rat looks hideously deformed.", "It starts oozing ",
                "yellowish thick liquid from it's pours"],
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
    "The Craftsman": {
        "name": "The Craftsman",
        "hp": 35,
        "dmg": 21,
        "madness": 10,
        "can_escape": False,
        "intro":["The Craftsman twirls its' hammer in his hand,"
                 "rage in his eyes, for destroying his precious",
                 "bones."],
        "cry":["'Hak nar wrathek!'"],
        "loot_weights": {
            "common": 70,
            "rare": 25,
            "epic": 5,
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
    "epic": ["Big Nose"],
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

    #///Quest///
    "Goblin Emblem":{
        "type": "quest"
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
            "text": ["You see a chest full of gold and potions. ",
                     "Your eyes grow big as you decide to take the whole stash ",
                     "You see an old note stuck to the top of the lid ",
                     "Choose One: Take a potion or gold"],
            "options": {
                "1": {
                    "text": "You take some of the gold and obey the solemn note",
                    "effect":{"gp": random.randint(25, 75)},
                    "next_node": "end",
                },
                "2": {
                    "text": "Gold is worthless to you. You take a potion and close the chest lid.",
                    "effect":{"inventory": {"Small Health Potion": 1} },
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
            "text": ["The room looks crude. Grime lines the walls. ",
                     "Makeshift crooked cupboards cover a portion of ",
                     "the wall. It appears to be made out of bone and ",
                     "some type of sinew holding everything together. ",
                     "Utensils are scattered over the countertops. ",
                     "You hear a noise coming from the corner of the ",
                     "room. It sounds like a small creature is in ",
                     "pain. The heavy labored breathing and pungent ",
                     "stench that wafts through the room seems to say ",
                     "the creature is near death."],
            "next_node": "end",
            },

    (2, 8, 8): {
            "speaker": "Goblin",
            "text": ["As you draw near you can see the shelves held up by bones ",
                     "in this small room. On the shelves are a number of jars ",
                     "with different concoctions of body parts. There are strange ",
                     "spices in the air. That are all repugnant. in the corner ",
                     "there lies a small goblin, wounded it's thick ichor is ",
                     "draining from the crude knife that's stuck in its stomach. ",
                     "It looks up at you, sensing that you are the predator and ",
                     "it is the prey. It wallows its final cry, defeated. 'Ick rak ",
                     "grald nkree.' its hand shakes as it goes for the knife stuck ",
                     "in its belly, about to finish the job."],
            "options": {
                "1": {
                    "text": "[Instinct] Stop the goblin from killing itself.",
                    "skill_required": "instinct",
                    "difficulty": 1,
                    "success_node": "m2:goblin:alive",
                    "failure_node": "m2:goblin:dead",
                },
                "2": {
                    "text": "You are the preditor. Take the knife and finish the job.",
                    "next_node": "m2:goblin:dead",
                    "effect":{"inventory": {"Crooked Blade": 1} },
                },
            },
            },

    (2, 14, 0): {
            "speaker": "The Craftsman",
            "text": ["Bones litter this room of all different shapes and sizes.",
                     "The horrid smell of dried flesh and cut bone wafts through",
                     "the air. You use the inside of your shirt as meager protection",
                     "against the assaulting smell. You see 3 workbenches, lined up",
                     "towards the far wall. Laying haphazardly all around the benches",
                     "there are all manner of interesting tools at the heart of the operation,",
                     "a craftsman is hard at work at the bench, making what looks like a spear",
                     "His thin ashen body stands about 4 feet tall. His snow white hair disheveled.",],
            "options": {
                "1": {
                    "text": "[Instinct] Sneak your way past.",
                    "skill_required": "instinct",
                    "difficulty": 10,
                    "success_node": "m2:the_craftsman:sneak",
                    "failure_node": "m2:the_craftsman:alert",
                },
                "2": {
                    "text": "[Cunning] Try and talk to the craftsman",
                    "skill_required": "cunning",
                    "difficulty": 20,
                    "success_node": "m2:the_craftsman:talk",
                    "failure_node": "m2:the_craftsman:attack",
                },
                "3": {
                    "text": "Attack the craftsman",
                    "next_node": "m2:the_craftsman:attack",
                },
                "4": {
                    "text": "[Goblin Emblem]Show him your emblem.",
                    "item_required": {"Goblin Emblem": 1},
                    "next_node": "m2:the_craftsman:talk",
                },
            },
            },
    (2, 7, 2): {
                "speaker": "Rubble",
                "text": ["Before you is  A large pile of rocks. It "
                         "Looked like a cave in happened centuries ago",
                         "There are huge chunks of what looks like, "
                         "marble. This room or what you can see of it, ",
                         "looks extravagant. In the far distance beyond ",
                         "the rubble that blocks your path. You could see ",
                         "what looks like a dilapidated chair. You can imagine ",
                         "it back when this cavern use to be a throne room. How ",
                         "many guests did it entertain? You think back to your ",
                         "recent situation. 'Neil... is that why you did it? for ",
                         "the throne? We were on the same path. We could of done ",
                         "this together. We....",
                         "Neil, brother I don't understand."],
                },


        #///The Story Branches///
        "master": {
            "speaker": "",
            "text": [""],
            "options": {"1": {"text": "Continue", "next_node": "end"}},
            "effect": {"inventory": {} },
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
            "effect": {"gp": random.randint(25, 75), "inventory": {"Small Health Potion" : 1}, "sanity": -10},
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
            "text": ["You reach for the Goblins hand and smack it away.",
                     "You say to the goblin. 'I am friend.' He seems to",
                     "understand. 'Wait here a second. I'm going to find",
                     "something to stop the bleeding.' He looks desperate.",
                     "You go into the other room searching and scanning,",
                     "until you see it there on the table. Crude empty",
                     "bone plates and bowels are haphazardly scattered",
                     "about. a small rugged candle is the centerpiece",
                     "dimly lighting the room. The tablecloth drapes",
                     "over. You grab the candle and place it aside for",
                     "now. You take the tablecloth and yank it from out",
                     "of it's place, throwing all the bowls and utensils",
                     "all over the room. You head back to the goblin and",
                     "find the cleanest part of the tablecloth and rip it",
                     "apart to make strips. He looks confused. 'Brace yourself,",
                     "this is going to hurt. You pull out the blade and quickly",
                     "tie the cloth around his abdomen. He Howls out in pain",
                     "and begins to claw around scratching you a couple times.",
                     "You brace yourself and tie the cloth tight. After a few",
                     "agonizing moments, the situation seems to calm down.",
                     "He then reaches for the side of his loincloth and tears",
                     "off a piece of it. He hands it to you. 'Huk zra nub gratz'",
                     "You look at the cloth, an emblem of some kind. He repeats",
                     "himself. 'Huk zra nub gratz.' 'Thank you friend, rest well.'",
                     "Despite there being 'food' around in this pantry. You see",
                     "That he's starving."],
            "options": {
                "1": {
                    "text": "You've done all you can. The rest is up to him.",
                    "next_node": "end"
                },
                "2": {
                    "text": "[Bread] give the goblin a loaf of bread",
                    "item_required": {"Bread": 1},
                    "next_node": "m2:goblin:bread"

                }
            },
            "effect": {"sanity": 20,"inventory": {"Goblin Emblem": 1} }

        },
        "m2:goblin:dead": {
            "speaker": "Goblin",
            "text": ["The goblin groans in pain. ",
                     "It lets out its final cry ",
                     "and then it is listless on ",
                     "the floor. You walk away ",
                     "with nothing more to do"],
            "options": {"1": {"text": "Continue", "next_node": "end"}},
            "effect": {"sanity": -10},
        },
        "m2:goblin:bread": {
                    "speaker": "Goblin",
                    "text": ["He eats the bread wincing, the cloth wrapped around ",
                             "him has stopped for now. You feel like this is all ",
                             "you can do for him now. 'Good luck friend.' 'Ark uh ",
                             "tar tar.' You step out into the dining area feeling "
                             "relieved."],
                    "effect": {"inventory": {"Bread": -1}, "sanity": 15},
                    "next_node": "end",
        },
        "m2:the_craftsman:sneak": {
                    "speaker": "The Craftsman",
                    "text": ["You sneak past him, not to disturb his work.",
                             "You feel a sense of clarity come over you."],
                    "effect": {"sanity": 15, "xp": 50},
                    "next_node": "end",
        },
        "m2:the_craftsman:alert": {
                    "speaker": "The Craftsman",
                    "text": ["You try and sneak past. To your horror, you trip over",
                             "One of the bones and the bone pile comes clanking down.",
                             "The craftsman whips around in a state of shock. He then",
                             "see's you and that shock turns into rage. He picks up his",
                             "hammer and begins his attack. To a craftsman, his work is",
                             "life or death."],
                    "battle": {
                            "enemy": "The Craftsman",
                            "win_next": "m2:the_craftsman:defeated",
                            "lose_next": "m2:the_craftsman:won"
                    },
                    "effect": {"inventory": {} },
                    "next_node": "end",
        },
        "m2:the_craftsman:talk": {
                    "speaker": "",
                    "text": [""],
                    "options": {"1": {"text": "Continue", "next_node": "end"}},
                    "effect": {"inventory": {} },
                    "next_node": "end",
        },
        "m2:the_craftsman:attack": {
                    "battle": {
                            "enemy": "The Craftsman",
                            "win_next": "m2:the_craftsman:defeated",
                            "lose_next": "m2:the_craftsman:won"
                    },
        },
        "m2:the_craftsman:defeated": {
                    "speaker": "The Craftsman",
                    "text": ["'Ugol nor greetz nkrall.' The Craftsman",
                             "looks at you with detest full in its eyes",
                             "he understands the law of the land. He is",
                             "the prey and you are the preditor. He clutches",
                             "his chest tight. Blood staining his silver body",
                             "He looks over to his hammer. The thing that helped",
                             "him, a non-fighter survive in this unforgiving dark.",
                             "you step on his arm and kick his hand away. This",
                             "hammer you earned by defeating this evil goblin.",
                             "it is your right to carry, your honor. You take the",
                             "hammer and finish the job that you started. You take",
                             "the last breath from him and laugh in his face."],
                    "effect": {"inventory": {"Bone Hammer": 1}, "sanity": -20 },
                    "next_node": "end",
        },
        "m2:the_craftsman:won": {
                    "speaker": "The Craftsman",
                    "text": [""],
                    "options": {"1": {"text": "Continue", "next_node": "end"}},
                    "effect": {"inventory": {} },
                    "next_node": "end",
        },
        "master": {
                    "speaker": "",
                    "text": [""],
                    "options": {"1": {"text": "Continue", "next_node": "end"}},
                    "effect": {"inventory": {} },
                    "next_node": "end",
        },

}










