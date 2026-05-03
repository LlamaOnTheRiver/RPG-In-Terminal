import os

def place_player_on_map(game_map, x, y, player_marker):
    if game_map and 0 <= x < len(game_map[0]) and 0 <= y < len(game_map): 
        game_map[y][x] = player_marker
    new_map = []
    return ["".join(row) for row in game_map]
    

def move_player():
    move = input("Move (wasd): ").strip().lower()
    if move == "w": return 0, -1
    if move == "s": return 0, 1
    if move == "a": return -1, 0
    if move == "d": return 1, 0
    print("Hero ponders about life")
    input("Press Enter to continue")
    return 0, 0

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')