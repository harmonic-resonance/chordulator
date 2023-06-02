#!/usr/bin/env bash
for file in html/*.html; do
    open "$file"
    sleep 2
done
