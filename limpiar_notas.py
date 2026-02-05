#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys

from limpiar_notas.config import get_paths, load_and_validate

parser = argparse.ArgumentParser(description="Clean a Notes folder using Gemini (MOVE = junk, KEEP = keep).")
parser.add_argument(
    "folder",
    nargs="?",
    help="Name of the folder in the Notes app to process (overrides NOTES_FOLDER in .env)",
)
args = parser.parse_args()

load_and_validate(folder_override=args.folder)
paths = get_paths()

os.environ["GEMINI_WORKER_PATH"] = str(paths["run_worker_path"])
os.environ["GEMINI_PROMPT_PATH"] = str(paths["prompt_path"])

print("--- CLEANUP: AGGRESSIVE ON ORPHAN LINKS ---")
print(f"Folder: {paths['source_folder']}")
print("Criteria: bare Google Docs/Drive links → MOVE.")
print("----------------------------------------------")

os.environ["SOURCE_FOLDER"] = paths["source_folder"]
os.environ["TARGET_FOLDER"] = paths["target_folder"]
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY", "")
os.environ["GEMINI_MODEL"] = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

result = subprocess.run(
    ["osascript", str(paths["script_dir"] / "notes_cleaner.applescript")],
    env=os.environ,
)
sys.exit(result.returncode)
