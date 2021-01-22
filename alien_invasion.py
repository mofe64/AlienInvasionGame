import sys
import pygame
from settings import Settings


class AlienInvasion:
    """"Overall class to manage game assets and behavior."""

    def __init__(self):
        """"Initialize the game and create game resources"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(  # creates a display window(called a surface) of size 1200 by 800
            (self.settings.screen_height, self.settings.screen_width)
            # surface is part of screen where a game element can be displayed
        )  # surface returned by display.set_mode reps the games entire window,
        # when game animation loop is activated, this surface will be redrawn on every pass of the loop,
        # so it can be updated by with any changes triggered by user input
        pygame.display.set_caption("Alien invasion")
        # colors in pygame are specified as RGB values¶

    # game is controlled by the run_game method
    def run_game(self):
        """"Start the main loop for the game"""
        while True:  # contains a while loop which runs continuously
            # Watch for keyboard and mouse events
            for event in pygame.event.get():  # event loop that manages screen updates.
                # Listens for events and performs actions based on events
                # An event is an action user performs when playing game
                # pygame.event.get returns a list of events that have taken place since function last called
                if event.type == pygame.QUIT:
                    sys.exit()
            self.screen.fill(self.settings.bg_color)  # Fill screen with background color
            # Tells Pygame to make the most recently drawn screen visible
            pygame.display.flip()  # continually updates the display to show the new position
            # of game elements giving the illusion of movement


if __name__ == '__main__':
    # make a game instance and run the game
    ai = AlienInvasion()
    ai.run_game()
