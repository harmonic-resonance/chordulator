import re
from rich import print, inspect

CHORDS = {
    "M": [0, 4, 7],
    "6": [0, 4, 7, 9],
    "M7": [0, 4, 7, 11],
    "7": [0, 4, 7, 10],
    "9": [0, 4, 7, 10, 14],
    "11": [0, 4, 7, 10, 14, 17],
    "13": [0, 4, 7, 10, 14, 17, 21],
    "m": [0, 3, 7],
    "m7": [0, 3, 7, 10],
    "m9": [0, 3, 7, 10, 14],
    "m11": [0, 3, 7, 10, 14, 17],
    "m13": [0, 3, 7, 10, 14, 17, 21],
    "o": [0, 3, 6],
    "sus2": [0, 2, 7],
    "sus4": [0, 5, 7],
}


class ChordSheet:
    def __init__(self):
        self.title = ""
        self.performer = ""
        self.bpm = 120
        self.bpM = 4
        self.key = "C"
        self.sections = {}  # Each section contains a list of line groups

    def add_section(self, name):
        self.sections[name] = []

    def add_line_group(self, section_name, chords, lyrics):
        if section_name not in self.sections:
            self.add_section(section_name)
        self.sections[section_name].append({"chords": chords, "lyrics": lyrics})

    def parse_csml(self, csml):
        lines = csml.strip().split("\n")
        current_section = None
        pending_chords = None  # Store chords waiting for their lyrics

        for line in lines:
            line = line.strip()
            if line.startswith(":"):
                key, value = line[1:].split(":", 1)
                setattr(self, key.strip(), value)
            elif line.startswith("*"):
                current_section = line[2:].strip()
            elif current_section:
                if "|" in line:  # This is a chord line
                    pending_chords = self._process_chord_line(line[2:])
                elif line.startswith("-") and pending_chords is not None:
                    # This is a lyric line corresponding to the last seen chord line
                    lyrics = self._process_lyric_line(
                        line[2:], pending_chords["measure_positions"]
                    )
                    self.add_line_group(
                        current_section, pending_chords["chords"], lyrics
                    )
                    pending_chords = None

        # In case the last line is chords without corresponding lyrics
        if pending_chords is not None:
            self.add_line_group(current_section, pending_chords["chords"], [])

    def _process_chord_line(self, line):
        # Store the positions of the '|' characters
        measure_positions = [pos for pos, char in enumerate(line) if char == "|"]
        # Extract chords splitting by '|'
        chords = [measure for measure in re.split(r"\|+", line) if measure]
        chords = [self.parse_chord_line(chord) for chord in chords]
        return {"chords": chords, "measure_positions": measure_positions}

    def parse_chord_line(self, raw_chord_line):
        # Split the chord line into chord symbols, handling spaces and known
        # symbols '%' for repeat, 'x' for no chord.
        chord_symbols = raw_chord_line.split()

        # Filter out empty strings that may occur due to excessive spacing
        chord_symbols = list(filter(None, chord_symbols))

        # Process individual chord symbols
        parsed_chords = [self.parse_chord_symbol(symbol) for symbol in chord_symbols]

        return parsed_chords

    def parse_chord_symbol(self, symbol):
        # Special symbols handling
        if symbol == "%":
            return "repeat"
        elif symbol == "x":
            return "no_chord"

        # Parse the actual chord notation (root + quality/type)
        match = re.match(r"([A-G][#b]?)(.*)", symbol)

        if match:
            root = match.group(1)  # Root note, like 'A', 'A#', 'Bb', etc.
            type_string = match.group(2)  # Remaining string after root note

            # Validate the remaining string as a known chord type
            if type_string in CHORDS:
                chord_type = type_string
            else:
                # If not found in the dictionary, it could be an empty string
                # (just a root note chord) or an invalid/malformed chord
                # symbol. For this case, we'll default to a major chord 'M' or
                # return the symbol as invalid.
                chord_type = "M" if type_string == "" else None

            # Return the root and chord type if it's valid
            if chord_type:
                return (root, chord_type)

            # Handle the case for invalid chord types not in CHORDS You can
            # define your error handling here, such as printing an error
            # message, etc.  For the sake of this example, I'll just return the
            # original symbol for manual review.
            return f"Invalid chord: {symbol}"

        # If the symbol doesn't match a chord pattern (root note with optional #/b)
        # return it as-is
        return symbol

    def _process_lyric_line(self, lyric_line, measure_positions):
        lyrics = []
        current_pos = 0
        for pos in measure_positions:
            lyrics.append(lyric_line[current_pos:pos])
            current_pos = pos + 1

        # Add the remaining part of the lyric line if any
        if lyric_line:
            lyrics.append(lyric_line[current_pos:])

        return lyrics


# A function that reads CSML from a file and returns a populated ChordSheet object
def parse_csml_file_to_chordsheet(file_path):
    with open(file_path, "r") as file:
        csml_content = file.read()

    chordsheet = ChordSheet()
    chordsheet.parse_csml(csml_content)
    return chordsheet


def main():
    chord_sheet = parse_csml_file_to_chordsheet("./flip-flop-and-fly.csml")
    #  inspect(chord_sheet)
    print(chord_sheet.sections)


if __name__ == "__main__":
    main()
