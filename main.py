import engine
import data
from engine import clear_screen, death_check


def main():
    engine.clear_screen()

    # 1. Initialization
    game_state = "EXPLORE"
    last_map_id = data.PLAYER["current_map"]
    active_enemy = None

    # Load the initial level
    current_level = engine.get_level_data(last_map_id)

    # Create the local fog map
    fog_map = [[" " for _ in range(current_level["width"])]
               for _ in range(current_level["height"])]

    while True:
        if game_state == "EXPLORE":
            if engine.death_check() == "death":
                # ... existing messages and pauses ...

                # 1. Reset the coordinates and map ID in the data source
                data.PLAYER["current_map"] = 1
                data.PLAYER["x"], data.PLAYER["y"] = 1, 1
                data.PLAYER['hp'] = data.PLAYER['max_hp']
                data.PLAYER['gp'] = int( data.PLAYER['gp'] * 0.8)
                data.PLAYER['sanity'] -= 30

                # 2. Wipe the visited memory so the maps reset to their original state
                data.visited_levels = {}

                # 3. CRITICAL: Use your function to reload the local loop variables!
                current_level = engine.get_level_data(1)
                # If you have other variables like monsters or width/height:
                # monsters = level_info["monsters"]
                # width = level_info["width"]

                # 4. Reset the fog for the new starting position

                fog_map = [[" " for _ in range(current_level["width"])]
               for _ in range(current_level["height"])]

                engine.clear_screen()
                engine.msg("Your time has not yet come warrior,","death","on your feet.")
                engine.pause()
                continue
            elif death_check() == "sanity":
                break

            # 2. Draw the Screen
            engine.draw_exploration_screen(current_level, fog_map)

            # 4. Input
            dx, dy = engine.move_player()
            if dx == -10 and dy == -10: break # Quit
            if dx == 10 and dy == 10:
                game_state = "INVENTORY"
                continue
            if dx == 11 and dy == 11:
                game_state = "STATS"
                continue

            # 5. Turn Logic (Only proceed if player moved)
            if dx == 0 and dy == 0:
                continue

            new_pos = (data.PLAYER["x"] + dx, data.PLAYER["y"] + dy)

            # Check if move is possible
            if engine.is_passable(new_pos[0], new_pos[1], current_level):
                # Move Player & Process Tile (like stairs)
                data.PLAYER = engine.check_tile_event(data.PLAYER, new_pos, current_level)

                # Check if stairs changed the map ID
                if data.PLAYER["current_map"] != last_map_id:
                    last_map_id = data.PLAYER["current_map"]
                    current_level = engine.get_level_data(last_map_id)
                    # Reset fog for new map size
                    fog_map = [[" " for _ in range(current_level["width"])]
                               for _ in range(current_level["height"])]
                    continue  # Re-draw immediately on the new map

                # Move Monsters
                engine.move_monsters(current_level)

                # Check for Combat
                active_enemy = engine.check_for_combat(current_level["monsters"])
                if active_enemy:
                    game_state = "BATTLE"
            else:
                print("The way is blocked!")
                engine.pause()

        elif game_state == "BATTLE":
            engine.battle(active_enemy, current_level)
            game_state = "EXPLORE"
        elif game_state == "INVENTORY":
            engine.show_inventory()
            game_state = "EXPLORE"

        elif game_state == "STATS":
            engine.show_stats_screen()
            game_state = "EXPLORE"


if __name__ == "__main__":
    main()



































'''
import engine
import data



def main():
    engine.clear_screen()
    if not data.DUNGEON[1]["map"]:
        print("The world has not been created yet! (Empty Map)")
        return
    # Load the first level into a "live" variable
    # 1. Setup initial values
    game_state = "EXPLORE"
    last_map_id = data.PLAYER["current_map"]

    # 2. DEFINE current_level HERE
    # This calls your function to get the map, monsters, width, and height
    current_level = engine.get_level_data()

    # 3. Use current_level to set up other things (like fog)
    fog_map = [[" " for _ in range(current_level["width"])]
               for _ in range(current_level["height"])]

    while True:
        if game_state == "EXPLORE":
            if data.PLAYER["hp"] <= 0:
                print("You have perished...")
                break
            # 4. If the player moved to a new map ID, redefine current_level
            if data.PLAYER["current_map"] != last_map_id:
                current_level = engine.get_level_data()
                # ... reset fog, update last_map_id ...
            # Wait for input
            dx, dy = engine.move_player()
            if dx == -10 and dy == -10: break  # Exit condition

            # Process Movement/Logic
            new_pos = (data.PLAYER["x"] + dx, data.PLAYER["y"] + dy)
            data.PLAYER = engine.check_tile_event(data.PLAYER, new_pos, current_level)
            engine.move_monsters(current_level)

            # Check for combat
            active_enemy = engine.check_for_combat()
            if active_enemy:
                data.game_state = "BATTLE"


            if dx == -10 and dy == -10: break

            # 2. Handle Invalid Input (Hero Pondering)
            if dx == 0 and dy == 0:
                # This skips everything below and redraws the screen immediately
                # The monsters never get to move!
                continue

            # 3. Handle Valid Movement
            new_pos = (data.PLAYER["x"] + dx, data.PLAYER["y"] + dy)

            # Check if the tile is passable BEFORE processing the turn
            if engine.is_passable(new_pos[0], new_pos[1], current_level):
                data.PLAYER = engine.check_tile_event(data.PLAYER, new_pos, current_level)
                # Monsters only move if the player successfully moved or tried to!
                engine.move_monsters(current_level)
            else:
                print("The way is blocked!")
                engine.pause()
                # Since we didn't call move_monsters here, they don't get a turn!

                # Check if we need to load a new map's fog
            if data.PLAYER["current_map"] != data.last_map_id:
                if data.last_map_id is not None:
                    data.visited_levels[data.last_map_id] = current_level["map"]
                current_level = engine.get_level_data(data.PLAYER["current_map"])
                height = len(current_level["map"])
                width = len(current_level["map"][0]) if height > 0 else 0
                # Reset fog for the new floor
                data.fog_map = [[" " for _ in range(width)] for _ in range(height)]
                #last_map_id = data.PLAYER["current_map"]

            engine.update_visibility(fog_map)
            temp_view = [list(row) for row in data.fog_map]
            engine.place_entities(temp_view, data.monsters)
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
        elif data.game_state == "BATTLE":
            engine.battle(data.active_enemy, current_level)
            data.game_state = "EXPLORE"
main()
'''




