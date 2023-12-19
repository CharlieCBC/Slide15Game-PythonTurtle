"""
Bingchun Chang
CS 5001, Fall 2022
Project -- slide-15 puzzle game
"""

import turtle
from time import sleep
import os
import math
from random import shuffle
import datetime

WIDTH = 800
HEIGHT = 800

offset = WIDTH // 20
puzzle_width = ((WIDTH - offset * 2) / 3) * 2
leaderboard_width = WIDTH - puzzle_width - offset * 2 - 20

user_panel_y = ((HEIGHT / 2) - offset) - \
               ((HEIGHT - offset * 3) / 10) * 8 - offset
user_panel_height = ((HEIGHT - offset * 3) / 10) * 2


class Image(turtle.Turtle):
    """
    An Image is class that inherits turtle.Turtle to show image
    on the Turtle Screen
    """

    def __init__(self, x, y, image):
        """
        Method -- __init__
            Set its speed to instant, Pull its pen up
            so not drawing when going to given x and y and set its
            shape to given path
        Parameters:
            x -- a float to set turtle position x component
                on Turtle Screen
            y -- a float to set turtle position y component
                on Turtle Screen
            image -- a string as the path for its own shape
        Returns nothing
        """
        super().__init__()
        self.speed(0)
        self.up()
        self.goto(x, y)
        self.shape(image)


class Button:
    """
    A Button is class that creates a Clickable image on Turtle Screen
    with Callback on click
    """

    def __init__(self, x, y, image, onclick):
        """
        Method -- __init__
            create an image and pass its onclick to its
            image turtle onclick
        Parameters:
            x -- a float to set image position x component
                on Turtle Screen
            y -- a float to set image position y component
                on Turtle Screen
            image -- a string as the path for its image shape

            onclick -- a func as Callback trigger when image turtle clicked
        Returns nothing
        """
        self.image = Image(x, y, image)
        self.image.onclick(lambda x, y: onclick())


