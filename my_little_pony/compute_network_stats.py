import argparse
import networkx as nx
import json


def compute_stats(in_file):
    """
    Compute three most connected characters by degree centrality, weighted
    degree centrality, closeness centrality, and betweenness centrality.
    """
    # open in_file
    with open(in_file, "r") as f:
        interactions = json.load(f)

    g = nx.DiGraph()
    g_weighted = nx.DiGraph()

    # Add nodes and edges with weights
    for source, targets in interactions.items():
        for target, weight in targets.items():
            g.add_edge(source, target)
            g_weighted.add_edge(source, target, weight=weight)

    # Compute centrality measures
    degree_centrality = nx.degree_centrality(g)
    weighted_degree_centrality = nx.degree_centrality(g_weighted)
    closeness_centrality = nx.closeness_centrality(g)
    betweenness_centrality = nx.betweenness_centrality(g)

    # Get top characters for each centrality measure
    top_degree_characters = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:3]
    top_weighted_degree_characters = sorted(weighted_degree_centrality.items(), key=lambda x: x[1], reverse=True)[:3]
    top_closeness_characters = sorted(closeness_centrality.items(), key=lambda x: x[1], reverse=True)[:3]
    top_betweenness_characters = sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[:3]

    # Create the output dictionary
    stats = {
        "degree": [character for character, centrality in top_degree_characters],
        "weighted_degree": [character for character, centrality in top_weighted_degree_characters],
        "closeness": [character for character, centrality in top_closeness_characters],
        "betweenness": [
            character for character, centrality in top_betweenness_characters
        ],
    }

    return stats


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input_file", help="Input json interactions file", required=True
    )
    parser.add_argument(
        "-o", "--output_file", help="Output json stats file", required=True
    )

    in_file = parser.parse_args().input_file
    out_file = parser.parse_args().output_file

    stats = compute_stats(in_file)

    # Output the interactions as a JSON file
    with open(out_file, "w") as json_file:
        json.dump(stats, json_file, indent=4)


if __name__ == "__main__":
    main()
