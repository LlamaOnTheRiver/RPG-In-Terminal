import engine
import data
import copy


from engine import check_for_combat, draw_battle_screen, clear_screen


def load_level(level_id):
    # .deepcopy() creates a brand new version of everything,
    # including the nested lists, so the original stays safe!
    return copy.deepcopy(data.DUNGEON[level_id])


visited_levels = {}


def get_level_data(level_id):
    # 1. If we haven't been here, create the live map
    if level_id not in visited_levels:
        visited_levels[level_id] = copy.deepcopy(data.DUNGEON[level_id]["map"])

    # 2. Always get FRESH monsters from the blueprint (Respawning)
    fresh_monsters = copy.deepcopy(data.DUNGEON[level_id]["monsters"])

    return {
        "map": visited_levels[level_id],
        "monsters": fresh_monsters,
    }

def main():
    engine.clear_screen()
    if not data.DUNGEON[1]["map"]:
        print("The world has not been created yet! (Empty Map)")
        return
    # Load the first level into a "live" variable
    game_state = "EXPLORE"
    active_enemy = None
    current_level = load_level(data.PLAYER["current_map"])
    height = len(data.DUNGEON[1]["map"])
    width = len(data.DUNGEON[1]["map"][0])
    last_map_id = 1
    fog_map = [[" " for _ in range(width)] for _ in range(height)]
    first_turn = True


    while True:
        if game_state == "EXPLORE":
            if data.PLAYER["hp"] <= 0:
                print("You have perished in the dungeon...")
                break
            monsters = current_level["monsters"]
            if first_turn:
                # Skip waiting for input and just set movement to zero
                dx, dy = 0, 0
                first_turn = False
            else:
                # Normal behavior: wait for the player to press a key
                dx, dy = engine.move_player()
                new_pos = (data.PLAYER["x"] + dx, data.PLAYER["y"] + dy)
                data.PLAYER = engine.check_tile_event(data.PLAYER, new_pos, current_level)
                engine.move_monsters(monsters)
                active_enemy = check_for_combat(monsters)
                if active_enemy:
                    game_state = "BATTLE"

            if dx == -10 and dy == -10: break

            # Check if we need to load a new map's fog
            if data.PLAYER["current_map"] != last_map_id:
                if last_map_id is not None:
                    visited_levels[last_map_id] = current_level["map"]
                current_level = get_level_data(data.PLAYER["current_map"])
                height = len(current_level["map"])
                width = len(current_level["map"][0]) if height > 0 else 0
                # Reset fog for the new floor
                fog_map = [[" " for _ in range(width)] for _ in range(height)]
                last_map_id = data.PLAYER["current_map"]

            engine.update_visibility(fog_map, current_level["map"], width, height)
            temp_view = [list(row) for row in fog_map]
            engine.place_entities(temp_view, monsters)
            view = engine.place_player_on_map(temp_view)
            viewport = engine.get_viewport(view)
            engine.clear_screen()

            if data.PLAYER["hp"] > 60:
                color = "\033[92m" # Green
            elif data.PLAYER["hp"] > 25:
                color = "\033[93m" # Yellow
            else:
                color = "\033[91m" # Red
            reset = "\033[0m"

            print(f"{color}HP: {data.PLAYER['hp']}{reset} | GP:{data.PLAYER['gp']} | Map:{data.PLAYER["current_map"]} | Position: ({data.PLAYER['x']}, {data.PLAYER['y']})")
            print("~" * 40)

            for line in viewport:
                print(line)
        elif game_state == "BATTLE":
            engine.battle(active_enemy, current_level)
            first_turn = True
            game_state = "EXPLORE"
main()





