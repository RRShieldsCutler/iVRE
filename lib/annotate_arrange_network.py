#!/usr/bin/env python

import argparse
import csv
from collections import defaultdict


# The arg parser for this script
def make_arg_parser():
	parser = argparse.ArgumentParser(description='Annotate a scores table and format for network visualization')
	parser.add_argument('-i', '--input', help='Input is a long format cluster-vs-cluster scores table with columns query, target, and score', required=True)
	parser.add_argument('-o', '--output', help='If nothing is given, then stdout, else write to file', default='-')
	parser.add_argument('-t', '--threshold', help='Score must exceed this value to be included', default=0, required=False)
	parser.add_argument('-m', '--mapping', help='Map the NCBI identifier to the strain name', required=True)
	return parser


def annotate_table(inf, outf, thresh, map_dd):
	df_l = csv.reader(inf, delimiter='\t')
	next(df_l, None)
	stored = set()
	for line in df_l:
		query = line[0]
		target = line[1]
		score = line[2]
		query_refid = '_'.join(query.split('_')[0:2])
		query_species = str(map_dd[query_refid][0])
		query_strain = str(map_dd[query_refid][1])

		# Now for the target strain
		target_refid = '_'.join(target.split('_')[0:2])
		target_species = str(map_dd[target_refid][0])
		target_strain = str(map_dd[target_refid][1])

		# Check for duplicate matches between clusters, A vs B = B vs A.
		pair = set(['|'.join(sorted([query, target]))])
		if query_strain != target_strain and float(score) > thresh:
			if list(pair)[0] not in stored:
				stored.update(pair)
				outf.write(query + '\t' + query_species + '\t' + query_strain + '\t' + target + '\t' + target_species + '\t' + target_strain + '\t' + score)
				outf.write('\n')
		else:
			continue
	return None


def main():
	parser = make_arg_parser()
	args = parser.parse_args()

	# parse command line
	thresh = float(args.threshold)
	if args.mapping:
		map_dd = defaultdict(list)
		with open(args.mapping, 'rU') as infu:
			readit = csv.reader(infu, delimiter='\t')
			next(readit)
			for line in readit:
				map_dd[line[0]] = [line[1], line[2]]
	# Prepare the output file headers and run the annotation script
	with open(args.input, 'r') as inf, open(args.output, 'w') if args.output != '-' else sys.stdout as outf:
		outf.write('query' + '\t' + 'query_species' + '\t' + 'query_strain' + '\t' + 'target' + '\t' + 'target_species' + '\t' + 'target_strain' + '\t' + 'score')
		outf.write('\n')
		annotate_table(inf, outf, thresh, map_dd)
	print('\nFinished\n')

if __name__ == '__main__':
	main()
