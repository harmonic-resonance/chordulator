import os
import subprocess
from pathlib import Path
from slugify import slugify

for file in Path(".").rglob("*.doc"):
    print(f"Converting: {file}")
    new_file = Path(f"{slugify(file.stem)}.csml")
    command = ["pandoc", str(file), "-t", "plain", "-o", str(new_file)]
    subprocess.run(command, check=True)
    print(f"Converted to: {new_file}")

