#!/usr/bin/env python                                                                     

import argparse
import csv
import sys
from joblib import Parallel, delayed 
import numpy
from mpi4py import MPI
import random

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


def process_date(link=None, folder='', limit=1000):
    """
        TIME STAMP, ID, LINK, TEXT
    """ 
    # Download CSV
    csv_file = gscrape.extract_csv(link=link, path=folder)

    # grab the links from the CSV and start scraping them
    data = gscrape.grab_csv_data(filename=csv_file)
    new_data = []

    random.shuffle(data)

    outfile = csv_file[:csv_file.index(".CSV")] + ".data.csv"

    links_written = 0
    out = open(outfile, 'w')

    # crawl through randomly shuffled events until we have 1000
    with open(outfile, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for event in data:
            new_row = list(event)
            text = gscrape.get_text(link=new_row[-1])
            if text != '':
                try:
                    new_row.append(text)
                    writer.writerow(new_row)
                    links_written = links_written + 1

                    if links_written >= limit:
                        break
                except:
                        continue


if __name__ == "__main__":
    # argument parsing
    args = build_args()

    # dist stuff
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    num = comm.Get_size()

    link_buckets = []
    for i in range(0, num):
        link_buckets.append([])

    # generate some links
    links = gscrape.generate_links(start=args.start_date, end=args.end_date)	

    for i, link in enumerate(links):
        link_buckets[i%num].append(link)    
    
    for link in link_buckets[rank]:
        process_date(link=link, folder=args.output_folder)
