import pygame.font  # Import the font module from Pygame.
from pygame.sprite import Group  # Import Group to manage multiple sprites.

from ship import Ship  # Import the Ship class from the ship module.


class Scoreboard:
    """Class to manage and display scoring information in the game."""

    def __init__(self, ai_game):
        """Initialize the attributes for scorekeeping."""
        self.ai_game = ai_game  # Store the instance of the main game.
        self.screen = ai_game.screen  # Get the screen from the game instance.
        self.screen_rect = self.screen.get_rect()  # Get the dimensions of the screen.
        self.settings = ai_game.settings  # Access the game's settings.
        self.stats = ai_game.stats  # Access the game's statistics.

        # Set font color for the score display.
        self.text_color = (30, 30, 30)  # Define the color for the text.
        self.font = pygame.font.SysFont(None, 48)  # Set the font style and size.

        # Prepare images for the initial score display.
        self.prep_score()  # Prepare the score image.
        self.prep_high_score()  # Prepare the high score image.
        self.prep_level()  # Prepare the level image.
        self.prep_ships()  # Prepare the ships remaining display.

    def prep_score(self):
        """Convert the score to a rendered image for display."""
        rounded_score = round(self.stats.score, -1)  # Round the score to the nearest ten.
        score_str = "{:,}".format(rounded_score)  # Format the score with commas.
        self.score_image = self.font.render(score_str, True,  # Render the score as an image.
                                             self.text_color, self.settings.bg_color)

        # Position the score image at the top-right corner.
        self.score_rect = self.score_image.get_rect()  # Get the rectangle for the score image.
        self.score_rect.right = self.screen_rect.right - 20  # Set the right position.
        self.score_rect.top = 20  # Set the top position.

    def prep_high_score(self):
        """Convert the high score to a rendered image for display."""
        high_score = round(self.stats.high_score, -1)  # Round the high score.
        high_score_str = "{:,}".format(high_score)  # Format the high score with commas.
        self.high_score_image = self.font.render(high_score_str, True,  # Render the high score image.
                                                  self.text_color, self.settings.bg_color)

        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()  # Get the rectangle for the high score image.
        self.high_score_rect.centerx = self.screen_rect.centerx  # Center it horizontally.
        self.high_score_rect.top = self.score_rect.top  # Align it with the score's top.

    def prep_level(self):
        """Convert the current level to a rendered image for display."""
        level_str = str(self.stats.level)  # Convert the level number to a string.
        self.level_image = self.font.render(level_str, True,  # Render the level image.
                                             self.text_color, self.settings.bg_color)

        # Position the level display below the score.
        self.level_rect = self.level_image.get_rect()  # Get the rectangle for the level image.
        self.level_rect.right = self.score_rect.right  # Align it with the score's right.
        self.level_rect.top = self.score_rect.bottom + 10  # Position it below the score.

    def prep_ships(self):
        """Display the number of remaining ships."""
        self.ships = Group()  # Create a group to hold ship sprites.
        for ship_number in range(self.stats.ships_left):  # Loop through the number of remaining ships.
            ship = Ship(self.ai_game)  # Create a new ship instance.
            ship.rect.x = 10 + ship_number * ship.rect.width  # Position ships horizontally.
            ship.rect.y = 10  # Set the vertical position.
            self.ships.add(ship)  # Add the ship to the group.

    def check_high_score(self):
        """Check if the current score is a new high score."""
        if self.stats.score > self.stats.high_score:  # Compare current score with high score.
            self.stats.high_score = self.stats.score  # Update the high score if needed.
            self.prep_high_score()  # Prepare the new high score image.

    def show_score(self):
        """Render the score, level, and ships on the screen."""
        self.screen.blit(self.score_image, self.score_rect)  # Draw the score image.
        self.screen.blit(self.high_score_image, self.high_score_rect)  # Draw the high score image.
        self.screen.blit(self.level_image, self.level_rect)  # Draw the level image.
        self.ships.draw(self.screen)  # Draw the remaining ships on the screen.
