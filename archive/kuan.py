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

def quiz_all(file_path, english_mode=False, reset=False, use_wrong_words=False):
    # Load the QuizAllCorrect.csv file, which contains the list of correctly quizzed words
    quiz_all_correct = load_csv("QuizAllCorrect.csv")
    
    # Reset WrongWords.csv if required
    if reset:
        open('WrongWords.csv', 'w').close()  # Clear the file content
        print("WrongWords.csv has been reset.")
    
    # Load the data from the specified file path
    if use_wrong_words:
        # If the use_wrong_words flag is True, use the "WrongWords.csv" file for quizzing
        file_path = os.path.expanduser('WrongWords.csv')
        data = load_csv(file_path)
        
        # Check if WrongWords.csv is empty
        if not data:
            print("There are no words in WrongWords.csv. Please use '--quiz' or '--quizall' instead.")
            return
    else:
        # Otherwise, use the provided file path (default is "BisayaLog.csv")
        data = load_csv(file_path)
    
    # Initialize counters
    correct_count = 0
    total_quizzes = 0
    incorrect_words = []  # To track incorrect words
    
    try:
        while True:
            # Filter out words that have already been quizzed
            remaining_words = [entry for entry in data if entry['Word'] not in {row['Word'] for row in quiz_all_correct}]
            
            # Calculate the remaining words
            remaining_words_count = len(remaining_words)
            print(f"Remaining undefined words in BisayaLog.csv: {remaining_words_count}")
            
            # If there are no remaining words, check if we should repeat incorrect words
            if not remaining_words:
                print("You've been quizzed on all available words!")
                if use_wrong_words:
                    print("Repeating incorrectly answered words from WrongWords.csv.")
                break
            
            # Randomly select a word from remaining words
            random_entry = random.choice(remaining_words)
            word, definition1, definition2 = random_entry['Word'], random_entry['Definition1'], random_entry['Definition2']
            synonym = random_entry.get('Synonym', '')
            
            # For English mode: display definitions and prompt for the word
            if english_mode:
                print(f"Definition: {definition1}, {definition2}")
                if synonym:
                    print(f"Synonym: {synonym}")
                user_input = input("Enter the word (Ctrl+C to exit): ")

                # Check if the user's input is correct
                if user_input.strip().lower() == word.strip().lower() or (synonym and user_input.strip().lower() == synonym.strip().lower()):
                    correct_count += 1
                    print("Correct!")
                    quiz_all_correct.append(random_entry)
                    save_csv("QuizAllCorrect.csv", quiz_all_correct)
                else:
                    print("Incorrect!")
                    print(f"Correct word: {word}")
                    incorrect_words.append(random_entry)  # Add the incorrect word to the list
            
            # For non-English mode: display the word and prompt for the definition
            else:
                print(f"Word: {word}")
                user_input = input("Enter the definition (Ctrl+C to exit): ")

                # Check if the user's input is correct
                if user_input.strip().lower() == definition1.strip().lower() or user_input.strip().lower() == definition2.strip().lower():
                    correct_count += 1
                    print("Correct!")
                    quiz_all_correct.append(random_entry)
                    save_csv("QuizAllCorrect.csv", quiz_all_correct)
                else:
                    print("Incorrect!")
                    print(f"Correct definitions: {definition1}, {definition2}")
                    incorrect_words.append(random_entry)  # Add the incorrect word to the list

            total_quizzes += 1
            
    except KeyboardInterrupt:
        pass

    # Save incorrect words to "WrongWords.csv"
    # Ensure to save entire rows of incorrect words
    if incorrect_words:
        # Load existing incorrect words from "WrongWords.csv"
        existing_incorrect_words = load_csv('WrongWords.csv')
        # Combine new and existing incorrect words and remove duplicates
        all_incorrect_words = existing_incorrect_words + incorrect_words
        all_incorrect_words = [dict(t) for t in {tuple(d.items()) for d in all_incorrect_words}]
        # Save all incorrect words to "WrongWords.csv"
        save_csv('WrongWords.csv', all_incorrect_words)

    # Calculate and print final results
    print(f"Total words quizzed: {total_quizzes}")
    print(f"Correctly defined: {correct_count}")

    # Handle case where total_quizzes is zero
    if total_quizzes > 0:
        accuracy = (correct_count / total_quizzes) * 100
        print(f"Accuracy: {accuracy:.2f}%")
    else:
        print("No quizzes taken.")


def sift_csv(file_path):
    # Load the data without shuffling
    data = load_csv(file_path)
    modified_data = []
    remaining_words_with_empty_cells = 0

    try:
        # Filter rows with missing information
        rows_with_missing_info = [row for row in data if any(not value for value in row.values())]

        while rows_with_missing_info:
            # Randomly select a row from the filtered list
            random_row = random.choice(rows_with_missing_info)

            # Prompt the user for missing fields
            empty_fields = [key for key, value in random_row.items() if not value]
            print(f"\nRow with Word '{random_row['Word']}':")
            print('\n'.join([f"{key}: {value}" for key, value in random_row.items()]))

            # Update the row with user input for missing fields
            modified_row = random_row.copy()
            for key in empty_fields:
                user_input = input(f"{key} (enter to keep current value): ")
                if user_input.strip():
                    modified_row[key] = user_input.strip()

            # Replace the existing row in the data with the modified row
            data[data.index(random_row)] = modified_row

            # Remove the modified row from the list of rows with missing information
            rows_with_missing_info = [row for row in rows_with_missing_info if row != random_row]
            remaining_words_with_empty_cells = len(rows_with_missing_info)

        print(f"Rows remaining with empty cells or 'none': {remaining_words_with_empty_cells}")

    except KeyboardInterrupt:
        print("\nSifting process interrupted. Saving the current progress.")

    # Save the data without shuffling
    save_csv(file_path, data)
    print("Sifting complete.")

def save_wrong_words(file_path, words):
    # Save the incorrect words to a CSV file
    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        for word in words:
            writer.writerow([word])

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
    parser.add_argument('--wrong_words', help='Take a quiz with words the user got wrong previously and prompt for definitions', action='store_true')
    parser.add_argument('--reset', help='Reset WrongWords.csv', action='store_true')
    args = parser.parse_args()

    if args.add:
        add_row_interactive(default_file_path)
    elif args.search:
        search_result = search_word(default_file_path, args.search)
        print(search_result) if search_result else print("No matching rows found.")
    elif args.quiz:
        quiz(default_file_path, args.category, args.last, args.english)
    elif args.quizall:
        quiz_all(default_file_path, args.english, reset=args.reset, use_wrong_words=args.wrong_words)
    elif args.quizall_reset:
        quiz_all("BisayaLog.csv", reset=True)
    elif args.sift:
        sift_csv(default_file_path)
    else:
        print("No action specified. Use '--add' to add a new row or '--search' to search for a word.")

if __name__ == "__main__":
    main()
