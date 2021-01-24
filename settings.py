class Settings:
    """"A class to store all settings for AlienInvasion"""

    def __init__(self):
        # Screen Settings
        self.screen_width = 800
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ship Settings
        self.ship_speed = 1.5
        self.ship_limit = 1

        # Bullet Settings
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Alien settings
        self.alien_speed = 0.5
        self.fleet_drop_speed = 10
        # Fleet direction of 1 represents right, -1 represent left
        self.fleet_direction = 1
