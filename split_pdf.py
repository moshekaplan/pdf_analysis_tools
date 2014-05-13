#! /usr/bin/env python

"""
Splits a PDF file into one page per file, in a similar fashion to the extract
function in Adobe Acrobat

Requires PyPDF2

Copyright (c) 2014, Moshe Kaplan
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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
