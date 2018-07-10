"""
CSV Splitter

Description
-----------
Split large CSV into smaller files.

Adjusted for GILBypasser Package from Source

Author
------
Beom Jin Lee <cluesbj@berkeley.edu>

Source
------
https://gist.github.com/palewire/596056
"""

import os
import csv
import sys


def split(file, delimiter = ',', row_limit = 10000,
          output_name_template = 'output_%s.csv', output_path = '.',
          keep_headers = True):
    """ Splits a CSV file into multiple pieces.

    Arguments
    ---------
    `row_limit`: The number of rows you want in each output file. 10,000 by default.
    `output_name_template`: A %s-style template for the numbered output files.
    `output_path`: Where to stick the output files.
    `keep_headers`: Whether or not to print the headers in each output file.

    Example usage
    -------------
    >> from GILBypasser import csv_splitter;
    >> csv_splitter.split(open('/home/brian_lee/input.csv', 'r'));
    """
    reader = csv.reader(file, delimiter=delimiter)
    current_piece = 1
    current_out_path = os.path.join(
        output_path,
        output_name_template % current_piece
    )

    current_out_writer = csv.writer(
        open(current_out_path, 'wb'), delimiter = delimiter)

    current_limit = row_limit

    if keep_headers:
        headers = reader.next()
        current_out_writer.writerow(headers)

    for i, row in enumerate(reader):
        if i + 1 > current_limit:
            current_piece += 1
            current_limit = row_limit * current_piece

            current_out_path = os.path.join(
                output_path,
                output_name_template % current_piece
            )

            current_out_writer = csv.writer(
                open(current_out_path, 'wb'), delimiter=delimiter)

            if keep_headers:
                current_out_writer.writerow(headers)

        current_out_writer.writerow(row)


if __name__ == "__main__":
    rfile = sys.argv[0]
    num_files_split = sys.argv[1]

    num_lines = sum(1 for line in open(rfile))
    split_lines = num_lines // num_files_split + 1

    split(rfile, row_limit=split_lines)
