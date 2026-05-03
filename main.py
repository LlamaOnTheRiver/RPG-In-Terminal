import engine
game_map = [
    [".",".",".","G","G",".",".",".","G","G",],
    [".",".",".","G","G",".",".",".","G","G",],
    [".",".",".","G","G",".",".",".","G","G",],
    [".",".",".","G","G",".",".",".","G","G",],
    [".","T","T","G","G","W","W","W","G","G",],
    [".","T","T","G","G",".",".","W","G","G",],
    [".",".",".","G","G",".",".","W","G","G",],
    [".",".",".","G","G","H","H",".","G","G",],
    [".",".",".","G","G",".",".",".","G","G",],
    [".",".",".","G","G",".",".",".","G","G",],
]

    
def main(game_map):
    if not game_map or not game_map[0]:
        print("The world has not been created yet! (Empty Map)")
        return
    player = {
        "x": 2,
        "y": 2,
        "hp": 100,
        "gp": 0,
        "marker": "P",
        "max_hp": 200
}
    height = len(game_map)
    width = len(game_map[0])
    fog_map = [[" " for _ in range(width)] for _ in range(height)]
    while True:
        if player["hp"] <= 0:
            print("You have perished in the dungeon...")
            return
        engine.update_visibility(fog_map,player,game_map, width, height)
        temp_view = [row[:] for row in fog_map]
        view = engine.place_player_on_map(temp_view, player)
        viewport = engine.get_viewport(view, player)
        
        engine.clear_screen()
        if player["hp"] > 60:
            color = "\033[92m" # Green
        elif player["hp"] > 25:
            color = "\033[93m" # Yellow
        else:
            color = "\033[91m" # Red     
        reset = "\033[0m"

        print(f"{color}HP: {player['hp']}{reset} | GP:{player['gp']} | Position: ({player['x']}, {player['y']})")
        print("~" * 30)
        
        for line in viewport:
            print(line)
        dx, dy = engine.move_player()
        if dx == -10 and dy == -10: break
        new_pos = (player["x"] + dx, player["y"] + dy)
        player = engine.check_tile_event(player, new_pos, game_map)   
    
main(game_map)





