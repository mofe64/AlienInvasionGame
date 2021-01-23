import pygame


# best type of image resources to use with pygame are bitmaps, pygame loads bitmaps by default
# Pygame is efficient because it lets you treat all game elements like rectangles (rects),
# even if they’re not exactly shaped like rectangles
class Ship:
    """"A class to manage the ship"""

    def __init__(self, ai_game):  # giving the ship an instance of the game gives
        # the ship access to game resources defined in alien invasion
        """"Initialize the ship and set it's starting position"""
        self.screen = ai_game.screen  # assign screen to ship attr so we can have access to it
        self.screen_rect = ai_game.screen.get_rect()  # we access screen’s rect attribute using the get_rect() method
        # and assign it to self.screen_rect. Doing so allows us to place the ship in the
        # correct location on the screen.

        # Load the ship and get its rect
        self.image = pygame.image.load('images/ship.bmp')  # returns a surface representing the ship
        self.rect = self.image.get_rect()  # access ship's surface rect attr, can be used to place ship

        # Start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

    def blitme(self):
        """"Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
