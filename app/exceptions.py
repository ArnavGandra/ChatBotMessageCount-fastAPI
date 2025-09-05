"""
Custom exceptions for domain logic.
"""

class LimitExceededException(Exception):
    """Raised when a user exceeds their message quota."""
    def __init__(self, wait_hours: int):
        self.wait_hours = wait_hours
