#!/usr/bin/python

"""Generate a table of contents from the encountered h1,...,h4-Tags



"""

from HTMLParser import HTMLParser

class MyHTMLParser(HTMLParser):
    prevtag = ""
    prevtitle = ""
    titletags = ['h1', 'h2', 'h3', 'h4']
    titlelist = []

    def handle_starttag(self, tag, attrs):
        if self.prevtag in self.titletags and tag == "a":
            nameattrs = [a[1] for a in attrs if a[0] == "name"]
            self.titlelist.append((self.prevtag,
                                   self.prevtitle,
                                   nameattrs[0]))

        self.prevtag = tag


    def handle_data(self, data):
        if self.prevtag in self.titletags:
            self.prevtitle = data


def main():
    filename = "INBOX.html"
    htmlfile = open(filename, 'r')
    htmlfilestr = htmlfile.read()
    parser = MyHTMLParser()
    parser.feed(htmlfilestr)
    for t in parser.titlelist:
        print t

main()
