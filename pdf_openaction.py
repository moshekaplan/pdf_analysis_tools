#!/usr/bin/env python
# encoding:UTF-8
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


def find_openactions(pdf_object):
    openactions = list()
    root = pdf_object.trailer
    # Ignore warnings from failed Object dereferences
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for node in walk_pdf_tree(root):
            if isinstance(node, DictionaryObject) and '/OpenAction' in node.keys():
                # As per PDF 1.7, section 3.6.1, OpenAction can be an an Array or dictionary
                # The value is either an array defining a destination (see Section 8.2.1, “Destinations”)
                # or an action dictionary representing an action (Section 8.5, “Actions”)
                action = node['/OpenAction']
                if isinstance(action, DictionaryObject):
                    actionType = action['/S']
                    # Possibly dangerous types include Launch, URI, and JavaScript
                    openactions.append(actionType)
                elif isinstance(action, ArrayObject):
                    actionType = "Destination"
                    # Destinations may be associated with:
                    # outline items (see Section 8.2.2, “Document Outline”), 
                    # annotations (“Link Annotations” on page 622), or 
                    # actions (“Go-To Actions” on page 654 and “Remote Go-To Actions” on page 655).
                    # These are not fully supported
                    openactions.append(actionType)
            if isinstance(node, DictionaryObject) and '/AA' in node.keys():
                # As per PDF 1.7, section 3.6.2 (page 147), AA (Additional Actions) can be specified
                # when a _trigger event_ occurs.
                # Didier Stevens writes (https://blog.didierstevens.com/programs/pdf-tools/) that these
                # can also be used maliciously.
                # No samples yet to test this
                actionType = "Unsupported Additional Action (AA)!"
                openactions.append(actionType)
    return openactions


def extract_openactions(fpath):
    with open(fpath, 'rb') as fh:
        src_pdf_blob = fh.read()
    pdf_data = PyPDF2.PdfFileReader(StringIO.StringIO(src_pdf_blob))
    openactions = find_openactions(pdf_data)
    if openactions:
        print "\n".join(openactions)


def main():
    if len(sys.argv) < 2:
        print "USAGE: %s %s <filename>" % (sys.executable, sys.argv[0])
        sys.exit(1)
    fpath = sys.argv[1]
    extract_openactions(fpath)

if __name__ == "__main__":
    main()
