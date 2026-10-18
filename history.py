from datetime import datetime
import json
from pathlib import Path

# Priority 4 Fix: Anchor HISTORY_FILE relative to history.py's directory using pathlib.Path
BASE_DIR = Path(__file__).resolve().parent
HISTORY_FILE = BASE_DIR / "translation_history.json"


def save_translation(input_data, output_data, direction):
  """Saves a translation record to the JSON file with normalized whitespace."""
  try:
    try:
      with open(HISTORY_FILE, "r", encoding="utf-8") as file:
        history = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
      history = []

    clean_input = str(input_data).strip()
    clean_output = str(output_data).strip()

    is_duplicate = any(
        str(r.get("input", "")).strip() == clean_input
        and str(r.get("output", "")).strip() == clean_output
        and r.get("direction") == direction
        for r in history
    )

    if not is_duplicate:
      record = {
          "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
          "direction": direction,
          "input": clean_input,
          "output": clean_output,
      }
      history.append(record)
      # Priority 5 Fix: Catch specific I/O and serialization errors instead of broad Exception
      with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=4)

  except (IOError, OSError, TypeError) as e:
    print(f"⚠️ File I/O Error saving history: {e}")


def view_history():
  """Loads and displays past translations and quiz records with distinct error handling."""
  try:
    with open(HISTORY_FILE, "r", encoding="utf-8") as file:
      history = json.load(file)
  except FileNotFoundError:
    print("\n📁 No translation history file found yet.")
    return
  except json.JSONDecodeError:
    print(
        "\n⚠️ Warning: The history file is corrupted or contains malformed JSON."
    )
    return
  except OSError as e:
    print(f"\n⚠️ OS Error reading history file: {e}")
    return

  if not history:
    print("\n📁 No saved history found.")
    return

  print("\n*** Saved Translation & Quiz History ***")
  for i, record in enumerate(history, 1):
    print(f"\n[{i}] Timestamp: {record.get('timestamp')}")
    print(f"    Category: {record.get('direction')}")
    print(f"    Input:    {record.get('input')}")
    print(f"    Result:   {record.get('output')}")


def clear_history():
  """Clears all records by overwriting the JSON file with an empty list."""
  try:
    with open(HISTORY_FILE, 'w') as file:
      json.dump([], file)
    print('\n🗑️ Translation history cleared successfully.')
  except Exception as e:
    print(f'⚠️ Error clearing history: {e}')

def save_quiz_record(score, total, difficulty):
  """Saves a completed or early-exited quiz score to the history JSON file."""
  try:
    try:
      with open(HISTORY_FILE, "r", encoding="utf-8") as file:
        history = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
      history = []

    record = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "direction": f"Quiz Mode ({difficulty})",
        "input": f"Attempted {total} question(s)",
        "output": f"Score: {score}/{total} ({(score/total)*100:.0f}%)"
        if total > 0
        else "Score: 0/0 (0%)",
    }

    history.append(record)
    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
      json.dump(history, file, indent=4)

  except (IOError, OSError, TypeError) as e:
    print(f"⚠️ File I/O Error saving quiz history: {e}")