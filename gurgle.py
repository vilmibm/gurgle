#!/usr/bin/env python
import sys
import subprocess
import textwrap
import urllib2

from lxml import etree
import lxml.html


def main():
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0')]

    if len(sys.argv) > 1:
        search_term = "%20".join(sys.argv[1:])
    else:
        print "usage: gurgle.py search-term"
        return 255

    try:
        data = opener.open("http://google.com/search?q=%s" % search_term)
    except urllib2.HTTPError, e:
        print "encountered HTTP error talking to the google: %s" % e
        return 255

    tree = lxml.html.parse(data)
    body = tree.find("body")

    links = [{'title':l.text_content(), 'href':l.get("href")} for l in body.cssselect("a.l")]
    sums = [s.text_content() for s in body.cssselect("div.s")]

    results = zip(links, sums)

    index = 0
    for link, summary in results:
        print "%d: %s" % (index, link['title'])
        print "".join(map(lambda x: "\t%s\n" % x, textwrap.wrap(summary, 72)))
        index += 1

    choice = -1
    while int(choice) not in range(0, len(results)):
        choice = raw_input("choice [%sq]: " % ''.join([str(i) for i in range(0, len(results))]))
        if choice == '':
            choice = 0 # assumes at least one result
        elif choice == 'q':
            sys.exit(0)

    choice_href = results[int(choice)][0]['href']

    browser = raw_input("default browser or terminal-based? [Dt]: ")
    browser = browser.lower()
    if browser == 't':
        browser_command = "w3m"
    else:
        browser_command = "x-www-browser"
    subprocess.call([browser_command, choice_href])

    return 0

if __name__ == '__main__':
    sys.exit(main())
