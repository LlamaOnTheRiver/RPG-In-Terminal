import os
import data
import random
import copy
import items


def msg(text, style="standard", text1="", text2="", text3=""):
    # Define different border characters for different event types
    styles = {
        "standard": ("-", "|"),
        "combat": ("*", "!"),
        "loot": ("=", "$"),
        "error": ("!", "X")
    }

    border_char, side_char = styles.get(style, ("-", "|"))

    # Calculate the width based on the text length
    width = max(len(text), len(text1), len(text2), len(text3))


    # Print the "pretty" box
    print(border_char * (width + 4))
    print(f"{side_char} {text.ljust(width)} {side_char}")
    if text1: print(f"{side_char} {text1.ljust(width)} {side_char}")
    if text2: print(f"{side_char} {text2.ljust(width)} {side_char}")
    if text3: print(f"{side_char} {text3.ljust(width)} {side_char}")
    print(border_char * (width + 4))

def get_level_data(level_id): # I renamed last_map_id to level_id for clarity
    # 1. Use the level_id we were handed!
    if level_id not in data.visited_levels:
        data.visited_levels[level_id] = copy.deepcopy(data.DUNGEON[level_id]["map"])

    # 2. Get the map and calculate dimensions
    current_map = data.visited_levels[level_id]
    h = len(current_map)
    w = len(current_map[0]) if h > 0 else 0
    inv = data.PLAYER["inventory"]

    # 3. Get monsters for THIS specific level_id
    fresh_monsters = copy.deepcopy(data.DUNGEON[level_id]["monsters"])

    return {
        "map": current_map,
        "monsters": fresh_monsters,
        "width": w,
        "height": h,
        "inv": inv
    }

def place_player_on_map(temp_view):
        px = data.PLAYER["x"]
        py = data.PLAYER["y"]
        colored_marker = data.PLAYER["marker"]

        if 0 <= py < len(temp_view) and 0 <= px < len(temp_view[0]):
            temp_view[py][px] = colored_marker

        return temp_view


def move_player():
    # Remove the while loop and the drawing from here!
    move = input("Move (wasd) | q (quit) | i(Inventory):").strip().lower()

    if move == "w": return 0, -1
    if move == "s": return 0, 1
    if move == "a": return -1, 0
    if move == "d": return 1, 0
    if move == "q": return -10, -10
    if move == "i": return 10, 10

    # If they hit a random key
    msg("Hero ponders about life")
    pause()
    return 0, 0


def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def pause():
    input("\nPress Enter to continue...")

def update_visibility(fog_map, current_level, radius=2):
    w = current_level['width']
    h = current_level['height']
    grid = current_level['map']
    px, py = data.PLAYER["x"], data.PLAYER["y"]

    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            rx, ry = px + dx, py + dy
            if 0 <= rx < w and 0 <= ry < h:
                fog_map[ry][rx] = grid[ry][rx]
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

def move_monsters(current_level, view_radius=3):
    monsters = current_level["monsters"]
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
        if is_passable(nx, ny, current_level):
            m["x"], m["y"] = nx, ny

def place_entities(temp_view, monsters):
    for m in monsters:
        mx, my = m["x"], m["y"]
        if 0 <= my < len(temp_view) and 0 <= mx < len(temp_view[0]):
            # Only draw the monster if the tile isn't "Fog" (empty space)
            if temp_view[my][mx] != " ":
                temp_view[my][mx] = m["marker"]

def run_battle(player, enemy):
    msg(f"--- BATTLE: {player['marker']} vs {enemy['name']} ---", "battle")
    while player["hp"] > 0 and enemy["hp"] > 0:
        print(f"\nYour HP: {player['hp']} | {enemy['name']} HP: {enemy['hp']}")
        action = input("Do you (A)ttack or (F)lee? ").lower()

        if action == "a":
            # Player attacks
            dmg = random.randint(5, 15)
            enemy["hp"] -= dmg
            msg(f"You hit the {enemy['name']} for {dmg} damage!", "battle")
        elif action == "f":
            msg("You escaped back to the dungeon!", "battle")
            return "fled"
        else:
            msg("You stumble, paralyzed by indecision!", "battle")

        # Monster attacks back if it's still alive
        if enemy["hp"] > 0:
            m_dmg = enemy["dmg"]
            player["hp"] -= m_dmg
            msg(f"The {enemy['name']} hits you for {m_dmg} damage!", "battle")

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
    hero_stats = f"HP: {data.PLAYER['hp']}"
    print(hero_stats)
    print("-" * width)


