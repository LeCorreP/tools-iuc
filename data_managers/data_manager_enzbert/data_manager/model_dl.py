#!/usr/bin/env python3

import argparse
import json
import os
import sys
import zipfile
from collections import OrderedDict

import requests


def download_and_unpack_zip(url, dest_dir):

    try:
        # Create directories if they don't exist
        os.makedirs(dest_dir, exist_ok=True)
        zip_path = os.path.join(dest_dir, "DATA.zip")

        # Download the file
        print(f"Download {url}...")
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(zip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded the model to : {zip_path}")

        # Extract the zip file
        print(f"Extracting {dest_dir}...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(dest_dir)
        print(f"Extracted to : {dest_dir}")

    except requests.exceptions.RequestException as e:
        print(f"Download error: {e}")
        sys.exit(1)
    except zipfile.BadZipFile as e:
        print(f"Decompression error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('output_directory', type=str)
    parser.add_argument('json', type=str)
    args = parser.parse_args()

    # URL of the ZIP file to download
    url = "https://zenodo.org/records/10041121/files/data.zip?download=1"

    # Decompression
    download_and_unpack_zip(url, args.output_directory)

    # Generate JSON
    data_manager_entry = OrderedDict([
        ("name", "Enzbert_model"),
        ("path", "enzbert/"),
        ("value", "Enzbert_model")
    ])
    data_manager_json = OrderedDict([
        ("data_tables", OrderedDict([
            ("enzbert", [data_manager_entry])
        ]))
    ])

    try:
        os.makedirs(os.path.dirname(args.json), exist_ok=True)
        with open(args.json, "w") as f:
            json.dump(data_manager_json, f, indent=2)
        print(f"Generated JSON: {args.json}")
    except Exception as e:
        print(f"Error writing JSON: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
