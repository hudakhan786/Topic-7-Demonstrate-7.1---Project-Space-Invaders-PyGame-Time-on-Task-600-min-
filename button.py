import pygame.font  # Import the font module from pygame for text rendering.


class Button:
    """Class to create a button on the screen for the game."""

    def __init__(self, ai_game, msg):
        """Initialize button properties and settings."""
        self.screen = ai_game.screen  # Retrieve the screen from the main game instance.
        self.screen_rect = self.screen.get_rect()  # Get the rectangle representing the screen's dimensions.

        # Define the button's dimensions and visual properties.
        self.width, self.height = 200, 50  # Set the width and height of the button.
        self.button_color = (0, 255, 0)  # Set the button's background color to green.
        self.text_color = (255, 255, 255)  # Set the text color to white.
        self.font = pygame.font.SysFont(None, 48)  # Load a default font for rendering text.

        # Create a rectangle for the button and center it on the screen.
        self.rect = pygame.Rect(0, 0, self.width, self.height)  # Create the button's rectangle.
        self.rect.center = self.screen_rect.center  # Center the button's rectangle on the screen.

        # Prepare the button message; it only needs to be done once.
        self._prepare_message(msg)  # Call the method to create the button's message.

    def _prepare_message(self, msg):
        """Render the button message into an image and center it on the button."""
        # Create an image of the text message and set its background color.
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)  # Render the text message.
        self.msg_image_rect = self.msg_image.get_rect()  # Get the rectangle of the rendered message image.
        self.msg_image_rect.center = self.rect.center  # Center the message rectangle on the button.

    def draw_button(self):
        """Draw the button and its message onto the screen."""
        # Fill the button rectangle with the specified button color.
        self.screen.fill(self.button_color, self.rect)  # Draw the button background.
        self.screen.blit(self.msg_image, self.msg_image_rect)  # Draw the button message on top of the button.
