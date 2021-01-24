import sys
import pygame
from settings import Settings
from Ship import Ship
from Bullet import Bullet
from Alien import Alien
from time import sleep
from GameStats import GameStats
from button import Button
from ScoreBoard import Scoreboard


class AlienInvasion:
    """"Overall class to manage game assets and behavior."""

    def __init__(self):
        """"Initialize the game and create game resources"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_height, self.settings.screen_width))
        # full screen settings
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien invasion")
        # Create an instance to store game statistics.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.play_button = Button(self, "Play")

    def run_game(self):
        """"Start the main loop for the game"""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

            # Get rid of bullets that have gone off screen

    def _check_events(self):
        """Respond to keypress and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_play_button(self, mouse_pos):
        """"Start a new game when player clicks play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game stats
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            # Get rid of any remaining game assets
            self.aliens.empty()
            self.bullets.empty()
            # Create new fleet and center ship
            self._create_fleet()
            self.ship.center_ship()
            # Hide mouse cursor
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Respond to keypresses. """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_q:
            sys.exit()

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _create_fleet(self):
        """Create a fleet of Aliens"""
        # create an alien and find the number of aliens in a row
        # spacing between the aliens is equal to one alien width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # determine number of rows of aliens that fit on screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # create fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """create an alien and place it in row """
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * (alien_width * alien_number)
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Updates images on the screen, and flips to new screen"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.sb.show_score()
        # Draw play button if game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()
        pygame.display.flip()

    def _update_bullets(self):
        """Update position of bullets and gets rid of old bullets"""
        # Update bullet positions
        self.bullets.update()
        # Get rid of bullets that have gone off screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # print(f" bullets generated : {len(self.bullets)}")
        self._check_bullet_alien_collision()

    def _check_bullet_alien_collision(self):
        # Check for bullet alien collisions
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        # check if all aliens in fleet destroyed
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.prep_high_score()
        if not self.aliens:
            # Destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """ Check if the fleet is at an edge,
        Update the positions of all aliens in the fleet
        """
        self._check_fleet_edges()
        self.aliens.update()
        # Look for alien ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()

    def _ship_hit(self):
        """Respond to ship being hit by an alien """
        if self.stats.ships_left > 0:
            # Decrement ships left and update scoreboard
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            # Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()
            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()
            # Pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the got hit.
                self._ship_hit()
                break


if __name__ == '__main__':
    # make a game instance and run the game
    ai = AlienInvasion()
    ai.run_game()
