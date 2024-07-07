class BadUrlError(Exception):
    """Custom exception for URL errors."""

    pass


class MissingTokenError(Exception):
    """Custom exception for token errors."""

    pass


class WikipediaLimitError(Exception):
    """Custom exception for Wikipedia errors."""

    pass
