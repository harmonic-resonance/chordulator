import re
from rich import print, inspect
import harmonic_resonance.midiator as pm
import itertools as itertools
import random as random

class Section:
    def __init__(self, name):
        self.name = name
        self.line_groups = []


class ChordSheet:
    def __init__(self):
        self.title = ""
        self.performer = ""
        self.bpm = 120
        self.bpM = 4
        self.root = "C4"
        self.key = "C"
        self.sections = []  # Each section contains a list of line groups

    def parse_csml(self, csml):
        lines = csml.strip().split("\n")
        current_section = None
        pending_line_group = {'chords': [], 'lyrics': []}

        for line in lines:
            #  print(line)
            line = line.strip()
            if line.startswith(":"):
                key, value = line[1:].split(":", 1)
                setattr(self, key.strip(), value.strip())
            elif line.startswith("*"):
                section_name = line[2:].strip()
                current_section = Section(section_name)
                self.sections.append(current_section)
            elif line.startswith("|"):  # This is a chord line
                # TODO need to handle case where there is not a section defined yet
                chord_bars = self._process_chord_line(line[2:])
                pending_line_group = {'chords': [], 'lyrics': []}
                pending_line_group['chords'] = chord_bars
                current_section.line_groups.append(pending_line_group)
            elif line.startswith("-"):
                # This is a lyric line corresponding to the last seen chord line
                lyrics = self._process_lyric_line(
                    line[2:], pending_line_group['chords']["measure_positions"]
                )
                pending_line_group['lyrics'].append(lyrics)


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
            return ("%", "")
        elif symbol == "x":
            return ("x", "")

        # Parse the actual chord notation (root + quality/type)
        match = re.match(r"([A-G][#b]?)(.*)", symbol)

        if match:
            root = match.group(1)  # Root note, like 'A', 'A#', 'Bb', etc.
            type_string = match.group(2)  # Remaining string after root note

            # Validate the remaining string as a known chord type
            if type_string in pm.C.CHORDS:
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

    def create_part(self):
        """
        create a midi part from the chord sheet

        .. todo:: Add lyrics to midi part
        """

        PROJECT = 'chordsheet_test'
        title = self.title
        bpm = int(self.bpm) # beats per minute
        bpM = int(self.bpM)  # beats per Measure
        root = pm.N.NOTES_BY_NAME[self.root.strip()]  # the root note of the key
        key = self.key

        part = pm.Part(PROJECT, title, bpm=bpm, root=root, key=key)
        M = bpM * part.ticks_per_beat  # ticks per Measure

        piano = part.add_piano()

        #  conga = pm.Conga(part)
        standard = pm.Standard(part)

        for section in self.sections:
            print(section.name)
            part.set_marker(f'{section.name=}', 0)
            for line_num, line_group in enumerate(section.line_groups):
                print(line_num)
                part.set_marker(f'{line_num=}', 0)

                for measure in line_group['chords']['chords']:
                    
                    #  part.set_marker(f'{measure}', 0)
                    #  print(measure)
                    #  chord2 = [note + 12 for note in chord]
                    for chord in measure:
                        print(chord)
                        part.set_marker(f'{chord}', M)
                        chord_root_name, modifier = chord
                        if chord_root_name == 'x':
                            piano.set_rest(M)
                        elif chord_root_name == '%':
                            chord = last_chord
                            piano.set_notes(chord, M, velocity=60)
                        else:
                            chord_root_name += '3'
                            chord_root = pm.N.NOTES_BY_NAME[chord_root_name.strip()]
                            chord = pm.get_chord_notes(chord_root, modifier)
                            piano.set_notes(chord, M, velocity=60)
                            last_chord = chord

                    patterns = standard.patterns["bille_jean"]
                    standard.set_patterns(patterns, M, velocity_mod=-10)


        return part


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
    for section in chord_sheet.sections:
        print(section.name)
        print(section.line_groups)

    part = chord_sheet.create_part()
    part.save()
    part.play()


if __name__ == "__main__":
    main()
