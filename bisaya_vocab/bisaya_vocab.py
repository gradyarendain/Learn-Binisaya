import os
import random
import csv

path_to_BisayaLog = "data/BisayaLog.csv"
path_to_WrongWords = "data/WrongWords.csv"
path_to_QuizAllCorrect = "data/QuizAllCorrect.csv"

# Function to load CSV data
def load_csv(file_path):
    with open(file_path, 'r') as file:
        return list(csv.DictReader(file))

# Function to save CSV data
def save_csv(file_path, data):
    fieldnames = ['Word', 'Type', 'Definition1', 'Definition2', 'Example', 'Synonym']
    with open(file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

# Function to add a new row interactively
def add_row_interactive(file_path):
    data = load_csv(file_path)
    new_row = {key: input(f"{key}: ") for key in data[0].keys()}
    data.append(new_row)
    save_csv(file_path, data)
    print("Row added successfully.")

# Function to search for a word
def search_word(file_path, search_word):
    data = load_csv(file_path)
    return [row for row in data if search_word.lower() in row.values()]

# Function to count remaining words
def count_remaining_words(data, quiz_all_correct):
    asked_words = {entry['Word'] for entry in quiz_all_correct}
    return sum(1 for entry in data if entry['Word'] not in asked_words)