#!/usr/bin/env python

"""
This script extracts all strings from a supplied PDF file.

Running strings against PDF files is not always helpful, because interesting values
like URLs and JavaScript can be encoded so they are not human-readable.

This script works around that by first decoding all text inside of the PDF file
so that the strings are human-readable. This also has the benefit of not including
strings that are not displayed to the user.
"""

import sys

import PyPDF2


def get_strings(fpath):
    texts = []
    pdf = PyPDF2.PdfFileReader(fpath)
    for page_num, page in enumerate(pdf.pages):
        texts.append(page.extractText())
    extracted_text = ("\n" + "*"*80 + "\n").join(texts)
    return extracted_text.encode('utf-8', errors="replace")


def main():
    if len(sys.argv) < 2:
        print "USAGE: %s %s <filename>" % (sys.executable, sys.argv[0])
        sys.exit(1)
    fpath = sys.argv[1]
    print get_strings(fpath)


if __name__ == "__main__":
    main()
