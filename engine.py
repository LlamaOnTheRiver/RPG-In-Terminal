import os
import data
import random
import copy
import items


# engine.py

def msg(*lines, style="standard", pause_msg=True, draw=False):
    # ... (your styles logic) ...
    styles = {
        "standard": ("-", "|"),
        "combat": ("*", "!"),
        "loot": ("=", "$"),
        "error": ("!", "X"),
        "death": ("X", "X"),
        "skill": ("%", "&"),
        "shop": ("%", "$"),
        "event": ("~", "*")
    }
    border_char, side_char = styles.get(style, ("-", "|"))


    for i in range(0, len(lines), 4):
        chunk = lines[i: i + 4]

        # 1. THE REDRAW STEP
        if draw:
            draw_stats()
            draw_exploration_screen()
        # If we have the data, we can draw the world before the text

        # 2. DRAW THE DIALOGUE BOX
        width = max(len(str(line)) for line in chunk)
        print(border_char * (width + 4))
        for line in chunk:
            print(f"{side_char} {str(line).ljust(width)} {side_char}")
        print(border_char * (width + 4))

        # 3. PAUSE
        if i + 3 < len(lines):
            if pause_msg:
                pause()
                clear_screen()
        else:
            if pause_msg:
                pause()


def get_level_data(level_id): # I renamed last_map_id to level_id for clarity
    # 1. Use the level_id we were handed!
    if level_id not in data.visited_levels:
        data.visited_levels[level_id] = copy.deepcopy(data.DUNGEON[level_id]['map'])

    # 2. Get the map and calculate dimensions
    current_map = data.visited_levels[level_id]
    h = len(current_map)
    w = len(current_map[0]) if h > 0 else 0
    inv = data.PLAYER['inventory']

    # 3. Get monsters for THIS specific level_id
    fresh_monsters = copy.deepcopy(data.DUNGEON[level_id]['monsters'])

    return {
        "map": current_map,
        "monsters": fresh_monsters,
        "width": w,
        "height": h,
        "inv": inv
    }

def place_player_on_map(temp_view):
        px = data.GAME_STATE['x']
        py = data.GAME_STATE['y']
        colored_marker = data.GAME_STATE['marker']

        if 0 <= py < len(temp_view) and 0 <= px < len(temp_view[0]):
            temp_view[py][px] = colored_marker

        return temp_view


def move_player():
    # Remove the while loop and the drawing from here!
    print("Move (wasd) |  (Q)uit | (I)nventory:")
    move = input(">...").strip().lower()

    if move == "w": return 0, -1
    if move == "s": return 0, 1
    if move == "a": return -1, 0
    if move == "d": return 1, 0
    if move == "q": return -10, -10
    if move == "i": return 10, 10
    if move == "f": return 11, 11

    # If they hit a random key
    msg("Hero ponders about life")
    return 0, 0


def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def pause():
    input(">...")

def update_visibility(radius=1):
    fog_map = data.GAME_STATE['fog_map']
    m_grid = data.visited_levels[data.GAME_STATE['current_map']]
    w = len(m_grid[0]) if len(m_grid) > 0 else 0
    h = len(m_grid)
    px, py = data.GAME_STATE['x'], data.GAME_STATE['y']

    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            rx, ry = px + dx, py + dy
            if 0 <= rx < w and 0 <= ry < h:
                fog_map[ry][rx] = m_grid[ry][rx]
    return fog_map


def get_viewport(view, radius=4):
    # 'view' should be a list of lists (the grid) for this to work best
    height = len(view)
    width = len(view[0]) if height > 0 else 0
    size = (radius * 2) + 1

    start_y = max(0, min(data.GAME_STATE['y'] - radius, height - size))
    start_x = max(0, min(data.GAME_STATE['x'] - radius, width - size))

    viewport = []
    for y in range(start_y, start_y + size):
        if y < len(view):
            # Slice the list, then join
            row_list = view[y]
            sliced_row = row_list[start_x: start_x + size]
            viewport.append("".join(sliced_row))
    return viewport

