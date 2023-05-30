"""
chordulator
"""
from pychord import Chord

def generate_chord_sheet_html(chord_sheet):
    lines = chord_sheet.strip().split('\n')

    output = '<html>\n<head>\n<style>\n' \
             '.chordsheet { font-family: monospace; }\n' \
             '.line { page-break-inside: avoid; }\n' \
             '.chords, .lyrics { margin: 0; }\n' \
             '</style>\n</head>\n<body>\n'

    open_section = False
    open_line = False

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith('*'):
            if open_section:
                output += '</section>\n'
            section_class = line[1:].strip().lower().replace(' ', '-')
            output += f'<section class="{section_class}">\n'
            open_section = True
            open_line = False
        elif line.startswith('|'):
            if open_line:
                output += '</div>\n'
            output += '<div class="line">\n'
            output += f'<pre class="chords">{line[1:]}</pre>\n'
            open_line = True
        elif line.startswith('-'):
            if not open_line:
                output += '<div class="line">\n'
                open_line = True
            output += f'<pre class="lyrics">{line[1:]}</pre>\n'
        else:
            if open_line:
                output += '</div>\n'
                open_line = False
            output += '<div class="line">\n'
            output += f'<pre class="lyrics">{line}</pre>\n'
            open_line = True

    if open_section:
        output += '</section>\n'

    output += '</body>\n</html>'

    return output

