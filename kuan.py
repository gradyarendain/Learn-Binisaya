import argparse
import csv
import os
import random

def load_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        data = list(reader)
    return data

def save_csv(file_path, data):
    fieldnames = ['Word', 'Type', 'Definition1', 'Definition2', 'Example', 'Synonym']
    with open(file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def add_row_interactive(file_path):
    data = load_csv(file_path)

    new_row = {}
    new_row['Word'] = input("Word: ")
    new_row['Type'] = input("Type: ")
    new_row['Definition1'] = input("Definition1: ")
    new_row['Definition2'] = input("Definition2: ")
    new_row['Example'] = input("Example: ")
    new_row['Synonym'] = input("Synonym: ")

    data.append(new_row)
    save_csv(file_path, data)
    print("Row added successfully.")


def search_word(file_path, search_word):
    data = load_csv(file_path)
    found_rows = []
    for row in data:
        for value in row.values():
            if search_word.lower() == value.lower():
                found_rows.append(row)
                break  # If found in any column, add the row and move to the next
    return found_rows

def quiz(file_path, category_filter=None, last=None, english_mode=False):
    data = load_csv(file_path)
    if last:
        data = data[-int(last):]  # Consider only the last 'xx' rows
    correct_count = 0
    total_quizzes = 0
    asked_words = []
    incorrect_words = []

    try:
        while True:
            remaining_words = [entry for entry in data if entry['Word'] not in asked_words]

            if category_filter:
                remaining_words = [entry for entry in remaining_words if entry['Type'].lower() == category_filter.lower()]

            if not remaining_words:
                if incorrect_words:  # Check if there are incorrect words
                    print("Repeating incorrectly answered words.")
                    remaining_words = [entry for entry in data if entry['Word'] in incorrect_words]
                else:
                    print("You've been quizzed on all available words!")
                    break

            random_entry = random.choice(remaining_words)
            word = random_entry['Word']
            definition1 = random_entry['Definition1']
            definition2 = random_entry['Definition2']

            if english_mode:
                print(f"Definition: {definition1}, {definition2}")
                user_word = input("Enter the word (Ctrl+C to exit): ")
            else:
                print(f"Word: {word}")
                user_definition = input("Enter the definition (Ctrl+C to exit): ")

            if (english_mode and user_word.lower() == word.lower()) or \
            (not english_mode and (user_definition.lower() == definition1.lower() or user_definition.lower() == definition2.lower())):
                correct_count += 1
                print("Correct!")
                if word in incorrect_words:
                    incorrect_words.remove(word)
            else:
                if english_mode:
                    print("Incorrect!")
                    print(f"Correct word: {word}")
                else:
                    print("Incorrect!")
                    print(f"Correct definitions: {definition1}, {definition2}")

                if word not in incorrect_words:
                    incorrect_words.append(word)

            total_quizzes += 1
            asked_words.append(word)

    except KeyboardInterrupt:
        pass

    print(f"Total words quizzed: {total_quizzes}")
    print(f"Correctly defined: {correct_count}")
    if total_quizzes > 0:
        accuracy = (correct_count / total_quizzes) * 100
        print(f"Accuracy: {accuracy:.2f}%")


def count_remaining_words(data, quiz_all_correct):
    asked_words = [entry['Word'] for entry in quiz_all_correct]
    remaining_words = [entry for entry in data if entry['Word'] not in asked_words]
    return len(remaining_words)

def quiz_all(file_path, english_mode=False, reset=False):
    if reset:
        with open("QuizAllCorrect.csv", "w"):
            pass

    quiz_all_correct = load_csv("QuizAllCorrect.csv")
    data = load_csv(file_path)
    asked_words = [entry['Word'] for entry in quiz_all_correct]
    correct_count = 0  # initialize - this variable stores correct answers per loop

    try:
        while True:
            remaining_count = count_remaining_words(data, quiz_all_correct)
            print(f"Words remaining to be quizzed: {remaining_count}")

            remaining_words = [entry for entry in data if entry['Word'] not in asked_words]

            if not remaining_words:
                print("You've been quizzed on all available words!")
                break

            random_entry = random.choice(remaining_words)
            word = random_entry['Word']
            definition1 = random_entry['Definition1']
            definition2 = random_entry['Definition2']

            if english_mode:
                print(f"Definition: {definition1}, {definition2}")
                user_word = input("Enter the word (Ctrl+C to exit): ")
            else:
                print(f"Word: {word}")
                user_definition = input("Enter the definition (Ctrl+C to exit): ")

            if (english_mode and user_word.lower() == word.lower()) or \
                    (not english_mode and (
                            user_definition.lower() == definition1.lower() or user_definition.lower() == definition2.lower())):
                correct_count += 1
                print("Correct!")
                quiz_all_correct.append(random_entry)
                save_csv("QuizAllCorrect.csv", quiz_all_correct)
            else:
                print("Incorrect!")
                if english_mode:
                    print(f"Correct word: {word}")
                else:
                    print(f"Correct definitions: {definition1}, {definition2}")

            asked_words.append(word)

    except KeyboardInterrupt:
        remaining_count = count_remaining_words(data, quiz_all_correct)
        print(f"Words remaining to be quizzed: {remaining_count}")
        total_bisaya_log = len(data)
        total_quiz_correct = len(quiz_all_correct)
        print(f"Total rows in BisayaLog.csv: {total_bisaya_log}")
        print(f"Total rows in QuizAllCorrect.csv: {total_quiz_correct}")

def main():
    default_file_path = os.path.expanduser('BisayaLog.csv')

    parser = argparse.ArgumentParser(description='Process CSV file')
    parser.add_argument('--add', help='Add a new row to the CSV file', action='store_true')
    parser.add_argument('--search', help='Search for a word in the CSV file', type=str)
    parser.add_argument('--quiz', help='Take a quiz with a random word and prompt for definition', action='store_true')
    parser.add_argument('--category', help='Filter words by category', type=str)
    parser.add_argument('--last', help='Take the last number of rows for the quiz', type=int)
    parser.add_argument('--english', help='Take a quiz with definitions in English and prompt for the corresponding word', action='store_true')
    parser.add_argument('--quizall', help='Take a quiz with all words and store correctly defined words in QuizAllCorrect.csv', action='store_true')
    parser.add_argument('--quizall_reset', help='Reset QuizAllCorrect.csv', action='store_true')
    args = parser.parse_args()

    if args.add:
        add_row_interactive(default_file_path)
    elif args.search:
        search_result = search_word(default_file_path, args.search)
        if search_result:
            for row in search_result:
                print(row)
        else:
            print("No matching rows found.")
    elif args.quiz:
        quiz(default_file_path, args.category, args.last, args.english)
    elif args.quizall:
        quiz_all(default_file_path, args.english)
    elif args.quizall_reset:
        quiz_all("BisayaLog.csv", reset=True)
    else:
        print("No action specified. Use '--add' to add a new row or '--search' to search for a word.")

if __name__ == "__main__":
    main()
