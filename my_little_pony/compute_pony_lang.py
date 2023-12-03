import argparse
import json
import math


TOTAL_NUM_PONIES = 6


def compute_top_tfidf(word_counts, num_words):
    """
    Compute TF-IDF scores for each word spoken by each pony and
    return dict of the top num_words for each pony.
    """
    tfidf_scores = {}

    # tf-idf(w, pony, script) = tf(w, pony) x idf(w, script)
    # tf(w, pony) = number of times word w is spoken by pony / total number of words spoken by pony
    # idf(w, script) = log10(total number of ponies / number of ponies that speak word w)

    for pony, word_count in word_counts.items():
        tfidf_scores[pony] = []

        # get total number of words spoken by the current pony
        total_words = sum(word_count.values())

        # Compute tf-idf for each word
        for word, count in word_count.items():
            tf = count #/ total_words
            idf = math.log10(TOTAL_NUM_PONIES / sum(1 for p in word_counts if word in word_counts[p]))
            tfidf = tf * idf
            tfidf_scores[pony].append((word, tfidf))

        # Sort words by score and keep only the top num_words
        tfidf_scores[pony] = sorted(tfidf_scores[pony], key=lambda x: x[1], reverse=True)[:num_words]

    # return top words for each pony
    top_words = {pony: [word for word, score in words] for pony, words in tfidf_scores.items()}

    return top_words


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
    top_words = compute_top_tfidf(word_counts, num_words)

    # write result to a JSON file
    with open("data/distinctive_pony_words.json", "w") as f:
        json.dump(top_words, f, indent=4)


if __name__ == "__main__":
    main()