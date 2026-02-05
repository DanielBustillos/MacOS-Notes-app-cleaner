#!/usr/bin/env python3
"""Script invoked by AppleScript: reads stdin and env, calls limpiar_notas.gemini.run()."""
import sys

from limpiar_notas.gemini import run

if __name__ == "__main__":
    note_content = sys.stdin.read()
    run(note_content)
    sys.exit(0)
