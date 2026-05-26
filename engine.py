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
        "error": ("!", "X"),
        "death": ("X", "X"),
        "skill": ("%", "&")
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
    if move == "f": return 11, 11

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

def check_for_combat(monsters):
    for monster in monsters:
        if monster["x"] == data.PLAYER["x"] and monster["y"] == data.PLAYER["y"]:
            return monster # Return the monster we bumped into
    return None


def draw_battle_screen(enemy, temp_hp):
    clear_screen()

    # 1. Top Right: Monster Stats
    # 'width' should match your typical terminal width (e.g., 40 characters)
    width = 40
    monster_stats = f"{enemy['name']} HP: {temp_hp} "
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
    # Update player stats based on current level/points
    stats = get_derived_stats()
    # [atk, accuracy, crit_chance, regen, max_hp, armor]

    # Now use the derived values


    enemy = data.MONSTERS[active_enemy["name"]]
    # Extract all lines after the first one
    # Slicing is safe: if the list is short, it just returns what it can (even an empty list)
    extra_lines = enemy["intro"][1:4]

    clear_screen()

    # Unpack the list into the optional parameters
    msg(enemy["intro"][0], "battle", *extra_lines)
    pause()
    temp_hp = enemy['hp']
    while True:
        p_hit = random.randint(1, 100) <= stats[1]
        p_atk = stats[0]
        p_crit = random.randint(1,100) <= stats[2]
        data.PLAYER['hp'] += stats[3]
        if data.PLAYER['hp'] > data.PLAYER['max_hp']:
            data.PLAYER['hp'] = data.PLAYER['max_hp']
        p_armor = stats[5]
        clear_screen()
        draw_battle_screen(enemy, temp_hp)
        msg(f"What will you do?", "battle")
        action = input("(A)ttack or (R)un? ").lower()
        def atk():
            draw_battle_screen(enemy, temp_hp)
            # Extract all lines after the first one
            # Slicing is safe: if the list is short, it just returns what it can (even an empty list)
            cry_lines = enemy["cry"][1:4]

            # Unpack the list into the optional parameters
            msg(enemy["cry"][0], "battle", *cry_lines)
            pause()
            draw_battle_screen(enemy, temp_hp)
            msg(f"{enemy['name']} does {enemy['dmg']} damage!", "battle")
            pause()
            data.PLAYER['hp'] -= enemy['dmg'] - p_armor
            if data.PLAYER['hp'] <= 0:
                data.PLAYER['hp'] = 0
                return True
            return False


        if action == "a":
            # Handle combat...
            if p_hit:
                if p_crit:
                    clear_screen()
                    draw_battle_screen(enemy, temp_hp)
                    msg(f"{data.PLAYER['name']} landed a crit and did {p_atk * 2} damage!", "battle")
                    pause()
                    temp_hp -= p_atk
                temp_hp -= p_atk
                if temp_hp <= 0:
                    temp_hp = 0
                    draw_battle_screen(enemy, temp_hp)
                    xp_screen(enemy)
                    pause()
                    # Remove the monster from the live list
                    current_level['monsters'].remove(active_enemy)
                    return
                else:
                    if atk():
                        return
            else:
                clear_screen()
                draw_battle_screen(enemy, temp_hp)
                msg(f"{data.PLAYER['name']} missed their attack!")
                pause()
                if atk():
                    return
        elif action == "r":
            num = random.randint(1, 3)
            if num == 3:
                msg(f"You managed to get away from the {enemy["name"]}", "battle")
                pause()
                if active_enemy in current_level['monsters']:
                    current_level['monsters'].remove(active_enemy)
                return
            else:
                msg(f"The {enemy["name"]} wont let you escape", "battle")
                pause()
                if atk():
                    return

def sanity_bar():
    num = data.PLAYER['sanity'] // 10
    san = ((10 - num) * "-") + (num * "#")
    return san

def draw_stats():
    color = "\033[92m"  # Green
    if data.PLAYER["hp"] <= 0.25 * data.PLAYER["max_hp"]:
        color = "\033[91m"  # Red
    elif data.PLAYER["hp"] <= 0.6 * data.PLAYER["max_hp"] :
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
        msg("The edge of the world blocks you!")
        pause()
        return player

        # 3. Get the tile now that we know we are in bounds
    tile = current_map[ny][nx]
    if not (0 <= nx < width and 0 <= ny < height):
        msg("The edge of the world blocks you!")
        pause()
        return player  # Return player unchanged

    if tile in data.TILE_EFFECTS:
        effect = data.TILE_EFFECTS[tile]

        # 1. Handle Blocking immediately
        if effect.get("block"):
            msg(effect["msg"])
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
                msg(effect["msg"])
                pause()
            return data.PLAYER

        # Update position and return

        if "msg" in effect:
            msg(effect["msg"])
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
        msg(f"The {item_name} is a curious object, but you can't use it now.")

    pause()


