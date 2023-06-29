# msdsparse

MSDSparse is a command line tool for scraping MSDS files for alarming hazard statements.

## Usage

Collect all MSDS files (currently only supports Sigma-Aldrich standard format) to a directory

```
msds\
  example1.pdf
  example2.pdf
  example3.pdf
  example4.pdf
```

Run the parser in the directory and direct the output to a text file (`output.txt`).

```
python3 main.py > output.txt
```

An output file will be generated with all relevant information. This can now be transferred over to the departmental form.

```
ETOS group A!lto MSDS scaper
4 MSDS files found in the directory

File: example.pdf (1/4)
--------------------------------
Compound name: Potassium cyanide EMPLURA®
Compound CAS: 151-50-8
Particularily hazardous: Yes
CMR chemical: Yes
CMR H-phrases: H372
Other H and EU Phrases chemical: H300, H310, H330

File: example2.pdf (2/4)
--------------------------------
Compound name: n-Butyllithium solution
Compound CAS: NOT FOUND IN MSDS
Particularily hazardous: Yes
CMR chemical: Yes
CMR H-phrases: H361, H373
Other H and EU Phrases: No

File: example3.pdf (3/4)
--------------------------------
Compound name: Sodium azide extra pure
Compound CAS: 26628-22-8
Particularily hazardous: Yes
CMR chemical: Yes
CMR H-phrases: H373
Other H and EU Phrases chemical: H300, H310, H330

File: example4.pdf (4/4)
--------------------------------
Compound name: Water
Compound CAS: 7732-18-5
Particularily hazardous: No
CMR chemical: No
Other H and EU Phrases: No
```
