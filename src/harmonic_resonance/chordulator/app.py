"""
run the main app
"""
import click
from pathlib import Path
from rich import print, inspect
from .chordulator import generate_chord_sheet_html

@click.command()
@click.argument('input_path')
#  @click.argument('output_file', type=click.File('w'))
def run(input_path):
    input_file = Path(input_path)
    inspect(input_path)
    inspect(input_file)
    chord_sheet = input_file.read_text()
    #  output_path = str(input_file)
    #  click.echo(output_path)
    output_file = input_file.with_suffix('.html')
    html_output = generate_chord_sheet_html(chord_sheet)
    output_file.write_text(html_output)

if __name__ == '__main__':
    run()
