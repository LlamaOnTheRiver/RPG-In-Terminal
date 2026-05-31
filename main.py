import engine
import data
from engine import clear_screen, death_check


def main():
    engine.clear_screen()

    # 1. Initialization
    game_state = "EXPLORE"
    last_map_id = data.GAME_STATE['current_map']
    active_enemy = None

    # Load the initial level
    current_level = engine.get_level_data(last_map_id)

    # Create the local fog map
    #data.PLAYER['name'] = input("Please enter your name: ")
    data.GAME_STATE['fog_map'] = [[" " for _ in range(current_level["width"])]
               for _ in range(current_level["height"])]

    while True:
        if game_state == "EXPLORE":

            # 2. Draw the Screen
            fog_map = data.GAME_STATE['fog_map']
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

            new_pos = (data.GAME_STATE["x"] + dx, data.GAME_STATE["y"] + dy)
            # Check if move is possible
            if engine.is_passable(new_pos):
                # Move Player & Process Tile (like stairs)
                game_state = engine.check_tile_event(new_pos, current_level)
                if game_state != "EXPLORE":
                    continue

                # Check if stairs changed the map ID
                if data.GAME_STATE["current_map"] != last_map_id:
                    last_map_id = data.GAME_STATE["current_map"]
                    print(last_map_id)
                    engine.pause()
                    current_level = engine.get_level_data(last_map_id)
                    # Reset fog for new map size
                    data.GAME_STATE['fog_map'] = [[" " for _ in range(current_level["width"])]
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

        elif game_state == "GAME OVER":
            if engine.death_check() == "death":
                # ... existing messages and pauses ...

                # 1. Reset the coordinates and map ID in the data source
                data.GAME_STATE["current_map"] = 1
                data.GAME_STATE["x"], data.GAME_STATE["y"] = 1, 1
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

                data.GAME_STATE['fog_map'] = [[" " for _ in range(current_level["width"])]
               for _ in range(current_level["height"])]

                engine.clear_screen()
                engine.msg("Your time has not yet come warrior,","on your feet.", style='death')
                game_state = "EXPLORE"
                continue
            elif death_check() == "sanity":
                break
        elif game_state == "BATTLE":
            #game_state = "EXPLORE"
            #continue
            game_state = engine.battle(active_enemy, current_level)

        elif game_state == "INVENTORY":
            game_state = engine.show_inventory()

        elif game_state == "STATS":
            game_state = engine.show_stats_screen()

        elif game_state == "SHOP":
            game_state = engine.show_shop_screen(data.GAME_STATE['current_map'])


if __name__ == "__main__":
    main()