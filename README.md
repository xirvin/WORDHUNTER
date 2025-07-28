# 🧠 WORDHUNTER

**WORDHUNTER** is an intelligent auto-typer built for word puzzle games. It types out valid words based on user-specified letters, dictionary language, and game logic.

🚀 [Live on GitHub](https://github.com/xirvin/WORDHUNTER/)

---

## ✨ Features

- 🔤 Supports English and Spanish dictionaries
- 🎯 Enforces required center letter and allows/disallows repeated letters
- 🪄 Automatically types words into any input box (paste + enter)
- ⏱️ Customizable typing delay and start wait time
- 💾 Option to save results to a file
- 🔡 Sort words in ascending or descending order by length
- 🔒 Global hotkey `⌘ + Shift + S` to stop typing

---

## 🖼️ Screenshot

> Coming soon...

---

## 🛠 Requirements

- Python 3.8+
- Install required packages:

```bash
pip install pyautogui pyperclip pynput
```

---

## 📦 Dictionary Files

Place these JSON files in the root directory:

- `english_words.json` (Source: [dwyl/english-words](https://github.com/dwyl/english-words))
- `spanish_words.json` (Source: [eymenefealtun/all-words-in-all-languages](https://github.com/eymenefealtun/all-words-in-all-languages))

Each file must be structured like this:

```json
{
  "4": ["word", "more", "game"],
  "5": ["puzzle", "brain"],
  ...
}
```

---

## 🧑‍💻 Usage

1. Clone this repository:
   ```bash
   git clone https://github.com/xirvin/WORDHUNTER.git
   cd WORDHUNTER
   ```

2. Run the application:
   ```bash
   python wordhunter.py
   ```

3. Enter letters (minimum 4).
4. Press **Start Typing**.
5. Use **Settings** to:
   - Switch between languages
   - Set typing delay
   - Save to file
   - Customize word logic

---

## ⌨️ Hotkeys

- **Stop Typing Globally**: `⌘ + Shift + S`  
  *(Windows: Replace ⌘ with Ctrl if modified)*

---

---

## 📄 License

MIT License © [xirvin](https://github.com/xirvin)

---
