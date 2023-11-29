# my_little_pony

## Description
Using the following dataset from Kaggle: https://www.kaggle.com/datasets/liury123/my-little-pony-transcript,
I perform data analysis and network analysis on the transcripts of the show My Little Pony: Friendship is Magic.

## Usage
To compile the word counts for each pony and save them as a json file, run the following command:
```bash
python compile_word_counts.py -o </path/to/word_counts.json> -d </path/to/clean_dialog.csv>
```

To compile most frequent words said by each pony based on tf-idf and save them as a json file, run the following command:
```bash
python compute_pony_lang.py -c </path/to/word_counts.json> -n <number-of-top-words-to-obtain>
```

To build the interaction network between all ponies and save it as a json file, run the following command:
```bash
python build_interaction_network.py -i </path/to/script_input.csv> -o </path/to/interaction_network.json>
```

To compute the stats for network analysis and save them as a json file, run the following command:
```bash
python compute_network_stats.py -i </path/to/interaction_network.json> -o </path/to/stats.json>
```