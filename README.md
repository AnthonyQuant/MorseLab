# 📡 MorseLab

MorseLab is a robust, dual-interface (CLI & GUI) Python application designed for translating text to Morse code and vice versa. It features persistent JSON history tracking, duplicate filtering, robust error validation, and an interactive continuous practice quiz mode.

---

## ✨ Features

* **Dual Interfaces:** Fully functional Command Line Interface (CLI) and a modern dark-mode Tkinter Graphical User Interface (GUI).
* **Robust Translation & Validation:** Normalized whitespace handling with explicit `ValueError` checking for unsupported characters and invalid Morse sequences.
* **Persistent History:** Automatically logs translations and quiz scores into a localized JSON file using `pathlib` for reliable cross-platform pathing.
* **Interactive Quiz Mode:** Continuous practice mode with difficulty filtering (Letters, Numbers, or Mixed), live score tracking, and immediate correct-answer feedback.

---

## 🗂️ Project Structure

```text
MorseLab/
├── GUI.py                  # Tkinter desktop interface
├── history.py              # Persistent JSON I/O & duplicate filtering backend
├── morse_engine.py         # Core translation logic and validation rules
├── tests/
│   └── test_morse_engine.py# Unit tests for translation engine
└── README.md