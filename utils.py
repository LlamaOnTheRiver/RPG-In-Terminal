import re
import os

ANSI_ESCAPE = re.compile(r'\033\[[0-9;]*m')

def visible_len(text):
    return len(ANSI_ESCAPE.sub('', text))

def pad_line(text, width):
    padding = width - visible_len(text)
    return f"{text}{' ' * padding}"

def pause():
    input(">...")

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')







def msg(*lines, style="standard", pause_msg=True, draw_fn=None):
    # ... (your styles logic) ...
    colors = {
        "standard": "\033[37m",  # white
        "combat": "\033[31m",  # red
        "loot": "\033[33m",  # yellow
        "error": "\033[31m",  # red
        "death": "\033[35m",  # magenta
        "skill": "\033[36m",  # cyan
        "shop": "\033[32m",  # green
        "event": "\033[34m",  # blue
    }
    reset = "\033[0m"

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
        if draw_fn:
            draw_fn()
        # If we have the data, we can draw the world before the text

        # 2. DRAW THE DIALOGUE BOX
        color = colors.get(style, "\033[37m")
        width = max(visible_len(str(line)) for line in chunk)
        print(f"{color}{border_char * (width + 4)}{reset}")
        for line in chunk:
            print(f"{color}{side_char} {pad_line(str(line), width)} {side_char}{reset}")
        print(f"{color}{border_char * (width + 4)}{reset}")

        '''
        width = max(len(str(line)) for line in chunk)
        print(border_char * (width + 4))
        for line in chunk:
            print(f"{side_char} {str(line).ljust(width)} {side_char}")
        print(border_char * (width + 4))
        '''

        # 3. PAUSE
        if i + 3 < len(lines):
            if pause_msg:
                pause()
                clear_screen()
        else:
            if pause_msg:
                pause()