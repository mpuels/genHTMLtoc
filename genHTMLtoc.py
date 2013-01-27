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

def generateTOC(level_title_ref_list):
    currLevel = 2;
    ret = "<ul>\n"
    for level, title, ref in level_title_ref_list:
        level_ = int(level[1])
        print level_, title, ref
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
    filename = "INBOX.html"
    htmlfile = open(filename, 'r')
    htmlfilestr = htmlfile.read()
    parser = MyHTMLParser()
    parser.feed(htmlfilestr)
    for t in parser.titlelist:
        print t
    toc = generateTOC(parser.titlelist)
    tocfilename = "TOC.html"
    tocfile = open(tocfilename, 'w')
    tocfile.write(toc)

main()
