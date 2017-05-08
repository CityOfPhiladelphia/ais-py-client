import csv
import sys

import click
import smart_open

import client

@click.command()
@click.option('--map', '-m', type=(unicode, unicode), multiple=True)
@click.option('--remove', '-r', type=unicode, multiple=True)
@click.option('--query', '-q', type=unicode)
@click.argument('input')
@click.argument('output')
def geocode(mappings, removals, query_column, input, output):
    if input == '-' or input == '':
        infile = sys.stdin
    else:
        infile = smart_open.smart_open(input)

    if output == '-' or output == '':
        outfile = sys.stdout
    else:
        outfile = smart_open.smart_open(output)

    reader = csv.DictReader

if __name__ == "__main__":
    geocode()