import os
import data



def place_player_on_map(temp_view):
        px = data.PLAYER["x"]
        py = data.PLAYER["y"]
        colored_marker = data.PLAYER["marker"]

        if 0 <= py < len(temp_view) and 0 <= px < len(temp_view[0]):
            temp_view[py][px] = colored_marker

        return temp_view
    

def move_player():
    move = input("Move (wasd) | q (quit): ").strip().lower()
    if move == "w": return 0, -1
    if move == "s": return 0, 1
    if move == "a": return -1, 0
    if move == "d": return 1, 0
    if move == "q": return -10, -10
    print("Hero ponders about life")
    input("Press Enter to continue")
    return 0, 0

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def check_tile_event(player, new_pos):
    nx, ny = new_pos
    height = len(data.DUNGEON[player["current_map"]]["map"])
    width = len(data.DUNGEON[player["current_map"]]["map"][0])

    # 1. Boundary Check
    if not (0 <= nx < width and 0 <= ny < height):
        print("The edge of the world blocks you!")
        input("...")
        return player # Return player unchanged

    # 2. Tile Logic
    tile = data.DUNGEON[player["current_map"]]["map"][ny][nx]
    
    if tile in data.TILE_EFFECTS:
        effect = data.TILE_EFFECTS[tile]
        
        # 1. Handle Blocking immediately
        if effect.get("block"):
            print(effect["msg"])
            input("...")
            return player 
        player["hp"] += effect.get("hp", 0)
        player["gp"] += effect.get("gp", 0)
        
        # Clamp HP
        player["hp"] = min(player["max_hp"], player["hp"])

        # 4. Handle Consuming
        if "consume" in effect:
            data.DUNGEON[player["current_map"]]["map"][ny][nx] = effect["consume"]

        if "teleport" in effect:
            cords = (ny, nx)
            # Grab all the secret data from the CURRENT map before changing anything
            stair_data = data.DUNGEON[player["current_map"]]["stairs"][cords]

            # Now update the player using that saved data
            data.PLAYER["current_map"] = stair_data["target_map"]
            data.PLAYER["x"] = stair_data["target_x"]
            data.PLAYER["y"] = stair_data["target_y"]
            if "msg" in effect:
                print(effect["msg"])
                input("...")
            return data.PLAYER



    # Update position and return

        if "msg" in effect:
            print(effect["msg"])
            input("...")
    player["x"], player["y"] = nx, ny
    return player

def update_visibility(fog_map, width, height):
    # Reveal a 1-tile radius
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            rx, ry = data.PLAYER["x"] + dx, data.PLAYER["y"] + dy
            if 0 <= rx < width and 0 <= ry < height:
                fog_map[ry][rx] = data.DUNGEON[data.PLAYER["current_map"]]["map"][ry][rx]
    return fog_map


def get_viewport(view, radius=2):
    # 'view' should be a list of lists (the grid) for this to work best
    height = len(view)
    width = len(view[0]) if height > 0 else 0
    size = (radius * 2) + 1

    start_y = max(0, min(data.PLAYER["y"] - radius, height - size))
    start_x = max(0, min(data.PLAYER["x"] - radius, width - size))

    viewport = []
    for y in range(start_y, start_y + size):
        if y < len(view):
            # Slice the list, then join
            row_list = view[y]
            sliced_row = row_list[start_x: start_x + size]
            viewport.append("".join(sliced_row))
    return viewport