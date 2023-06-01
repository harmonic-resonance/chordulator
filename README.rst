chordulator
===========

The Chordulator is a utility for generating HTML chord sheets from text-based chord sheets.

Features
--------

.. todo:: TODO: insert features

Installation
------------

You can install **chordulator** using pip:

.. code-block:: bash

   pip install harmonic-resonance-chordulator

Usage
-----

After installation, you can use the ``chordulator`` command to translate a CSML file to HTML.

.. code-block:: bash

   chordulator <filename>.csml

**chordulator** will ``<filename>.html`` to the same folder.

To use the **chordulator**, pass a chord sheet as input to the `generate_chord_sheet_html` function. The chord sheet should be in a specific format, which includes chords, lyrics, and optional field statements.

Dependencies
------------

**chordulator** depends on the following Python packages:

.. todo:: TODO: read from pyproject.toml 
   pychord


Writing Chord Sheet Markup Language
----------------------------------

Chord sheets can be written using a simple markup language. The format consists of sections, chords, and lyrics. Additionally, field statements can be used to provide metadata for the chord sheet.

Sections
~~~~~~~~

Sections are denoted by starting a line with an asterisk `*`, followed by the section name. For example:

.. code-block:: text

   * Verse

Chords
~~~~~~

Chords are represented by starting a line with a vertical bar `|`, followed by the chord progression. For example:

.. code-block:: text

   | C       G     Am
   | F       C     G

Lyrics
~~~~~~

Lyrics are represented by starting a line with a hyphen `-`, followed by the lyrics. For example:

.. code-block:: text

   - This is the start
   - Of a beautiful song

Field Statements
~~~~~~~~~~~~~~~~

Field statements are used to provide metadata for the chord sheet. They are denoted by starting a line with a colon `:`, followed by the field name and value separated by a colon `:`. For example:

.. code-block:: text

   :title: My Song
   :performer: John Doe
   :key: C

The available field statements are:

- `title`: The title of the chord sheet.
- `performer`: The performer of the song.
- `capo`: The fret number of the capo (optional).
- `key`: The key of the song (optional).

Example Chord Sheet
~~~~~~~~~~~~~~~~~~~

An example chord sheet:

.. code-block:: text

   :title: My Song
   :performer: John Doe

   * Verse
   | C           G     Am
   - This is the start
   | F           C     G
   - Of a beautiful song

   * Chorus
   | Am          F     C
   - Sing it loud
   - Sing it proud

This will generate an HTML chord sheet with the specified sections, chords, and lyrics.

Dependencies
------------

The Chordulator requires the following dependencies:

- `Fira Sans` and `Fira Mono` fonts for styling the HTML output.

License
-------

The Chordulator is licensed under the MIT License.


