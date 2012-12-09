# $Id$
# element loader based on BeautifulSoup
# http://www.crummy.com/software/BeautifulSoup/

# ElementSoup from http://effbot.org/zone/element-soup.htm
# obviously by Fredrik Lundh who also wrote elementtree
# modified, see #<<modification by raspi177
# XPath provided by elementtree: http://effbot.org/zone/element-xpath.htm

# imports #<<modification by raspi177
import BeautifulSoup as BS

# soup classes that are left out of the tree
ignorable_soup = BS.Comment, BS.Declaration, BS.ProcessingInstruction


import etree13a2.ElementTree as ET

import htmlentitydefs, re

pattern = re.compile("&(\w+);")

try:
    name2codepoint = htmlentitydefs.name2codepoint
except AttributeError:
    # Emulate name2codepoint for Python 2.2 and earlier
    name2codepoint = {}
    for name, entity in htmlentitydefs.entitydefs.items():
        if len(entity) == 1:
            name2codepoint[name] = ord(entity)
        else:
            name2codepoint[name] = int(entity[2:-1])

def unescape(string):
    # work around oddities in BeautifulSoup's entity handling
    def unescape_entity(m):
        try:
            return unichr(name2codepoint[m.group(1)])
        except KeyError:
            return m.group(0) # use as is
    return pattern.sub(unescape_entity, string)

##
# Loads an XHTML or HTML file into an Element structure, using Leonard
# Richardson's tolerant BeautifulSoup parser.
#
# @param file Source file (either a file object or a file name). or a html text
# @param argIsHtml true is first param is html text   #<<modification by raspi177
# @param builder Optional tree builder.  If omitted, defaults to the
#     "best" available <b>TreeBuilder</b> implementation.
# @return An Element instance representing the HTML root element.

def parse(fileOrHtml, builder=None, encoding=None, argIsHtml=False):
    bob = builder
    def emit(soup):
        if isinstance(soup, BS.NavigableString):
            if isinstance(soup, ignorable_soup):
                return
            bob.data(unescape(soup))
        else:
            attrib = dict([(k, unescape(v)) for k, v in soup.attrs])
            bob.start(soup.name, attrib)
            for s in soup:
                emit(s)
            bob.end(soup.name)
    if argIsHtml==False:      #<<modification by raspi177
        file=fileOrHtml
        # determine encoding (the document charset is not reliable)
        if not hasattr(file, "read"):
            file = open(file)
        text = file.read()
    else:
        text=fileOrHtml
    if not encoding:
        try:
            encoding = "utf-8"
            unicode(text, encoding)
        except UnicodeError:
            encoding = "iso-8859-1"
    soup = BS.BeautifulSoup(
        text, convertEntities="html", fromEncoding=encoding
        )
    # build the tree
    if not bob:
        bob = ET.TreeBuilder()
    emit(soup)
    root = bob.close()
    # wrap the document in a html root element, if necessary
    if len(root) == 1 and root[0].tag == "html":
        return root[0]
    root.tag = "html"
    return root

if __name__ == "__main__":
    import sys
    source = sys.argv[1]
    if source.startswith("http:"):
        import urllib
        source = urllib.urlopen(source)
    print ET.tostring(parse(source))

