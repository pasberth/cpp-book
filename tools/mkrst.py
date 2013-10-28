#!/usr/bin/env python

import os
import os.path
import lxml.etree
import lxml.html

HEADER_SYMBOLS = ["=", "-", "~", "@", "^", "."]

fname   = os.path.dirname(__file__) + "/../C++11-Syntax-and-Feature.xhtml"
cppbook = open(fname)
tree    = lxml.html.parse(cppbook)

def print_article_body(rst_file, indent_level, article, indent=u""):

    for elem_count, text in enumerate(article.xpath("*")):
        if text.tag == "p":
            rst_file.write((indent).encode("UTF-8") + lxml.etree.tostring(text, encoding="UTF-8"))
        elif text.tag == "pre":
            rst_file.write(indent + u".. code-block:: c++")
            rst_file.write(indent + u"\n  ")
            rst_file.write((indent + text.text.replace("\n", "\n  " + indent)[0:-2]).encode("UTF-8"))
        elif text.tag == "h1" and elem_count != 0:
            if text.text:
                rst_file.write(text.text.encode("UTF-8"))
                rst_file.write(u"\n")
                rst_file.write(HEADER_SYMBOLS[indent_level + 1] * 80)
        elif text.tag == "h1":
            pass
        elif text.tag == "article":
            print_article(rst_file, indent_level + 1, text)
        elif text.tag == "section":
            print_article(rst_file, indent_level + 1, text)
        elif text.tag == "ul":
            for li in text.xpath("li"):
                rst_file.write(indent + u"* ")
                rst_file.write((indent + li.text).encode("UTF-8"))
                print_article_body(rst_file, indent_level, li, u"  ")
                rst_file.write(u"\n")
        elif text.tag == "ol":
            for i, li in enumerate(text.xpath("li")):
                rst_file.write(indent + (u"%d " % i))
                rst_file.write((indent + li.text).encode("UTF-8"))
                rst_file.write(u"\n")
        elif text.tag == "dl":
            for child in text:
                if child.tag == "dt":
                    rst_file.write(child.text.encode("UTF-8"))
                    rst_file.write(u"\n")
                elif child.tag == "dd":
                    rst_file.write(u"  ")
                    rst_file.write(child.text.encode("UTF-8"))
                    rst_file.write(u"\n")
        elif text.tag == "table":
            thead = text.find("thead")
            tbody = text.find("tbody")
            border = (u' ' * 10).join([ u"=" * 20 for th in thead.xpath("tr/th") ])
            rst_file.write(border)
            rst_file.write(u"\n")
            rst_file.write(((' ' * 20).join([ th.text for th in thead.xpath("tr/th") ])).encode("UTF-8"))
            rst_file.write(u"\n")
            rst_file.write(border)
            rst_file.write(u"\n")
            for tr in tbody:
                rst_file.write(((' ' * 20).join([ th.text for th in tr ])).encode("UTF-8"))
                rst_file.write(u"\n")
            rst_file.write(border)
            rst_file.write(u"\n")

        else:
            print text.tag
        rst_file.write(u"\n")
        rst_file.write(u"\n")

def print_article(rst_file, indent_level , article):
    article_header      = article[0]
    rst_file.write(''.join(article_header.itertext()).encode("UTF-8").replace("\n", " "))
    rst_file.write(u"\n")
    rst_file.write(HEADER_SYMBOLS[indent_level] * 80)
    rst_file.write(u"\n")
    rst_file.write(u"\n")

    print_article_body(rst_file, indent_level, article)

for toplevel in tree.xpath('id("content")/article'):
    header          = toplevel[0]
    rst_filename    = header.attrib["id"] + ".rst"
    rst_file        = open(rst_filename, "w")

    rst_file.write(''.join(header.itertext()).encode("UTF-8").replace("\n", " "))
    rst_file.write(u"\n")
    rst_file.write(u"================================================================================\n")
    rst_file.write(u"\n")

    for article in toplevel.xpath("article"):
        print_article(rst_file, 1, article)

cppbook.close()