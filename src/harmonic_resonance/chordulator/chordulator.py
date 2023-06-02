import pkg_resources
import re

def generate_chord_sheet_html(chord_sheet):
    lines = chord_sheet.strip().split("\n")

    # Parse field statements
    fields = {}
    for line in lines:
        if line.startswith(":"):
            key, value = line[1:].split(":", 1)
            fields[key.strip()] = value.strip()

    title = fields.get("title", "Chord Sheet")

    css_path = pkg_resources.resource_filename("harmonic_resonance.chordulator", "styles.css")
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
<h1>{title}</h1>
"""

    # Add fields (excluding title) as key-value list
    fields_list = [
        f"<li>{key}: {value}</li>" for key, value in fields.items() if key != "title"
    ]
    if fields_list:
        output += "<ul>"
        output += "\n".join(fields_list)
        output += "</ul>"

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
            section_class = section_name.lower().replace(" ", "-")
            output += f'<section class="{section_class}">\n'
            output += f'<h2>{section_name}</h2>\n'
            open_section = True
            open_line = False
        elif line.startswith("|"):
            if open_line:
                output += "</div>\n"
            output += '<div class="line">\n'
            chord_line = line[1:]
            chord_line_with_spans = re.sub(r"([A-G][#b]?(?:sus|maj|min|dim|aug)?\d?(?:\/[A-G][#b]?)?)", r'<span class="chord">\1</span>', chord_line)
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

    output += "</body>\n</html>"

    return output

