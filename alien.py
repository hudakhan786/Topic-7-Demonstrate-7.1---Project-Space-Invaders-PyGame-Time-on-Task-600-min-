import pygame  # Import the pygame module for game development.
from pygame.sprite import Sprite  # Import Sprite class for creating game objects.

class Alien(Sprite):
    """A class representing a single alien in the game fleet."""

    def __init__(self, ai_game):
        """Initialize the alien and set its initial position."""
        super().__init__()  # Call the parent class (Sprite) constructor.
        self.screen = ai_game.screen  # Get the game screen from the main game instance.
        self.settings = ai_game.settings  # Get game settings from the main game instance.

        # Load the alien image and set its rectangle attribute for positioning.
        self.image = pygame.image.load('images/alien.bmp')  # Load the alien image from the specified path.
        self.rect = self.image.get_rect()  # Get the rectangle surrounding the image.

        # Position the alien at the top-left corner of the screen.
        self.rect.x = self.rect.width  # Set the x position to the width of the alien.
        self.rect.y = self.rect.height  # Set the y position to the height of the alien.

        # Store the exact horizontal position of the alien as a floating-point number.
        self.x = float(self.rect.x)  # Initialize the x-coordinate as a float for smoother movement.

    def check_edges(self):
        """Check if the alien is at the edge of the screen."""
        screen_rect = self.screen.get_rect()  # Get the dimensions of the screen.
        # Return True if the alien is at the right or left edge of the screen.
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:  
            return True  # The alien has reached the edge.

    def update(self):
        """Move the alien horizontally based on the fleet direction."""
        # Update the alien's x position based on its speed and direction.
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)  
        self.rect.x = self.x  # Update the rect's x-coordinate to reflect the new position.