def move_monsters(view_radius=3):
    monsters = data.DUNGEON[data.GAME_STATE['current_map']]['monsters']

    for m in monsters:
        player_x = data.GAME_STATE['x']
        player_y = data.GAME_STATE['y']

        dx = player_x - m['x']
        dy = player_y - m['y']

        nx, ny = m['x'], m['y']

        if abs(dx) <= view_radius and abs(dy) <= view_radius:

            if dx != 0 and dy != 0:
                if random.choice([True, False]):
                    nx += 1 if dx > 0 else -1
                else:
                    ny += 1 if dy > 0 else -1

            elif dx != 0:
                nx += 1 if dx > 0 else -1

            elif dy != 0:
                ny += 1 if dy > 0 else -1

        else:
            # wandering logic
            pass
        new_pos = [nx, ny]
        if is_passable(new_pos):
            m['x'], m['y'] = nx, ny

            
def place_entities(temp_view, monsters):
    for m in monsters:
        mx, my = m['x'], m['y']
        if 0 <= my < len(temp_view) and 0 <= mx < len(temp_view[0]):
            # Only draw the monster if the tile isn't "Fog" (empty space)
            if temp_view[my][mx] != " ":
                temp_view[my][mx] = m['marker']

def check_for_combat():
    monsters = data.DUNGEON[data.GAME_STATE['current_map']]['monsters']
    for monster in monsters:
        if monster['x'] == data.GAME_STATE['x'] and monster['y'] == data.GAME_STATE['y']:
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


def is_passable(new_pos):
    level_id = data.GAME_STATE['current_map']
    # Look directly at the stored map
    m_grid = data.visited_levels[level_id]

    h = len(m_grid)
    w = len(m_grid[0])
    nx, ny = new_pos

    # 1. BOUNDARY CHECK
    if nx < 0 or nx >= w or ny < 0 or ny >= h:
        return False

    # 2. COLLISION CHECK (Fixed the quotes!)
    if m_grid[ny][nx] in ["W", "#"]:
        return False
    return True

def battle(active_enemy):
    current_level = data.DUNGEON[data.GAME_STATE['current_map']]
    msg(f"A wild {active_enemy['name']} appeared!", style="combat")
    # Update player stats based on current level/points
    stats = get_derived_stats()
    # [atk, accuracy, crit_chance, regen, max_hp, armor]

    # Now use the derived values


    enemy = data.MONSTERS[active_enemy['name']]
    # Extract all lines after the first one
    # Slicing is safe: if the list is short, it just returns what it can (even an empty list)
    extra_lines = enemy['intro'][1:4]

    clear_screen()

    # Unpack the list into the optional parameters
    msg(enemy['intro'][0], *extra_lines, style='combat')
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
        msg(f"What will you do?", style="combat", pause_msg=False)
        action = input("(A)ttack or (R)un? ").lower()
        def atk():
            p = data.PLAYER
            draw_battle_screen(enemy, temp_hp)
            # Extract all lines after the first one
            # Slicing is safe: if the list is short, it just returns what it can (even an empty list)
            cry_lines = enemy['cry'][1:4]

            # Unpack the list into the optional parameters
            msg(enemy['cry'][0], *cry_lines, style="combat")
            draw_battle_screen(enemy, temp_hp)
            msg(f"{enemy['name']} does {enemy['dmg']} damage!", style="combat")
            p['hp'] -= max(enemy['dmg'] - p_armor, 0)
            if data.PLAYER['hp'] <= 0:
                data.PLAYER['hp'] = 0
                return True
            return False


        if action == "a":
            # Handle combat...
            if p_hit:
                damage = p_atk
                if p_crit:
                    clear_screen()
                    draw_battle_screen(enemy, temp_hp)
                    damage *= 2
                    msg(f"{data.PLAYER['name']} landed a crit and did {damage} damage!", style="combat")
                temp_hp -= p_atk
                if temp_hp <= 0:
                    temp_hp = 0
                    draw_battle_screen(enemy, temp_hp)
                    xp_screen(enemy)
                    # Remove the monster from the live list
                    current_level['monsters'].remove(active_enemy)
                    return "EXPLORE"
                else:
                    if atk():
                        return "GAME OVER"
            else:
                clear_screen()
                draw_battle_screen(enemy, temp_hp)
                msg(f"{data.PLAYER['name']} missed their attack!", style="combat")
                if atk():
                    return "GAME OVER"
        elif action == "r":
            num = random.randint(1, 3)
            if num == 3:
                msg(f"You managed to get away from the {enemy['name']}", style="combat")
                if active_enemy in current_level['monsters']:
                    current_level['monsters'].remove(active_enemy)
                return "EXPLORE"
            else:
                msg(f"The {enemy['name']} wont let you escape", style="combat")
                if atk():
                    return "GAME OVER"

