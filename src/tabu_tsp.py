# src/tabu_tsp.py

from __future__ import annotations

from typing import List, Tuple, Set
import random

from .tsp_utils import City, random_tour, tour_length, two_opt_swap


def tabu_search_tsp(
    cities: List[City],
    max_iterations: int = 20_000,
    tabu_tenure: int = 20,
    neighbourhood_size: int = 150,
    rng: random.Random | None = None,
) -> Tuple[List[int], float, List[float]]:
    """
    Solve TSP using Tabu Search with 2-opt neighbourhood.

    Parameters
    ----------
    cities : list of City
        TSP instance.
    max_iterations : int
        Maximum number of iterations.
    tabu_tenure : int
        Number of iterations a move remains tabu.
    neighbourhood_size : int
        Number of neighbour candidates sampled per iteration.
    rng : random.Random, optional
        Random generator.

    Returns
    -------
    best_tour : list of int
        Best tour found.
    best_length : float
        Length of best tour.
    history : list of float
        Best-so-far tour length at each iteration.
    """

    if rng is None:
        rng = random.Random()

    num_cities = len(cities)

    current_tour = random_tour(num_cities, rng)
    current_length = tour_length(current_tour, cities)

    best_tour = list(current_tour)
    best_length = current_length

    history: List[float] = [best_length]

    tabu_list: dict[tuple[int, int], int] = {}

    for iteration in range(max_iterations):

        best_candidate = None
        best_candidate_length = float("inf")
        best_move = None

        for _ in range(neighbourhood_size):
            i, k = sorted(rng.sample(range(num_cities), 2))
            candidate = two_opt_swap(current_tour, i, k)
            candidate_length = tour_length(candidate, cities)

            edge = (i, k)
            is_tabu = tabu_list.get(edge, 0) > iteration

            # Aspiration criterion
            if is_tabu and candidate_length >= best_length:
                continue

            if candidate_length < best_candidate_length:
                best_candidate = candidate
                best_candidate_length = candidate_length
                best_move = edge

        if best_candidate is None:
            break

        current_tour = best_candidate
        current_length = best_candidate_length

        tabu_list[best_move] = iteration + tabu_tenure

        if current_length < best_length:
            best_tour = list(current_tour)
            best_length = current_length

        history.append(best_length)

    return best_tour, best_length, history