from pathlib import Path
import requests
import argparse

import bs4

REL_TABLE_FIELDS = [
    "NUM",
    "NAME",
    "TYPE",
    "RUMOR",
    "START",
    "END",
    "DURATION",
]


def get_celebrity_html_data(name):
    """Get the HTML data for a given celebrity name."""
    # format name for URL
    name = name.lower().replace(" ", "-")

    fpath = Path(f"{name}.html")  # output file path

    if not fpath.exists():  # if data not already downloaded
        # get data from website
        data = requests.get(f"https://www.whosdatedwho.com/dating/{name}")

        # cache html data
        with open(fpath, "w") as f:
            f.write(data.text)

    # return html data
    with open(fpath) as f:
        return f.read()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="Name of celebrity")

    args = parser.parse_args()

    name = args.name

    html_data = get_celebrity_html_data(name)

    soup = bs4.BeautifulSoup(html_data, "html.parser")

    table_div = soup.find("div", id="ff-dating-history-table")
    rel_table = table_div.find("table")

    # print each relationship from the table
    rows = rel_table.find_all("tr")
    for i, row in enumerate(rows):
        if i == 0:
            continue

        cells = row.find_all("td")

        relationship = {}
        for field, cell in zip(REL_TABLE_FIELDS, cells):
            relationship[field] = cell.text.strip()

        print(relationship)

        # Alternate method
        # rel_num = cells[0].text.strip()
        # rel_name = cells[1].text.strip()
        # rel_type = cells[2].text.strip()
        # rel_start = cells[3].text.strip()
        # rel_end = cells[4].text.strip()
        # rel_duration = cells[5].text.strip()
        #
        # print(rel_num, rel_name, rel_type, rel_start, rel_end, rel_duration)


if __name__ == "__main__":
    main()
