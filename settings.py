class Settings:
    """Class to manage all the settings for the Alien Invasion game."""

    def __init__(self):
        """Initialize the static settings for the game."""
        # Define screen dimensions
        self.screen_width = 1200  # Width of the game window.
        self.screen_height = 800  # Height of the game window.
        self.bg_color = (230, 230, 230)  # Background color of the game.

        # Ship settings
        self.ship_limit = 3  # Maximum number of ships a player can have.

        # Bullet settings
        self.bullet_width = 3  # Width of the bullets.
        self.bullet_height = 15  # Height of the bullets.
        self.bullet_color = (60, 60, 60)  # Color of the bullets.
        self.bullets_allowed = 3  # Maximum number of bullets on the screen at once.

        # Alien settings
        self.fleet_drop_speed = 10  # Speed at which aliens drop down the screen.

        # Speed-up settings
        self.speedup_scale = 1.1  # Scale factor for increasing game speed.
        self.score_scale = 1.5  # Scale factor for increasing alien score values.

        # Initialize dynamic settings that can change during the game.
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Set up the settings that will change throughout the gameplay."""
        self.ship_speed = 1.5  # Speed of the player's ship.
        self.bullet_speed = 3.0  # Speed of the bullets.
        self.alien_speed = 1.0  # Speed of the aliens.

        # Direction of the alien fleet: 1 means moving right, -1 means moving left.
        self.fleet_direction = 1  

        # Scoring for destroying aliens
        self.alien_points = 50  # Points awarded for each alien destroyed.

    def increase_speed(self):
        """Adjust speed settings and scoring values as the game progresses."""
        self.ship_speed *= self.speedup_scale  # Increase ship speed.
        self.bullet_speed *= self.speedup_scale  # Increase bullet speed.
        self.alien_speed *= self.speedup_scale  # Increase alien speed.

        # Update the point value for aliens.
        self.alien_points = int(self.alien_points * self.score_scale)  # Increase alien points.
