"""Gemini classification logic: MOVE (junk) vs KEEP."""
import json
import os
import ssl
import sys
import urllib.error
import urllib.request

try:
    import certifi
except ImportError:
    sys.stderr.write("Install certifi for SSL: pip install certifi\n")
    sys.exit(1)


def run(note_content: str, note_date: str = "") -> None:
    """
    Reads prompt and API key from os.environ, classifies the note with Gemini, prints MOVE or KEEP (or ERROR: ... + MOVE).
    Used by run_worker.py with stdin and NOTE_DATE in the environment.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    prompt_path = os.environ.get("GEMINI_PROMPT_PATH")
    note_date = note_date or os.environ.get("NOTE_DATE", "")

    if not prompt_path or not os.path.isfile(prompt_path):
        print("ERROR: GEMINI_PROMPT_PATH not set or file does not exist")
        print("MOVE")
        sys.exit(0)

    if not note_content or len(note_content.strip()) < 10:
        print("MOVE")
        sys.exit(0)

    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt_text = (
            f.read()
            .replace("{{NOTE_DATE}}", note_date if note_date else "not set")
            .replace("{{NOTE_CONTENT}}", note_content[:4000])
        )

    model = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt_text}]}]}

    ssl_ctx = ssl.create_default_context(cafile=certifi.where())
    try:
        req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers=headers)
        with urllib.request.urlopen(req, timeout=30, context=ssl_ctx) as response:
            result = json.load(response)
            answer = result["candidates"][0]["content"]["parts"][0]["text"].strip().upper()
            if "MOVE" in answer:
                print("MOVE")
            else:
                print("KEEP")
    except Exception as e:
        err_msg = str(e).replace("\n", " ").replace("\r", " ")[:500]
        print("ERROR:", err_msg)
        print("MOVE")
