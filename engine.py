import os
import data
import random



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

def check_tile_event(player, new_pos, current_level):
    nx, ny = new_pos
    current_map = current_level["map"]
    height = len(data.DUNGEON[player["current_map"]]["map"])
    width = len(data.DUNGEON[player["current_map"]]["map"][0])

    tile = current_map[ny][nx]

    # 1. Boundary Check
    if not (0 <= nx < width and 0 <= ny < height):
        print("The edge of the world blocks you!")
        input("...")
        return player # Return player unchanged


    
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
            current_map[ny][nx] = effect["consume"]

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

def update_visibility(fog_map, current_map, width, height):
    # Reveal a 1-tile radius
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            rx, ry = data.PLAYER["x"] + dx, data.PLAYER["y"] + dy
            if 0 <= rx < width and 0 <= ry < height:
                fog_map[ry][rx] = current_map[ry][rx]
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


import random


def move_monsters(monsters, view_radius=5):
    # NESW mapping
    directions = {1: (0, -1), 2: (0, 1), 3: (1, 0), 4: (-1, 0)}

    for m in monsters:
        dist_x = abs(m["x"] - data.PLAYER["x"])
        dist_y = abs(m["y"] - data.PLAYER["y"])

        nx, ny = m["x"], m["y"]

        # 1. HUNTING LOGIC
        if dist_x <= view_radius and dist_y <= view_radius:
            if m["x"] < data.PLAYER["x"]:
                nx += 1
            elif m["x"] > data.PLAYER["x"]:
                nx -= 1
            elif m["y"] < data.PLAYER["y"]:
                ny += 1
            elif m["y"] > data.PLAYER["y"]:
                ny -= 1

        # 2. WANDERING LOGIC (If not hunting)
        else:
            num = random.randint(1, 4)
            dx, dy = directions[num]
            nx += dx
            ny += dy

        # 3. VALIDATION (The "is_passable" check)
        # Use the function we discussed to make sure they don't hit walls!
        if is_passable(nx, ny, data.PLAYER["current_map"]):
            m["x"], m["y"] = nx, ny

def place_entities(temp_view, monsters):
    for m in monsters:
        mx, my = m["x"], m["y"]
        if 0 <= my < len(temp_view) and 0 <= mx < len(temp_view[0]):
            # Only draw the monster if the tile isn't "Fog" (empty space)
            if temp_view[my][mx] != " ":
                temp_view[my][mx] = m["marker"]


import random


def run_battle(player, enemy):
    print(f"--- BATTLE: {player['marker']} vs {enemy['name']} ---")

    while player["hp"] > 0 and enemy["hp"] > 0:
        print(f"\nYour HP: {player['hp']} | {enemy['name']} HP: {enemy['hp']}")
        action = input("Do you (A)ttack or (F)lee? ").lower()

        if action == "a":
            # Player attacks
            dmg = random.randint(5, 15)
            enemy["hp"] -= dmg
            print(f"You hit the {enemy['name']} for {dmg} damage!")
        elif action == "f":
            print("You escaped back to the dungeon!")
            return "fled"
        else:
            print("You stumble, paralyzed by indecision!")

        # Monster attacks back if it's still alive
        if enemy["hp"] > 0:
            m_dmg = enemy["dmg"]
            player["hp"] -= m_dmg
            print(f"The {enemy['name']} hits you for {m_dmg} damage!")

    if player["hp"] <= 0:
        return "lost"
    return "won"

def check_for_combat(monsters):
    for monster in monsters:
        if monster["x"] == data.PLAYER["x"] and monster["y"] == data.PLAYER["y"]:
            return monster # Return the monster we bumped into
    return None


def draw_battle_screen(enemy):
    clear_screen()

    # 1. Top Right: Monster Stats
    # 'width' should match your typical terminal width (e.g., 40 characters)
    width = 40
    monster_stats = f"{enemy['name']} HP: {enemy['hp']} "
    print(monster_stats.rjust(width))

    # 2. Middle: Visuals or spacing
    # Print several empty lines to push the player stats to the bottom
    for _ in range(10):
        print()

    # 3. Bottom Left: Hero Stats
    hero_stats = f"{data.PLAYER['marker']} HP: {data.PLAYER['hp']}"
    print(hero_stats)
    print("-" * width)


def is_passable(nx, ny, current_map):
    # 1. BOUNDARY CHECK
    # Get the height (number of rows) and width (length of first row)
    height = len(data.DUNGEON[data.PLAYER["current_map"]]["map"])
    width = len(data.DUNGEON[data.PLAYER["current_map"]]["map"][0])

    # If the coordinate is less than 0 or greater than the max index, it's out of bounds
    if nx < 0 or nx >= width or ny < 0 or ny >= height:
        return False

    # 2. WALL CHECK
    # Now that we know it's in bounds, we can safely look at the character
    tile = data.DUNGEON[data.PLAYER["current_map"]]["map"][ny][nx]

    # If the tile is a wall, return False
    if tile == "W" or tile == "#":
        return False

    # If it passed both checks, the path is clear!
    return True

