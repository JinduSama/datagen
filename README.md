# Synthetische Daten Generator

Dieses Projekt generiert synthetische deutsche Ausweisnummern und Steuer-IDs für Test- und Entwicklungszwecke. Alle generierten Nummern haben **gültige Prüfziffern** und entsprechen dem offiziellen Format, sind aber **keine echten Dokumente** und können nicht für illegale Zwecke verwendet werden.

## Warum synthetische Daten?

Bei der Entwicklung und beim Testen von Software, die mit Ausweisdaten oder Steuer-IDs arbeitet, benötigt man realistische Testdaten. Echte personenbezogene Daten dürfen aus Datenschutzgründen (DSGVO) nicht verwendet werden. Dieses Tool generiert Daten, die:

- Das korrekte Format haben
- Gültige Prüfziffern besitzen
- Alle offiziellen Strukturregeln einhalten
- Aber keiner echten Person zugeordnet sind

## Generierte Datentypen

### Deutsche Ausweisnummer (Personalausweis)

Die Seriennummer eines deutschen Personalausweises besteht aus:
- **9 alphanumerischen Zeichen** (Ziffern 0-9 und Buchstaben C, F, G, H, J, K, L, M, N, P, R, T, V, W, X, Y, Z)
- **1 Prüfziffer** (berechnet nach dem 7-3-1-Gewichtungsverfahren)

**Prüfziffern-Algorithmus:**
1. Jedes Zeichen erhält einen numerischen Wert (0-9 für Ziffern, A=10, B=11, ..., Z=35)
2. Die Werte werden abwechselnd mit den Gewichten 7, 3, 1 multipliziert
3. Die Summe wird modulo 10 genommen → das ist die Prüfziffer

### Deutsche Steuer-ID (Steuer-Identifikationsnummer / IdNr)

Die Steuer-ID besteht aus 11 Ziffern und unterliegt strengen Regeln:

**Strukturregeln für die ersten 10 Ziffern:**
- Die erste Ziffer darf **nicht 0** sein
- Genau **eine Ziffer muss 2- oder 3-mal** vorkommen
- Alle anderen Ziffern kommen **0- oder 1-mal** vor
- Bei 3-fachem Vorkommen dürfen die Ziffern **nicht direkt hintereinander** stehen

**Prüfziffern-Algorithmus (ISO 7064, MOD 11, 10):**
1. Starte mit `remainder = 10`
2. Für jede der 10 Ziffern:
   - `summe = (ziffer + remainder) mod 10`
   - Falls `summe = 0`, setze `summe = 10`
   - `remainder = (summe × 2) mod 11`
3. `prüfziffer = 11 - remainder`
4. Falls `prüfziffer = 10`, setze `prüfziffer = 0`

## Voraussetzungen

- [uv](https://github.com/astral-sh/uv) für das Paketmanagement.

## Verwendung

Du kannst das Skript mit `uv run` ausführen:

```bash
uv run python main.py -n 10 -f json
```

### Parameter

- `-n`, `--count`: Anzahl der zu generierenden Datensätze (Standard: 10).
- `-f`, `--format`: Ausgabeformat (`csv` oder `json`, Standard: `json`).
- `-o`, `--output`: Pfad zur Ausgabedatei (optional).

## Beispiel

```bash
uv run python main.py -n 100 -f csv -o daten.csv
```
