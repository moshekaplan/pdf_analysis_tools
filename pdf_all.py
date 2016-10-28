#!/usr/bin/env python
# encoding:UTF-8
"""
This script runs a file through all of the PDF tools
"""

import sys

import pdf_js
import pdf_links
import pdf_strings
import pdf_openaction


def run_all(fpath):
    print  "*"*20 + "PDF OpenAction" + "*"*20
    pdf_openaction.extract_openactions(fpath)
    print  "*"*20 + "PDF URLs" + "*"*20
    pdf_links.extract_urls(fpath)
    print  "*"*20 + "PDF JavaScript" + "*"*20
    pdf_js.extract_js(fpath)
    print  "*"*20 + "PDF Strings" + "*"*20
    pdf_strings.get_strings(fpath)


def main():
    if len(sys.argv) < 2:
        print "USAGE: %s %s <filename>" % (sys.executable, sys.argv[0])
        sys.exit(1)
    fpath = sys.argv[1]
    run_all(fpath)

if __name__ == "__main__":
    main()
