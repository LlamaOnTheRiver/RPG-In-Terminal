import engine
import data

def main():
    # 1. Initialization
    game_state = "EXPLORE"
    # 1. Get the map data
    m_grid = data.DUNGEON[2]['map']

    # 2. Identify the current map
    last_map_id = 2
    data.GAME_STATE['current_map'] = last_map_id

    # 3. CRITICAL: Store it in visited_levels so other functions can find it!
    data.visited_levels[last_map_id] = m_grid

    # 4. Now calculate dimensions and create fog
    w = len(m_grid[0]) if len(m_grid) > 0 else 0
    h = len(m_grid)
    data.GAME_STATE['fog_map'] = [[" " for _ in range(w)] for _ in range(h)]
    active_enemy = None

    engine.clear_screen()
    '''
    engine.msg("...", style="event", draw_fn=engine.redraw)
    engine.msg("Neil", style="event", draw_fn=engine.redraw)
    engine.msg("...", style="event", draw_fn=engine.redraw)
    engine.msg("Why am I?...", style="event", draw_fn=engine.redraw)
    engine.msg("Why did you?...", style="event", draw_fn=engine.redraw)
    engine.msg("You wake up in a haze and look at your surroundings.",
               "Filth and dust line the walls of this ancient place.",
               "You hold your chest as you brace your knee and stand yourself up.",
               "How long has it been since the last time you've seen the moon?", draw_fn=engine.redraw)
    engine.msg("I'm heading for you...", "Brother...", style="event", draw_fn=engine.redraw)
    print("What is your name?")
    data.PLAYER['name'] = input(">...")
    '''
    engine.redraw()


    while True:
        if game_state == "EXPLORE":
            if engine.death_check() == "death" or engine.death_check() == "sanity":
                game_state = "GAME OVER"
                continue

            # 1. Get movement intent
            result = engine.move_player()
            if isinstance(result, tuple):
                dx, dy = result
                new_pos = (data.GAME_STATE['x'] + dx, data.GAME_STATE['y'] + dy)

                # 2. ONLY check the event for the NEW position
                game_state = engine.check_tile_event(new_pos)

                # Check if stairs changed the map ID
                if data.GAME_STATE["current_map"] != last_map_id:
                    last_map_id = data.GAME_STATE["current_map"]
                    engine.pause()
                    current_level = engine.get_level_data(last_map_id)
                    # Reset fog for new map size
                    data.GAME_STATE['fog_map'] = [[" " for _ in range(current_level["width"])]
                                                  for _ in range(current_level["height"])]
                    continue  # Re-draw immediately on the new map

                # 3. THEN update what the player sees
                engine.update_visibility()

            if game_state != "EXPLORE":
                continue
            engine.redraw()

            # Move Monsters
            engine.move_monsters()

            # Check for Combat
            active_enemy = engine.check_for_combat()
            if active_enemy:
                game_state = "BATTLE"

        elif game_state == "GAME OVER":
            if engine.death_check() == "death":
                # 1. Reset the coordinates and map ID in the data source
                data.GAME_STATE["current_map"] = 1
                data.GAME_STATE["x"], data.GAME_STATE["y"] = 1, 1
                data.PLAYER['hp'] = data.PLAYER['max_hp']
                data.PLAYER['gp'] = int( data.PLAYER['gp'] * 0.8)
                data.PLAYER['sanity'] -= 30
                data.visited_levels = {}
                current_level = engine.get_level_data(1)
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
            result = engine.battle(
                active_enemy["name"],
                map_monster=active_enemy,
                remove_from_level=True
            )
            if result == "win":
                game_state = "EXPLORE"
            elif result == "escape":
                game_state = "EXPLORE"
            else:
                game_state = "GAME OVER"

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