import argparse
import os
from bisaya_vocab.bisaya_vocab import add_row_interactive, search_word
from quiz_management.quizzing import quiz, quiz_all
from sift_csv.sift import sift_csv

def main():
    default_file_path = os.path.expanduser('/home/grady/Learn-Binisaya/data/BisayaLog.csv')

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
