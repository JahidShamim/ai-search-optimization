# src/experiments.py

from __future__ import annotations

from typing import Callable, Dict, List, Tuple
from pathlib import Path
import random
import time
import csv

from src.tsp_utils import City
from src.tsp_io import load_cities_from_csv
from src.tabu_tsp import tabu_search_tsp
from src.ga_tsp import genetic_algorithm_tsp


Result = Tuple[float, float]  # (best_length, runtime)


def run_multiple(
    solver: Callable[..., Tuple[List[int], float, List[float]]],
    cities: List[City],
    runs: int,
    base_seed: int,
    **kwargs,
) -> List[Result]:
    """
    Run a TSP solver multiple times with different random seeds.

    Parameters
    ----------
    solver : callable
        TSP solver function.
    cities : list of City
        TSP instance.
    runs : int
        Number of independent runs.
    base_seed : int
        Base random seed.
    kwargs :
        Additional solver parameters.

    Returns
    -------
    list of (best_length, runtime)
    """
    results: List[Result] = []

    for i in range(runs):
        rng = random.Random(base_seed + i)

        start = time.perf_counter()
        _, best_length, _ = solver(cities=cities, rng=rng, **kwargs)
        end = time.perf_counter()

        runtime = end - start
        results.append((best_length, runtime))

    return results


def compute_stats(results: List[Result]) -> Dict[str, float]:
    """
    Compute mean and standard deviation for length and runtime.
    """
    lengths = [r[0] for r in results]
    times = [r[1] for r in results]

    mean_len = sum(lengths) / len(lengths)
    mean_time = sum(times) / len(times)

    std_len = (sum((x - mean_len) ** 2 for x in lengths) / len(lengths)) ** 0.5
    std_time = (sum((t - mean_time) ** 2 for t in times) / len(times)) ** 0.5

    return {
        "mean_length": mean_len,
        "std_length": std_len,
        "mean_time": mean_time,
        "std_time": std_time,
    }


def main() -> None:
    """
    Full experimental pipeline:

    - City sizes: 10, 20, 30, 40, 50
    - Runs per size: 30
    - Algorithms: Tabu, GA
    - Output: CSV for each algorithm
    """
    data_path = Path("data") / "cities.csv"
    output_dir = Path("results") / "metrics"
    output_dir.mkdir(parents=True, exist_ok=True)

    all_cities = load_cities_from_csv(str(data_path))
    sizes = [10, 20, 30, 40, 50]
    runs = 30
    base_seed = 100

    algorithms = {
        "TabuSearch": lambda **kw: tabu_search_tsp(
            max_iterations=20_000,
            tabu_tenure=25,
            neighbourhood_size=150,
            **kw,
        ),
        "GeneticAlgorithm": lambda **kw: genetic_algorithm_tsp(
            population_size=120,
            generations=500,
            tournament_size=5,
            mutation_rate=0.02,
            elite_size=2,
            **kw,
        ),
    }

    for name, solver in algorithms.items():
        csv_path = output_dir / f"{name}_results.csv"

        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                ["Cities", "MeanLength", "StdLength", "MeanTime", "StdTime"]
            )

            for n in sizes:
                rng = random.Random(999)
                cities_subset = rng.sample(all_cities, n)

                print(f"Running {name} on {n} cities...")

                results = run_multiple(
                    solver=solver,
                    cities=cities_subset,
                    runs=runs,
                    base_seed=base_seed,
                )

                stats = compute_stats(results)

                writer.writerow([
                    n,
                    round(stats["mean_length"], 3),
                    round(stats["std_length"], 3),
                    round(stats["mean_time"], 4),
                    round(stats["std_time"], 4),
                ])

        print(f"Saved: {csv_path}")


if __name__ == "__main__":
    main()