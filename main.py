import curses
import time

def colour_in_square(display, row, column):
    """switches whether a cell is alive or dead"""
    if display[row][column] == dead:
        display[row][column] = alive
    else:
        display[row][column] = dead


def image_on_screen(stdscr, total_columns, total_rows) -> list[int, int, curses.window]:
    """creates window in which game is played"""
    stdscr.clear()
    stdscr.refresh()
    maxy, maxx = stdscr.getmaxyx()
    game_window_y = (maxy - total_rows) // 2
    game_window_x = (maxx - total_columns) // 2
    game_window = curses.newwin(total_rows + 2, total_columns + 2, game_window_y - 1, game_window_x - 1)
    game_window.border()
    game_window.refresh()
    return game_window_y, game_window_x, game_window


def check_for_new_life(display, row, column) -> int:
    """checks whether a particular cell is alive or dead"""
    if row >= 0 and column >= 0:
        try:
            if display[row][column] == alive:
                count = 1
            else:
                count = 0
        except:
            count = 0
    else:
        count = 0
    return count


def simulate_game_of_life(display, temp_display) -> tuple[list, int]:
    """updates which cells are alive and which are dead each generation"""
    for row in range(len(display)):
        for column in range(len(display[row])):
            temp_display[row][column] = display[row][column]
    for row in range(len(display)):
        for column in range(len(display[row])):
            if display[row][column] == dead:
                if scanning(display,row,column) == 3:
                    temp_display[row][column] = alive
            else:
                if scanning(display,row,column) < 2 or scanning(display,row,column) > 3:
                    temp_display[row][column] = dead
    different = 0
    for row in range(len(temp_display)):
        for column in range(len(temp_display[row])):
            if display[row][column] != temp_display[row][column]:
                different += 1
            display[row][column] = temp_display[row][column]
    return display, different


def scanning(display, row, column) -> int:
    """checks how many cells are alive around a particular cell"""
    count = 0
    count += check_for_new_life(display, row - 1, column - 1)
    count += check_for_new_life(display, row - 1, column)
    count += check_for_new_life(display, row - 1, column + 1)
    count += check_for_new_life(display, row, column - 1)
    count += check_for_new_life(display, row, column + 1)
    count += check_for_new_life(display, row + 1, column - 1)
    count += check_for_new_life(display, row + 1, column)
    count += check_for_new_life(display, row + 1, column + 1)
    return count