def show_inventory():
    page = 0
    items_per_page = 6
    categories = ["all", "food", "equipment", "quest"]
    cat_idx = 0

    while True:
        clear_screen()
        draw_stats()
        current_cat = categories[cat_idx]
        print(f"=== INVENTORY: {current_cat.upper()} ===")

        # --- FILTERING LOGIC ---
        all_item_names = list(sorted(data.PLAYER["inventory"].keys()))

        if current_cat == "all":
            filtered_names = all_item_names
        else:
            # Only keep items that match the current category type
            filtered_names = [
                name for name in all_item_names
                if data.ITEMS.get(name, {}).get("type") == current_cat
            ]

        total_items = len(filtered_names)
        # -----------------------

        if total_items == 0:
            print(f"\n   (No {current_cat} items)   \n")
            for _ in range(items_per_page - 2): print()
        else:
            start_idx = page * items_per_page
            end_idx = start_idx + items_per_page
            page_items = filtered_names[start_idx:end_idx]

            for i, name in enumerate(page_items, start_idx + 1):
                count = data.PLAYER["inventory"][name]
                print(f"{i}. {name[:20]:<20} x{count}")

            for _ in range(items_per_page - len(page_items)):
                print()

            total_pages = (total_items - 1) // items_per_page + 1
            print(f"\n--- Page {page + 1} of {total_pages} ---")

        print("=" * 25)
        print("(A/D) Pages | (W/S) Category | (Q)uit")

        choice = input("> ").lower()

        # Category Switching
        if choice == 'w':
            cat_idx = (cat_idx - 1) % len(categories)
            page = 0  # Reset page when switching categories
        elif choice == 's':
            cat_idx = (cat_idx + 1) % len(categories)
            page = 0
        # Navigation
        elif choice == 'q':
            break
        elif choice == 'a' and page > 0:
            page -= 1
        elif choice == 'd' and (page + 1) * items_per_page < total_items:
            page += 1
        # Use Item Logic
        elif choice.isdigit():
            selection = int(choice)
            if 1 <= selection <= total_items:
                chosen_item = filtered_names[selection - 1]
                use_item(chosen_item)


def xp_screen(enemy):
    # Calculate base XP based on monster toughness
    xp = int(0.25 * enemy['dmg'] * enemy['hp'])

    # GP is a randomized portion of the "effort" (XP) spent
    multipliers = [0.5, 0.75, 1.0, 1.25]
    gp = int(random.choice(multipliers) * xp)
    loot = get_random_loot(enemy)
    data.PLAYER["xp"] += xp
    xp_msg = ""
    if data.PLAYER["xp"] >= (data.PLAYER["level"] + 1) * 100:
        data.PLAYER["xp"] -= data.PLAYER["level"] * 100
        data.PLAYER["level"] += 1
        xp_msg = f"Nice! You have now reached Level: {data.PLAYER['level']}!"
    msg(f"You have gained. {xp} XP","loot" ,f"and {gp} GP was added to your stash.", f"You also found a {loot}!", xp_msg)
    data.PLAYER["gp"] += gp
    data.PLAYER["sanity"] -= enemy["madness"]
    if loot in data.PLAYER["inventory"]:
        data.PLAYER["inventory"][loot] += 1
    else:
        data.PLAYER["inventory"][loot] = 1




def get_random_loot(enemy):
    # random.choices returns a list based on the weights provided
    # population: the list of categories to choose from
    # weights: the list of chances corresponding to those categories
    rarities = list(enemy['loot_weights'].keys())
    weights = list(enemy['loot_weights'].values())
    selected_rarity = random.choices(rarities, weights=weights, k=1)[0]

    # Pick a random item from the chosen category
    items_to_pick_from = data.LOOT_DATA[selected_rarity]
    return random.choice(items_to_pick_from)

def death_check():
    if data.PLAYER['hp'] <= 0:
        return "death"
    elif data.PLAYER['sanity'] <= 0:
        return "sanity"
    return None

def helper_confirm(skill):
    clear_screen()
    msg(f"Are you sure you want to train {skill}? (Y/N)","skill")
    choice = input("> ").lower()
    if choice == 'y':
        return True
    return False



