# src/tsp_utils.py

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Sequence
import math
import random


@dataclass
class City:
    """Represents a city with a name and 2D coordinates."""
    name: str
    x: float
    y: float


def euclidean_distance(a: City, b: City) -> float:
    """
    Compute the Euclidean distance between two cities.
    """
    return math.hypot(a.x - b.x, a.y - b.y)


def tour_length(tour: Sequence[int], cities: Sequence[City]) -> float:
    """
    Compute the total length of a closed TSP tour.
    """
    total = 0.0
    n = len(tour)

    for i in range(n):
        current_idx = tour[i]
        next_idx = tour[(i + 1) % n]
        total += euclidean_distance(
            cities[current_idx], cities[next_idx]
        )

    return total


def random_tour(num_cities: int, rng: random.Random | None = None) -> List[int]:
    """
    Generate a random tour (permutation of indices).
    """
    if rng is None:
        rng = random.Random()

    tour = list(range(num_cities))
    rng.shuffle(tour)
    return tour


def two_opt_swap(tour: Sequence[int], i: int, k: int) -> List[int]:
    """
    Perform a 2-opt swap between indices i and k.
    """
    new_tour = list(tour)
    new_tour[i:k + 1] = reversed(new_tour[i:k + 1])
    return new_tour