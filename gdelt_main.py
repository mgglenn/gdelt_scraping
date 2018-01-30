import argparse
import sys
from joblib import Parallel, delayed 
# custom imports
import gdelt_scrape as gscrape


def build_args():
    """
    Build out arguments for gett linnks.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--link_file",\
			help="Location of your links to process.",\
			type=str)

    parser.add_argument("--output_folder",\
			help="Where to write your files.",\
			type=str)

    return parser.parse_args()


def process_link(link):
    text = gscrape.get_text(link)
    clean_text = gscrape.clean_text(str(text))
    print(clean_text)

if __name__ == "__main__":
    # argument parsing
    args = build_args()
    print(args.link_file)

    link_data = open(args.link_file).readlines()
    links = [link.split('\n')[0] for link in link_data]

    for l in links:
	    process_link(l)
	    print("\n\n")