def is_passable(nx, ny, current_level):
    # Access everything from the one dictionary
    w = current_level["width"]
    h = current_level["height"]
    m_grid = current_level["map"]

    # 1. BOUNDARY CHECK
    if nx < 0 or nx >= w or ny < 0 or ny >= h:
        return False

    if m_grid[ny][nx] in ["W", "#"]:
        return False

    return True

def battle(active_enemy, current_level):
    msg(f"A wild {active_enemy['name']} appeared!", "battle")
    pause()
    while True:
        clear_screen()
        draw_battle_screen(active_enemy)
        monster_hp = active_enemy["hp"]
        monster_atk = active_enemy["dmg"]
        stats = [monster_hp, monster_atk]
        msg(f"What will you do?", "battle")
        action = input("(A)ttack or (R)un? ").lower()
        def atk():
            draw_battle_screen(active_enemy)
            msg(f"The mighty {active_enemy['name']} takes a swipe at you!", "battle")
            pause()
            draw_battle_screen(active_enemy)
            msg(f"{active_enemy['name']} does {active_enemy['dmg']} damage!", "battle")
            pause()
            data.PLAYER['hp'] -= active_enemy['dmg']
            if data.PLAYER['hp'] <= 0:
                data.PLAYER['hp'] = 0
                return


        if action == "a":
            # Handle combat...
            active_enemy['hp'] -= 10
            if active_enemy['hp'] <= 0:
                active_enemy['hp'] = 0
                draw_battle_screen(active_enemy)
                xp_screen(stats)
                pause()
                # Remove the monster from the live list
                current_level['monsters'].remove(active_enemy)
                return

            else:
                atk()
        elif action == "r":
            num = random.randint(1, 3)
            if num == 3:
                msg(f"You managed to get away from the {active_enemy["name"]}", "battle")
                pause()
                if active_enemy in current_level['monsters']:
                    current_level['monsters'].remove(active_enemy)
                return
            else:
                msg(f"The {active_enemy["name"]} wont let you escape", "battle")
                pause()
                atk()
def sanity_bar():
    num = data.PLAYER['sanity'] // 10
    san = ((10 - num) * "-") + (num * "#")
    return san

def draw_stats():
    color = "\033[92m"  # Green
    if data.PLAYER["hp"] <= 25:
        color = "\033[91m"  # Red
    elif data.PLAYER["hp"] <= 60:
        color = "\033[93m"  # Yellow
    reset = "\033[0m"

    color_san = "\033[92m"  # Green
    if data.PLAYER["sanity"] <= 40:
        color_san = "\033[91m"  # Red
    elif data.PLAYER["sanity"] <= 70:
        color_san = "\033[93m"  # Yellow


    print(f"{color}HP: {data.PLAYER['hp']}{reset} | {color_san}SN:{sanity_bar()}{reset} | GP:{data.PLAYER['gp']} | Map:{data.PLAYER['current_map']}")
    print("~" * 40)

def draw_exploration_screen(current_level, fog_map):
    update_visibility(fog_map, current_level)
    m = current_level['monsters']
    # 2. Create a temporary copy of the fog to draw entities on
    temp_view = [list(row) for row in fog_map]

    # 3. Layer the monsters and player on top
    place_entities(temp_view, m)
    view = place_player_on_map(temp_view)

    # 4. Get the final cropped view
    viewport = get_viewport(view)

    # ... then clear_screen() and print the viewport ...

    # 2. Clear and Print
    clear_screen()

    # Health coloring logic
    draw_stats()

    for line in viewport:
        print(line)

def load_level(level_id):
    # .deepcopy() creates a brand new version of everything,
    # including the nested lists, so the original stays safe!
    return copy.deepcopy(data.DUNGEON[level_id])

