#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script scrapes Sigma-Aldrich MSDS pdf files for hazard statements as required by Aalto University School of Chemical Engineering requirements.

Juha Siitonen 5.2.2025
Juha Siitonen 29.6.2023
Aalto University

This project is licensed under the terms of the MIT license.

Example:

    Directory msds\ contains MSDS pdf files (example.pdf, example1.pdf, example2.pdf, example3.pdf, example4.pdf) downloaded from Sigma-Aldrich website.

    msds\
        example1.pdf
        example2.pdf
        example3.pdf
        example4.pdf
    
    Running the script in the directory:

        $ python3 msds_scrape.py
    
    Will output the following:

        ETOS group A!lto MSDS scaper
        4 MSDS files found in the directory

        File: example.pdf (1/4)
        --------------------------------
        Compound name: Potassium cyanide EMPLURA®
        Compound CAS: 151-50-8
        Red flag: Yes
        Particularily hazardous: Yes
        CMR chemical: Yes
        CMR H-phrases: H372
        Other H and EU Phrases chemical: H300, H310, H330

        File: example2.pdf (2/4)
        --------------------------------
        Compound name: n-Butyllithium solution
        Compound CAS: NOT FOUND IN MSDS
        Red flag: Yes
        Particularily hazardous: Yes
        CMR chemical: Yes
        CMR H-phrases: H361, H373
        Other H and EU Phrases: No

        File: example3.pdf (3/4)
        --------------------------------
        Compound name: Sodium azide extra pure
        Compound CAS: 26628-22-8
        Red flag: Yes
        Particularily hazardous: Yes
        CMR chemical: Yes
        CMR H-phrases: H373
        Other H and EU Phrases chemical: H300, H310, H330

        File: example4.pdf (4/4)
        --------------------------------
        Compound name: Water
        Compound CAS: 7732-18-5
        Red flag: No
        Particularily hazardous: No
        CMR chemical: No
        Other H and EU Phrases: No

    Todo:
        * Allow for other MSDS formats
        * Scraper directly with CAS-numbers
"""

import PyPDF3
from os import listdir
import re

# Define red flags
RED_FLAGS = ("H340", "H341", "H350", "H350i", "H360", "H360D", "H360Df", "H360F", "H360FD", "H360Fd", "H361", "H361d", "H361df", "H362", "H370", "H371", "H372", "H373", "H300", "H301", "H310", "H311", "H330", "H331", "UEH001", "EUH006", "EUH019", "EUH029", "EUH031", "EUH32", "EUH044", "EUH070", "EUH071")
CMR_FILTER = ("H340", "H350", "H341", "H350", "H350i", "H351", "H360", "H360D", "H360Df", "H360F", "H360FD", "H360Fd", "H361", "H361d", "H361f", "H361fd", "H362", "H370", "H371", "H372", "H373")
OTHER_FILTER = ("H300", "H301", "H310", "H311", "H330", "H331", "EUH001", "EUH006", "EUH019", "EUH029", "EUH031", "EUH032", "EUH044", "EUH070", "EUH071")

# Extract text using regexp
def extract_text(text, pattern):
    match = re.search(pattern, text, re.DOTALL)
    if match:
        extracted_text = match.group(1).strip()
        return extracted_text
    else:
        return None

def extract_first_page_info(pdf_reader):
    # Collect the compound name and CAS number from the first page
    first_page = pdf_reader.getPage(0).extractText().replace('\n', '')

    # Get the name and MSDS, this assumes Sigma-Aldrich style MSDS
    name = extract_text(first_page, r"Product name :(.*?)Product Number")
    cas = extract_text(first_page, r"CAS-No. :(.*?)1.2")

    return name, cas

def extract_hazard_statements(pdf_reader):
    # This list will contain all the red flag hazard statements
    statements = []

    # Go through the document and check for red flags appearing on each page
    for pageIndex in range(0, pdf_reader.getNumPages()):
        page_obj = pdf_reader.getPage(pageIndex)
        page_text = page_obj.extractText()

        # Add to results if a new red flag statement was found
        results = [statement for statement in RED_FLAGS if statement in page_text and statement not in statements]

        # Append any new ones to the masterlist
        if results:
            statements = statements + results

    return statements

if __name__ == "__main__":
    # Check for all pdfs in the current directory
    all_files = [file for file in listdir() if file.endswith(".pdf")]
    no_of_files = len(all_files)

    # Print the initialization text
    print("ETOS group A!lto MSDS parser")
    print(f"{no_of_files} MSDS files found in the directory")
    print()

    # Go through all the files
    for index, file in enumerate(all_files):
        # Read the file and extract key information
        with open(file, 'rb') as pdf_file:
            pdf_reader = PyPDF3.PdfFileReader(pdf_file)

            name, cas = extract_first_page_info(pdf_reader)
            statements = extract_hazard_statements(pdf_reader)

        # Filter out CMR chemical (Yes/No, which statements)
        cmr_statements = [statement for statement in statements if statement in CMR_FILTER]

        # Filter out other statements with major risks (Yes/No, which statements)
        other_statements = [statement for statement in statements if statement in OTHER_FILTER]

        # Output stage

        print(f"File: {file} ({index + 1}/{no_of_files})")
        print("--------------------------------")

        print("Compound name:", name if name else "NOT FOUND IN MSDS")
        print("Compound CAS:", cas if cas else "NOT FOUND IN MSDS")

        # Particularily hazardous substance (Yes/No)
        print("Particularily hazardous:", "Yes" if statements else "No")

        # CMR (Yes/No)
        print("CMR chemical:", "Yes" if cmr_statements else "No")

        # H-prases associated with CMR in any
        if cmr_statements:
            print(f"CMR H-phrases: {', '.join(cmr_statements)}")

        # Other major risk (Yes/No)
        print("Other major risk chemical:", "Yes" if other_statements else "No")

        # H-phrases associated with other major risk if any
        if other_statements:
            print(f"Other H-phrases: {', '.join(other_statements)}")
    
        print()