def show_stats_screen():
    p = data.PLAYER
    current_page = 1
    total_pages = 4

    while True:
        clear_screen()
        title = ""
        if current_page == 1:
            title = "CHARACTER SHEET"
        if current_page == 2:
            title = "SECONDARY SKILLS"
        if current_page == 3:
            title = "SKILLS"
        if current_page == 4:
            title = "EQUIPMENT"


        # 1. Header showing navigation
        print(f"--- {title} (Page {current_page}/{total_pages}) ---")

        # 2. Page Content
        if current_page == 1:
            skills = get_derived_stats()
            stat_width = 25
            stats = [
                ("Name", p['name']),
                ("Level", p['level']),
                ("XP", f"{p['xp']}/{p['level'] * 100}"),
                ("Health",  f"{p['hp']}/{skills[4]}"),
                ("Attack",  skills[0]),
                ("Sanity", sanity_bar()),
            ]
            for label, value in stats:
                print(f"{label}:{value: >{stat_width - len(label) - 1}}")





        elif current_page == 3:

            base = 5
            # 1. Calculate how many points they have earned in total
            total_earned = 5 * p['level'] + base

            # 2. Calculate how many points they have already assigned
            # Note the parentheses around the sum!
            total_spent = (
                    p['stats']['dread'] +
                    p['stats']['bastion'] +
                    p['stats']['instinct'] +
                    p['stats']['vigor'] +
                    p['stats']['cunning']
            )


            dread = get_current_stat("dread")
            bastion = get_current_stat("bastion")
            instinct = get_current_stat("instinct")
            vigor = get_current_stat("vigor")
            cunning = get_current_stat("cunning")



            p['stat_points'] = total_earned - total_spent

            width = 25  # Total width of the line
            # Define labels and values
            skills = [
                ("Dread", dread),
                ("Bastion", bastion),
                ("Instinct", instinct),
                ("Vigor", vigor),
                ("Cunning", cunning),
                ("Points", p['stat_points']),
            ]

            for label, value in skills:
                # Calculate how much space is left for the number
                # label_width = width - len(label)
                # {value: >X} right-aligns the value in a block of X characters
                print(f"{label}:{value: >{width - len(label) - 1}}")

        elif current_page == 2:
            skills = get_derived_stats()
            width = 25
            stats = [
            ("Accuracy", f"{skills[1]}%"),
            ("Crit Chance", f"{skills[2]}%"),
            ("Regen", skills[3]),
            ("Armor", skills[5]),
            ]
            for label, value in stats:
                # Calculate how much space is left for the number
                # label_width = width - len(label)
                # {value: >X} right-aligns the value in a block of X characters
                print(f"{label}:{value: >{width - len(label) - 1}}")

        elif current_page == 4:
            width = 25
            for slot, item in p["equipment"].items():
                display_item = item if item else "Empty"
                # Using your alignment logic!
                print(f"{slot.capitalize()}:{display_item: >{width - len(slot)}}")


            #TODO make equipment stats matter


        # 3. Footer and Input
        print("-" * 35)
        nav_bar = f"[A/D] Change Page | [Q] Quit "
        if current_page == 4:
            print("E Equip Item | ",nav_bar)
        else:
            print(nav_bar)

        if p['stat_points'] > 0 and current_page == 3:
            level_up = True
            print("\nYou are able to deepen your understanding.")
            print("Which skill would you like to train?")
            print("(F)Dread, (B)astion (I)nstint, (V)igor, (C)unning,")
        else:
            level_up = False
        choice = input("> ").lower()

        # 4. Navigation Logic
        if choice == 'd':
            current_page = current_page + 1 if current_page < total_pages else 1
        elif choice == 'a':
            current_page = current_page - 1 if current_page > 1 else total_pages
        elif choice == 'q':
            break
        # 5. Stat Spending Logic (only on page 2)
        if level_up:
            if choice == 'f' and p['stat_points'] > 0:
                if helper_confirm("Dread"):
                    p['stats']['dread'] += 1
            elif choice == 'i' and p['stat_points'] > 0:
                if helper_confirm("Instinct"):
                    p['stats']['instinct'] += 1
            elif choice == 'v' and p['stat_points'] > 0:
                if helper_confirm("Vigor"):
                    p['stats']['vigor'] += 1
            elif choice == 'c' and p['stat_points'] > 0:
                if helper_confirm("Cunning"):
                    p['stats']['cunning'] += 1
            elif choice == 'b' and p['stat_points'] > 0:
                if helper_confirm("Bastion"):
                    p['stats']['bastion'] += 1
        if current_page == 4:
            if choice == 'e':
                show_equipment_picker()