class Game:
    """
    Game is class that handle all the visual and logical
    part of the game
    """

    def __init__(self):
        """
        Method -- __init__
            Create and set up the turtle Screen,
            load all the resources and load the puzzle
            and draw the game interface
        Returns nothing
        """
        self.window = turtle.Screen()
        self.window.setup(820, 820)
        self.window.setworldcoordinates\
            (-WIDTH / 2, -HEIGHT / 2, WIDTH / 2, HEIGHT / 2)
        self.load_resources()
        self.turtle = turtle.Turtle()
        self.puzzleturtle = turtle.Turtle()
        self.puzzleturtle.ht()
        self.turtle.ht()

        self.tiles = []
        self.leaders = []

        self.moves_played = 0
        self.thumbnail_position = (
            -WIDTH / 2 + offset + puzzle_width + 20 +
            (leaderboard_width / 5) * 4, (HEIGHT / 2) - int(offset * 1.5))

        self.show_dialog_image("splash_screen.gif", 3)

        self.P_name = turtle.textinput("CS5001 Puzzle Slide", "Your Name:")
        self.moves = turtle.numinput("CS5001 Puzzle Slide - Moves",
                                     "Enter the number of moves (chances)"
                                     " you want (5-200)?")

        self.interface()

        self.load_new_puzzle("mario.puz")

        self.gameover = False
        while not self.gameover:
            self.window.update()

    def show_dialog_image(self, image, time):
        """
        Method -- show_dialog_image
            Show the Dialog Image for given time in
            seconds
        Parameters:
            image -- a str as path of dialog image
            time -- an int as time in second by which image hold
            on screen
        Returns nothing
        """
        dialog = Image(0, 0, os.path.join("Resources", image))
        turtle.update()
        sleep(time)
        dialog.ht()
        turtle.update()

    def load_resources(self):
        """
        Method -- load_resources
            Register all the images from Resources Folder
            to Turtle Screen
        Returns nothing
        """
        self.window.addshape(os.path.join("Resources", "splash_screen.gif"))
        self.window.addshape(os.path.join("Resources", "Lose.gif"))
        self.window.addshape(os.path.join("Resources", "credits.gif"))
        self.window.addshape(os.path.join("Resources", "winner.gif"))
        self.window.addshape(os.path.join("Resources", "file_error.gif"))
        self.window.addshape(os.path.join("Resources", "quitmsg.gif"))
        self.window.addshape(os.path.join("Resources", "file_warning.gif"))
        self.window.addshape(os.path.join("Resources",
                                          "leaderboard_error.gif"))
        self.window.addshape(os.path.join("Resources", "resetbutton.gif"))
        self.window.addshape(os.path.join("Resources", "loadbutton.gif"))
        self.window.addshape(os.path.join("Resources", "quitbutton.gif"))

    def draw_rectangle(self, x, y, width, height, thickness=1,
                       color="black", turtle=None):
        """
        Method -- draw_rectangle
            Draw a Rectangle at given x and y with given width and height
            of specified thickness and color
        Parameters:
            x -- a float to set rectangle position x component
                on Turtle Screen
            y -- a float to set rectangle position y component
                on Turtle Screen
            width -- a float as width of rectangle on Turtle Screen
            height -- a float as height of rectangle on Turtle Screen
            thickness -- an int as the thickness of rectangle,
                default value set to 1 if no input from user
            color -- a str as the color of rectangle outline,
                default value set to black if no input from user
            turtle -- a Turtle as turtle to draw rectangle if given,
                default value set to None if no input from user
        Returns nothing
        """
        t = self.turtle
        if turtle:
            t = turtle
        t.speed(0)
        t.pensize(thickness)
        t.pencolor(color)
        t.up()
        t.goto(x, y)
        t.setheading(0)
        if turtle:
            t.fillcolor("green")
        t.down()
        for i in range(2):
            t.fd(width)
            t.right(90)
            t.fd(height)
            t.right(90)

    def log_error(self, error):
        """
        Method -- log_error
            Log the given error to 5001_puzzle.err file
        Parameters:
            error -- an str as error text,
        Returns nothing
        """
        f = open("5001_puzzle.err", "a")
        DT = datetime.datetime.now().strftime("%a %b %d %H:%M:%S %Y")
        f.write(f"{DT}:Error: {error}\n")
        f.close()

    def reset_puzzle(self):
        """
        Method -- reset_puzzle
            Reset the puzzle to solve it
        Returns nothing
        """
        for i in range(self.no_of_tiles):
            self.puzzle[i] = i
            self.tiles[i].shape(self.tilepaths[i])

    def load_new_puzzle(self, path):
        """
        Method -- load_new_puzzle
            Load the puzzle from given path
        Parameters:
            path -- a str as the path for the puzzle file
        Returns nothing
        """
        try:
            f = open(path, "r")
        except:
            self.log_error(f"File {path} does not exist "
                           f"LOCATION: Game.load_new_puzzle()")
            self.show_dialog_image("file_error.gif", 2)
            return
        self.puzzleturtle.clear()
        for t in self.tiles:
            t.ht()

        self.moves_played = 0
        lines = f.read().split("\n")
        f.close()
        self.no_of_tiles = int(lines[1].split(": ")[1])
        thumbnail = lines[3].split(": ")[1]
        self.row_length = int(math.sqrt(self.no_of_tiles))
        self.tilepaths = [x.split(": ")[1]
                          for x in lines[4:4 + self.no_of_tiles]]

        self.window.addshape(thumbnail)
        self.thumbnail = Image(*self.thumbnail_position, thumbnail)
        self.puzzle = list(range(self.no_of_tiles))
        shuffle(self.puzzle)
        self.tiles = []
        x = 0
        y = 0
        for i, tile in enumerate(self.puzzle):
            self.window.addshape(self.tilepaths[tile])
            t = turtle.Turtle()
            t.speed(0)
            self.draw_rectangle((-WIDTH / 2 + WIDTH // 20 + 10) + x * 106,
                                (WIDTH / 2 - WIDTH // 20 - 50) - y * 106,
                                102, 102, turtle=self.puzzleturtle)
            t.up()
            t.goto((-WIDTH / 2 + WIDTH // 20 + 10) + x * 106 + 50 + 1,
                   WIDTH / 2 - WIDTH // 20 - 50 - y * 106 - 50 - 1)
            t.shape(self.tilepaths[tile])
            self.tiles.append(t)
            x += 1
            if x == self.row_length:
                x = 0
                y += 1
        for i, tile in enumerate(self.tiles):
            tile.onclick(lambda x, y, i=i: self.tile_clicked(i))

    def is_solved(self):
        """
        Method -- is_solved
            Check whether the puzzle is solved or not
        Returns whether the puzzle is solved or not
        """
        return self.puzzle == list(range(self.no_of_tiles))

    def save_leaderboard(self):
        """
        Method -- save_leaderboard
            Save the leaders to leaderboard.txt file with
            sorted by score
        Returns nothing
        """
        self.leaders.append([self.moves_played, self.P_name])
        self.leaders = sorted(self.leaders, key=lambda x: x[0])
        if len(self.leaders) > 10:
            self.leaders = self.leaders[:10]
        leaderboard_text = ""
        for leader in self.leaders:
            leaderboard_text += f"{leader[0]} : {leader[1]}\n"

        try:
            f = open("leaderboard.txt", "w")
            f.write(leaderboard_text)
            f.close()
        except:
            pass

    def tile_clicked(self, i):
        """
        Method -- tile_clicked
            Check whether the right tile is clicked and
            slide the tile
        Parameters:
            i -- an int as index of clicked tile
        Returns nothing
        """
        if i < self.row_length:
            top = None
        else:
            top = i - self.row_length
        if i >= self.no_of_tiles - self.row_length:
            bottom = None
        else:
            bottom = i + self.row_length
        if i % self.row_length == 0:
            left = None
        else:
            left = i - 1
        if (i + 1) % self.row_length == 0:
            right = None
        else:
            right = i + 1
        neighbours = [top, bottom, left, right]
        for n in neighbours:
            if n != None:
                if self.puzzle[n] == self.no_of_tiles - 1:
                    self.tiles[i].shape(self.tilepaths[self.puzzle[n]])
                    self.tiles[n].shape(self.tilepaths[self.puzzle[i]])
                    a = self.puzzle[i]
                    self.puzzle[i] = self.puzzle[n]
                    self.puzzle[n] = a
                    self.moves_played += 1
                    if self.is_solved():
                        self.save_leaderboard()
                        self.moves_turtle.clear()
                        self.moves_turtle.write(f"Player Moves: "
                                                f"{self.moves_played}",
                                                font=("arial", 25, "normal"))

                        self.show_dialog_image("winner.gif", 3)
                        self.gameover = True
                        break
                    elif self.moves_played > self.moves:
                        self.show_dialog_image("Lose.gif", 2)
                        self.show_dialog_image("credits.gif", 5)

                        self.gameover = True
                        break

                    self.moves_turtle.clear()
                    self.moves_turtle.write(f"Player Moves: "
                                            f"{self.moves_played}",
                                            font=("arial", 25, "normal"))

                    break

    def load_dialog(self):
        """
        Method -- load_dialog
            Open the dialog on load button clicked to with
            puzzle list to load the puzzle by entered path
        Returns nothing
        """
        filelist = os.listdir('.')
        for each in filelist[:]:
            if not (each.endswith(".puz")):
                filelist.remove(each)

        if len(filelist) > 10:
            self.show_dialog_image("file_warning.gif", 2)

        filelist = filelist[:10]
        name = turtle.textinput("Load Puzzle",
                                "Enter the name of the puzzle you "
                                "wish to load. Choices are:\n" + '\n'.join(
                                    [str(elem) for elem in filelist]))

        self.load_new_puzzle(name)

    def read_leaderboard_file(self):
        """
        Method -- read_leaderboard_file
            Read all leaders from leaderboard.txt file
            and store in game leaders list
        Returns nothing
        """
        self.leaders = []
        try:
            f = open("leaderboard.txt", "r")
            lines = f.read().split("\n")
            f.close()
            if len(lines) > 10:
                lines = lines[:10]
            for line in lines:
                if " : " in line:
                    score, name = line.split(" : ")
                    self.leaders.append([int(score), name])
            self.leaders = sorted(self.leaders, key=lambda x: x[0])

        except:
            self.log_error("Could not open leaderboard.txt. "
                           "LOCATION: Game.read_leaderboard_file()")
            self.show_dialog_image("leaderboard_error.gif", 2)

    def interface(self):
        """
        Method -- interface
            Draw the interface of the game
        Returns nothing
        """
        self.draw_rectangle((-WIDTH / 2) + offset, (HEIGHT / 2) -
                            offset, ((WIDTH - offset * 2) / 3) * 2,
                            ((HEIGHT - offset * 3) / 10) * 8, 5)
        self.draw_rectangle((-WIDTH / 2) + offset, user_panel_y, WIDTH -
                            offset * 2, ((HEIGHT - offset * 3) / 10) * 2, 5)

        self.draw_rectangle(-WIDTH / 2 + offset + puzzle_width + 20,
                            (HEIGHT / 2) - offset, leaderboard_width,
                            ((HEIGHT - offset * 3) / 10) * 8, 3, "blue")

        turtle.up()
        turtle.goto(-WIDTH / 2 + offset + puzzle_width + 20 + 10,
                    (HEIGHT / 2) - offset - 60)
        turtle.color("blue")
        turtle.ht()
        turtle.write("Leaders:", font=("Arial", 25, 'normal'))
        self.read_leaderboard_file()
        for i, leader in enumerate(self.leaders):
            turtle.goto(-WIDTH / 2 + offset + puzzle_width + 35,
                        (HEIGHT / 2) - offset - 120 - (40 * i))
            turtle.write(f"{leader[0]} : {leader[1]}",
                         font=("Arial", 22, 'normal'))

        self.reset_button = Button(100, user_panel_y -
                                   (user_panel_height / 2),
                                   os.path.join("Resources",
                                                "resetbutton.gif"),
                                   self.reset_puzzle)
        self.load_button = Button(200, user_panel_y -
                                  (user_panel_height / 2),
                                  os.path.join("Resources",
                                               "loadbutton.gif"),
                                  self.load_dialog)
        self.quit_button = Button(300, user_panel_y -
                                  (user_panel_height / 2),
                                  os.path.join("Resources",
                                               "quitbutton.gif"),
                                  self.quit)

        self.moves_turtle = turtle.Turtle()
        self.moves_turtle.ht()
        self.moves_turtle.up()
        self.moves_turtle.goto((-WIDTH / 2) + offset + 20, user_panel_y -
                               (user_panel_height / 2) - 20)

    def quit(self):
        """
        Method -- quit
            Quit the game when quit button clicked
        Returns nothing
        """
        self.show_dialog_image("quitmsg.gif", 3)
        self.gameover = True


def main():
    Game()


if __name__ == "__main__":
    main()
