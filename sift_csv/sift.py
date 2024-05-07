import random
from bisaya_vocab.bisaya_vocab import load_csv

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