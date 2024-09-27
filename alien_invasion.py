import sys  # Import the sys module for system-specific parameters and functions.
from time import sleep  # Import sleep function to create delays.

import pygame  # Import the pygame module for game development.

# Import custom classes for game settings and functionalities.
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """Class that handles the overall management of the game assets and behavior."""

    def __init__(self):
        """Initialize the game and set up resources."""
        pygame.init()  # Initialize all imported pygame modules.
        self.settings = Settings()  # Create an instance of the Settings class.

        # Set up the game window in fullscreen mode and get its dimensions.
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")  # Set the window title.

        # Create an instance for tracking game statistics and the scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)  # Create a ship instance.
        self.bullets = pygame.sprite.Group()  # Group to manage bullet sprites.
        self.aliens = pygame.sprite.Group()  # Group to manage alien sprites.

        self._create_fleet()  # Create the fleet of aliens.

        # Initialize the Play button.
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Main loop for the game execution."""
        while True:  # Infinite loop to keep the game running.
            self._check_events()  # Check for user events.

            if self.stats.game_active:  # If the game is active.
                self.ship.update()  # Update the ship's position.
                self._update_bullets()  # Update bullets.
                self._update_aliens()  # Update aliens.

            self._update_screen()  # Refresh the screen with updated graphics.

    def _check_events(self):
        """Handle key presses and mouse events."""
        for event in pygame.event.get():  # Loop through event queue.
            if event.type == pygame.QUIT:  # If the quit event is triggered.
                sys.exit()  # Exit the game.
            elif event.type == pygame.KEYDOWN:  # If a key is pressed down.
                self._check_keydown_events(event)  # Check for specific key actions.
            elif event.type == pygame.KEYUP:  # If a key is released.
                self._check_keyup_events(event)  # Check for specific key releases.
            elif event.type == pygame.MOUSEBUTTONDOWN:  # If a mouse button is clicked.
                mouse_pos = pygame.mouse.get_pos()  # Get the mouse position.
                self._check_play_button(mouse_pos)  # Check if the Play button was clicked.

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks the Play button."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)  # Check if the button was clicked.
        if button_clicked and not self.stats.game_active:  # If button is clicked and the game is inactive.
            self.settings.initialize_dynamic_settings()  # Reset game settings.

            self.stats.reset_stats()  # Reset game statistics.
            self.stats.game_active = True  # Set the game to active.
            self.sb.prep_score()  # Prepare the scoreboard with current score.
            self.sb.prep_level()  # Prepare the scoreboard with current level.
            self.sb.prep_ships()  # Update the number of ships left.

            # Clear any existing aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()  # Create a new fleet of aliens.
            self.ship.center_ship()  # Center the ship on the screen.

            pygame.mouse.set_visible(False)  # Hide the mouse cursor.

    def _check_keydown_events(self, event):
        """Respond to key presses."""
        if event.key == pygame.K_RIGHT:  # If the right arrow key is pressed.
            self.ship.moving_right = True  # Set ship to move right.
        elif event.key == pygame.K_LEFT:  # If the left arrow key is pressed.
            self.ship.moving_left = True  # Set ship to move left.
        elif event.key == pygame.K_q:  # If the 'q' key is pressed.
            sys.exit()  # Exit the game.
        elif event.key == pygame.K_SPACE:  # If the space bar is pressed.
            self._fire_bullet()  # Fire a bullet.

    def _check_keyup_events(self, event):
        """Handle key releases."""
        if event.key == pygame.K_RIGHT:  # If the right arrow key is released.
            self.ship.moving_right = False  # Stop moving the ship right.
        elif event.key == pygame.K_LEFT:  # If the left arrow key is released.
            self.ship.moving_left = False  # Stop moving the ship left.

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullet group."""
        if len(self.bullets) < self.settings.bullets_allowed:  # Check if bullets limit is not reached.
            new_bullet = Bullet(self)  # Create a new Bullet instance.
            self.bullets.add(new_bullet)  # Add the new bullet to the group.

    def _update_bullets(self):
        """Update bullet positions and remove old bullets."""
        self.bullets.update()  # Update the position of all bullets.

        # Remove bullets that have gone off the screen.
        for bullet in self.bullets.copy():  # Iterate through a copy of the bullets.
            if bullet.rect.bottom <= 0:  # If the bullet has moved off the top of the screen.
                self.bullets.remove(bullet)  # Remove the bullet.

        self._check_bullet_alien_collisions()  # Check for collisions between bullets and aliens.

    def _check_bullet_alien_collisions(self):
        """Handle bullet-alien collisions."""
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)  # Check for collisions and remove colliding sprites.

        if collisions:  # If any collisions occurred.
            for aliens in collisions.values():  # Iterate through the collided aliens.
                self.stats.score += self.settings.alien_points * len(aliens)  # Update the score.
            self.sb.prep_score()  # Update the score display.
            self.sb.check_high_score()  # Check for a new high score.

        if not self.aliens:  # If there are no aliens left.
            self.bullets.empty()  # Remove all bullets.
            self._create_fleet()  # Create a new fleet of aliens.
            self.settings.increase_speed()  # Increase the game speed.

            self.stats.level += 1  # Increment the level.
            self.sb.prep_level()  # Update the level display.

    def _update_aliens(self):
        """Check for edge conditions and update all aliens."""
        self._check_fleet_edges()  # Check if aliens are at the screen edges.
        self.aliens.update()  # Update the positions of all aliens.

        # Check for collisions between the ship and aliens.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()  # Handle the ship being hit.

        # Check for aliens reaching the bottom of the screen.
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()  # Get the dimensions of the screen.
        for alien in self.aliens.sprites():  # Loop through all aliens.
            if alien.rect.bottom >= screen_rect.bottom:  # If an alien reaches the bottom.
                self._ship_hit()  # Handle the ship being hit.
                break  # Exit the loop.

    def _ship_hit(self):
        """Handle the event of the ship being hit by an alien."""
        if self.stats.ships_left > 0:  # If there are ships left.
            self.stats.ships_left -= 1  # Decrease the number of remaining ships.
            self.sb.prep_ships()  # Update the ships display.

            # Clear remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()  # Create a new fleet of aliens.
            self.ship.center_ship()  # Center the ship on the screen.

            sleep(0.5)  # Pause for half a second.
        else:
            self.stats.game_active = False  # Set the game to inactive.
            pygame.mouse.set_visible(True)  # Show the mouse cursor.

    def _create_fleet(self):
        """Create a fleet of aliens."""
        alien = Alien(self)  # Create an instance of Alien to use for calculations.
        alien_width, alien_height = alien.rect.size  # Get the size of the alien.
        available_space_x = self.settings.screen_width - (2 * alien_width)  # Calculate available space on x-axis.
        number_aliens_x = available_space_x // (2 * alien_width)  # Calculate the number of aliens that fit in the space.

        # Calculate the number of rows that fit on the screen.
        ship_height = self.ship.rect.height  # Get the height of the ship.
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)  # Calculate available space on y-axis.
        number_rows = available_space_y // (2 * alien_height)  # Calculate the number of rows.

        # Create the fleet of aliens.
        for row_number in range(number_rows):  # For each row.
            for alien_number in range(number_aliens_x):  # For each alien in the row.
                self._create_alien(alien_number, row_number)  # Create an alien.

    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the fleet."""
        alien = Alien(self)  # Create an instance of Alien.
        alien_width, alien_height = alien.rect.size  # Get the size of the alien.
        alien.x = alien_width + 2 * alien_width * alien_number  # Set the x position of the alien.
        alien.rect.x = alien.x  # Update the x coordinate of the alien's rect.
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number  # Set the y position of the alien.
        self.aliens.add(alien)  # Add the alien to the group.

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens reach the edge of the screen."""
        for alien in self.aliens.sprites():  # Loop through all aliens.
            if alien.check_edges():  # If the alien is at the edge.
                self._change_fleet_direction()  # Change the fleet's direction.
                break  # Exit the loop.

    def _change_fleet_direction(self):
        """Drop the entire fleet and change its direction."""
        for alien in self.aliens.sprites():  # Loop through all aliens.
            alien.rect.y += self.settings.fleet_drop_speed  # Move the fleet down.
        self.settings.fleet_direction *= -1  # Change the direction of the fleet.

    def _update_screen(self):
        """Update images on the screen and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)  # Fill the screen with the background color.
        self.ship.blitme()  # Draw the ship on the screen.
        for bullet in self.bullets.sprites():  # Draw each bullet.
            bullet.draw_bullet()  # Call the bullet's draw method.
        self.aliens.draw(self.screen)  # Draw all aliens.

        # Draw the score and level information.
        self.sb.show_score()  # Display the score.
        # If the game is inactive, display the Play button.
        if not self.stats.game_active:  
            self.play_button.draw_button()  # Draw the Play button.

        pygame.display.flip()  # Refresh the screen to display the new updates.

# Run the game if this module is executed.
if __name__ == '__main__':
    ai = AlienInvasion()  # Create an instance of the AlienInvasion class.
    ai.run_game()  # Start the game loop.
