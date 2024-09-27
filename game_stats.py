class GameStats:
    """Class to manage and track game statistics for the Alien Invasion game."""

    def __init__(self, ai_game):
        """Initialize the game's statistics."""
        self.settings = ai_game.settings  # Retrieve the game settings from the main game instance.
        self.reset_stats()  # Call the method to reset the statistics.

        # Set the initial state of the game to inactive.
        self.game_active = False  # Indicates whether the game is currently active.

        # Initialize the high score, which should persist across sessions.
        self.high_score = 0  # High score starts at zero.

    def reset_stats(self):
        """Set statistics that can change during the course of the game to their initial values."""
        self.ships_left = self.settings.ship_limit  # Set the number of remaining ships to the limit defined in settings.
        self.score = 0  # Reset the player's score to zero.
        self.level = 1  # Start the level at one.
