#!/usr/bin/env python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('inf', type=str, help='Input file')
parser.add_argument('outf', type=str, help='Output file')
args = parser.parse_args()

# --------- some transform

with open(args.inf, 'r') as file:
    data = file.read()

with open(args.outf, 'w+') as file:
    file.write(data)
# ---------
