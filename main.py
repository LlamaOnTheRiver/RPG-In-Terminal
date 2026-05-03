import engine

game_map = [
    ["w","w","w","w","w",],
    ["w","w","w","w","w",],
    ["w","w","w","w","w",],
    ["w","w","w","w","w",],
    ["w","w","w","w","w",],
]
player_marker = "P"
    
def main(game_map, player_marker):
    current_x = 2
    current_y = 2
    while True:
        temp_map = [row[:] for row in game_map]
        view = engine.place_player_on_map(temp_map, current_x, current_y, player_marker)
        engine.clear_screen()
        for line in view:
            print(line)
        dx, dy = engine.move_player()
        current_x += dx
        current_y += dy



main(game_map, player_marker)





