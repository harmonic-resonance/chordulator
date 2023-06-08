import os
import click
from bs4 import BeautifulSoup
from jinja2 import Environment, PackageLoader


@click.command()
@click.option("--playlist", "-p", type=click.Path(exists=True))
@click.option(
    "--output", "-o", default="output.html", help="Name of the output HTML file."
)
def main(playlist, output):
    """Main function."""
    # Read the subset list file
    with open(playlist, "r") as f:
        files = [line.strip() for line in f]

    # Get the titles of the HTML files
    files_with_titles = get_html_titles(files)

    # Generate the HTML file
    generate_html(files_with_titles, output)


def get_html_titles(files):
    """Return a list of tuples containing file names and their corresponding titles."""
    titles = []
    for file in files:
        with open(file, "r") as f:
            soup = BeautifulSoup(f, "html.parser")
            title = soup.title.string if soup.title else "No title"
            titles.append((file, title))
    return titles


def generate_html(files_with_titles, output):
    """Generate the HTML file."""
    env = Environment(
        loader=PackageLoader("harmonic_resonance.chordulator", "templates")
    )
    template = env.get_template("playlist.j2")
    with open(output, "w") as f:
        f.write(template.render(files_with_titles=files_with_titles))


if __name__ == "__main__":
    main()
