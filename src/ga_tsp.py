# src/ga_tsp.py
# imported all required libraries
from __future__ import annotations

from typing import List, Tuple
import random

from .tsp_utils import City, random_tour, tour_length, two_opt_swap

# tournament selection function
def tournament_selection(
    population: List[List[int]],
    fitness: List[float],
    k: int,
    rng: random.Random,
) -> List[int]:
    """
    Selecting the best individual among k random ones.
    """
    selected_indices = rng.sample(range(len(population)), k)
    best_idx = min(selected_indices, key=lambda i: fitness[i])
    return population[best_idx]


def ordered_crossover(
    parent1: List[int],
    parent2: List[int],
    rng: random.Random,
) -> List[int]:
    """
    Ordered Crossover (OX) for TSP.
    """
    n = len(parent1)
    a, b = sorted(rng.sample(range(n), 2))

    child = [-1] * n
    child[a:b + 1] = parent1[a:b + 1]

    pos = (b + 1) % n
    for gene in parent2:
        if gene not in child:
            child[pos] = gene
            pos = (pos + 1) % n

    return child


def swap_mutation(
    individual: List[int],
    mutation_rate: float,
    rng: random.Random,
) -> None:
    """
    Swap mutation: exchange two cities with some probability.
    """
    if rng.random() < mutation_rate:
        i, j = rng.sample(range(len(individual)), 2)
        individual[i], individual[j] = individual[j], individual[i]


def genetic_algorithm_tsp(
    cities: List[City],
    population_size: int = 100,
    generations: int = 400,
    tournament_size: int = 5,
    mutation_rate: float = 0.02,
    elite_size: int = 2,
    rng: random.Random | None = None,
) -> Tuple[List[int], float, List[float]]:
    """
    Solve TSP using a Genetic Algorithm.

    Returns:
        best_tour, best_length, history
    """

    if rng is None:
        rng = random.Random()

    num_cities = len(cities)

    # --- Initial Population ---
    population = [
        random_tour(num_cities, rng)
        for _ in range(population_size)
    ]

    history: List[float] = []

    for generation in range(generations):

        fitness = [
            tour_length(individual, cities)
            for individual in population
        ]

        best_idx = min(range(population_size), key=lambda i: fitness[i])
        best_length = fitness[best_idx]
        history.append(best_length)

        new_population: List[List[int]] = []

        # --- Elitism ---
        elite_indices = sorted(
            range(population_size),
            key=lambda i: fitness[i]
        )[:elite_size]

        for idx in elite_indices:
            new_population.append(list(population[idx]))

        # --- Create Rest of New Population ---
        while len(new_population) < population_size:

            parent1 = tournament_selection(
                population, fitness, tournament_size, rng
            )
            parent2 = tournament_selection(
                population, fitness, tournament_size, rng
            )

            child = ordered_crossover(parent1, parent2, rng)

            swap_mutation(child, mutation_rate, rng)

            new_population.append(child)

        population = new_population

    # --- Final Best Solution ---
    final_fitness = [
        tour_length(individual, cities)
        for individual in population
    ]
    best_idx = min(range(population_size), key=lambda i: final_fitness[i])

    best_tour = population[best_idx]
    best_length = final_fitness[best_idx]

    return best_tour, best_length, history