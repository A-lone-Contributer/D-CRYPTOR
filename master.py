import curses
import os
import time
from curses.textpad import Textbox, rectangle
from random import choice

from asciimatics.effects import RandomNoise
from asciimatics.renderers import SpeechBubble, Rainbow
from asciimatics.scene import Scene
from asciimatics.screen import Screen

from decypher import DECRYPT
from encoder import ENCRYPT

os.system('cls||clear')


def demo(screen):
    render = Rainbow(screen, SpeechBubble('D - C R Y P T O R'))
    effects = [RandomNoise(screen, signal=render)]
    screen.play([Scene(effects, 330)], stop_on_resize=True, repeat=False)


Screen.wrapper(demo)


class MenuDisplay:

    def __init__(self, menu):

        # set menu parameter as class property
        self.menu = menu

        # run curses application
        curses.wrapper(self.mainloop)

    def mainloop(self, stdscr):
        # turn off cursor blinking
        curses.curs_set(0)

        # color scheme for selected row
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLUE)
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
        curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_CYAN)

        # set screen object as class property
        self.stdscr = stdscr

        # get screen height and width
        self.screen_height, self.screen_width = self.stdscr.getmaxyx()

        # specify the current selected row
        current_row = 0

        self.stdscr.clear()

        # print the menu
        self.print_menu(current_row)

        random_splashes = ['DECIPHERING... | PLEASE STANDBY!',
                           '>>>APPLYING MAGIC SPELLS<<<',
                           'GREAT THINGS TAKE TIME, PLEASE WAIT!',
                           'THESE SPELLS IS BACKED BY GENETIC ALGORITHM!!']

        while 1:

            key = self.stdscr.getch()

            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(self.menu) - 1:
                current_row += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:

                # if user selected last row (Exit), confirm before exit the program
                if current_row == len(self.menu) - 1:
                    if self.confirm("Are you sure you want to exit?"):
                        break

                elif current_row == len(self.menu) - 2:

                    self.stdscr.clear()
                    if os.path.exists('encoded_text.txt'):
                        with open('encoded_text.txt') as file:

                            self.print_center(choice(random_splashes), 4)
                            message = DECRYPT(file.read())

                    else:

                        self.print_center("No encoded text available to decode!")
                        break

                    with open('decoded_text.txt', 'w') as file:
                        file.write(message)

                    message = "DECODED MESSAGE: " + message
                    self.stdscr.clear()
                    maximum = self.maxlines()
                    for i in range(maximum):

                        try:
                            self.stdscr.attron(curses.color_pair(5))
                            self.stdscr.addstr(message[i])
                            self.stdscr.attron(curses.color_pair(5))
                            self.stdscr.refresh()
                        except:
                            pass

                    time.sleep(3)
                    self.stdscr.getch()

                else:
                    self.stdscr.clear()
                    self.color_print(1, 4, "Enter a message (>100 words) and press (Ctrl+G) to execute.", 3)

                    self.color_print(2, 4,
                                     "You can type the message below or click right mouse button to paste clipboard text",
                                     3)

                    # initial settings
                    curses.curs_set(0)
                    stdscr.nodelay(1)
                    stdscr.timeout(100)

                    # create a boz
                    sh, sw = stdscr.getmaxyx()
                    box = [[3, 3], [sh - 3, sw - 3]]  # [[ul_y, ul_x], [dr_y, dr_x]]

                    editwin = curses.newwin(23, box[1][1] - box[0][0] - 2, 3 + 1, 3 + 1)
                    rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])

                    self.stdscr.refresh()

                    box = Textbox(editwin)

                    # Let the user edit until Ctrl-G is struck.
                    box.edit()

                    # Get resulting contents
                    message = box.gather()

                    encoded_message = ENCRYPT(message)

                    with open('encoded_text.txt', 'w') as file:
                        file.write(encoded_message)

                    self.stdscr.clear()

                    maximum = self.maxlines()

                    encoded_message = "ENCODED MESSAGE: " + encoded_message
                    for i in range(maximum):

                        try:
                            self.stdscr.attron(curses.color_pair(2))
                            self.stdscr.addstr(encoded_message[i])
                            self.stdscr.attroff(curses.color_pair(2))

                        except:
                            pass

                        self.stdscr.refresh()

                    time.sleep(2)
                    self.stdscr.getch()

            self.print_menu(current_row)

    def maxlines(self):

        n = 0
        try:
            for i in range(300):
                self.stdscr.addstr(str(i))
                n += 1

        except:
            pass

        self.stdscr.erase()

        return n

    def print_menu(self, selected_row_idx):
        self.stdscr.clear()
        for idx, row in enumerate(self.menu):
            x = self.screen_width // 2 - len(row) // 2
            y = self.screen_height // 2 - len(menu) // 2 + idx
            if idx == selected_row_idx:
                self.color_print(y, x, row, 1)
            else:
                self.stdscr.addstr(y, x, row)
        self.stdscr.refresh()

    def color_print(self, y, x, text, pair_num):
        self.stdscr.attron(curses.color_pair(pair_num))
        self.stdscr.addstr(y, x, text)
        self.stdscr.attroff(curses.color_pair(pair_num))

    def print_confirm(self, selected="Yes"):
        # clear yes/no line
        curses.setsyx(self.screen_height // 2 + 1, 0)
        self.stdscr.clrtoeol()

        y = self.screen_height // 2 + 1
        options_width = 10

        # print yes
        option = "Yes"
        x = self.screen_width // 2 - options_width // 2 + len(option)
        if selected == option:
            self.color_print(y, x, option, 1)
        else:
            self.stdscr.addstr(y, x, option)

        # print no
        option = "No"
        x = self.screen_width // 2 + options_width // 2 - len(option)
        if selected == option:
            self.color_print(y, x, option, 1)
        else:
            self.stdscr.addstr(y, x, option)

        self.stdscr.refresh()

    def confirm(self, confirmation_text):
        self.print_center(confirmation_text)

        current_option = "Yes"
        self.print_confirm(current_option)

        while 1:
            key = self.stdscr.getch()

            if key == curses.KEY_RIGHT and current_option == "Yes":
                current_option = "No"
            elif key == curses.KEY_LEFT and current_option == "No":
                current_option = "Yes"
            elif key == curses.KEY_ENTER or key in [10, 13]:
                return True if current_option == "Yes" else False

            self.print_confirm(current_option)

    def print_center(self, text, pair_num=None):
        self.stdscr.clear()
        x = self.screen_width // 2 - len(text) // 2
        y = self.screen_height // 2

        if pair_num:
            self.stdscr.attron(curses.color_pair(pair_num))
            self.stdscr.addstr(y, x, text)
            self.stdscr.attroff(curses.color_pair(pair_num))
        else:
            self.stdscr.addstr(y, x, text)

        self.stdscr.refresh()


if __name__ == "__main__":
    menu = ['I want to encrypt a message.', 'I have already encrypted, just decipher!', 'leave?']

    MenuDisplay(menu)
