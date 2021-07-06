#!/usr/bin/env python
import argparse
import gzip

def main():
    prefs = parse_arguments()
    annot = read_gtf(prefs.gtf)
    filtered = filter_gtf(annot,prefs.distance)
    write_gtf(filtered,prefs.outfile)

def write_gtf(annot,outfile):
    pass

def filter_gtf(annot, distance):
    pass

def read_gtf(file):
    pass


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("gtf", type=str)
    parser.add_argument("distance", type=int)
    parser.add_argument("outfile", type=str)
    return parser.parse_args()


if __name__ == "__main__":
    main()