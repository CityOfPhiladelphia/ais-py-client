import csv
import sys

import click
import client
import logging

@click.command()
@click.option('--map', 'mappings', '-m', type=(unicode, unicode), multiple=True, help="Field to add/replace from the Geocoder. [AIS field name, CSV column name]")
@click.option('--remove', 'removals', '-r', type=unicode, multiple=True, help="Name of column to remove from CSV.")
@click.option('--query', 'query', '-q', type=unicode, multiple=True, help="Name of csv column to use to query AIS. Multiple are tried in order.")
@click.option('--param', 'parameters', '-p', type=(unicode, unicode), multiple=True, help="Additional parameter to pass to AIS")
@click.option('--ais-server', "server", '-s', type=unicode, help="AIS Server URL", default="http://api.phila.gov/ais/v1/")
@click.option('--ais-key', "key", '-k', default="6ba4de64d6ca99aa4db3b9194e37adbf")
@click.option('--input', '-i')
@click.option('--output', '-o')

def geocode(mappings, removals, query, parameters, server, key, input, output):
    if input in ['-', '', None]:
        infile = sys.stdin
    else:
        infile = open(input)

    if input in ['-', '', None]:
        outfile = sys.stdout
    else:
        outfile = open(output, 'w')

    reader = csv.DictReader(infile)
    output_fieldnames = reader.fieldnames[:]

    map_dict = {}

    for ais_name, column_name in mappings:
        if column_name not in output_fieldnames:
            output_fieldnames.append(column_name)
        map_dict[ais_name] = column_name

    params = {"opa_only": True}
    for key, val in parameters:
        params[key] = val

    for removed_fieldname in removals:
        output_fieldnames.remove(removed_fieldname)

    writer = csv.DictWriter(outfile, output_fieldnames)

    rows = [row for row in reader]
    infile.close()

    my_client = client.AISClient(server, key)
    geocoded_rows, errors = my_client.batch_search(rows, query, map_dict, removals, params=params)
    writer.writeheader()
    writer.writerows(geocoded_rows)
    if errors:
        logging.error(errors)
    outfile.close()

if __name__ == "__main__":
    geocode()