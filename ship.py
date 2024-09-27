import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """Class to manage the player's ship."""

    def __init__(self, ai_game):
        """Initialize the ship and set its initial position on the screen."""
        super().__init__()  # Initialize the parent class (Sprite).
        self.screen = ai_game.screen  # Reference to the game screen.
        self.settings = ai_game.settings  # Reference to game settings.
        self.screen_rect = ai_game.screen.get_rect()  # Get the dimensions of the screen.

        # Load the ship image and create a rect object for it.
        self.image = pygame.image.load('images/ship.bmp')  # Load the ship's image.
        self.rect = self.image.get_rect()  # Create a rect object for positioning.

        # Position the ship at the center bottom of the screen.
        self.rect.midbottom = self.screen_rect.midbottom  # Center the ship at the bottom.

        # Use a float for precise movement calculations.
        self.x = float(self.rect.x)  # Store the ship's horizontal position as a float.

        # Flags to manage the ship's movement.
        self.moving_right = False  # Flag for moving right.
        self.moving_left = False  # Flag for moving left.

    def update(self):
        """Update the ship's position based on movement flags."""
        # Adjust the ship's x-coordinate if movement is flagged.
        if self.moving_right and self.rect.right < self.screen_rect.right:  # Move right if within screen bounds.
            self.x += self.settings.ship_speed  # Increase x position by ship speed.
        if self.moving_left and self.rect.left > 0:  # Move left if within screen bounds.
            self.x -= self.settings.ship_speed  # Decrease x position by ship speed.

        # Update the rect position based on the float x value.
        self.rect.x = self.x  # Apply updated x position to the rect object.

    def blitme(self):
        """Draw the ship on the screen at its current position."""
        self.screen.blit(self.image, self.rect)  # Render the ship image at its rect position.

    def center_ship(self):
        """Center the ship on the screen after respawning."""
        self.rect.midbottom = self.screen_rect.midbottom  # Reposition the ship to the center bottom.
        self.x = float(self.rect.x)  # Update the float value to match the new position.