def display_title(stdscr, game_window, game_window_x, total_columns):
    """displays title of game"""
    title = "THE GAME OF LIFE"
    stdscr.move(((stdscr.getmaxyx()[0] - game_window.getmaxyx()[0]) // 4) - 1, (total_columns - len(title)) // 2 + game_window_x)
    typing(title, stdscr)


def final_action(stdscr) -> bool:
    """checks if user wants to play again and returns stop flag"""
    typing("Press p to play again, otherwise press q to quit", stdscr)
    while True:
        action = stdscr.getkey()
        if action == "q":
            stdscr.clear()
            stdscr.refresh()
            farewell = "THE END"
            stdscr.move(stdscr.getmaxyx()[0] // 2, (stdscr.getmaxyx()[1] - len(farewell)) // 2)
            typing(farewell, stdscr)
            stdscr.refresh()
            time.sleep(5)
            return True
        elif action == "p":
            stdscr.clear()
            return False


def play_game(stdscr, total_columns, total_rows) -> bool:
    """sets up start pattern and oversees the running of the game"""
    display = [[dead for x in range(total_columns)] for y in range(total_rows)]
    temp_display = [[dead for x in range(total_columns)] for y in range(total_rows)]
    game_window_y, game_window_x, game_window = image_on_screen(stdscr, total_columns, total_rows)
    display_title(stdscr, game_window, game_window_x, total_columns)
    game_window.move(1,1)
    game_window.nodelay(False)
    direction = game_window.getkey()
    while direction != " ":
        try:
            curses.curs_set(1)
            if direction == "w" and game_window.getyx()[0] > 1:
                game_window.move(game_window.getyx()[0] - 1, game_window.getyx()[1])
                curses.flushinp()
                game_window.refresh()
            elif direction == "s" and game_window.getyx()[0] < total_rows:
                game_window.move(game_window.getyx()[0] + 1, game_window.getyx()[1])
                curses.flushinp()
                game_window.refresh()
            elif direction == "a" and game_window.getyx()[1] > 1:
                game_window.move(game_window.getyx()[0], game_window.getyx()[1] - 1)
                curses.flushinp()
                game_window.refresh()
            elif direction == "d" and game_window.getyx()[1] < total_columns:
                game_window.move(game_window.getyx()[0], game_window.getyx()[1] + 1)
                curses.flushinp()
                game_window.refresh()
            elif direction == ".":
                curses.curs_set(0)
                currenty, currentx = game_window.getyx()
                colour_in_square(display, currenty - 1, currentx - 1)
                game_window.addch(display[currenty - 1][currentx - 1])
                game_window.move(currenty, currentx)
                curses.flushinp()
                game_window.refresh()
            else:
                game_window.refresh()
                direction = game_window.getkey()
                continue
            game_window.refresh()
            direction = game_window.getkey()
        except:
            direction = game_window.getkey()
            continue
    return play_game_impl(display, temp_display, stdscr, game_window_y, game_window_x, game_window, total_columns, total_rows)



def update_board(display, game_window, total_columns, total_rows, stdscr, gen) -> int:
    """displays the updated board each generation"""
    curses.curs_set(0)
    for row in range(total_rows):
        for column in range(total_columns):
            game_window.move(row + 1, column + 1)
            game_window.addch(display[row][column])
            game_window.refresh()
    stdscr.refresh()
    gen += 1
    stdscr.clrtoeol()
    stdscr.refresh()
    return gen


def manual_mode(display, temp_display, stdscr, game_window, total_columns, total_rows, gen, game_window_y, game_window_x):
    """oversees progressing through the generations when manual mode is selected"""
    char = stdscr.getkey()
    while char != " ":
        if char == "q":
            return
        char = stdscr.getkey()
    display, different = simulate_game_of_life(display, temp_display)
    gen = update_board(display, game_window, total_columns, total_rows, stdscr, gen)
    stdscr.addstr(game_window_y + total_rows + 1, game_window_x, f"Generation: {gen}")
    while different != 0:
        char = stdscr.getkey()
        if char == "q":
            break
        while char != " ":
            if char == "q":
                different = 0
                break
            char = stdscr.getkey()
        display, different = simulate_game_of_life(display, temp_display)
        gen = update_board(display, game_window, total_columns, total_rows, stdscr, gen)
        if different != 0:
            stdscr.addstr(game_window_y + total_rows + 1, game_window_x, f"Generation: {gen}")


def auto_mode(display, temp_display, stdscr, game_window, speed, total_columns, total_rows, gen, game_window_y, game_window_x):
    """oversees progressing through the generations when one of the automatic modes is selected"""
    stdscr.nodelay(True)
    display, different = simulate_game_of_life(display, temp_display)
    curses.napms(speed)
    gen = update_board(display, game_window, total_columns, total_rows, stdscr, gen)
    stdscr.addstr(game_window_y + total_rows + 1, game_window_x, f"Generation: {gen}")
    while different != 0:
        char = stdscr.getch()
        if char == ord("q"):
            break
        elif char == -1:
            display, different = simulate_game_of_life(display, temp_display)
            curses.napms(speed)
            gen = update_board(display, game_window, total_columns, total_rows, stdscr, gen)
            if different != 0:
                stdscr.addstr(game_window_y + total_rows + 1, game_window_x, f"Generation: {gen}")
    stdscr.nodelay(False)


def play_game_impl(display, temp_display, stdscr, game_window_y, game_window_x, game_window, total_columns, total_rows) -> bool:
    """allows user to select which mode to play the game in"""
    gen = 0
    stdscr.addstr(game_window_y + total_rows + 1, game_window_x, f"Generation: {gen}")
    stdscr.move(game_window_y - 3, game_window_x)
    typing("Press 1 for manual mode, press 2 for slow mode, press 3 for normal mode, press 4 for fast mode...", stdscr)
    stdscr.refresh()
    stdscr.nodelay(False)
    num = stdscr.getkey()
    while True:
        if num == "1":
            stdscr.refresh()
            stdscr.move(game_window_y - 3, game_window_x)
            stdscr.clrtoeol()
            stdscr.refresh()
            stdscr.move(game_window_y - 3, game_window_x)
            typing("Manual mode: press space to see the next iteration", stdscr)
            manual_mode(display, temp_display, stdscr, game_window, total_columns, total_rows, gen, game_window_y, game_window_x)
            break
        elif num == "2":
            stdscr.move(game_window_y - 3, game_window_x)
            stdscr.clrtoeol()
            stdscr.move(game_window_y - 3, game_window_x)
            typing("Slow mode: leaves time for deep contemplation", stdscr)
            auto_mode(display, temp_display, stdscr, game_window, 3000, total_columns, total_rows, gen, game_window_y, game_window_x)
            break
        elif num == "3":
            stdscr.move(game_window_y - 3, game_window_x)
            stdscr.clrtoeol()
            stdscr.move(game_window_y - 3, game_window_x)
            typing("Normal mode: exactly how things should be", stdscr)
            auto_mode(display, temp_display, stdscr, game_window, 300, total_columns, total_rows, gen, game_window_y, game_window_x)
            break
        elif num == "4":
            stdscr.move(game_window_y - 3, game_window_x)
            stdscr.clrtoeol()
            stdscr.move(game_window_y - 3, game_window_x)
            typing("Fast mode: it just looks cool", stdscr)
            auto_mode(display, temp_display, stdscr, game_window, 10, total_columns, total_rows, gen, game_window_y, game_window_x)
            break
        else:
            num = stdscr.getkey()
    stdscr.refresh()
    stdscr.move(game_window_y - 3, game_window_x)
    stdscr.clrtoeol()
    stdscr.refresh()
    stdscr.move(game_window_y - 3, game_window_x)
    return final_action(stdscr)


def typing(sentence, stdscr):
    """displays a line of text one character after another"""
    col = 0
    curses.curs_set(0)
    for char in range(len(sentence)):
        stdscr.addstr(sentence[char])
        stdscr.refresh()
        col += 1
        curses.napms(50)
    curses.curs_set(1)


def instructions(stdscr):
    """displays the instructions for the game"""
    stdscr.addch("\n")
    stdscr.addch("\n")
    typing("WHAT IS THE GAME OF LIFE?\n", stdscr)
    typing("The Game of Life is a simulation invented by mathematician John Conway in which very simple rules cause complex patterns to emerge.\n", stdscr)
    typing(f"Each cell in a square grid can either be \"alive\" or \"dead\" (represented in this version by \"{alive}\" and \"{dead}\" respectively).\n", stdscr)
    typing("In order to survive to the next generation, an alive cell must have 2 or 3 neighbouring alive cells.\n", stdscr)
    typing("Each alive cell with 4 or more neighbours will die from overpopulation.\n", stdscr)
    typing("Each alive cell with 1 or 0 neighbours will die from isolation.\n", stdscr)
    typing("Each dead cell adjacent to exactly 3 neighbours is a birth cell and will become alive in the next generation.\n", stdscr)
    typing("All births and deaths occur simultaneously within each generation.\n", stdscr)
    stdscr.addch("\n")
    stdscr.addch("\n")
    typing("HOW TO PLAY:\n", stdscr)
    typing("Use \"w\", \"a\", \"s\", and \"d\" keys to move the cursor around the box.\n", stdscr)
    typing("Use \".\" to select the cell beneath the cursor.\n", stdscr)
    typing("When satisfied with the starting pattern press space to begin the simulation.\n", stdscr)
    typing("TIP: if unsure what makes a good start pattern, just select lots of cells randomly but close to each other and see what happens.\n", stdscr)
    typing("Once the simulation is running you can press \"q\" at any point to quit.\n", stdscr)
    typing("Press any key to start...", stdscr)
    stdscr.refresh()
    stdscr.nodelay(False)
    stdscr.getch()





def main():
    curses.wrapper(curses_main)


def curses_main(stdscr):
    """introduces the game"""
    while True:
        typing("Welcome to the game of life", stdscr)
        stdscr.addch("\n")
        typing("Press i for instructions, any other key to start...", stdscr)
        choice = stdscr.getkey()
        if choice == "i":
            instructions(stdscr)
        total_columns = stdscr.getmaxyx()[1] * 2 // 3
        total_rows = stdscr.getmaxyx()[0] * 2 // 3
        if play_game(stdscr, total_columns, total_rows):
            break


if __name__ == "__main__":
    alive = "*"
    dead = " "
    main()