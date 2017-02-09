# -*- coding: utf-8 -*-


class Utils:
    """
    Utility class for common, often re-used functions.
    """

    @staticmethod
    def to_mega(size):
        mega = 1000 * 1000
        new_size = round(size / mega, 2)
        return new_size
