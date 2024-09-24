import argparse
import random
import genanki
import yaml
import os

# Command-line argument parsing
parser = argparse.ArgumentParser(
    description="Generate Anki flashcards from a YAML file."
)
parser.add_argument(
    "--file",
    required=True,
    help="Path to the YAML file containing terms and definitions.",
)
parser.add_argument(
    "--model_type",
    required=True,
    choices=["cloze", "basic"],
    help="The model type to use for the cards (cloze or basic).",
)
parser.add_argument(
    "--output",
    required=True,
    help="Output directory where the Anki package will be saved.",
)
parser.add_argument(
    "--deck_name", required=True, help="The name of the Anki deck to be created."
)
args = parser.parse_args()

# Read YAML file
with open(args.file) as f:
    data = yaml.safe_load(f)

# Function to generate a random ID
def generate_random_id():
    return random.randint(1000000000, 9999999999)


# Define the CSS for card styling
my_css = """
.card {
  font-family: Arial, sans-serif;
  font-size: 20px;
  text-align: left;
  color: #DDDDDD; /* Lighter text for dark mode */
  background-color: #333333; /* Dark background for dark mode */
  padding: 10px;
  border-radius: 8px; /* Optional: rounded corners */
}

.code {
  font-family: 'Courier New', monospace;
  background-color: transparent; /* Removing the grayish background */
  border-left: 3px solid #666666; /* Subtle border for dark mode */
  padding: 2px 10px;
  display: block;
  margin: 5px 0;
  white-space: pre-wrap;
}

.example_keyword {
  font-weight: bold;
  color: #5599FF; /* A color that stands out in dark mode */
  display: block; /* Ensure 'Example:' starts on a new line */
  margin-bottom: 5px;
}

/* Additional styling for better dark mode support */
body {
  background-color: #333333; /* Match card background for seamless integration */
}
"""

# Cloze model setup with random ID and custom CSS
cloze_model = genanki.Model(
    generate_random_id(),
    "Cloze Model",
    fields=[{"name": "Text"}],
    templates=[
        {
            "name": "Cloze",
            "qfmt": "{{cloze:Text}}",
            "afmt": "{{cloze:Text}}",
        },
    ],
    model_type=genanki.Model.CLOZE,
    css=my_css,  # Set the CSS for the model
)

# Basic model setup with random ID and custom CSS
basic_model = genanki.Model(
    generate_random_id(),
    "Basic Model",
    fields=[{"name": "Question"}, {"name": "Answer"}],
    templates=[
        {
            "name": "Card 1",
            "qfmt": "{{Question}}",
            "afmt": '{{FrontSide}}<hr id="answer">{{Answer}}',
        },
    ],
    css=my_css,  # Set the CSS for the model
)

# Function to create cloze deletion note with enhanced formatting
def create_cloze_note(term, definition):
    # Escape only the merge symbol '<<' to prevent it from being interpreted as HTML
    definition_escaped = definition.replace("<<", "&lt;&lt;")

    # Style 'definition:' keyword with red color
    definition_formatted = definition_escaped.replace(
        "definition:", "<span style='color:red;'>definition:</span>"
    )

    # Check if 'Example:' exists and style it
    if "Example:" in definition_formatted:
        parts = definition_formatted.split("Example:")
        definition_formatted = (
            parts[0]
            + "<div class='example_keyword'>Example:</div><div class='code'>"
            + parts[1].strip().replace("\n", "<br>")
            + "</div>"
        )
    else:
        definition_formatted = definition_formatted.replace("\n", "<br>")

    cloze_text = f"{term} {{c1::{definition_formatted}}}"
    return genanki.Note(
        model=cloze_model,
        fields=[cloze_text],
    )


# Function to create basic note with enhanced formatting
def create_basic_note(term, definition):
    # Escape only the merge symbol '<<' to prevent it from being interpreted as HTML
    definition_escaped = definition.replace("<<", "&lt;&lt;")

    # Identify and style 'definition' keyword
    definition_formatted = definition_escaped.replace(
        "definition:", "<span style='color:red;'>definition:</span>"
    )

    # Check if 'Example:' exists and style it
    if "Example:" in definition_formatted:
        parts = definition_formatted.split("Example:")
        definition_formatted = (
            parts[0]
            + "<div class='example_keyword'>Example:</div><div class='code'>"
            + parts[1].strip().replace("\n", "<br>")
            + "</div>"
        )
    else:
        definition_formatted = definition_formatted.replace("\n", "<br>")

    return genanki.Note(
        model=basic_model,
        fields=[term, definition_formatted],
    )


# Create deck with a dynamic name based on the command-line argument
my_deck = genanki.Deck(generate_random_id(), args.deck_name)

# Decide which function to use for creating cards based on model type
note_creator = create_cloze_note if args.model_type == "cloze" else create_basic_note

# Create Anki cards
for term, definition in data.items():
    my_note = note_creator(term, definition)
    my_deck.add_note(my_note)

# Generate Anki package (.apkg) with a dynamic file name based on the command-line argument
output_path = os.path.join(args.output, f"{args.deck_name.replace(' ', '_')}.apkg")
genanki.Package(my_deck).write_to_file(output_path)

print(f"Anki deck with {args.model_type} model has been generated at '{output_path}'.")
