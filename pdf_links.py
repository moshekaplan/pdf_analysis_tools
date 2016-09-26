#!/usr/bin/env python

"""
This script extracts all URLs from a supplied PDF file.

The script finds all URLs by walking the PDF tree and looking for all URI
references, as specified in Section 8.5 of PDF v1.7:

<</Type/Action/S/URI/URI/<dest>

For Example:
<</Type/Action/S/URI/URI(http://www.google.com/) >>
"""
import sys
import StringIO
import warnings

import PyPDF2
from PyPDF2.generic import DictionaryObject, ArrayObject, IndirectObject

from PyPDF2.utils import PdfReadError

def walk_pdf_tree(node, already_visited=None):
    # Indirect objects can refer to each other in a loop.
    # Maintain a set of visited nodes to avoid a stack overflow
    if already_visited is None:
        already_visited = set()     
 
    yield node
    # Walk through the node's children
    if isinstance(node, DictionaryObject):
        for k, v in node.iteritems():
            for node in walk_pdf_tree(v, already_visited):
                yield node
    elif isinstance(node, ArrayObject):
        for v in node:
            for node in walk_pdf_tree(v, already_visited):
                yield node
    elif isinstance(node, IndirectObject):
        idnum = node.idnum
        if idnum in already_visited:
            pass
        else:
            already_visited.add(idnum)
            # Dereferencing an object can sometimes fail
            try:
                v = node.getObject()
            except PdfReadError:
                pass
            else:
                for node in walk_pdf_tree(v, already_visited):
                    yield node


def find_URIs(pdf_object):
    urls = set()
    root = pdf_object.trailer
    # Ignore warnings from failed Object dereferences
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for node in walk_pdf_tree(root):
            if isinstance(node, DictionaryObject) and '/URI' in node.keys():
                urls.add(str(node['/URI']))
    return sorted(urls)


def extract_urls(fpath):
    with open(fpath, 'rb') as fh:
        src_pdf_blob = fh.read()
    pdf_data = PyPDF2.PdfFileReader(StringIO.StringIO(src_pdf_blob))
    urls = find_URIs(pdf_data)
    if urls:
        print "\n".join(urls)


def main():
    if len(sys.argv) < 2:
        print "USAGE: %s %s <filename>" % (sys.executable, sys.argv[0])
        sys.exit(1)
    fpath = sys.argv[1]
    extract_urls(fpath)

if __name__ == "__main__":
    main()
