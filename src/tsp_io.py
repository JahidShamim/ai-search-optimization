# src/tsp_io.py

from __future__ import annotations

from typing import List
import csv

from src.tsp_utils import City


def load_cities_from_csv(path: str) -> List[City]:
    """
    Load cities from a CSV file with columns: City, X, Y.

    Parameters
    ----------
    path : str
        Path to the CSV file.

    Returns
    -------
    list of City
        The list of cities.
    """
    cities: List[City] = []

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            cities.append(
                City(
                    name=row["City"],
                    x=float(row["X"]),
                    y=float(row["Y"]),
                )
            )

    return cities