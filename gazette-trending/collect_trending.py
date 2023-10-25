from pathlib import Path
import requests
import argparse
import json

import bs4

def get_html_data(url):
    """Get the HTML data from the given URL."""
    # get file name from url
    url_split = url.split("/")

    if url_split[-1] == "":
        file_name = url_split[-2]
    else:
        file_name = url_split[-1]

    # get cache file path
    fpath = Path(f"{file_name}.html")

    # check if cache file exists
    if not fpath.exists():
        # retrieve data from website
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        data = requests.get(url, headers=headers)

        # cache html data
        with open(fpath, "w") as f:
            f.write(data.text)

    # return html data
    with open(fpath) as f:
        return f.read()


def get_trending_links(url):
    """Get the subfolder links of the 5 trending stories on the newspaper homepage."""
    html_data = get_html_data(url)

    soup = bs4.BeautifulSoup(html_data, "html.parser")

    trending_div = soup.find("div", class_="list-widget-trending")
    trending_list = trending_div.find("ol")

    links = []
    for list_item in trending_list.find_all("li"):
        link = list_item.find("a")
        links.append(link["href"])

    return links


def scrape_article(url):
    """Scrape the article at the given URL."""
    html_data = get_html_data(url)

    soup = bs4.BeautifulSoup(html_data, "html.parser")

    # get article info
    title = soup.find("h1", id="articleTitle").text.strip()
    publication_date = soup.find("span", class_="published-date__since").text.strip()
    author = soup.find("span", class_="published-by__author").text.strip()
    blurb = soup.find("p", class_="article-subtitle").text.strip()

    info_dict = {"title": title, "publication_date": publication_date, "author": author, "blurb": blurb}

    return info_dict

def main():
    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", help="output file name")
    args = parser.parse_args()

    output_file = args.output

    base_url = "https://montrealgazette.com"

    # get subfolder links of trending stories
    sub_links = get_trending_links(base_url + "/category/news/")

    # scrape articles and store info in list
    articles_info = []

    for sub_link in sub_links:
        info_dict = scrape_article(base_url + sub_link)
        articles_info.append(info_dict)

    # write info to json file
    with open(output_file, "w") as f:
        json.dump(articles_info, f, indent=4)

if __name__ == "__main__":
    main()