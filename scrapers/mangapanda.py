################################################################
# File: mangapanda.py
# Title: MANGAdownloader's site scraper
# Author: ASL97/ASL <asl97@outlook.com>
# Version: 2
# Notes : DON'T EMAIL ME UNLESS YOU NEED TO
# TODO: *blank*
################################################################

import re
import misc

# used in __main__, download using id is currently not implemented yet
id_supported = False

def note():
    print("the mangapanda scraper require you to input the chapter page")
    print("or else it would just crash with an error")
    print("eg: http://www.mangapanda.com/name_here/129")

_type = ["1","5"]

def get_name(link):
    """
    this should cover 2 cases

    eg, get `wild-life`:

    http://www.mangapanda.com/wild-life
    http://www.mangapanda.com/751/wild-life.html
    """
    tmp = link.split("/")[-1].split(".")[0]
    if tmp.isdigit():
        return link.split("/")[-2]
    else:
        return tmp

def get_chapter(link):
    """
    this should cover 2 cases

    eg, get `1`:

    http://www.mangapanda.com/wild-life/1
    http://www.mangapanda.com/751-35090-1/wild-life/chapter-1.html

    problem:
    http://www.mangapanda.com/wild-life
    """
    return link.split("/")[-1].split("-")[-1].split(".")[0]

def scrap_manga(link,chapters):
    pat1 = re.compile('<div id="imgholder">.*?\n?.*?<a href=".*?">'
                      '<img.*?src="(.*?)"')
    pat2 = re.compile("</select> of (\d+)</div>")


    name = get_name(link)

    tmp = get_chapter(link)
    if tmp.isdigit():
        chapter = int(tmp)
    else:
        chapter = 1

    while True:
        link = "http://www.mangapanda.com/%s/%d"%(name,chapter)
        data = misc.download_page(link)
        tmp = pat1.search(data)

        if not tmp:
            # end of chapter hopefully
            break

        chapters[chapter] = {}
        page = 0

        image = tmp.group(1)
        chapters[chapter][page] = {"link":image}

        tmp = pat2.search(data)

        for page in range(2,int(tmp.group(1))+1):
            link = "http://www.mangapanda.com/%s/%d/%d"%(name,chapter,page)

            data = misc.download_page(link)
            tmp = pat1.search(data)

            image = tmp.group(1)
            chapters[chapter][page-1] = {"link":image}

        chapter += 1

    return name

def scrap_manga_old1(link, chapters):
    #pat1 = re.compile("http://.*?/.*?/(\d+)")
    pat2 = re.compile('<div id="imgholder">.*?\n?.*?<a href="(.*?)">'
                      '<img.*?src="(.*?)"')

    tmp = link.split("/")
    name = tmp[3]

    if len(tmp) > 4 and type(tmp[4]) == int:
        chapter = int(tmp[4])
    else:
        chapter = 1

    page = 0

    link = "http://www.mangapanda.com/%s/%d"%(name,chapter)

    while True:
        data = misc.download_page(link)
        tmp = pat2.search(data)

        if not tmp:
            # end of chapter hopefully
            break

        link = "http://www.mangapanda.com"+tmp.group(1)

        image = tmp.group(2)
        if chapter not in chapters:
            chapters[chapter] = {}
        chapters[chapter][page] = {"link":image}

        tmp = link.split("/")
        chapter = int(tmp[4])
        if len(tmp) > 5 and type(tmp[5]) == int:
            page = int(tmp[5])-1
        else:
            page = 0

    return name
