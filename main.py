import time
import pyautogui
import pyperclip
import json
import tkinter as tk
from tkinter import messagebox, filedialog
from threading import Thread, Event
from pynput import keyboard
from collections import defaultdict

class AutoTyperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Typer")

        self.is_typing = False
        self.stop_event = Event()

        self.delay_ms = 0
        self.wait_before_typing = 2
        self.save_path = None
        self.order_ascending = True
        self.allow_repeats = False
        self.require_mandatory_letter = True

        self.words = self.load_words()

        tk.Label(root, text="Enter allowed letters (e.g. siocagt):").pack(padx=10, pady=5)
        self.entry_letters = tk.Entry(root, width=30)
        self.entry_letters.pack(padx=10, pady=5)

        frame = tk.Frame(root)
        frame.pack(pady=10)
        self.btn_start = tk.Button(frame, text="Start Typing", command=self.start_typing)
        self.btn_start.grid(row=0, column=0, padx=5)
        self.btn_stop = tk.Button(frame, text="Stop", command=self.stop_typing, state='disabled')
        self.btn_stop.grid(row=0, column=1, padx=5)
        self.btn_settings = tk.Button(frame, text="Settings", command=self.open_settings)
        self.btn_settings.grid(row=0, column=2, padx=5)

        tk.Label(root, text="Global stop hotkey: ⌘ + Shift + S").pack(pady=5)

        self._listener = keyboard.Listener(on_press=self._on_press, on_release=self._on_release)
        self._listener.daemon = True
        self._listener.start()
        self._pressed = set()
        self._hotkey = {keyboard.Key.cmd, keyboard.Key.shift, keyboard.KeyCode(char='s')}

    def load_words(self):
        try:
            with open("spanish_words.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            words = []
            for lst in data.values():
                words.extend(lst)
            return words
        except Exception as e:
            messagebox.showerror("Error", f"Unable to load word list:\n{e}")
            return []

    def _on_press(self, key):
        self._pressed.add(key)
        if self._hotkey <= self._pressed:
            self.stop_typing()

    def _on_release(self, key):
        self._pressed.discard(key)

    def start_typing(self):
        letters = self.entry_letters.get().strip().lower()
        if len(letters) < 4:
            messagebox.showerror("Error", "Please enter at least 4 letters.")
            return
        if self.is_typing:
            return

        self.is_typing = True
        self.stop_event.clear()
        self.btn_start.config(state='disabled')
        self.btn_stop.config(state='normal')
        Thread(target=self.run_typing, args=(letters,), daemon=True).start()

    def stop_typing(self):
        if self.is_typing:
            self.stop_event.set()
            self.is_typing = False
            self.reset_buttons()
            messagebox.showinfo("Stopped", "Typing stopped.")

    def run_typing(self, letters):
        letra_obligatoria = letters[3] if self.require_mandatory_letter and len(letters) >= 4 else None
        allowed = set(letters)

        def is_valid(word):
            if len(word) < 4 or (letra_obligatoria and word.endswith(letra_obligatoria)):
                return False
            if self.allow_repeats:
                if not all(c in allowed for c in word):
                    return False
            else:
                if not set(word).issubset(allowed):
                    return False
            if letra_obligatoria and letra_obligatoria not in word:
                return False
            return True

        word_groups = defaultdict(list)
        for w in self.words:
            if is_valid(w):
                word_groups[len(w)].append(w)

        sorted_lengths = sorted(word_groups.keys())
        if not self.order_ascending:
            sorted_lengths.reverse()

        final_words = []
        for length in sorted_lengths:
            final_words.extend(sorted(word_groups[length]))

        time.sleep(self.wait_before_typing)
        delay = self.delay_ms / 1000.0

        if self.save_path:
            try:
                with open(self.save_path, "w", encoding="utf-8") as f:
                    f.write("\n".join(final_words))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save results:\n{e}")

        for w in final_words:
            if self.stop_event.is_set():
                break
            pyperclip.copy(w)
            pyautogui.hotkey('command', 'v')
            pyautogui.press('enter')
            time.sleep(delay)

        self.reset_buttons()
        if not self.stop_event.is_set():
            messagebox.showinfo("Done", "Typing finished.")

    def reset_buttons(self):
        self.is_typing = False
        self.btn_start.config(state='normal')
        self.btn_stop.config(state='disabled')

    def open_settings(self):
        SettingsWindow(self)

class SettingsWindow:
    def __init__(self, parent):
        self.parent = parent
        self.win = tk.Toplevel()
        self.win.title("Settings")
        self.win.grab_set()

        tk.Label(self.win, text="Save results to file:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.path_entry = tk.Entry(self.win, width=40)
        self.path_entry.grid(row=0, column=1, padx=10, pady=5)
        if parent.save_path:
            self.path_entry.insert(0, parent.save_path)
        tk.Button(self.win, text="Browse...", command=self.browse).grid(row=0, column=2, padx=5)

        tk.Label(self.win, text="Delay between words (ms):").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.delay_entry = tk.Entry(self.win, width=10)
        self.delay_entry.grid(row=1, column=1)
        self.delay_entry.insert(0, str(parent.delay_ms))

        tk.Label(self.win, text="Wait before typing (sec):").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.wait_entry = tk.Entry(self.win, width=10)
        self.wait_entry.grid(row=2, column=1)
        self.wait_entry.insert(0, str(parent.wait_before_typing))

        tk.Label(self.win, text="Paste order:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.order_var = tk.StringVar(value="asc" if parent.order_ascending else "desc")
        tk.Radiobutton(self.win, text="Ascending (4→7)", variable=self.order_var, value="asc").grid(row=3, column=1, sticky="w")
        tk.Radiobutton(self.win, text="Descending (7→4)", variable=self.order_var, value="desc").grid(row=4, column=1, sticky="w")

        self.repeat_var = tk.BooleanVar(value=parent.allow_repeats)
        tk.Checkbutton(self.win, text="Allow repeated letters in words", variable=self.repeat_var).grid(row=5, column=0, columnspan=2, sticky="w", padx=10)

        self.mandatory_var = tk.BooleanVar(value=parent.require_mandatory_letter)
        tk.Checkbutton(self.win, text="Require 4th letter to be present in word", variable=self.mandatory_var).grid(row=6, column=0, columnspan=2, sticky="w", padx=10)

        tk.Button(self.win, text="Save", command=self.save).grid(row=7, column=0, columnspan=3, pady=10)

    def browse(self):
        p = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All", "*.*")])
        if p:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, p)

    def save(self):
        d = self.delay_entry.get().strip()
        w = self.wait_entry.get().strip()
        if not d.isdigit() or not w.isdigit():
            messagebox.showerror("Error", "Values must be integers.")
            return
        self.parent.delay_ms = int(d)
        self.parent.wait_before_typing = int(w)
        self.parent.save_path = self.path_entry.get().strip() or None
        self.parent.order_ascending = self.order_var.get() == "asc"
        self.parent.allow_repeats = self.repeat_var.get()
        self.parent.require_mandatory_letter = self.mandatory_var.get()

        messagebox.showinfo("Settings", "Saved.")
        self.win.destroy()

if __name__ == "__main__":
    import sys
    try:
        import pyautogui, pyperclip, pynput
    except ImportError:
        print("Install required packages:\n pip install pyautogui pyperclip pynput")
        sys.exit(1)

    root = tk.Tk()
    app = AutoTyperApp(root)
    root.mainloop()
