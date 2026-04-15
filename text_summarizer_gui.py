import tkinter as tk
import PyPDF2

from tkinter import filedialog, messagebox
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# Run once, then comment out
# nltk.download('punkt')
# nltk.download('punkt_tab')
# nltk.download('stopwords')

# =========================
# SUMMARIZER FUNCTION
# =========================
def summarize_text(text):
    if len(text.strip()) == 0:
        return "Please enter some text."

    sentences = sent_tokenize(text)
    words = word_tokenize(text.lower())

    stop_words = set(stopwords.words("english"))

    # Filter words
    filtered_words = [word for word in words if word.isalnum() and word not in stop_words]

    # Word frequency
    word_frequency = {}
    for word in filtered_words:
        word_frequency[word] = word_frequency.get(word, 0) + 1

    # Normalize frequency
    max_freq = max(word_frequency.values())
    for word in word_frequency:
        word_frequency[word] /= max_freq

    # Sentence scoring
    sentence_scores = {}
    for sentence in sentences:
        word_count = len(word_tokenize(sentence))
        if 5 < word_count < 30:  # ignore too short/long sentences
            for word in word_tokenize(sentence.lower()):
                if word in word_frequency:
                    sentence_scores[sentence] = sentence_scores.get(sentence, 0) + word_frequency[word]

    if not sentence_scores:
        return "Text too short to summarize."

    # Summary size (30%)
    summary_length = max(1, int(len(sentences) * 0.4))

    # Select top sentences
    ranked_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)

    # Remove very similar sentences
    selected = []
    for sent in ranked_sentences:
        if sent not in selected:
            selected.append(sent)
        if len(selected) == summary_length:
            break

    # Restore original order
    selected = sorted(selected, key=lambda s: sentences.index(s))

    # Format nicely
    summary = " ".join(selected)
    return summary

#=======================
def load_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        text = ""
        try:
            with open(file_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text() + "\n"

            if text.strip() == "":
                messagebox.showerror("Error", "No readable text found in PDF.")
                return

            input_box.delete("1.0", tk.END)
            input_box.insert(tk.END, text)

        except Exception as e:
            messagebox.showerror("Error", "Failed to read PDF.")


# =========================
# BUTTON FUNCTIONS
# =========================
def summarize_button():
    input_text = input_box.get("1.0", tk.END)
    summary = summarize_text(input_text)
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, summary)

def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            input_box.delete("1.0", tk.END)
            input_box.insert(tk.END, content)

# =========================
# ULTRA MODERN AI GUI
# =========================
root = tk.Tk()
root.title("Text Summarizer")
root.geometry("1100x720")
root.configure(bg="#0b0f19")

# ===== COLORS =====
BG_MAIN = "#0b0f19"
BG_CARD = "#121826"
ACCENT = "#6c63ff"
ACCENT_HOVER = "#5848e5"
TEXT = "#e6e9f0"
SUBTEXT = "#9aa4b2"

# ===== HEADER =====
header = tk.Label(
    root,
    text="Text Summarizer AI",
    font=("Segoe UI", 30, "bold"),
    bg=BG_MAIN,
    fg=ACCENT
)
header.pack(pady=20)

subtitle = tk.Label(
    root,
    text="Smart Text & PDF Summarization Engine",
    font=("Segoe UI", 11),
    bg=BG_MAIN,
    fg=SUBTEXT
)
subtitle.pack()

# ===== MAIN CONTAINER =====
main_frame = tk.Frame(root, bg=BG_MAIN)
main_frame.pack(fill="both", expand=True, padx=40, pady=30)

# ===== LEFT PANEL (Controls) =====
left_panel = tk.Frame(main_frame, bg=BG_CARD, bd=0)
left_panel.pack(side="left", fill="y", padx=(0, 25))

left_panel.config(width=250)

tk.Label(
    left_panel,
    text="Controls",
    font=("Segoe UI", 14, "bold"),
    bg=BG_CARD,
    fg=TEXT
).pack(pady=20)

def styled_button(parent, text, command):
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        bg=ACCENT,
        fg="white",
        activebackground=ACCENT_HOVER,
        activeforeground="white",
        font=("Segoe UI", 11, "bold"),
        relief="flat",
        padx=20,
        pady=10,
        cursor="hand2",
        bd=0
    )
    btn.pack(pady=10, fill="x", padx=20)

    btn.bind("<Enter>", lambda e: btn.config(bg=ACCENT_HOVER))
    btn.bind("<Leave>", lambda e: btn.config(bg=ACCENT))

styled_button(left_panel, "Load TXT File", load_file)
styled_button(left_panel, "Load PDF File", load_pdf)
styled_button(left_panel, "Summarize Text", summarize_button)

# ===== WORD COUNTER =====
word_label = tk.Label(
    left_panel,
    text="Words: 0",
    font=("Segoe UI", 10),
    bg=BG_CARD,
    fg=SUBTEXT
)
word_label.pack(pady=30)

def update_word_count(event=None):
    text = input_box.get("1.0", tk.END)
    words = len(text.split())
    word_label.config(text=f"Words: {words}")

# ===== RIGHT PANEL (Workspace) =====
right_panel = tk.Frame(main_frame, bg=BG_MAIN)
right_panel.pack(side="right", fill="both", expand=True)

# INPUT CARD
input_card = tk.Frame(right_panel, bg=BG_CARD)
input_card.pack(fill="both", expand=True, pady=(0, 20))

tk.Label(
    input_card,
    text="Input Text",
    font=("Segoe UI", 12, "bold"),
    bg=BG_CARD,
    fg=TEXT
).pack(anchor="w", padx=15, pady=10)

input_box = tk.Text(
    input_card,
    bg="#1a2233",
    fg=TEXT,
    insertbackground="white",
    font=("Consolas", 11),
    relief="flat",
    height=10
)
input_box.pack(fill="both", expand=True, padx=15, pady=(0, 15))
input_box.bind("<KeyRelease>", update_word_count)

# OUTPUT CARD
output_card = tk.Frame(right_panel, bg=BG_CARD)
output_card.pack(fill="both", expand=True)

tk.Label(
    output_card,
    text="Summary Output",
    font=("Segoe UI", 12, "bold"),
    bg=BG_CARD,
    fg=TEXT
).pack(anchor="w", padx=15, pady=10)

output_box = tk.Text(
    output_card,
    bg="#1a2233",
    fg=TEXT,
    insertbackground="white",
    font=("Consolas", 11),
    relief="flat",
    height=8
)
output_box.pack(fill="both", expand=True, padx=15, pady=(0, 15))

root.mainloop()
