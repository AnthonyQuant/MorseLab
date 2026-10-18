import tkinter as tk
from tkinter import messagebox, ttk  # Import ttk for modern themed widgets


class MorseLabApp:

  def __init__(self, root):
    self.root = root
    self.root.title("MorseLab Desktop")
    self.root.geometry("520x600")
    self.root.minsize(480, 550)

    # Configure a clean background color for the main window
    self.root.configure(bg="#1e1e2e")

    self.direction_var = tk.StringVar(value="Text to Morse")
    self.input_text = None
    self.output_text = None

    self.create_styles()
    self.create_widgets()

  def create_styles(self):
    """Configures modern styling for ttk widgets."""
    style = ttk.Style()
    style.theme_use("clam")

    # Configure custom colors and fonts
    style.configure(
        "TLabel", background="#1e1e2e", foreground="#cdd6f4", font=("Segoe UI", 11)
    )
    style.configure(
        "Header.TLabel",
        background="#1e1e2e",
        foreground="#89b4fa",
        font=("Segoe UI", 16, "bold"),
    )
    style.configure(
        "TRadiobutton",
        background="#1e1e2e",
        foreground="#cdd6f4",
        font=("Segoe UI", 10),
    )
    style.configure(
        "Accent.TButton",
        font=("Segoe UI", 11, "bold"),
        background="#89b4fa",
        foreground="#1e1e2e",
    )
    style.configure(
        "Danger.TButton",
        font=("Segoe UI", 10),
        background="#f38ba8",
        foreground="#1e1e2e",
    )

# Import your core translation engine functions and history module
# (Note: Change 'main' if your core file is named something else, like 'morse_engine')
from morse_engine import morse_to_text, text_to_morse
import history