def check_tile_event(player, new_pos, current_level):
    nx, ny = new_pos

    # 1. Use the data from current_level
    current_map = current_level["map"]
    width = current_level["width"]
    height = current_level["height"]

    # 2. Boundary Check (Crucial to prevent "Index out of range" crashes)
    if not (0 <= nx < width and 0 <= ny < height):
        print("The edge of the world blocks you!")
        pause()
        return player

        # 3. Get the tile now that we know we are in bounds
    tile = current_map[ny][nx]
    if not (0 <= nx < width and 0 <= ny < height):
        print("The edge of the world blocks you!")
        pause()
        return player  # Return player unchanged

    if tile in data.TILE_EFFECTS:
        effect = data.TILE_EFFECTS[tile]

        # 1. Handle Blocking immediately
        if effect.get("block"):
            print(effect["msg"])
            pause()
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
                pause()
            return data.PLAYER

        # Update position and return

        if "msg" in effect:
            print(effect["msg"])
            pause()
    player["x"], player["y"] = nx, ny
    return player


def use_item(item_name):
    # Check the registry in the items file
    if item_name in items.ITEM_REGISTRY:
        effect_function = items.ITEM_REGISTRY[item_name]

        # Execute the function
        effect_function()

        # Handle the inventory subtraction
        data.PLAYER["inventory"][item_name] -= 1
        if data.PLAYER["inventory"][item_name] <= 0:
            del data.PLAYER["inventory"][item_name]
    else:
        print(f"The {item_name} is a curious object, but you can't use it now.")

    pause()


def show_inventory():
    page = 0
    items_per_page = 6

    while True:
        clear_screen()
        draw_stats()
        print("=== INVENTORY ===")

        # 1. Get the list of names
        item_names = list(sorted(data.PLAYER["inventory"].keys()))
        total_items = len(item_names)

        if total_items == 0:
            print("Your pack is empty.")
            # Print 5 empty lines because we used 1 for the empty message
            for _ in range(items_per_page - 1):
                print()
        else:
            start_idx = page * items_per_page
            end_idx = start_idx + items_per_page
            page_items = item_names[start_idx:end_idx]

            # 1. Print the items we actually have
            for i, name in enumerate(page_items, start_idx + 1):
                count = data.PLAYER["inventory"][name]
                print(f"{i}. {name[:20]:<20} x{count}")

            # 2. PADDING: Print blank lines for the remaining "slots"
            # If we only printed 2 items, this prints 4 empty lines
            for _ in range(items_per_page - len(page_items)):
                print()

            total_pages = (total_items - 1) // items_per_page + 1
            print(f"\n--- Page {page + 1} of {total_pages} ---")

        print("=" * 18)
        print("(A) Prev | (D) Next | (B)ack")

        choice = input("> ").lower()

        if choice == 'b':
            break
        elif choice == 'a' and page > 0:
            page -= 1
        elif choice == 'd' and (page + 1) * items_per_page < total_items:
            page += 1
        elif choice.isdigit():
            selection = int(choice)
            if 1 <= selection <= total_items:
                chosen_item = item_names[selection - 1]
                use_item(chosen_item)
                # If the item was used up and removed, we might need to adjust the page
                # Refresh names to check if we still have items
                item_names = list(data.PLAYER["inventory"].keys())
                if len(item_names) <= page * items_per_page and page > 0:
                    page -= 1
def xp_screen(stats):
    # Calculate base XP based on monster toughness
    print(stats[0], stats[1])
    xp = int(0.25 * stats[0] * stats[1])

    # GP is a randomized portion of the "effort" (XP) spent
    multipliers = [0.5, 0.75, 1.0, 1.25]
    gp = int(random.choice(multipliers) * xp)
    loot = get_random_loot()
    msg(f"You have gained. {xp} XP","loot" ,f"and {gp} GP was added to your stash.", f"You also found a {loot}!")
    data.PLAYER["gp"] += gp
    data.PLAYER["xp"] += xp
    if loot in data.PLAYER["inventory"]:
        data.PLAYER["inventory"][loot] += 1
    else:
        data.PLAYER["inventory"][loot] = 1




def get_random_loot():
    # random.choices returns a list based on the weights provided
    # population: the list of categories to choose from
    # weights: the list of chances corresponding to those categories
    rarities = list(data.RARITY_WEIGHTS.keys())
    weights = list(data.RARITY_WEIGHTS.values())
    selected_rarity = random.choices(rarities, weights=weights, k=1)[0]

    # Pick a random item from the chosen category
    items_to_pick_from = data.LOOT_DATA[selected_rarity]
    return random.choice(items_to_pick_from)