def sanity_bar():
    num = data.PLAYER['sanity'] // 10
    san = ((10 - num) * "-") + (num * "#")
    return san

def draw_stats():
    color = "\033[92m"  # Green
    if data.PLAYER['hp'] <= 0.25 * data.PLAYER['max_hp']:
        color = "\033[91m"  # Red
    elif data.PLAYER['hp'] <= 0.6 * data.PLAYER['max_hp'] :
        color = "\033[93m"  # Yellow
    reset = "\033[0m"

    color_san = "\033[92m"  # Green
    if data.PLAYER['sanity'] <= 40:
        color_san = "\033[91m"  # Red
    elif data.PLAYER['sanity'] <= 70:
        color_san = "\033[93m"  # Yellow


    print(f"{color}HP: {data.PLAYER['hp']}{reset} | {color_san}SN:{sanity_bar()}{reset} | GP:{data.PLAYER['gp']}  \nMap:{data.GAME_STATE['current_map']} | Pos:{data.GAME_STATE['x'], data.GAME_STATE['y']}")
    print("~" * 40)

def draw_exploration_screen():
    fog_map = data.GAME_STATE['fog_map']
    update_visibility()
    m = data.DUNGEON[data.GAME_STATE['current_map']]['monsters']
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


def check_tile_event(new_pos):
    g = data.GAME_STATE
    p = data.PLAYER
    current_map = data.visited_levels[data.GAME_STATE['current_map']]
    nx, ny = new_pos[0], new_pos[1]
    tile = current_map[ny][nx]
    next_state = "EXPLORE"



    # 2. Boundary Check (Crucial to prevent "Index out of range" crashes)
    new_pos = (nx, ny)
    if is_passable(new_pos):
        g['x'], g['y'] = nx, ny
    else:
        msg("The path is blocked!")

    if tile in data.TILE_EFFECTS:
        effect = data.TILE_EFFECTS[tile]

        if effect.get("block"):
            msg(effect['msg'])
            return next_state # Stay in EXPLORE if blocked


        # Apply standard rewards (HP/GP)
        p['hp'] = min(p['max_hp'], p['hp'] + effect.get("hp", 0))
        p['gp'] += effect.get("gp", 0)

        # Trigger the State Change if the tile is a Shop
        if effect.get("shop"):
            msg(f"Welcome {data.PLAYER['name']} I may have something, that might interest you.", style="shop")
            next_state = "SHOP"

        if "consume" in effect:
            current_map[ny][nx] = effect['consume']

        if "event" in effect:
            next_state = 'EVENT'

        if "teleport" in effect:
            cords = (ny, nx)
            # Grab all the secret data from the CURRENT map before changing anything
            stair_data = data.DUNGEON[g['current_map']]['stairs'][cords]

            # Now update the player using that saved data
            g['current_map'] = stair_data['target_map']
            g['x'] = stair_data['target_x']
            g['y'] = stair_data['target_y']
            if "msg" in effect:
                msg(effect['msg'], pause_msg=False)
            return next_state

    return next_state


