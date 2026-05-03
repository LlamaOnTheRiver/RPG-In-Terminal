import os

def place_player_on_map(game_map, player):
    # Use the dictionary values directly
    px = player["x"]
    py = player["y"]
    marker = player["marker"]

    if game_map and 0 <= px < len(game_map[0]) and 0 <= py < len(game_map): 
        # Update the map at the correct row (py) and column (px)

        game_map[py][px] = marker
    return ["".join(row) for row in game_map]
    

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

def check_tile_event(player, new_pos, game_map):
    nx, ny = new_pos
    height = len(game_map)
    width = len(game_map[0])

    # 1. Boundary Check
    if not (0 <= nx < width and 0 <= ny < height):
        print("The edge of the world blocks you!")
        input("...")
        return player # Return player unchanged

    # 2. Tile Logic
    tile = game_map[ny][nx]
    
    # Define what each tile does
    tile_effects = {
        "T": {"msg": "TRAP! -10 HP", "hp": -10, "consume": "."},
        "G": {"msg": "GOLD! +5 GP", "gp": 5, "consume": "."},
        "H": {"msg": "HEALED! HP to 100", "hp": 100, "consume": "."},
        "W": {"msg": "A solid wall.", "block": True}
    }

    if tile in tile_effects:
        effect = tile_effects[tile]
        
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
            game_map[ny][nx] = effect["consume"]

    # Update position and return

        if "msg" in effect:
            print(effect["msg"])
            input("...")
    player["x"], player["y"] = nx, ny
    return player

def update_visibility(fog_map, player, game_map, width, height):
    # Reveal a 1-tile radius
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            rx, ry = player["x"] + dx, player["y"] + dy
            if 0 <= rx < width and 0 <= ry < height:
                fog_map[ry][rx] = game_map[ry][rx]
    return fog_map

def get_viewport(view, player, radius=2):
    height = len(view)
    width = len(view[0]) if height > 0 else 0
    size = (radius * 2) + 1
    
    # Calculate the bounds
    start_y = max(0, min(player["y"] - radius, height - size))
    start_x = max(0, min(player["x"] - radius, width - size))
    
    viewport = []
    for y in range(start_y, start_y + size):
        if y < height:
            row_string = view[y]
            viewport.append(row_string[start_x : start_x + size])
    return viewport