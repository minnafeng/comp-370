"""Output a TSV file of N random posts from a JSON file of subreddit posts."""

import argparse
import random
import json
import csv


def main():
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--out_file", help="Output file name", required=True)
    parser.add_argument("--json_file", help="JSON file of subreddit posts", required=True)
    parser.add_argument("--num_posts_to_output", type=int, help="Number of posts to output", required=True)

    args = parser.parse_args()

    out_file = args.out_file
    json_file = args.json_file
    num_posts = args.num_posts_to_output

    # load posts from JSON file
    with open(json_file, "r") as f:
        data = json.load(f)

    posts = data["data"]["children"]

    # select N random posts
    if num_posts >= 100:
        selected_posts = posts
    else:
        selected_posts = random.sample(posts, num_posts)

    # write data to TSV file
    with open(out_file, "w") as f:
        writer = csv.writer(f, delimiter="\t")

        headers = ["name", "title", "coding"]
        writer.writerow(headers)

        for post in selected_posts:
            name = post["data"]["author_fullname"]
            title = post["data"]["title"]

            writer.writerow([name, title, ""])


if __name__ == "__main__":
    main()