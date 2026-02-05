# MacOS Notes app cleaner

**Clean up your macOS Notes app** using Google Gemini to classify notes: keep what matters, move junk (orphan links, copy-paste, old checklists) into a review folder in Notes.

macOS · Python 3 · [Gemini API](https://aistudio.google.com/apikey)

---

## What it does

- Reads all notes from **one folder** you choose in the Notes app.
- For each note: **attachments → keep**. No attachments → sends the text to Gemini.
- Gemini returns **MOVE** (junk) or **KEEP** (keep).
- Notes marked **MOVE** are moved into a `<folder>_to_delete` subfolder in Notes so you can review or delete later.

Default behavior: orphan links (Google Docs, Drive, etc.), generic copy-paste, and old meeting notes get **MOVE**; personal context, sensitive data, and your own ideas get **KEEP**.

---

## Quick start

```bash
cp .env.example .env
# Edit .env: set GEMINI_API_KEY (and optionally NOTES_FOLDER)
pip install -r requirements.txt
python limpiar_notas.py "My Notes Folder"
```

Pass the **Notes folder name** as the first argument (overrides `NOTES_FOLDER` in `.env`). If you omit it, the script uses `NOTES_FOLDER` from `.env`. (Legacy: `CARPETA_ORIGEN` in `.env` is still supported.)

Requires **macOS** (Notes app), **Python 3**, and a [Gemini API key](https://aistudio.google.com/apikey).

---

## Example prompts

The classification rules live in **`prompt.txt`**. You can replace or tweak the instructions. Here are some variants.

**Strict (aggressive cleanup):**
```text
You classify notes as MOVE (junk) or KEEP (keep). Reply with only one word.
MOVE = links without personal context, marketing copy-paste, logs, old meeting notes.
KEEP = personal notes, passwords, original ideas, poems.
Note date: {{NOTE_DATE}}
Note:
{{NOTE_CONTENT}}
```

**Keep more (conservative):**
```text
Reply only MOVE or KEEP. MOVE only for obvious junk: bare URLs, session tokens, JSON dumps. When in doubt, reply KEEP.
Date: {{NOTE_DATE}}
{{NOTE_CONTENT}}
```

**By language:**
```text
Classify this note. Reply only: MOVE (trash) or KEEP (keep). Use MOVE for links without context, generic articles, old checklists. Use KEEP for personal content.
Date: {{NOTE_DATE}}
{{NOTE_CONTENT}}
```

You **must** keep the placeholders `{{NOTE_DATE}}` and `{{NOTE_CONTENT}}` so the script can inject the note date and body.

---

## Where to personalize

| Goal | File | What to edit |
|------|------|--------------|
| Classification rules / tone | **`prompt.txt`** | Full prompt text. Keep `{{NOTE_DATE}}` and `{{NOTE_CONTENT}}`. |
| API key, default folder, model | **`.env`** | `GEMINI_API_KEY` (required), optional `NOTES_FOLDER` (used if no CLI folder), optional `GEMINI_MODEL`. |
| Short-note threshold | **`limpiar_notas/gemini.py`** | Line ~30: `len(note_content.strip()) < 10` (notes shorter than this are auto MOVE). |
| Delay between notes | **`notes_cleaner.applescript`** | Search for `delay` (e.g. `delay 4`) and change the number of seconds. |

---

## License

[MIT](LICENSE)
