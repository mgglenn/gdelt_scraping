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
    print("Downloading...")
    gscrape.extract_links(link=link, data_path=folder)
    

if __name__ == "__main__":
    # argument parsing
    args = build_args()

	# generate some links
    links = gscrape.generate_links(start=args.start_date, end=args.end_date)	
    print(links[0])
