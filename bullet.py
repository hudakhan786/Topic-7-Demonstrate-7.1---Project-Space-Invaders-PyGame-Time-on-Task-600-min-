import pygame  # Import the pygame module for game development.
from pygame.sprite import Sprite  # Import the Sprite class for creating game objects.

class Bullet(Sprite):
    """Class to handle bullets fired from the spaceship."""

    def __init__(self, ai_game):
        """Initialize a bullet object at the ship's current position."""
        super().__init__()  # Call the parent class (Sprite) constructor.
        self.screen = ai_game.screen  # Get the game screen from the main game instance.
        self.settings = ai_game.settings  # Access game settings for bullet attributes.
        self.color = self.settings.bullet_color  # Set the bullet color from settings.

        # Create a bullet rectangle at (0, 0) and position it correctly.
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)  # Define the bullet's rectangle.
        self.rect.midtop = ai_game.ship.rect.midtop  # Position the bullet at the ship's current top middle.

        # Store the bullet's vertical position as a floating-point number for precise movement.
        self.y = float(self.rect.y)  # Initialize the y-coordinate of the bullet.

    def update(self):
        """Move the bullet upwards on the screen."""
        # Decrease the bullet's y position based on its speed.
        self.y -= self.settings.bullet_speed  # Update the bullet's decimal y-coordinate.
        self.rect.y = self.y  # Update the rectangle's y-coordinate to match the decimal position.

    def draw_bullet(self):
        """Render the bullet on the screen."""
        # Draw the bullet rectangle using the specified color.
        pygame.draw.rect(self.screen, self.color, self.rect)  # Render the bullet on the game screen.