class MorseLabApp:

    def __init__(self, root):
        """Initializes the main application window and variable states."""
        self.root = root
        self.root.title("MorseLab Desktop")
        self.root.geometry("500x550")
        self.root.config(padx=20, pady=20)

        # Tracks the user's selected translation direction
        self.direction_var = tk.StringVar(value="Text to Morse")

        # Call method to render widgets
        self.create_widgets()

    def create_widgets(self):
        # Main Title using styled ttk Label
        title_label = ttk.Label(
            self.root, text="MorseLab Desktop", style="Header.TLabel"
        )
        title_label.pack(pady=(20, 10))

        # Direction Frame
        frame_dir = ttk.LabelFrame(
            self.root, text=" Translation Direction ", padding=15
        )
        frame_dir.pack(fill="x", padx=20, pady=10)

        ttk.Radiobutton(
            frame_dir,
            text="Text to Morse Code",
            variable=self.direction_var,
            value="Text to Morse",
        ).pack(anchor="w", pady=2)
        ttk.Radiobutton(
            frame_dir,
            text="Morse Code to Text",
            variable=self.direction_var,
            value="Morse to Text",
        ).pack(anchor="w", pady=2)

        # Input Section
        ttk.Label(self.root, text="Enter Input Text / Morse:").pack(
            anchor="w", padx=20, pady=(10, 2)
        )
        self.input_text = tk.Text(
            self.root,
            height=5,
            font=("Consolas", 10),
            bg="#313244",
            fg="#cdd6f4",
            insertbackground="white",
            relief="flat",
            bd=5,
        )
        self.input_text.pack(fill="x", padx=20, pady=5)

        # Translate Button (Using styled ttk Button)
        translate_btn = ttk.Button(
            self.root,
            text="Translate",
            style="Accent.TButton",
            command=self.handle_translation,
        )
        translate_btn.pack(fill="x", padx=20, pady=12)

        # Output Section
        ttk.Label(self.root, text="Translation Result:").pack(
            anchor="w", padx=20, pady=(10, 2)
        )
        self.output_text = tk.Text(
            self.root,
            height=5,
            font=("Consolas", 10),
            bg="#313244",
            fg="#a6e3a1",
            insertbackground="white",
            relief="flat",
            bd=5,
        )
        self.output_text.pack(fill="x", padx=20, pady=5)

        # Clear Button
        clear_btn = ttk.Button(
            self.root,
            text="Clear Fields",
            style="Danger.TButton",
            command=self.clear_fields,
        )
        clear_btn.pack(fill="x", padx=20, pady=10)

        # History & Quiz Action Buttons
        history_btn = ttk.Button(
            self.root,
            text="View History",
            command=self.show_history_window,
        )
        history_btn.pack(fill="x", padx=20, pady=2)

        clear_history_btn = ttk.Button(
            self.root,
            text="Clear History File",
            style="Danger.TButton",
            command=self.clear_history_action,
        )
        clear_history_btn.pack(fill="x", padx=20, pady=2)

        # Added: Button to open the interactive practice quiz window
        quiz_btn = ttk.Button(
            self.root,
            text="Practice Mode (Quiz)",
            style="Accent.TButton",
            command=self.open_quiz_window,
        )
        quiz_btn.pack(fill="x", padx=20, pady=2)

        # Added: Dedicated Exit button to cleanly shut down the GUI application
        exit_btn = ttk.Button(
            self.root,
            text="Exit Application",
            style="Danger.TButton",
            command=self.root.destroy,
        )
        exit_btn.pack(fill="x", padx=20, pady=10)

    def handle_translation(self):
        """Translates input text/Morse, normalizes spacing, and handles errors cleanly in the GUI."""
        user_input = self.input_text.get("1.0", tk.END).strip()
        direction = self.direction_var.get()

        if not user_input:
            messagebox.showwarning("Warning", "Please enter text or Morse code to translate!")
            return

        try:
            if direction == "Text to Morse":
                result = text_to_morse(user_input)
            else:
                result = morse_to_text(user_input)

            # Display result in output box
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, result)

            # Save to history with automatic duplicate prevention
            history.save_translation(user_input, result, direction)

        except ValueError as e:
            # Display error cleanly in the GUI instead of the console
            messagebox.showerror("Translation Error", str(e))

    def show_history_window(self):
        """Opens a secondary window displaying unified history with accurate error reporting."""
        hist_win = tk.Toplevel(self.root)
        hist_win.title("MorseLab History Viewer")
        hist_win.geometry("480x450")
        hist_win.configure(bg="#1e1e2e")

        ttk.Label(
            hist_win, text="Translation & Quiz History", style="Header.TLabel"
        ).pack(pady=12)

        text_area = tk.Text(
            hist_win,
            font=("Consolas", 10),
            bg="#313244",
            fg="#cdd6f4",
            padx=10,
            pady=10,
        )
        text_area.pack(fill="both", expand=True, padx=15, pady=10)

        try:
            with open(history.HISTORY_FILE, "r", encoding="utf-8") as file:
                records = history.json.load(file)
                if not records:
                    text_area.insert(tk.END, "No history records found yet.")
                else:
                    for i, r in enumerate(records, 1):
                        text_area.insert(
                            tk.END,
                            f"[{i}] {r.get('timestamp')}\n"
                            f"Category: {r.get('direction')}\n"
                            f"Input: {r.get('input')}\n"
                            f"Output: {r.get('output')}\n"
                            + "-" * 42
                            + "\n",
                        )
        except FileNotFoundError:
            text_area.insert(
                tk.END, "No history file found yet. Make a translation or take a quiz!"
            )
        except history.json.JSONDecodeError:
            text_area.insert(
                tk.END,
                "⚠️ Error: History file is corrupted or contains malformed JSON.",
            )
        except OSError as e:
            text_area.insert(tk.END, f"⚠️ OS Error accessing history file: {e}")

        text_area.config(state="disabled")

        ttk.Button(hist_win, text="Close Viewer", command=hist_win.destroy).pack(
            pady=10
        )

    def open_quiz_window(self):
        """Opens a secondary GUI window for an interactive, continuous

        Morse code practice quiz with live score tracking and next-question flow.
        """
        import random
        from morse_engine import MORSE_CODE_DICT

        quiz_win = tk.Toplevel(self.root)
        quiz_win.title("MorseLab Practice Quiz")
        quiz_win.geometry("450x450")
        quiz_win.configure(bg="#1e1e2e")

        # Quiz Header
        ttk.Label(
            quiz_win, text="MorseLab Practice Quiz", style="Header.TLabel"
        ).pack(pady=15)

        # Difficulty Selection Frame & Radio Buttons
        diff_frame = ttk.LabelFrame(
            quiz_win, text=" Select Quiz Difficulty ", padding=15
        )
        diff_frame.pack(fill="x", padx=20, pady=10)

        diff_var = tk.StringVar(value="Letters")
        ttk.Radiobutton(
            diff_frame, text="Letters Only", variable=diff_var, value="Letters"
        ).pack(anchor="w", pady=2)
        ttk.Radiobutton(
            diff_frame, text="Numbers Only", variable=diff_var, value="Numbers"
        ).pack(anchor="w", pady=2)
        ttk.Radiobutton(
            diff_frame,
            text="Mixed (Letters & Numbers)",
            variable=diff_var,
            value="Mixed",
        ).pack(anchor="w", pady=2)

        # 1. Define start_quiz_session FIRST so PyCharm recognizes it before the button call
        def start_quiz_session():
            """Initializes quiz state variables and loads the first question interface."""
            choice = diff_var.get()
            if choice == "Letters":
                pool = {k: v for k, v in MORSE_CODE_DICT.items() if k.isalpha()}
            elif choice == "Numbers":
                pool = {k: v for k, v in MORSE_CODE_DICT.items() if k.isdigit()}
            else:
                pool = {k: v for k, v in MORSE_CODE_DICT.items() if k != " "}

            # Clear out difficulty selection widgets
            for widget in quiz_win.winfo_children():
                widget.destroy()

            # Quiz session state dictionary to track score and progress across questions
            state = {
                "score": 0,
                "total": 0,
                "current_char": None,
                "correct_morse": None,
            }

            # Render Persistent Session Header (Score & Question Counter)
            header_frame = ttk.Frame(quiz_win)
            header_frame.pack(fill="x", padx=20, pady=10)

            score_lbl = ttk.Label(
                header_frame, text="Score: 0 / 0", font=("Segoe UI", 11, "bold")
            )
            score_lbl.pack(side="left")

            progress_lbl = ttk.Label(
                header_frame, text="Question: 1", font=("Segoe UI", 11)
            )
            progress_lbl.pack(side="right")

            # Question Display Area
            question_lbl = ttk.Label(
                quiz_win, text="", font=("Segoe UI", 13, "bold")
            )
            question_lbl.pack(pady=15)

            ans_entry = tk.Entry(
                quiz_win, font=("Consolas", 14), bg="#313244", fg="#cdd6f4"
            )
            ans_entry.pack(pady=10, fill="x", padx=30)

            feedback_lbl = ttk.Label(
                quiz_win, text="", font=("Segoe UI", 11), wraplength=380
            )
            feedback_lbl.pack(pady=10)

            def load_next_question():
                """Selects and displays the next random character from the pool."""
                if not pool:
                    return
                char, morse = random.choice(list(pool.items()))
                state["current_char"] = char
                state["correct_morse"] = morse

                question_lbl.config(text=f"What is the Morse code for '{char}'?")
                ans_entry.delete(0, tk.END)
                feedback_lbl.config(text="")
                submit_btn.config(state="normal")
                next_btn.config(state="disabled")

            def check_answer():
                """Evaluates user input, updates score, displays correct answer, and logs progress."""
                user_ans = ans_entry.get().strip()
                if not user_ans:
                    return

                state["total"] += 1
                is_correct = user_ans == state["correct_morse"]

                if is_correct:
                    state["score"] += 1
                    feedback_lbl.config(text="✅ Correct! Great job.")
                else:
                    feedback_lbl.config(
                        text=(
                            f"❌ Incorrect. The correct Morse code for"
                            f" '{state['current_char']}' is '{state['correct_morse']}'."
                        )
                    )

                # Update running score and question counter display
                score_lbl.config(
                    text=(
                        f"Score: {state['score']} / {state['total']} "
                        f"({(state['score'] / state['total']) * 100:.0f}%)"
                    )
                )
                progress_lbl.config(text=f"Question: {state['total'] + 1}")

                # Save cumulative progress to history after each answer
                history.save_quiz_record(
                    state["score"], state["total"], f"Continuous Quiz ({choice})"
                )

                submit_btn.config(state="disabled")
                next_btn.config(state="normal")

            # Action Buttons Frame
            btn_frame = ttk.Frame(quiz_win)
            btn_frame.pack(pady=15)

            submit_btn = ttk.Button(
                btn_frame,
                text="Submit Answer",
                style="Accent.TButton",
                command=check_answer,
            )
            submit_btn.pack(side="left", padx=5)

            next_btn = ttk.Button(
                btn_frame,
                text="Next Question",
                state="disabled",
                command=load_next_question,
            )
            next_btn.pack(side="left", padx=5)

            ttk.Button(
                quiz_win, text="End & Close Quiz", command=quiz_win.destroy
            ).pack(pady=5)

            # Load the very first question immediately
            load_next_question()



        def start_quiz():
            """Filters character pool based on choice and loads the quiz question."""
            choice = diff_var.get()
            if choice == "Letters":
                pool = {k: v for k, v in MORSE_CODE_DICT.items() if k.isalpha()}
            elif choice == "Numbers":
                pool = {k: v for k, v in MORSE_CODE_DICT.items() if k.isdigit()}
            else:
                pool = {k: v for k, v in MORSE_CODE_DICT.items() if k != " "}

            # Clear out the difficulty selection widgets from the popup window
            for widget in quiz_win.winfo_children():
                widget.destroy()

            # Select a random character from the filtered pool
            char, correct_morse = random.choice(list(pool.items()))

            # Render Active Quiz UI
            ttk.Label(
                quiz_win, text="Practice Quiz Active", style="Header.TLabel"
            ).pack(pady=15)
            ttk.Label(
                quiz_win,
                text=f"What is the Morse code for '{char}'?",
                font=("Segoe UI", 12, "bold"),
            ).pack(pady=10)

            ans_entry = tk.Entry(
                quiz_win, font=("Consolas", 12), bg="#313244", fg="#cdd6f4"
            )
            ans_entry.pack(pady=10, fill="x", padx=30)

            feedback_lbl = ttk.Label(quiz_win, text="", font=("Segoe UI", 10))
            feedback_lbl.pack(pady=5)

            def check_ans():
                """Evaluates user input against correct Morse code and logs result."""
                user_ans = ans_entry.get().strip()
                if user_ans == correct_morse:
                    feedback_lbl.config(text="✅ Correct! +1 point.")
                    history.save_quiz_record(1, 1, f"GUI Quiz ({choice})")
                else:
                    feedback_lbl.config(text=f"❌ Incorrect. Correct: {correct_morse}")
                    history.save_quiz_record(0, 1, f"GUI Quiz ({choice})")

            ttk.Button(
                quiz_win,
                text="Submit Answer",
                style="Accent.TButton",
                command=check_ans,
            ).pack(pady=10)
            ttk.Button(quiz_win, text="Close Quiz", command=quiz_win.destroy).pack(
                pady=5
            )

        # Button to confirm difficulty and start the quiz
        ttk.Button(
            quiz_win,
            text="Start Quiz",
            style="Accent.TButton",
            command=start_quiz,
        ).pack(pady=15)

    def clear_history_action(self):
        """Clears history with a confirmation prompt."""
        if messagebox.askyesno(
                "Confirm", "Are you sure you want to clear all history?"
        ):
            history.clear_history()
            messagebox.showinfo("Success", "Translation history cleared!")

    def clear_fields(self):
        """Clears both the input and output text boxes."""
        self.input_text.delete("1.0", tk.END)
        self.output_text.delete("1.0", tk.END)

def run_gui():
  """Initializes and runs the MorseLab desktop graphical interface."""
  root = tk.Tk()
  app = MorseLabApp(root)
  root.mainloop()


if __name__ == "__main__":
  run_gui()
