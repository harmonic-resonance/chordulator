#!/usr/bin/env bash
for csml_file in *.csml; do
    chordulator "$csml_file"
done
