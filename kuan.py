import argparse
import csv
import os
import random

def load_csv(file_path):
    with open(file_path, 'r') as file:
        return list(csv.DictReader(file))

def save_csv(file_path, data):
    fieldnames = ['Word', 'Type', 'Definition1', 'Definition2', 'Example', 'Synonym']
    with open(file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def add_row_interactive(file_path):
    data = load_csv(file_path)
    new_row = {key: input(f"{key}: ") for key in data[0].keys()}
    data.append(new_row)
    save_csv(file_path, data)
    print("Row added successfully.")

def search_word(file_path, search_word):
    data = load_csv(file_path)
    return [row for row in data if search_word.lower() in row.values()]

def quiz(file_path, category_filter=None, last=None, english_mode=False):
    data = load_csv(file_path)[-int(last):] if last else load_csv(file_path)
    correct_count, total_quizzes, asked_words, incorrect_words = 0, 0, [], []

    try:
        while True:
            remaining_words = [entry for entry in data if entry['Word'] not in asked_words]
            if category_filter:
                remaining_words = [entry for entry in remaining_words if entry['Type'].lower() == category_filter.lower()]

            if not remaining_words:
                remaining_words = [entry for entry in data if entry['Word'] in incorrect_words] if incorrect_words else []
                print("Repeating incorrectly answered words." if incorrect_words else "You've been quizzed on all available words!")
                if not remaining_words:
                    break

            random_entry = random.choice(remaining_words)
            word, definition1, definition2 = random_entry['Word'], random_entry['Definition1'], random_entry['Definition2']

            if english_mode:
                print(f"Definition: {definition1}, {definition2}")
                user_word = input("Enter the word (Ctrl+C to exit): ")
            else:
                print(f"Word: {word}")
                user_definition = input("Enter the definition (Ctrl+C to exit): ")

            if (english_mode and user_word.strip().lower() == word.strip().lower()) or \
                (not english_mode and (user_definition.strip().lower() == definition1.strip().lower() or user_definition.strip().lower() == definition2.strip().lower())):

                correct_count += 1
                print("Correct!")
                incorrect_words.remove(word) if word in incorrect_words else None
            else:
                print("Incorrect!")
                print(f"Correct word: {word}" if english_mode else f"Correct definitions: {definition1}, {definition2}")
                incorrect_words.append(word) if word not in incorrect_words else None

            total_quizzes += 1
            asked_words.append(word)

    except KeyboardInterrupt:
        pass

    print(f"Total words quizzed: {total_quizzes}")
    print(f"Correctly defined: {correct_count}")
    print(f"Accuracy: {correct_count / total_quizzes * 100:.2f}%" if total_quizzes > 0 else "No quizzes taken.")

def count_remaining_words(data, quiz_all_correct):
    asked_words = {entry['Word'] for entry in quiz_all_correct}
    return sum(1 for entry in data if entry['Word'] not in asked_words)

def quiz_all(file_path, english_mode=False, reset=False):
    if reset:
        save_csv("QuizAllCorrect.csv", [])

    quiz_all_correct, data = load_csv("QuizAllCorrect.csv"), load_csv(file_path)
    correct_count, total_bisaya_log = 0, len(data)

    try:
        while True:
            remaining_count = count_remaining_words(data, quiz_all_correct)
            print(f"Words remaining to be quizzed: {remaining_count}")

            remaining_words = [entry for entry in data if entry['Word'] not in {row['Word'] for row in quiz_all_correct}]

            if not remaining_words:
                print("You've been quizzed on all available words!")
                break

            random_entry = random.choice(remaining_words)
            word, definition1, definition2, synonym = random_entry['Word'], random_entry['Definition1'], random_entry['Definition2'], random_entry['Synonym']

            if english_mode:
                if word in [entry['Word'] for entry in quiz_all_correct]:
                    continue  # Skip if the user has already been prompted for this word

                definitions = (definition1, definition2) if not synonym else (definition1, definition2, f"Synonym: {synonym}")
                print(f"Definition: {', '.join(definitions)}")

                while True:
                    user_word = input("Enter the word (Ctrl+C to exit): ") if not synonym else input("Synonym: ")
                    user_word_lower = user_word.strip().lower()

                    correct_words = [word, synonym] if synonym else [word]

                    if user_word_lower in [correct_word.strip().lower() for correct_word in correct_words]:
                        correct_count += 1
                        print("Correct!")
                        quiz_all_correct.append(random_entry)
                        save_csv("QuizAllCorrect.csv", quiz_all_correct)
                        break
                    else:
                        print("Incorrect!")
                        print(f"Correct word: {', '.join(correct_words)}")
            else:
                if word in [entry['Word'] for entry in quiz_all_correct]:
                    continue  # Skip if the user has already been prompted for this word

                print(f"Word: {word}")

                while True:
                    user_definition = input("Enter the definition (Ctrl+C to exit): ")

                    if user_definition.strip().lower() == definition1.strip().lower() or user_definition.strip().lower() == definition2.strip().lower():
                        correct_count += 1
                        print("Correct!")
                        quiz_all_correct.append(random_entry)
                        save_csv("QuizAllCorrect.csv", quiz_all_correct)
                        break
                    elif synonym:
                        synonyms = [s.strip() for s in synonym.split(',')]
                        if user_definition.lower() in [d.lower() for d in synonyms]:
                            print("Correct, but I am looking for a different word.")
                            user_definition = input("Try again (Ctrl+C to exit): ")
                        else:
                            print("Incorrect!")
                            print(f"Correct definitions: {definition1}, {definition2}")
                            break
                    else:
                        print("Incorrect!")
                        print(f"Correct definitions: {definition1}, {definition2}")
                        break

    except KeyboardInterrupt:
        remaining_count = count_remaining_words(data, quiz_all_correct)
        print(f"Words remaining to be quizzed: {remaining_count}")
        total_quiz_correct = len(quiz_all_correct)
        print(f"Total rows in QuizAllCorrect.csv: {total_quiz_correct}")

def sift_csv(file_path):
    data, modified_data = load_csv(file_path), []

    try:
        random.shuffle(data)

        for row in data:
            modified_row, empty_fields = row.copy(), [key for key, value in row.items() if value == ""]

            if empty_fields:
                print(f"\nRow with Word '{row['Word']}':")
                print('\n'.join([f"{key}: {value}" for key, value in row.items()]))
                modified_row.update({key: input(f"{key} (enter to keep current value): ") or row[key] for key in empty_fields})
                modified_data.append(modified_row)

    except KeyboardInterrupt:
        print("\nSifting process interrupted. Saving the current progress.")

    # Print this line after the for loop
    remaining_rows_with_empty_cells = sum(1 for row in modified_data if any(cell == "" or cell.lower() == 'none' for cell in row.values()))
    print(f"Rows remaining with empty cells or 'none': {remaining_rows_with_empty_cells}")


    for modified_row in modified_data:
        existing_row = next((row for row in data if row['Word'] == modified_row['Word']), None)
        if existing_row:
            existing_row.update(modified_row)
        else:
            data.append(modified_row)

    save_csv(file_path, data)
    print("Sifting complete.")

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
    parser.add_argument('--sift', help='Sift through BisayaLog.csv and input missing values', action='store_true')
    args = parser.parse_args()

    if args.add:
        add_row_interactive(default_file_path)
    elif args.search:
        search_result = search_word(default_file_path, args.search)
        print(search_result) if search_result else print("No matching rows found.")
    elif args.quiz:
        quiz(default_file_path, args.category, args.last, args.english)
    elif args.quizall:
        quiz_all(default_file_path, args.english)
    elif args.quizall_reset:
        quiz_all("BisayaLog.csv", reset=True)
    elif args.sift:
        sift_csv(default_file_path)
    else:
        print("No action specified. Use '--add' to add a new row or '--search' to search for a word.")

if __name__ == "__main__":
    main()
