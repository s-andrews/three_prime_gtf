#!/usr/bin/env python
import argparse
import gzip
from pathlib import Path

def main():
    prefs = parse_arguments()

    # The canonical transcripts aren't listed in the GTF
    # file, which would have been useful.  I've therefore
    # had to export them from biomart and put them in a 
    # file
    canonical_transcripts = read_canonical()

    # Read the GTF but keeping only transcripts in the
    # canonical list and protein coding genes
    annot = read_gtf(prefs.gtf, canonical_transcripts)

    
    # filtered = filter_gtf(annot,prefs.distance)
    # write_gtf(filtered,prefs.outfile)

def write_gtf(annot,outfile):
    pass

def filter_gtf(annot, distance):
    pass

def read_gtf(file):
    data = {}

    with gzip.open(file, "rt", encoding="UTF-8") as infile:
        for line in infile:

            # Skip comments
            if line.startswith("#"):
                continue


            print(line)


def read_canonical():
    canonical_transcripts = set()

    canonical_file = Path(__file__).parent.joinpath("grch38_canonical.txt")

    with open(canonical_file) as canon:
        for line in canon:
            transcript, canonical = line.split("\t")[0:2]
            if canonical:
                canonical_transcripts.add(transcript)

    print("Found",len(canonical_transcripts),"canonical protein coding transcripts")
    return canonical_transcripts


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("gtf", type=str)
    parser.add_argument("distance", type=int)
    parser.add_argument("outfile", type=str)
    return parser.parse_args()


if __name__ == "__main__":
    main()