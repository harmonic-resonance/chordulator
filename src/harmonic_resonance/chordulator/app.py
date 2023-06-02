"""
run the main app
"""
import click
from pathlib import Path
from rich import print, inspect
from .chordulator import generate_chord_sheet_html

@click.command()
@click.argument('csml_filename')
def run(csml_filename):
    csml_path = Path(csml_filename)
    
    # Make sure the csml file exists
    if not csml_path.exists():
        print(f"The file {csml_filename} does not exist.")
        return

    print(csml_filename)
    chord_sheet = csml_path.read_text()
    # Compute the output path
    output_file_path = csml_path.parent / 'html' / csml_path.stem
    output_file = output_file_path.with_suffix('.html')
    # Create the html subfolder if it doesn't exist
    output_file.parent.mkdir(parents=True, exist_ok=True)
    html_output = generate_chord_sheet_html(chord_sheet)
    output_file.write_text(html_output)
    print(output_file)

if __name__ == '__main__':
    run()
