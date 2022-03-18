from datetime import timedelta
from statistics import fmean

import numpy as np


class StatsCalculator:
    """Calculate average time of flight and percentile."""

    def __init__(self):
        self.array = []
        self.percentile = None
        self.average = None

    def calculate(self, percentile: int):
        """
        Calculate average value and percentile.
        :param percentile: percentile to compute
        """
        self.average = fmean(self.array)
        self.percentile = np.percentile(self.array, percentile)

    def get_results(self) -> tuple:
        """Get calculated results."""
        return timedelta(seconds=self.average), timedelta(seconds=self.percentile)

    def add(self, duration: float):
        """Fill array."""
        self.array.append(duration)