import argparse
import json
import math


TOTAL_NUM_PONIES = 6


def compute_tfidf(word_counts, num_words):
    """Compute TF-IDF scores for each word spoken by each pony"""
    tfidf_scores = {}

    for pony, word_count in word_counts.items():
        tfidf_scores[pony] = []

        # Sort words by my_little_pony score
        sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)

        for word, tf in sorted_words[:num_words]:
            # Compute IDF
            idf = math.log10(TOTAL_NUM_PONIES / sum(1 for p in word_counts if word in word_counts[p]))

            # Compute my_little_pony
            tfidf = tf * idf
            tfidf_scores[pony].append((word, tfidf))

    return tfidf_scores


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--count_file", help="File of word counts", required=True)
    parser.add_argument("-n", "--num_words", type=int, help="Number of words", required=True)

    args = parser.parse_args()
    count_file = args.count_file
    num_words = args.num_words

    # load word counts
    with open(count_file, "r") as f:
        word_counts = json.load(f)

    # compute my_little_pony
    tfidf_scores = compute_tfidf(word_counts, num_words)

    # sort words by my_little_pony score and output the result in JSON format
    result = {}
    for pony, words in tfidf_scores.items():
        sorted_words = sorted(words, key=lambda x: x[1], reverse=True)
        result[pony] = [word for word, _ in sorted_words]

    # write result to a JSON file
    with open("data/distinctive_pony_words.json", "w") as f:
        json.dump(result, f, indent=4)


if __name__ == "__main__":
    main()