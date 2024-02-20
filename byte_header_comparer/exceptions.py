"""Custom exceptions defined for use in multip.py."""


class OnlyOneFileError(Exception):
    """Implements an error to raise when there only are one file to comparer byte headers."""