def use_item(item_name):
    if item_name in items.ITEM_REGISTRY:
        effect_function = items.ITEM_REGISTRY[item_name]
        result = effect_function()

        if result and "msg" in result:
            msg(result["msg"])

        data.PLAYER['inventory'][item_name] -= 1
        if data.PLAYER['inventory'][item_name] <= 0:
            del data.PLAYER['inventory'][item_name]
    else:
        msg(f"The {item_name} is a curious object, but you can't use it now.", style="error")




def show_inventory():
    page = 0
    items_per_page = 6
    categories = ['all', 'consume', 'equipment', 'quest']
    cat_idx = 0

    while True:
        clear_screen()
        draw_stats()
        current_cat = categories[cat_idx]
        print(f"=== INVENTORY: {current_cat.upper()} ===")

        # --- FILTERING LOGIC ---
        all_item_names = list(sorted(data.PLAYER['inventory'].keys()))

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

            for i, name in enumerate(page_items, 1):
                count = data.PLAYER['inventory'][name]
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
            return "EXPLORE"
        elif choice == 'a' and page > 0:
            page -= 1
        elif choice == 'd' and (page + 1) * items_per_page < total_items:
            page += 1
        # Use Item Logic
        elif choice.isdigit():
            start_idx = page * items_per_page
            end_idx = start_idx + items_per_page
            page_items = filtered_names[start_idx:end_idx]
            selection = int(choice)
            if 1 <= selection <= total_items:
                chosen_item = page_items[selection - 1]
                use_item(chosen_item)


def xp_screen(enemy):
    p = data.PLAYER
    # Calculate base XP based on monster toughness
    xp = int(0.25 * enemy['dmg'] * enemy['hp'])

    # GP is a randomized portion of the "effort" (XP) spent
    multipliers = [0.5, 0.75, 1.0, 1.25]
    gp = int(random.choice(multipliers) * xp)
    loot = get_random_loot(enemy)
    p['xp'] += xp
    xp_msg = ""
    if p['xp'] >= (p['level']) * p['xp_curve']:
        p['xp'] -= p['level'] * p['xp_curve']
        p['level'] += 1
        p['hp'] = p['max_hp']
        xp_msg = f"Nice! You have now reached Level: {data.PLAYER['level']}!"
    msg(f"You have gained {xp} XP." ,f"and {gp} GP was added to your stash.", f"You also found a {loot}!", style="loot")
    if xp_msg:
        msg(xp_msg, style="loot")
    data.PLAYER['gp'] += gp
    data.PLAYER['sanity'] -= enemy['madness']
    if loot in data.PLAYER['inventory']:
        data.PLAYER['inventory'][loot] += 1
    else:
        data.PLAYER['inventory'][loot] = 1




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
    msg(f"Are you sure you want to train {skill}? (Y/N)",style="skill", pause_msg=False)
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
                ("XP", f"{p['xp']}/{p['level'] * p['xp_curve']}"),
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
            for slot, item in p['equipment'].items():
                display_item = item if item else "Empty"
                # Using your alignment logic!
                print(f"{slot.capitalize()}:{display_item: >{width - len(slot)}}")


            #TODO make a skilltree
            #TODO make a crafting system
            #TODO make an event system



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
            return "EXPLORE"
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
        msg("This item cannot be equipped!", style="error")
        return

    slot = item_info['slot']

    # 1. Take the current item off (if there is one) and put it in inventory
    old_item = p['equipment'].get(slot)
    if old_item:
        p['inventory'][old_item] = p['inventory'].get(old_item, 0) + 1
        print(f"Unequipped {old_item}.")

    # 2. Put the new item on
    p['equipment'][slot] = item_name

    # 3. Remove the new item from inventory
    p['inventory'][item_name] -= 1
    if p['inventory'][item_name] <= 0:
        del p['inventory'][item_name]

    print(f"Successfully equipped {item_name} to {slot}!")


def show_equipment_picker():
    page = 0
    items_per_page = 6
    p = data.PLAYER

    while True:
        clear_screen()
        # --- THE FILTER ---
        # Look through inventory, but only keep items that have a 'slot' defined
        all_items = sorted(p['inventory'].keys())
        equippable_names = [
            name for name in all_items
            if "slot" in data.ITEMS.get(name, {})
        ]

        total_items = len(equippable_names)
        # ------------------

        print("--- SELECT EQUIPMENT ---")
        width = 25
        for slot in p['equipment']:
            # 1. Get the name of the item (e.g., "Iron Helmet") or "Empty" if None
            item_name = p['equipment'][slot]
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
                slot_type = item_data['slot']
                count = p['inventory'][name]
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


