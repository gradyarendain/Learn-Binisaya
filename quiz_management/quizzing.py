import os
import csv
import random
from bisaya_vocab.bisaya_vocab import load_csv, save_csv

path_to_BisayaLog = "/home/grady/Learn-Binisaya/data/BisayaLog.csv"
path_to_WrongWords = "/home/grady/Learn-Binisaya/data/WrongWords.csv"
path_to_QuizAllCorrect = "/home/grady/Learn-Binisaya/data/QuizAllCorrect.csv"

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

def quiz_all(file_path, english_mode=False, reset=False, use_wrong_words=False):
    # Load the QuizAllCorrect.csv file, which contains the list of correctly quizzed words
    quiz_all_correct = load_csv(path_to_QuizAllCorrect)
    
    # Reset WrongWords.csv if required
    if reset:
        open(path_to_WrongWords, 'w').close()  # Clear the file content
        open(path_to_QuizAllCorrect, 'w').close()  # Clear the file content
        print("WrongWords.csv has been reset.")
    
    # Load the data from the specified file path
    if use_wrong_words:
        # If the use_wrong_words flag is True, use the "WrongWords.csv" file for quizzing
        file_path = os.path.expanduser(path_to_WrongWords)
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
                    save_csv(path_to_QuizAllCorrect, quiz_all_correct)
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
                    save_csv(path_to_QuizAllCorrect, quiz_all_correct)
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
        existing_incorrect_words = load_csv(path_to_WrongWords)
        # Combine new and existing incorrect words and remove duplicates
        all_incorrect_words = existing_incorrect_words + incorrect_words
        all_incorrect_words = [dict(t) for t in {tuple(d.items()) for d in all_incorrect_words}]
        # Save all incorrect words to "WrongWords.csv"
        save_csv(path_to_WrongWords, all_incorrect_words)

    # Calculate and print final results
    print(f"Total words quizzed: {total_quizzes}")
    print(f"Correctly defined: {correct_count}")

    # Handle case where total_quizzes is zero
    if total_quizzes > 0:
        accuracy = (correct_count / total_quizzes) * 100
        print(f"Accuracy: {accuracy:.2f}%")
    else:
        print("No quizzes taken.")
