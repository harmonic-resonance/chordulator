import re
from rich import print, inspect
import phimidi as pm
import itertools as itertools
import random as random

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
        self.root = "C4"
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

    def create_part(self):

        PROJECT = 'chordsheet_test'
        title = self.title
        bpm = int(self.bpm) # beats per minute
        bpM = int(self.bpM)  # beats per Measure
        root = pm.N.NOTES_BY_NAME[self.root]  # the root note of the key
        key = self.key

        part = pm.Part(PROJECT, title, bpm=bpm, root=root, key=key)
        M = bpM * part.ticks_per_beat  # ticks per Measure

        chords = pm.progressions.ii_V_i_i(root)
        chords = pm.progressions.i_vi_ii_V(root)

        piano = part.add_piano()
        vibes = part.add_vibes()
        bass = part.add_bass()
        strings = part.add_strings()

        choir = part.add_choir_swell()

        conga = pm.Conga(part)
        standard = pm.Standard(part)

        for section in self.sections:
            part.set_marker(f'{section=}', 0)
            for chord_num, (chord_name, chord) in enumerate(chords):
                chord2 = [note + 12 for note in chord]
                chord3 = [note + 12 for note in chord2]
                chord4 = [note + 12 for note in chord3]

                part.set_marker(f'{chord_name} - {chord}', 0)

                if chord_num in [0, 2]:
                    rhythm = pm.patterns.latin.bossa_nova
                if chord_num in [1, 3]:
                    rhythm = pm.patterns.latin.rhumba

                rhythm = pm.patterns.funky.billie_jean

                measures = 4
                for m in range(measures):
                    part.set_marker(f'{m + 1}', M)
                    #  if m == 0:
                        #  velocity_mod = 10 
                        #  #  conga.samba(2 * M, velocity_mod=-10)
                        #  standard.billie_jean(2 * M, velocity_mod=-10)
                    #  elif m == 2:
                        #  standard.billie_jean(2 * M, velocity_mod=-10)
                    #  else:
                        #  pass
                    standard.funky_drummer(M, velocity_mod=-10)

                    if chord_num == 3:
                        if m == measures - 1:
                            # last
                            bass.set_note(chord[1] - 12, M, velocity=90)
                        else:
                            bass.set_note(chord[2] - 12, M, velocity=70)
                    else:
                        if m == measures - 1:
                            # last
                            bass.set_note(chord[1] - 12, M, velocity=90)
                        else:
                            bass.set_note(chord[0] - 12, M, velocity=70)

                    if loop > 0:
                        if chord_num == 3:
                            # last
                            piano.set_notes(chord2, M, velocity=60)
                        else:
                            piano.set_notes(chord, M, velocity=60)
                    else:
                        piano.set_rest(M)



                if loop > 2:
                    strings.set_rest(3 * M)
                    strings.set_notes(chord2, M/2, velocity=20)
                    strings.set_notes(chord3, M/2, velocity=30)
                else:
                    strings.set_rest(4 * M)

                if loop > 1:
                    #  choir.set_rest(M)
                    #  choir.set_notes(chord, (measures - 1) * M, offset=M/8)
                    if chord_num == 3:
                        choir.set_rest(4 * M)
                        choir.set_volume(32, 4 * M)
                    else:
                        choir.set_notes(chord, measures  * M, offset=M/4)
                        choir.set_volume(32, 0)
                        choir.ramp_volume_up(2 * M)
                        choir.ramp_volume_down(2 * M)
                else:
                    choir.set_rest(4 * M)
                    choir.set_volume(32, 4 * M)




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
