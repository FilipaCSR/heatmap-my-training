#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Apple Health Export → CSV
=========================
Converts Apple Health's `export.xml` into a clean, readable `.csv` file.
Perfect for analysis, visualization, or loading into your own tools.

Author: Filipa CSR (based on script by Jason Meno)
Version: 1.0.0
License: BSD-2-Clause
"""

import os
import pandas as pd
import xml.etree.ElementTree as ET
import datetime as dt
import sys


def preprocess_to_temp_file(file_path: str) -> str:
    """
    Removes problematic characters and skips broken DTD markup.
    Creates a cleaned temporary XML file.
    """
    print("Pre-processing XML...", end=" ")
    sys.stdout.flush()

    temp_file_path = "temp_cleaned_export.xml"
    with open(file_path, 'r') as infile, open(temp_file_path, 'w') as outfile:
        skip_dtd = False
        for line in infile:
            if '<!DOCTYPE' in line:
                skip_dtd = True
            if not skip_dtd:
                line = line.replace("\x0b", "")  # Strip invisible characters
                outfile.write(line)
            if ']>' in line:
                skip_dtd = False

    print("done.")
    return temp_file_path


def xml_to_csv(file_path: str) -> pd.DataFrame:
    """
    Parses the XML file and extracts all health records into a Pandas DataFrame.
    """
    print("Parsing and converting to DataFrame...", end=" ")
    sys.stdout.flush()

    records = []

    for _, elem in ET.iterparse(file_path, events=('end',)):
        if elem.tag == 'Record':
            record = elem.attrib
            for child in elem:
                if len(child.attrib) == 2:
                    record.update({list(child.attrib.values())[0]: list(child.attrib.values())[1]})
            records.append(record)
        elem.clear()  # Save memory

    df = pd.DataFrame(records)

    # Clean column names
    df['type'] = df['type'].str.replace('HKQuantityTypeIdentifier', '', regex=False)
    df['type'] = df['type'].str.replace('HKCategoryTypeIdentifier', '', regex=False)
    df.columns = df.columns.str.replace("HKCharacteristicTypeIdentifier", "", regex=False)

    # Set preferred column order
    col_order = ['type', 'sourceName', 'value', 'unit', 'startDate', 'endDate', 'creationDate']
    remaining = [col for col in df.columns if col not in col_order]
    df = df[col_order + remaining]

    # Sort by newest first
    df['startDate'] = pd.to_datetime(df['startDate'], errors='coerce')
    df.sort_values('startDate', ascending=False, inplace=True)

    print("done.")
    return df


def save_to_csv(df: pd.DataFrame, output_path: str = None):
    """
    Saves the DataFrame to a CSV file.
    """
    if not output_path:
        today = dt.datetime.now().strftime('%Y-%m-%d')
        output_path = f"apple_health_export_{today}.csv"

    print(f"Saving CSV to {output_path}...", end=" ")
    df.to_csv(output_path, index=False)
    print("done.")


def remove_temp_file(file_path: str):
    if os.path.exists(file_path):
        os.remove(file_path)


def main():
    file_path = "export.xml"
    if not os.path.exists(file_path):
        print("❌ File 'export.xml' not found. Place it in the same folder as this script.")
        return

    temp_file = preprocess_to_temp_file(file_path)
    df = xml_to_csv(temp_file)
    save_to_csv(df)
    remove_temp_file(temp_file)


if __name__ == '__main__':
    main()