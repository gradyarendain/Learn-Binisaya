import tkinter as tk
from tkinter import messagebox
import os

def add_row():
    os.system("python3 kuan.py --add")

def search_word():
    search_term = search_entry.get()
    if search_term:
        result = os.popen(f"python your_script.py --search {search_term}").read()
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, result)
    else:
        messagebox.showwarning("Warning", "Please enter a search term.")

def start_quiz():
    os.system("python your_script.py --quiz")

def quiz_all():
    os.system("python3 kuan.py --quizall")

def reset_quiz_all():
    os.system("python your_script.py --quizall_reset")

def sift_csv():
    os.system("python your_script.py --sift")

# Create the main window
window = tk.Tk()
window.title("Interactive Application")

# Add Row Button
add_row_button = tk.Button(window, text="Add Row", command=add_row)
add_row_button.pack()

# Search
search_label = tk.Label(window, text="Search Word:")
search_label.pack()

search_entry = tk.Entry(window)
search_entry.pack()

search_button = tk.Button(window, text="Search", command=search_word)
search_button.pack()

result_text = tk.Text(window, height=5, width=50)
result_text.pack()

# Quiz
start_quiz_button = tk.Button(window, text="Start Quiz", command=start_quiz)
start_quiz_button.pack()

# Quiz All
quiz_all_button = tk.Button(window, text="Quiz All", command=quiz_all)
quiz_all_button.pack()

# Reset Quiz All
reset_quiz_all_button = tk.Button(window, text="Reset Quiz All", command=reset_quiz_all)
reset_quiz_all_button.pack()

# Sift CSV
sift_csv_button = tk.Button(window, text="Sift CSV", command=sift_csv)
sift_csv_button.pack()

window.mainloop()
