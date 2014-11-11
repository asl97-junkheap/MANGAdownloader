################################################################
# File: bato.py
# Title: MANGAdownloader's site scraper
# Author: ASL97/ASL <asl97@outlook.com>
# Version: 1
# Notes : DON'T EMAIL ME UNLESS YOU NEED TO
# TODO: *blank*
################################################################

import re
import misc

# used in __main__, download using id is currently not implemented yet
id_supported = False

_type = ["1", "5"]

def note():
    print("the bato scraper doesn't support `start chapter` downloading")
    print("meaning, no way to download chapter x to END like the other scraper")
    print("it will download the whole series")
    print()
    print("also, this scraper use part of koroshiya's batoto-downloader-py")

def chapter_scraper(links, chapters):
    # the chapters return from the scraper are backwards so we flip them here
    for chapter, link in enumerate(links[::-1], 1):
        chapters[chapter] = {}
        page = 0
        name = link.split("/")[-1]
        data = misc.download_page(link)
        tmp = re.search('<select name="page_select".*?</select>',
                        data, re.DOTALL)
        if tmp:
            pages = re.findall('value="(.*?)"', tmp.group(0), re.DOTALL)
            for link in pages:
                data = misc.download_page(link)
                tmp = re.search('id="full_image".*?</div>.*?<img src="(.*?)"'
                                '.*?</div>',data,re.DOTALL)
                if tmp:
                    image = tmp.group(1)
                    chapters[chapter] = {page: {"link":image,
                                                "name": "%s/%s" % (
                                                name, image.split("/")[-1])}}
                    page += 1

def scraper(link):
    data = misc.download_page(link)
    tmp = re.search("<select.*?chapter_select.*?</select>", data, re.DOTALL)
    links = re.findall('value="(.*?)"', tmp.group(0), re.DOTALL)
    name = re.search('<li style=".*?><a href=".*?">(.*?)</a></li>',data,
                    re.DOTALL).group(1)
    return links, name

def third_party_scraper(link):
    # use Koroshiya's batoto downloader's find chapters
    from . import _bato
    links = _bato.findChapters(link)
    name = _bato.get_name(link)
    return links, name

def scrap_manga(link, chapters):
    if "comic" in link:
        # if this import is place above, it would error due to
        # missing id_supported in _bato
        links, name = third_party_scraper(link)
    elif "read" in link:
        links, name = scraper(link)
    chapter_scraper(links, chapters)

    return name

