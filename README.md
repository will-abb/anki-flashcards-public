# Anki Flashcards Generator

This project includes a Python script (`import_cards.py`) that generates Anki flashcard decks from YAML files. These decks are intended to assist with studying various concepts, with each flashcard representing a term and its definition from the provided YAML files.

## Prerequisites

- Python 3.x
- Anki installed on your local machine
- The `genanki` Python package for generating Anki decks programmatically
- The `PyYAML` Python package for parsing YAML files

## YAML File Format

Each YAML file is structured with key-value pairs corresponding to flashcard terms and their definitions, allowing for an organized and structured way to compile study material.

```yaml
"Term1": "Definition1"
"Term2": "Definition2"
...
```

## Current Files Samples

- `ebs_volumes.yaml`: Flashcards for EBS volumes.
- `ec2_instances.yaml`: Flashcards for EC2 instances.
- `iam.yaml`: Flashcards for IAM concepts.

## Script Functionality

The `import_cards.py` script automates the creation of Anki decks. It takes a YAML file as input and generates a deck with a specified name. The script:

- Parses the YAML file to read the term-definition pairs.
- Generates a unique identifier for both the model (card style) and the deck.
- Creates a new Anki deck with the provided deck name.
- For each term-definition pair, it creates a flashcard and adds it to the deck.
- Exports the generated deck into an `.apkg` file suitable for import into Anki.

## Usage

Run the script from the command line, providing the path to the YAML file containing your study material and the desired name for your Anki deck.

```shell
python import_cards.py <path_to_yaml_file> "<deck_name>"
```

Example command:

```shell
python import_cards.py iam.yaml "AWS IAM Essentials"
```

Executing the above command will produce an Anki deck titled "AWS IAM Essentials" using the definitions in `iam.yaml`.
