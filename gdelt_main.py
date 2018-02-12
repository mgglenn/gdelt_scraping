import argparse
import sys
from joblib import Parallel, delayed 
# custom imports
import gdelt_scrape as gscrape


def build_args():
    """
    Build out arguments for getting linnks.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("--start_date",\
			help="What date do we start collecting on? YYYY-MM-DD format.",\
			type=str)

    parser.add_argument("--end_date",\
			help="What date do we start collecting on? YYYY-MM-DD format.",\
			type=str)

    parser.add_argument("--output_folder",\
			help="Where are we outputting the files (one per day)?.",\
			type=str)

    return parser.parse_args()


def process_date(link=None, folder=''):
    # Download CSV
    csv_file = gscrape.extract_csv(link=link, path=folder)

    # grab the links from the CSV and start scraping them
    links = gscrape.grab_links(filename=csv_file)
    outfile = csv_file[:csv_file.index(".CSV")] + ".txt"

    links_written = 0
    out = open(outfile, 'w')
    for link in links:
        text = gscrape.get_text(link=link)
        if text != '':
            try:
                out.write(text)
                out.write('\n')
                links_written = links_written + 1
            except:
                continue

    return (links_written, len(links))	


if __name__ == "__main__":
    # argument parsing
    args = build_args()

    # generate some links
    links = gscrape.generate_links(start=args.start_date, end=args.end_date)	
    print(links)
    process_date(links[0], folder=args.output_folder)
