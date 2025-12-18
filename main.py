import argparse
import csv
import json
import sys
from generator import generate_german_id, generate_german_tax_id

def generate_data(count):
    data = []
    for _ in range(count):
        data.append({
            "ausweisnummer": generate_german_id(),
            "steuer_id": generate_german_tax_id()
        })
    return data

def save_as_csv(data, filename):
    if not data:
        return
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

def save_as_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as output_file:
        json.dump(data, output_file, indent=4, ensure_ascii=False)

def main():
    parser = argparse.ArgumentParser(description="Generiere synthetische deutsche Ausweisnummern und Steuer-IDs.")
    parser.add_argument("-n", "--count", type=int, default=10, help="Anzahl der zu generierenden Datensätze (Standard: 10)")
    parser.add_argument("-f", "--format", choices=["csv", "json"], default="json", help="Ausgabeformat (Standard: json)")
    parser.add_argument("-o", "--output", type=str, help="Ausgabedatei (optional, sonst wird auf der Konsole ausgegeben)")

    args = parser.parse_args()

    data = generate_data(args.count)

    if args.output:
        if args.format == "csv":
            save_as_csv(data, args.output)
        else:
            save_as_json(data, args.output)
        print(f"Daten erfolgreich in {args.output} gespeichert.")
    else:
        if args.format == "json":
            print(json.dumps(data, indent=4, ensure_ascii=False))
        else:
            # Print CSV to stdout
            keys = data[0].keys()
            writer = csv.DictWriter(sys.stdout, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)

if __name__ == "__main__":
    main()
