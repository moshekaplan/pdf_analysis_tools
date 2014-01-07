#! /usr/bin/env python

"""
Splits a PDF file into one page per file, in a similar fashion to the extract
function in Adobe Acrobat

Requires PyPDF2
"""

import os
import sys
import os.path

import PyPDF2


def main():
    if len(sys.argv) < 2:
        print "No source file suppplied!"
        sys.exit(1)
    for fname in sys.argv[1:]:
        fh = open(fname, 'rb')
        source_pdf = PyPDF2.pdf.PdfFileReader(fh)
        dirname, fname = os.path.split(fname)
        destination = dirname + os.sep + fname + "_split"

        for i, page in enumerate(source_pdf.pages):
            try:
                os.mkdir(destination)
            except:
                pass
            writer = PyPDF2.pdf.PdfFileWriter()
            writer.addPage(page)
            fh = open(destination + os.sep + fname + '_%d.pdf' % i, 'wb')
            writer.write(fh)
            fh.close()

if __name__ == "__main__":
    main()