def show_shop_screen(floor_id):
    page = 0
    items_per_page = 6
    categories = ['all", "consume", "equipment", "material']
    cat_idx = 0
    mode = "buy"  # buy or sell

    while True:
        clear_screen()
        draw_stats()  # Your existing stats display
        current_cat = categories[cat_idx]

        # Determine which data source to use based on mode
        if mode == "buy":
            source_data = data.DUNGEON[floor_id]['shop']
            title = f"MERCHANT (BUYING - {current_cat.upper()})"
        else:
            source_data = data.PLAYER['inventory']
            title = f"YOUR PACK (SELLING - {current_cat.upper()})"

        print(f"======= {title} =======")

        # --- FILTERING LOGIC ---
        all_item_names = list(sorted(source_data.keys()))

        if current_cat == "all":
            filtered_names = all_item_names
        else:
            filtered_names = [
                name for name in all_item_names
                if data.ITEMS.get(name, {}).get("type") == current_cat
            ]

        total_items = len(filtered_names)

        # --- DISPLAY LOGIC ---
        if total_items == 0:
            print(f"\n   (No {current_cat} items)   \n")
            for _ in range(items_per_page - 2): print()
        else:
            start_idx = page * items_per_page
            end_idx = start_idx + items_per_page
            page_items = filtered_names[start_idx:end_idx]

            for i, name in enumerate(page_items, start_idx + 1):
                # Get price based on mode
                if mode == "buy":
                    # 1. Look up the price from the master ITEMS list
                    price = data.ITEMS[name]['value']

                    # 2. Look up the STOCK from the specific DUNGEON floor
                    # We use the 'name' to get the number from the shop dictionary
                    stock = data.DUNGEON[floor_id]['shop'][name]

                    # 3. Print the line with the actual stock number
                    print(f"{i}. {name[:18]:<18} | {price: >4} GP | x{stock: >2}")
                else:
                    # Sell for 50% of the buy price in data.ITEMS
                    price = data.ITEMS.get(name, {}).get("value", 10) // 2
                    count = data.PLAYER['inventory'][name]
                    print(f"{i}. {name[:18]:<18} | {price: >4} GP | x{count: >2}")

            for _ in range(items_per_page - len(page_items)):
                print()

            total_pages = (total_items - 1) // items_per_page + 1
            print(f"\n--- Page {page + 1} of {total_pages} ---")

        print("=" * 40)
        print("(A/D) Page | (W/S) Cat | (T)oggle Mode | (Q)uit")

        choice = input("> ").lower()

        # Logic for switching
        if choice == 'q':
            return "EXPLORE"
        elif choice == 't':
            mode = "sell" if mode == "buy" else "buy"
            page = 0  # Reset page on mode swap
        elif choice == 'w':
            cat_idx = (cat_idx - 1) % len(categories)
            page = 0
        elif choice == 's':
            cat_idx = (cat_idx + 1) % len(categories)
            page = 0
        elif choice == 'a' and page > 0:
            page -= 1
        elif choice == 'd' and (page + 1) * items_per_page < total_items:
            page += 1

        # --- TRANSACTION LOGIC ---
        elif choice.isdigit():
            selection = int(choice)
            if 1 <= selection <= total_items:
                chosen_name = filtered_names[selection - 1]

                if mode == "buy":
                    price = data.ITEMS[chosen_name]['value']
                    if data.PLAYER['gp'] >= price:
                        data.PLAYER['gp'] -= price
                        data.DUNGEON[floor_id]['shop'][chosen_name] -= 1
                        if data.DUNGEON[floor_id]['shop'][chosen_name] <= 0:
                            del data.DUNGEON[floor_id]['shop'][chosen_name]
                        # Add to player inventory
                        data.PLAYER['inventory'][chosen_name] = data.PLAYER['inventory'].get(chosen_name, 0) + 1
                        msg(f"Bought {chosen_name}!", style="shop")
                    else:
                        msg("Not enough gold!", style="shop")

                elif mode == "sell":
                    item_data = data.ITEMS.get(chosen_name, {})
                    base_price = item_data.get("value", 0)
                    sell_price = base_price // 2
                    if base_price <= 0:
                        msg("The merchant shakes their head. 'I have no use for this junk.'", style="shop")
                        continue  # Skip the rest of the transaction and restart the loop
                    # 2. Add gold to player
                    data.PLAYER['gp'] += sell_price

                    # 3. Remove from player's pack
                    data.PLAYER['inventory'][chosen_name] -= 1
                    if data.PLAYER['inventory'][chosen_name] <= 0:
                        del data.PLAYER['inventory'][chosen_name]

                    # 4. ADD TO MERCHANT'S STOCK
                    # Access the shop dictionary for the current floor
                    shop_stock = data.DUNGEON[floor_id]['shop']

                    if chosen_name in shop_stock:
                        shop_stock[chosen_name] += 1
                    else:
                        # If the merchant didn't sell this before, they do now!
                        shop_stock[chosen_name] = 1

                    msg(f"Sold {chosen_name} for {sell_price} GP. The merchant adds it to their shelf.", style="shop")
