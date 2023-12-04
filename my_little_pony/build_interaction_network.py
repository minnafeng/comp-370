import pandas as pd
import json
import argparse


def build_network(in_file):
    """Build network of interactions between ponies."""
    # Read the CSV file
    df = pd.read_csv(in_file)

    # Get the top 101 most frequent characters and convert to lowercase
    top_characters = df['pony'].value_counts().head(101).index.tolist()
    top_characters = [character.lower() for character in top_characters]

    # Create a dictionary to store interactions
    interactions = {}

    # List of words to not count as speakers
    forbidden_words = ["other", "others", "ponies", "and", "all"]

    # Go through each episode
    for episode, group in df.groupby('title'):

        # Go through each line in the episode
        for _, row in group.iterrows():
            speaker = row['pony'].lower()

            # get index of current speaker
            i = row.name

            # skip if last line of episode
            if i == group.index[-1]:  # skip if last line of episode
                continue

            next_speaker = group.at[i + 1, 'pony'].lower()

            # skip if any speaker not in top_characters
            if speaker not in top_characters or next_speaker not in top_characters:
                continue

            # check for forbidden words and if same speaker
            if any (word in speaker for word in forbidden_words) or \
                    any(word in next_speaker for word in forbidden_words) or \
                    speaker == next_speaker:
                continue

            # ensure all necessary keys exist
            interactions.setdefault(speaker, {}).setdefault(next_speaker, 0)
            interactions.setdefault(next_speaker, {}).setdefault(speaker, 0)

            # increment the interaction count
            interactions[speaker][next_speaker] += 1
            interactions[next_speaker][speaker] += 1

    return interactions

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_file", help="Input csv dialogue file", required=True)
    parser.add_argument("-o", "--output_file", help="Output json interactions file", required=True)

    in_file = parser.parse_args().input_file
    out_file = parser.parse_args().output_file

    interactions = build_network(in_file)

    # Output the interactions as a JSON file
    with open(out_file, 'w') as json_file:
        json.dump(interactions, json_file, indent=4)


if __name__ == '__main__':
    main()