"""CLI tool for collecting news articles from various sources."""
import argparse
import json
import os

from newscover.newsapi import fetch_latest_news


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--api_key", required=True, help="NewsAPI API key")
    parser.add_argument("-b", "--lookback_days", type=int, help="Number of lookback days")
    parser.add_argument("-i", "--input_file", required=True, help="Input file containing news keywords")
    parser.add_argument("-o", "--output_dir", required=True, help="Output directory for news articles")

    args = parser.parse_args()

    api_key = args.api_key
    lookback_days = args.lookback_days
    input_file = args.input_file
    output_dir = args.output_dir


    with open(input_file, "r") as file:
        keyword_sets = json.load(file)

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Iterate through each keyword set and fetch news
    for name, keywords in keyword_sets.items():
        results = fetch_latest_news(api_key, keywords, lookback_days)

        # Write the results to a JSON file in the output directory
        output_file = os.path.join(output_dir, f"{name}.json")
        with open(output_file, "w") as outfile:
            json.dump(results, outfile, indent=4)

if __name__ == "__main__":
    main()
