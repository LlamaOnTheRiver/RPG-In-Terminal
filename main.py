import engine
import data


def main():
    # 1. Initialization
    game_state = "EXPLORE"
    # 1. Get the map data
    m_grid = data.DUNGEON[1]['map']

    # 2. Identify the current map
    last_map_id = 1
    data.GAME_STATE['current_map'] = last_map_id

    # 3. CRITICAL: Store it in visited_levels so other functions can find it!
    data.visited_levels[last_map_id] = m_grid

    # 4. Now calculate dimensions and create fog
    w = len(m_grid[0]) if len(m_grid) > 0 else 0
    h = len(m_grid)
    data.GAME_STATE['fog_map'] = [[" " for _ in range(w)] for _ in range(h)]

    engine.clear_screen()
    '''
    engine.msg("...", style="event", draw=True)
    engine.msg("Neil", style="event", draw=True)
    engine.msg("...", style="event", draw=True)
    engine.msg("Why am I?...", style="event", draw=True)
    engine.msg("Why did you?...", style="event", draw=True)
    engine.msg("You wake up in a haze and look at your surroundings.",
               "Filth and dust line the walls of this ancient place.",
               "You hold your chest as you brace your knee and stand yourself up.",
               "How long has it been since the last time you've seen the moon?", draw=True)
    engine.msg("I'm heading for you...", "Brother...", style="event", draw=True)
    print("What is your name?")
    data.PLAYER['name'] = input(">...")
    '''

    while True:
        if game_state == "EXPLORE":
            if engine.death_check() == "death" or engine.death_check() == "sanity":
                game_state = "GAME OVER"
                continue

            # 2. Draw the Screen
            engine.draw_exploration_screen()

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
                game_state = engine.check_tile_event(new_pos)
                if game_state != "EXPLORE":
                    continue

                # Check if stairs changed the map ID
                if data.GAME_STATE["current_map"] != last_map_id:
                    last_map_id = data.GAME_STATE["current_map"]
                    engine.pause()
                    current_level = engine.get_level_data(last_map_id)
                    # Reset fog for new map size
                    data.GAME_STATE['fog_map'] = [[" " for _ in range(current_level["width"])]
                               for _ in range(current_level["height"])]
                    continue  # Re-draw immediately on the new map

                # Move Monsters
                engine.move_monsters()

                # Check for Combat
                active_enemy = engine.check_for_combat()
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
            elif engine.death_check() == "sanity":
                break
        elif game_state == "BATTLE":
            game_state = "EXPLORE"
            continue
            #game_state = engine.battle(active_enemy)

        elif game_state == "INVENTORY":
            game_state = engine.show_inventory()

        elif game_state == "STATS":
            game_state = engine.show_stats_screen()

        elif game_state == "SHOP":
            game_state = engine.show_shop_screen(data.GAME_STATE['current_map'])

        elif game_state == "EVENT":
            game_state = engine.run_dialogue()



if __name__ == "__main__":
    main()