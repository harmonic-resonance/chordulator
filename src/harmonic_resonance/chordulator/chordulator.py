import pkg_resources
from rich import print, inspect
import re


def generate_lines(lines):
    output = '\n<div class="lines">\n'
    open_section = False
    open_line = False

    for line in lines:
        line = line.strip()
        if not line or line.startswith(":"):
            continue

        if line.startswith("*"):
            if open_section:
                output += "</section>\n"
            section_name = line[1:].strip()
            #  section_class = section_name.lower().replace(" ", "-")
            section_class = section_name.lower()
            output += f'<section class="{section_class}">\n'
            output += f"<h2>{section_name}</h2>\n"
            open_section = True
            open_line = False
        elif line.startswith("|"):
            if open_line:
                output += "</div>\n"
            output += '<div class="line">\n'
            chord_line = line[1:]
            chord_line_with_spans = re.sub(
                r"([A-G][#b]?\w*)",
                r'<span class="chord">\1</span>',
                chord_line,
            )
            output += f'<pre class="chords">{chord_line_with_spans}</pre>\n'
            open_line = True
        elif line.startswith("-"):
            if not open_line:
                output += '<div class="line">\n'
                open_line = True
            output += f'<pre class="lyrics">{line[1:]}</pre>\n'
        elif line.startswith("#"):
            output += f'<p class="comment">{line[1:]}</p>\n'
        else:
            if open_line:
                output += "</div>\n"
                open_line = False
            output += '<div class="line">\n'
            output += f'<pre class="lyrics">{line}</pre>\n'
            open_line = True

    if open_section:
        output += "</section>\n"

    output += "</div>\n"

    return output


def parse_csml_chord_table(csml):
    lines = csml.strip().split("\n")
    chord_table = {}
    current_section = None

    for line in lines:
        line = line.strip()
        if line.startswith("*"):
            current_section = line[1:].strip()
            chord_table[current_section] = []
        elif line.startswith("|"):
            bars = line[1:].split("|")
            chords = [bar.split() for bar in bars]
            chord_table[current_section].extend([chords])

    return chord_table


def generate_chord_table_html(chord_table):
    output = '<div class="chord-tables">\n'

    for section, chord_lines in chord_table.items():
        output += f'  <section class="chord-table-section">\n'
        output += f"    <h2>{section}</h2>\n"
        output += f"    <table>\n"
        for chord_line in chord_lines:
            output += "      <tr>\n"
            for bar in chord_line:
                output += f'        <td class="chord">{" ".join(bar)}</td>\n'
            output += "      </tr>\n"
        output += "    </table>\n"
        output += f"  </section>\n"

    output += "</div>\n"

    return output


def generate_web_page(chord_sheet):
    lines = chord_sheet.strip().split("\n")

    # Parse field statements
    fields = {}
    for line in lines:
        if line.startswith(":"):
            key, value = line[1:].split(":", 1)
            fields[key.strip()] = value.strip()

    title = fields.get("title", "Chord Sheet")

    css_path = pkg_resources.resource_filename(
        "harmonic_resonance.chordulator", "styles.css"
    )
    with open(css_path) as css_file:
        css_contents = css_file.read()

    output = f"""\
<html>
<head>
<title>{title}</title>
<style>
{css_contents}
</style>
</head>
<body>
"""

    # header
    output += f"<header>\n<h1>{title}</h1>\n"
    # Add fields (excluding title) as key-value list
    fields_list = [
        f"<li>{key}: {value}</li>" for key, value in fields.items() if key != "title"
    ]
    if fields_list:
        output += "<ul>"
        output += "\n".join(fields_list)
        output += "</ul>"

    output += "</header>\n"

    # lines
    output += generate_lines(lines)

    chord_table = parse_csml_chord_table(chord_sheet)
    print(chord_table)
    output += generate_chord_table_html(chord_table)

    output += """
<script>
var sectionIndex = 0;
var sections = document.getElementsByTagName('section');

window.addEventListener('message', function(event) {
  if (event.data.action === 'scrollSection') {
    sectionIndex += event.data.dir;
    if (sectionIndex < 0) sectionIndex = 0;
    if (sectionIndex > sections.length - 1) sectionIndex = sections.length - 1;
    sections[sectionIndex].scrollIntoView({behavior: "smooth", block: "center"});
  }
}, false);
</script>
</body>
</html>
"""

    return output
