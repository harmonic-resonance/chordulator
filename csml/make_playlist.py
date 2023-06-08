import os
import click
import argparse
from bs4 import BeautifulSoup
from rich import print

@click.command()
@click.option('--playlist', prompt="playlist file", type=click.Path(exists=True))
@click.option('--output', '-o', default='output.html', help='Name of the output HTML file.')
def main(playlist, output):
    """Main function."""
    # Read the subset list file
    with open(playlist, 'r') as f:
        files = [line.strip() for line in f]
    print(files)

    # Get the titles of the HTML files
    files_with_titles = get_html_titles(files)
    print(files_with_titles)


    # Generate the HTML file
    generate_html(files_with_titles, output)


def get_html_titles(files):
    """Return a list of tuples containing file names and their corresponding titles."""
    titles = []
    for file in files:
        with open(file, 'r') as f:
            soup = BeautifulSoup(f, 'html.parser')
            title = soup.title.string if soup.title else 'No title'
            titles.append((file, title))
    return titles


def generate_html(files_with_titles, output):
    """Generate the HTML file."""
    with open(output, 'w') as f:
        f.write('<html>\n')
        f.write('<head>\n')
        f.write('<style>\n')
        f.write('iframe { width: 75%; height: 600px; }\n')
        f.write('nav { width: 25%; float: left; }\n')
        f.write('</style>\n')
        f.write('<script>\n')
        f.write('var urls = [' + ', '.join('"' + file + '"' for file, _ in files_with_titles) + '];\n')
        f.write('var index = 0;\n')
        f.write('function previous() { if (index > 0) { index--; update(); } }\n')
        f.write('function next() { if (index < urls.length - 1) { index++; update(); } }\n')
        f.write('function update() { document.getElementById("iframe").src = urls[index]; }\n')
        f.write('</script>\n')
        f.write('</head>\n')
        f.write('<body>\n')
        f.write('<nav>\n')
        f.write('<ul>\n')
        for i, (file, title) in enumerate(files_with_titles):
            f.write(f'<li><a href="{file}" target="iframe">{title}</a></li>\n')
        f.write('</ul>\n')
        f.write('<button onclick="previous()">Previous</button>\n')
        f.write('<button onclick="next()">Next</button>\n')
        f.write('</nav>\n')
        f.write('<iframe id="iframe" name="iframe"></iframe>\n')
        f.write('</body>\n')
        f.write('</html>\n')


if __name__ == "__main__":
    main()

