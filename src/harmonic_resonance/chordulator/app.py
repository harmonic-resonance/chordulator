"""
run the main app
"""
from .chordulator import Chordulator


def run() -> None:
    reply = Chordulator().run()
    print(reply)
