"""
Main module for generating synthetic German identification data.

This module provides a command-line interface for generating synthetic German
ID numbers and tax IDs with various output formats.
"""

import argparse
import csv
import json
import sys
from typing import Any

from generator import generate_german_id, generate_german_tax_id


def generate_data(count: int) -> list[dict[str, str]]:
    """
    Generate synthetic German identification data.

    Args:
        count: Number of data records to generate.

    Returns:
        List of dictionaries containing 'ausweisnummer' (ID number) and
        'steuer_id' (tax ID) keys.

    Example:
        >>> data = generate_data(5)
        >>> len(data)
        5
        >>> all('ausweisnummer' in record for record in data)
        True
    """
    data = []
    for _ in range(count):
        data.append({"ausweisnummer": generate_german_id(), "steuer_id": generate_german_tax_id()})
    return data


def save_as_csv(data: list[dict[str, Any]], filename: str) -> None:
    """
    Save data to a CSV file.

    Args:
        data: List of dictionaries to save.
        filename: Path to the output CSV file.

    Note:
        If the data list is empty, the function returns without creating a file.
    """
    if not data:
        return

    keys = data[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)


def save_as_json(data: list[dict[str, Any]], filename: str) -> None:
    """
    Save data to a JSON file.

    Args:
        data: List of dictionaries to save.
        filename: Path to the output JSON file.

    Note:
        The JSON output is formatted with 4-space indentation and preserves
        non-ASCII characters (ensure_ascii=False).
    """
    with open(filename, "w", encoding="utf-8") as output_file:
        json.dump(data, output_file, indent=4, ensure_ascii=False)


def main() -> None:
    """
    Main entry point for the command-line interface.

    Parses command-line arguments and generates synthetic German identification
    data in the specified format (JSON or CSV), either to a file or stdout.
    """
    parser = argparse.ArgumentParser(
        description="Generiere synthetische deutsche Ausweisnummern und Steuer-IDs."
    )
    parser.add_argument(
        "-n",
        "--count",
        type=int,
        default=10,
        help="Anzahl der zu generierenden Datensätze (Standard: 10)",
    )
    parser.add_argument(
        "-f",
        "--format",
        choices=["csv", "json"],
        default="json",
        help="Ausgabeformat (Standard: json)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Ausgabedatei (optional, sonst wird auf der Konsole ausgegeben)",
    )

    args = parser.parse_args()

    # Validate count is positive
    if args.count <= 0:
        parser.error("Die Anzahl muss größer als 0 sein.")

    data = generate_data(args.count)

    # Output to file or stdout based on arguments
    if args.output:
        if args.format == "csv":
            save_as_csv(data, args.output)
        else:
            save_as_json(data, args.output)
        print(f"Daten erfolgreich in {args.output} gespeichert.")
    else:
        # Output to stdout
        if args.format == "json":
            print(json.dumps(data, indent=4, ensure_ascii=False))
        else:
            if data:
                keys = data[0].keys()
                writer = csv.DictWriter(sys.stdout, fieldnames=keys)
                writer.writeheader()
                writer.writerows(data)


if __name__ == "__main__":
    main()
