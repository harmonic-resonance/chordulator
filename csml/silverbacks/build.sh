#!/usr/bin/env bash
for file in *.csml; do
  chordulator "$file"
done

playlister -p _playlist.txt -o index.html
open index.html
