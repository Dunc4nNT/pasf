class DeckNotFoundError(Exception):
    """Raised when a deck isn't found in the database."""


class TagNotFoundError(Exception):
    """Raised when a tag isn't found in the database."""
