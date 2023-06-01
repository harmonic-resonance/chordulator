def generate_chord_sheet_html(chord_sheet):
    lines = chord_sheet.strip().split("\n")

    # Parse field statements
    fields = {}
    for line in lines:
        if line.startswith(":"):
            key, value = line[1:].split(":", 1)
            fields[key.strip()] = value.strip()

    title = fields.get("title", "Chord Sheet")

    output = f"""\
<html>
<head>
<title>{title}</title>
<style>
body {{ font-family: 'Fira Sans', sans-serif; }}
pre {{ font-family: 'Fira Mono', monospace; }}
.line {{ 
  page-break-inside: avoid;
  margin-top: .5em;
}}
.comment {{ font-style: italics }}
.chords, .lyrics {{ margin: 0; }}
.chords {{
  font-weight: bold;
}}
section {{
  margin-top: 2em;
}}
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
            output += f'<pre class="chords">{line[1:]}</pre>\n'
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
