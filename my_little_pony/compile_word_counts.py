import argparse
import json
import string

import pandas as pd


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--out_file", help="Output file for JSON file", required=True)
    parser.add_argument("-d", "--dialogue_file", help="File of clean ponies dialogue", required=True)

    args = parser.parse_args()
    out_file= args.out_file
    dialogue_file = args.dialogue_file

    # Create dictionary of word counts
    pony_word_counts = {"Twilight Sparkle": {}, "Applejack": {}, "Rarity": {}, "Pinkie Pie": {}, "Rainbow Dash": {}, "Fluttershy": {}}

    # Load stopwords
    with open("data/stopwords.txt", "r") as stopwords_file:
        stopwords = set(stopwords_file.read().split())

    # Load CSV file
    df = pd.read_csv(dialogue_file)

    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
        pony = row["pony"]
        if pony not in pony_word_counts:
            continue

        dialog = row["dialog"]

        # Tokenize the dialog into words (remove punctuation)
        words = dialog.lower().translate(str.maketrans("", "", string.punctuation)).split()

        for word in words:
            # Update word count for the current pony
            pony_word_counts[pony][word] = pony_word_counts[pony].get(word, 0) + 1

    # Filter out words with a frequency less than or equal to 5 and stopwords
    filtered_word_counts = {}
    for pony, word_count in pony_word_counts.items():
        filtered_word_counts[pony] = {word: count for word, count in word_count.items() if
                                      count > 5 and word not in stopwords}

    # Write the word counts to a JSON file
    with open(out_file, "w") as f:
        json.dump(filtered_word_counts, f, indent=4)


if __name__ == "__main__":
    main()