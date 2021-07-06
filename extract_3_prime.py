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

    filtered = filter_gtf(annot,prefs.distance)
    
    write_gtf(filtered,prefs.outfile)

def write_gtf(annot,outfile):
    with gzip.open(outfile,"wt") as out:
        for v in annot.values():
            print(v["gene_gtf"],file=out,end="")
            for e in v["exons"]:
                print(e,file=out,end="")

def filter_gtf(annot, distance):
    filtered_annot = {}
    for gene,value in annot.items():
        value = value.copy()
        value["exons"] = shorten_exons(value["exons"],distance)

        filtered_annot[gene] = value


    return filtered_annot


def shorten_exons(exons,distance):
    """Cut the set of exons down to size"""
    short_exons = []

    split_exons = [x.split("\t") for x in exons]

    # We'll just do different logic for forward and
    # reverse
    if split_exons[0][5] == "+":
        split_exons.sort(key=lambda x: int(x[3]))

    else :
        #It's reverse
        split_exons.sort(key=lambda x: int(x[3]), reverse=True)
        pass

    distance_so_far = 0
    for e in split_exons:
        exon_distance = (int(e[4])-int(e[3]))+1
        if distance_so_far + exon_distance < distance:
            distance_so_far += exon_distance
            short_exons.append(e)

        else:
            # We need to cut this down. For + strand
            # we increase the start, for - strand we
            # decrease the end

            remaining_distance = distance - distance_so_far

            if e[6] == "+":
                e[3] = str(int(e[4])-remaining_distance)
            
            elif e[6] == "-":
                e[4] = str(int(e[3])+remaining_distance)

            else:
                raise ValueError("Strand"+e[6]+" wasn't + or -")

            short_exons.append(e)
            break


    # Re-sort and convert back to text
    short_exons.sort(key=lambda x: int(x[3]))

    short_exons = ["\t".join(x) for x in short_exons]

    return short_exons

def read_gtf(file, canonical):
    genes = {}

    with gzip.open(file, "rt", encoding="UTF-8") as infile:
        for line in infile:

            # Skip comments
            if line.startswith("#"):
                continue

            # Just for testing only do chr1
            if not line.startswith("1"):
                break

            type,attributes = parse_line(line)

            if type=="gene":
                if attributes["gene_biotype"] != "protein_coding":
                    continue

                # Add the gene to the data
                genes[attributes["gene_id"]] = {
                    "gene_gtf" : line,
                    "exons" : []
                }

            elif type=="exon":
                if attributes["transcript_id"] not in canonical:
                    continue
                genes[attributes["gene_id"]]["exons"].append(line)

    
    print("Found",len(genes),"genes")

    return genes


def parse_line(line):
    """Extracts the relevant attributes from a GTF line"""
    line = line.strip()
    sections = line.split("\t")
    type = sections[2]
    attributes = {}
    attribute_pairs = sections[8][:-2].split("\"; ")
#    print("Split into",attribute_pairs)
    for ap in attribute_pairs:
        key,val = ap.split(" \"")

        attributes[key] = val

    return (type,attributes)



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