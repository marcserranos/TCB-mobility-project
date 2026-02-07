import random

# This class provides utility functions for data loading, ID generation, PDF creation, and email sending.
class Utilities:
    # Public methods (+)
    
    # We decided to try and use @staticmethods, as these methods do not require any instance-specific data.
    # In the case of Utility funcions, we won't need to create an instance of Utilities to use them.

    @staticmethod
    def generate_random_id() -> str:
        """Generates a random 14-character ID as a string."""
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        # Compact form of generating a random string from the specified characters
        # The probability of collision is very low for our use case, thus we won't check for duplicates here.
        return ''.join(random.choice(chars) for _ in range(14))

    @staticmethod
    def choose_random_id(): pass
    
    @staticmethod
    def create_pdf(): pass
    
    @staticmethod
    def send_mail(): pass