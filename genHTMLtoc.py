#!/usr/bin/python

"""Generate a table of contents from the encountered h1,...,h4-tags

Read in an HTML file, record each h`n`-tag (`n` = 1 ... 4) and output a TOC.
E.g. if the input is

    <h1>Level 1 First <a name="ref1"></a></h1>
    <h1>Level 1 Second <a name="ref2"></a></h1>
        <h2>Level 2 First <a name="ref3></a><h2>
            <h3>Level 3 First <a name="ref4"></a></h3>
    <h1>Level 1 Third <a name="ref5"></a></h1>

the produced TOC is

    <ul>
        <li><a href="#ref1">Level 1 First</a></li>
        <li><a href="#ref2">Level 1 Second</a></li>
        <ul>
            <li><a href="#ref3">Level 2 First</a></li>
            <ul>
                <li><a href="#ref4">Level 3 First</a></li>
            </ul>
        </ul>
        <li><a href="#ref5">Level 1 Third</a></li>
    </ul>
"""

from HTMLParser import HTMLParser
import argparse
import fileinput

def parse_args():
    parser = argparse.ArgumentParser(description='Generate table of contents for the html file INHTML. If no `-o` argument is present, the TOC is written to stdout. Otherwise INTHML is copied to OUTHML, with the TOC inserted at line N.')
    parser.add_argument("infile",
                        metavar="INHTML",
                        help="Input html file.")
    parser.add_argument("-o", "--out",
                        metavar=("OUTHTML", "N"),
                        nargs=2,
                        help="TOC is written together with INHTML to OUTHTML. The TOC is inserted at line N of INHTML.")
    args = parser.parse_args()
    return args

class MyHTMLParser(HTMLParser):
    prevtag = ""
    prevtitle = ""
    titletags = ['h1', 'h2', 'h3', 'h4']
    titlelist = []

    def handle_starttag(self, tag, attrs):
        if self.prevtag in self.titletags and tag == "a":
            nameattrs = [a[1] for a in attrs if a[0] == "name"]
            # Ignore a <a>-tag, which has no "name" attribute.
            if len(nameattrs) == 0:
                return
            self.titlelist.append((self.prevtag,
                                   self.prevtitle,
                                   nameattrs[0]))

        self.prevtag = tag


    def handle_data(self, data):
        if self.prevtag in self.titletags:
            self.prevtitle = data

def generateTOC(level_title_ref_list):
    """Generate the TOC according to the list of triples `level_title_ref_list`

    The list of triples are of the form (`L`, `T`, `R`), where `L` is an HTML
    heading (e.g. "h1", "h2", ..., "h6"), `T` is the content of the heading
    (e.g. "Chapter 1", "Section 2") and `R` is the value of a name attribute in
    a `<a>`-tag, like in '<a name="`R`"></a>'.

    The resulting TOC is returned as a string, containing new lines.

    """
    currLevel = 2;
    ret = "<ul>\n"
    for level, title, ref in level_title_ref_list:
        level_ = int(level[1])
        # <li><a href="#currentAction">Aktuelle Aktion</a></li>
        toc_entry = '<li><a href="#' + ref + '">' + title + "</a></li>\n"
        open_or_close_ul = ""
        if level_ > currLevel:
            open_or_close_ul = "<ul>\n"
        elif level_ < currLevel:
            open_or_close_ul = "</ul>\n"
        else:
            open_or_close_ul = ""
        ret = ret + abs(level_ - currLevel) * open_or_close_ul + toc_entry
        currLevel = level_
    ret = ret + "</ul>"
    return ret

def main():
    args = parse_args()
    infile = args.infile
    parser = MyHTMLParser()
    parser.feed(open(infile, 'r').read())

    toc = generateTOC(parser.titlelist)

    if (args.out == None):
        print toc
    else:
        toc_linenumber = int(args.out[1])
        infilelines = open(infile, 'r').readlines()

        outhtmllines = infilelines[:toc_linenumber]
        outhtmllines.append(toc)
        outhtmllines = outhtmllines + infilelines[toc_linenumber:]

        outfilename = args.out[0]
        outfile = open(outfilename, 'w')
        outfile.writelines(outhtmllines)

main()
