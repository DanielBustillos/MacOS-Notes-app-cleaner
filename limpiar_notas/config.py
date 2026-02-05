"""Load .env, validation, and project paths."""
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Project root (directory containing the limpiar_notas package)
SCRIPT_DIR = Path(__file__).resolve().parent.parent


def load_and_validate(folder_override: str | None = None) -> None:
    """Ensure .env exists, load it, validate GEMINI_API_KEY. SOURCE folder: from folder_override or NOTES_FOLDER in .env. Exits with 1 on failure."""
    if not (SCRIPT_DIR / ".env").exists():
        print("ERROR: .env not found. Copy .env.example to .env and set GEMINI_API_KEY (and optionally NOTES_FOLDER).")
        sys.exit(1)

    load_dotenv(SCRIPT_DIR / ".env")

    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key or api_key in ("PASTE_YOUR_API_KEY_HERE", "PEGA_TU_API_KEY_AQUI"):
        print("ERROR: Set GEMINI_API_KEY in .env")
        sys.exit(1)

    if folder_override:
        os.environ["NOTES_FOLDER"] = folder_override
    else:
        folder = os.getenv("NOTES_FOLDER") or os.getenv("CARPETA_ORIGEN", "")
        if not folder:
            print("ERROR: Pass the folder as an argument (e.g. python limpiar_notas.py MyFolder) or set NOTES_FOLDER in .env")
            sys.exit(1)
        os.environ["NOTES_FOLDER"] = folder


def get_paths() -> dict:
    """After load_and_validate(), returns script_dir, prompt_path, run_worker_path, source_folder, target_folder."""
    source_folder = os.getenv("NOTES_FOLDER", "")
    target_folder = f"{source_folder}_to_delete"

    return {
        "script_dir": SCRIPT_DIR,
        "prompt_path": SCRIPT_DIR / "prompt.txt",
        "run_worker_path": SCRIPT_DIR / "run_worker.py",
        "source_folder": source_folder,
        "target_folder": target_folder,
    }
