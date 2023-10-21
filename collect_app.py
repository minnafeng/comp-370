"""App that collects episodes for a given show from TVmaze.com and outputs them to a JSON file."""
import argparse

from collector import collect_episodes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("show_name", help="Name of show to fetch episodes for")
    parser.add_argument("output_path_json", help="Path to output JSON file")
    args = parser.parse_args()

    collect_episodes(args.show_name, args.output_path_json)


if __name__ == "__main__":
    main()
