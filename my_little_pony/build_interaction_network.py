import pandas as pd
import json
import argparse


def build_network(in_file):
    """Build network of interactions between ponies."""
    # Read the CSV file
    df = pd.read_csv(in_file)

    # Create a dictionary to store interactions
    interactions = {}
    forbidden_words = ["other", "ponies", "and", "all"]

    # Go through each episode
    for episode, group in df.groupby('title'):

        # Go through each line in the episode
        for _, row in group.iterrows():
            speaker = row['pony']

            # get indices of current and next speaker
            i = row.name
            if i != group.index[-1]:  # skip if last line of episode
                next_speaker = group.at[i + 1, 'pony']

                # check for forbidden words and if same speaker
                if not any(word in next_speaker for word in forbidden_words) and speaker != next_speaker:
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