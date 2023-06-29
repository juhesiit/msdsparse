#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script scrapes Sigma-Aldrich MSDS pdf files for hazard statements as required by Aalto University School of Chemical Engineering requirements.

Juha Siitonen, ETOS group 29.6.2023
https://etosgroup.fi/
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

import PyPDF2
from os import listdir
import re

# Define red flags
redFlags = ["H340", "H341", "H350", "H350i", "H360", "H360D", "H360Df", "H360F", "H360FD", "H360Fd", "H361", "H361d", "H361df", "H362", "H370", "H371", "H372", "H373", "H300", "H301", "H310", "H311", "H330", "H331", "UEH001", "EUH006", "EUH019", "EUH029", "EUH031", "EUH32", "EUH044", "EUH070", "EUH071"]
cmrFilter = ["H340", "H350", "H341", "H350", "H350i", "H351", "H360", "H360D", "H360Df", "H360F", "H360FD", "H360Fd", "H361", "H361d", "H361f", "H361fd", "H362", "H370", "H371", "H372", "H373"]
otherFilter = ["H300", "H301", "H310", "H311", "H330", "H331", "EUH001", "EUH006", "EUH019", "EUH029", "EUH031", "EUH032", "EUH044", "EUH070", "EUH071"]

# Extract text using regexp
def extract_text(text, pattern):
    pattern = pattern
    match = re.search(pattern, text, re.DOTALL)
    if match:
        extracted_text = match.group(1).strip()
        return extracted_text
    else:
        return None

# Check for all pdfs in the current directory
allFiles = listdir()
allFiles = [i for i in allFiles if '.pdf' in i]
totalNumberOfFiles = len(allFiles)

# Print the initialization text
print("ETOS group A!lto MSDS scaper")
print("{} MSDS files found in the directory".format(totalNumberOfFiles))
print()



# Go through all the files
for index,f in enumerate(allFiles):
    print("File: " + f + " (" + str(index+1) + "/" + str(totalNumberOfFiles) + ")")
    print("--------------------------------")
    # Read the file
    pdfFile = open(f, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFile)
    documentPagesMax = pdfReader.numPages

    # Collect all found red flag statements in this list
    collectedStatements = []

    # Collect the compound name and CAS number from the first page
    pageObj = pdfReader.getPage(0)
    firstPage = pageObj.extractText().replace('\n', '')

    # Check to find a name for the chemical, this assumes Sigma-Aldrich style MSDS
    name = extract_text(firstPage, r"Product name(.*?)Product Number")

    if name:
        print("Compound name" + name)
    else:
        print("Compound name: NOT FOUND IN MSDS")

    # Check to find a CAS No for the chemical, this assumes Sigma-Aldrich style MSDS
    cas = extract_text(firstPage, r"CAS-No.(.*?)1.2")

    if cas:
        print("Compound CAS" + cas)
    else:
        print("Compound CAS: NOT FOUND IN MSDS")
    
    # This list will contain all the red flag hazard statements
    statements = []

    # Go through the document and check for red flags appearing on each page
    for pageIndex in range(0, documentPagesMax):
        pageObj = pdfReader.getPage(pageIndex)
        pageText = pageObj.extractText()

        # Add to results if a new red flag statement was found
        results = [statement for statement in redFlags if statement in pageText and statement not in statements]

        # Append any new ones to the masterlist
        if results:
            statements = statements + results

    # Were red flag statements found?
    if statements:
        print("Red flag: Yes")
    else:
        print("Red flag: No")

    # Particularily hazardous substance (Yes/No)
    if statements:
        print("Particularily hazardous: Yes")
    else:
        print("Particularily hazardous: No")

    # Filter out CMR chemical (Yes/No, which statements)
    cmrStatements = [i for i in statements if i in cmrFilter]

    if cmrStatements:
        print("CMR chemical: Yes")
        print("CMR H-phrases: ", end="")
        print(*cmrStatements, sep=", ")
    else:
        print("CMR chemical: No")

    # Filter out other statements with major risks (Yes/No, which statements)
    otherStatements = [i for i in statements if i in otherFilter]

    if otherStatements:
        print("Other H and EU Phrases chemical: ", end="")
        print(*otherStatements, sep=", ")
    else:
        print("Other H and EU Phrases: No")
    
    print()
