import pandas as pd
import json
import argparse


def build_network(in_file):
    """Build network of interactions between ponies."""
    # Read the CSV file
    df = pd.read_csv(in_file, header=0)

    # Create a dictionary to store interactions
    interactions = {}
    forbidden_words = ["other", "ponies", "and", "all"]

    # Iterate through each episode
    for episode, group in df.groupby('title'):

        for _, row in group.iterrows():
            speaker = row['pony']

            for word in forbidden_words:
                if word in speaker:
                    continue

            # Find the index of the current row in the group
            i = row.name

            # Skip if it's the last row in the group
            if i == group.index[-1]:
                continue

            # Get the next speaker
            next_speaker = group.at[i + 1, 'pony']

            for word in forbidden_words:
                if word in next_speaker:
                    i = i + 1
                    continue

            # Skip if the speaker is the same as the next_speaker
            if speaker == next_speaker:
                continue

            # Add the interaction to the dictionary
            if speaker not in interactions:
                interactions[speaker] = {}

            if next_speaker not in interactions:
                interactions[next_speaker] = {}

            if next_speaker not in interactions[speaker]:
                interactions[speaker][next_speaker] = 1
                interactions[next_speaker][speaker] = 1
            else:
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