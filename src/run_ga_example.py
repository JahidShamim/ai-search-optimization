# src/run_ga_example.py

from __future__ import annotations

from pathlib import Path
import random

from src.tsp_io import load_cities_from_csv
from src.ga_tsp import genetic_algorithm_tsp

DATA_PATH = Path("data") / "cities.csv"
OUTPUT_PATH = Path("results") / "routes" / "best_ga_50.txt"


def main() -> None:
    cities = load_cities_from_csv(str(DATA_PATH))

    rng = random.Random(42)

    best_tour, best_length, history = genetic_algorithm_tsp(
        cities=cities,
        population_size=120,
        generations=500,
        tournament_size=5,
        mutation_rate=0.02,
        elite_size=2,
        rng=rng,
    )

    print(f"[GA] Best tour length (50 cities): {best_length:.2f}")
    print(f"[GA] Generations: {len(history)}")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("Best Genetic Algorithm tour (indices):\n")
        f.write(",".join(map(str, best_tour)) + "\n")
        f.write(f"\nTour length: {best_length:.2f}\n")


if __name__ == "__main__":
    main()