def skill_check(skill_name, number):
    p = data.PLAYER['stats'][skill_name]
    modifier = random.randint(1, 20)
    return p + modifier >= number

def apply_effect(eff, p):
    p['hp'] = min(p['max_hp'], p['hp'] + eff.get("hp", 0))
    p['gp'] += eff.get("gp", 0)
    p['xp'] += eff.get("xp", 0)
    p['sanity'] += eff.get("sanity", 0)
    item = eff.get("inventory")
    if item:
        p['inventory'][item] = p['inventory'].get(item, 0) + 1


def run_dialogue():
    # We start at the beginning of the path
    m = data.GAME_STATE['current_map']
    x = data.GAME_STATE['x']
    y = data.GAME_STATE['y']
    current_node_id = (m, x, y)
    p = data.PLAYER

    while current_node_id != "end":
        if death_check() == "death" or death_check() == "sanity":
            return "GAME OVER"
        node = data.DIALOGUE_NODES.get(current_node_id)
        if "effect" in node:
            apply_effect(node["effect"], p)

        if not node:
            msg(f"Error: No dialogue found for {current_node_id}", style="error")
            break

        # Start your list
        name = node.get("speaker", "")
        node_text = node['text']
        lines = []

        # Add the name header
        if name:
            lines.append(f"--- {name} ---")

        # Add every string from the text list as its own entry
        if isinstance(node_text, list):
            lines.extend(node_text)
        else:
            lines.append(node_text)

        # Unpack into msg
        msg(*lines, style="event", draw=True)

        # Show choices without a pause
        options = node.get("options", {})
        if options:
            choice_lines = [f"{key}: {choice['text']}" for key, choice in options.items()]
            msg(*choice_lines, style="event", draw=True, pause_msg=False)
            player_input = input(">...")
            # ... handle player input
        elif "next_node" in node:
            pause()
            current_node_id = node["next_node"]
        else:
            break

        if player_input in options:
            selected_choice = options[player_input]

            if "effect" in selected_choice:
                apply_effect(selected_choice["effect"], p)

            # 4. Check for a skill check before moving to the next node
            if "skill_required" in selected_choice:
                skill = selected_choice["skill_required"]
                difficulty = selected_choice["difficulty"]



                if skill_check(skill, difficulty):
                    msg("Success!", style="skill")

                    current_node_id = selected_choice["success_node"]
                else:
                    msg("Failure!", style="skill")
                    current_node_id = selected_choice["failure_node"]
            else:
                # No skill check, just move to the next part of the story
                current_node_id = selected_choice["next_node"]

    return "EXPLORE"


