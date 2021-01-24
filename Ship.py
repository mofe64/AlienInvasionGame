import pygame


class Ship:
    """"A class to manage the ship"""

    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        #  start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        #  Store a decimal value for the ship's horizontal position
        self.x = float(self.rect.x)

        #  movement flags
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update The ships position based on the movement flag"""
        if self.moving_right:
            self.x += self.settings.ship_speed
        if self.moving_left:
            self.rect.x -= self.settings.ship_speed

        # update rect object from self.x
        self.rect.x = self.x

    def blitme(self):
        """Draw ship at the current location"""
        self.screen.blit(self.image, self.rect)
