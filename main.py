import engine
import data
    
def main():
    engine.clear_screen()
    if not data.DUNGEON[1]["map"]:
        print("The world has not been created yet! (Empty Map)")
        return
    height = len(data.DUNGEON[1]["map"])
    width = len(data.DUNGEON[1]["map"][0])
    last_map_id = 1
    fog_map = [[" " for _ in range(width)] for _ in range(height)]
    print(
        f"{"\033[92m"}HP: {data.PLAYER['hp']}{"\033[0m"} | GP:{data.PLAYER['gp']} | Map:{data.PLAYER["current_map"]} Position: ({data.PLAYER['x']}, {data.PLAYER['y']})")
    print("~" * 30)
    print("...\n.P.\n...")


    while True:
        if data.PLAYER["hp"] <= 0:
            print("You have perished in the dungeon...")
            break
        dx, dy = engine.move_player()
        if dx == -10 and dy == -10: break

        new_pos = (data.PLAYER["x"] + dx, data.PLAYER["y"] + dy)
        data.PLAYER = engine.check_tile_event(data.PLAYER, new_pos)

        # Check if we need to load a new map's fog
        if data.PLAYER["current_map"] != last_map_id:
            current_id = data.PLAYER["current_map"]
            current_map_data = data.DUNGEON[current_id]["map"]
            height = len(current_map_data)
            width = len(current_map_data[0])
            # Reset fog for the new floor
            fog_map = [[" " for _ in range(width)] for _ in range(height)]
            last_map_id = current_id



        engine.update_visibility(fog_map, width, height)
        temp_view = [row[:] for row in fog_map]
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

        print(f"{color}HP: {data.PLAYER['hp']}{reset} | GP:{data.PLAYER['gp']} | Map:{data.PLAYER["current_map"]} Position: ({data.PLAYER['x']}, {data.PLAYER['y']})")
        print("~" * 30)
        
        for line in viewport:
            print(line)

    
main()





