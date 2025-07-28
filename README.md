# WORDHUNTER
# 🔠 AutoTyper for Spanish Word Puzzles

**AutoTyper** is a Python desktop application designed to automatically type (or paste) Spanish words into any active window. It helps solve word games or puzzles by generating all valid words from a set of letters, ensuring a specific required letter is present, and sending them to the selected application using simulated keystrokes or clipboard pasting.

---

## ✨ Features

- ✅ GUI to input allowed letters
- ✅ Automatically finds valid Spanish words (length 4–7)
- ✅ Enforces a required letter (the 4th in the input)
- ✅ Excludes words where the required letter is at the end
- ✅ Supports ascending or descending paste order
- ✅ Pasting via clipboard (optimized for macOS)
- ✅ Global hotkey (⌘ + Shift + S) to stop typing anytime
- ✅ Save results to a `.txt` file
- ✅ Adjustable typing delay and initial wait time

---

## 🖥️ Interface

- **Start Typing**: Begins processing and typing words
- **Stop**: Halts typing immediately
- **Settings**: Configure delay, wait time, file path, and word paste order

---

## 🛠️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/auto-spanish-typer.git
cd auto-spanish-typer
