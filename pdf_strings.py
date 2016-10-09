#!/usr/bin/env python

"""
This script extracts all strings from a supplied PDF file.
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
