# src/run_tabu_example.py

from __future__ import annotations

from pathlib import Path
import random

from src.tsp_io import load_cities_from_csv
from src.tabu_tsp import tabu_search_tsp

DATA_PATH = Path("data") / "cities.csv"
OUTPUT_PATH = Path("results") / "routes" / "best_tabu_50.txt"


def main() -> None:
    cities = load_cities_from_csv(str(DATA_PATH))

    rng = random.Random(42)

    best_tour, best_length, history = tabu_search_tsp(
        cities=cities,
        max_iterations=20_000,
        tabu_tenure=25,
        neighbourhood_size=150,
        rng=rng,
    )

    print(f"[TABU] Best tour length (50 cities): {best_length:.2f}")
    print(f"[TABU] Iterations: {len(history)}")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("Best Tabu Search tour (indices):\n")
        f.write(",".join(map(str, best_tour)) + "\n")
        f.write(f"\nTour length: {best_length:.2f}\n")


if __name__ == "__main__":
    main()