def get_derived_stats():
    # p is your data.PLAYER dictionary
    p = data.PLAYER
    # ///MAIN STATS///
    dread = get_current_stat("dread")
    bastion = get_current_stat("bastion")
    instinct = get_current_stat("instinct")
    vigor = get_current_stat("vigor")
    cunning = get_current_stat("cunning")
    # ///DERIVED STATS///
    atk_bonus = get_current_stat("atk")
    accuracy_bonus = get_current_stat("accuracy")
    crit_chance_bonus = get_current_stat("crit_chance")
    regen_bonus = get_current_stat("regen")
    max_hp_bonus = get_current_stat("max_hp")
    armor_bonus = get_current_stat("armor")


    # 1. Dread -> Attack (e.g., 2 DMG per point of Dread)
    atk = 5 + (dread * 2) + atk_bonus

    # 2. Instinct -> Accuracy (e.g., base 70% + 2% per point)
    accuracy = 75 + (instinct * 2) + accuracy_bonus

    # 3. Cunning -> Crit Chance (e.g., 1% per point)
    crit_chance = cunning + crit_chance_bonus

    # 4. Vigor -> Defense/Armor (e.g., 1 Armor per 2 points)
    regen = vigor // 5 + regen_bonus

    # 5. Vigor -> Health (e.g., 10 HP per point)
    max_hp = 50 + int((vigor * 2.5)) + max_hp_bonus

    armor = bastion//2 + armor_bonus
    return [atk, accuracy, crit_chance, regen, max_hp, armor]


def equip_item(item_name):
    p = data.PLAYER
    item_info = data.ITEMS.get(item_name)

    if not item_info or "slot" not in item_info:
        msg("This item cannot be equipped!", "error")
        return

    slot = item_info["slot"]

    # 1. Take the current item off (if there is one) and put it in inventory
    old_item = p["equipment"].get(slot)
    if old_item:
        p["inventory"][old_item] = p["inventory"].get(old_item, 0) + 1
        print(f"Unequipped {old_item}.")

    # 2. Put the new item on
    p["equipment"][slot] = item_name

    # 3. Remove the new item from inventory
    p["inventory"][item_name] -= 1
    if p["inventory"][item_name] <= 0:
        del p["inventory"][item_name]

    print(f"Successfully equipped {item_name} to {slot}!")


def show_equipment_picker():
    page = 0
    items_per_page = 6
    p = data.PLAYER

    while True:
        clear_screen()
        # --- THE FILTER ---
        # Look through inventory, but only keep items that have a 'slot' defined
        all_items = sorted(p["inventory"].keys())
        equippable_names = [
            name for name in all_items
            if "slot" in data.ITEMS.get(name, {})
        ]

        total_items = len(equippable_names)
        # ------------------

        print("--- SELECT EQUIPMENT ---")
        width = 25
        for slot in p["equipment"]:
            # 1. Get the name of the item (e.g., "Iron Helmet") or "Empty" if None
            item_name = p["equipment"][slot]
            if item_name is None:
                item_name = "Empty"

            # 2. Use alignment to push the item name to the right
            # slot.capitalize() makes "helmet" look like "Helmet"
            # The > operator right-aligns the item_name
            print(f"{slot.capitalize()}:{item_name: >{width - len(slot) - 1}}")
        if total_items == 0:
            print("\n  No equippable items found. \n")
            # Fill space for UI consistency
            for _ in range(items_per_page): print()
        else:
            start_idx = page * items_per_page
            end_idx = start_idx + items_per_page
            page_items = equippable_names[start_idx:end_idx]

            print("=" * 40)
            print(f"--- INVENTORY ---")

            for i, name in enumerate(page_items, start_idx + 1):
                item_data = data.ITEMS[name]
                slot_type = item_data["slot"]
                count = p["inventory"][name]
                # Display name and what slot it fits into
                print(f"{i}. {name[:15]:<15} [{slot_type}] x{count}")

            # Padding
            for _ in range(items_per_page - len(page_items)):
                print()

            total_pages = (total_items - 1) // items_per_page + 1
            print(f"\n--- Page {page + 1} of {total_pages} ---")

        print("(A/D) Pages | (Number) to Equip | (Q)uit")
        choice = input("> ").lower()

        if choice == 'q':
            break
        elif choice == 'a' and page > 0:
            page -= 1
        elif choice == 'd' and (page + 1) * items_per_page < total_items:
            page += 1
        elif choice.isdigit():
            selection = int(choice)
            if 1 <= selection <= total_items:
                chosen_item = equippable_names[selection - 1]
                # Use the equip function we discussed earlier!
                equip_item(chosen_item)


def get_current_stat(stat_name):
    p = data.PLAYER
    # 1. Start with the raw base value from the player
    # Check primary stats first, then default to 0 for combat stats
    base_value = p['stats'].get(stat_name, 0)

    # 2. Add bonuses from every equipped slot
    bonus = 0
    for slot in p['equipment']:
        item_name = p['equipment'][slot]
        if item_name in data.ITEMS:
            # Add the bonus if the item has this specific stat
            item_bonuses = data.ITEMS[item_name].get("stats", {})
            bonus += item_bonuses.get(stat_name, 0)

    return base_value + bonus