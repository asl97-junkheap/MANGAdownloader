################################################################
# File: readms.py <mangastream>
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

def note():
    print("the readms (mangastream) scraper require you"
          "to input the chapter page")
    print("or else it would just crash with an error")
    print("eg: http://readms.com/r/name_here/401/2546/1")

_type = ["1","5"]

def scrap_manga(link, chapters):
    pat1 = re.compile('<a href="(.*?)"><img id="manga-page" src="(.*?)"/></a>')

    tmp = link.split("/")
    name = tmp[4]

    if tmp[5].isdigit():
        chapter = int(tmp[5])
    else:
        # special case
        chapter = tmp[5]

    if tmp[6].isdigit():
        manga_id = int(tmp[6])
    else:
        misc.exit("missing id")

    if type(chapter) == int:
        link = "http://readms.com/r/%s/%03d/%d"%(name,chapter,manga_id)
    else:
        link = "http://readms.com/r/%s/%s/%d"%(name,chapter,manga_id)

    while True:
        data = misc.download_page(link)
        tmp = link.split("/")
        chapter = int(tmp[5]) if tmp[5].isdigit() else tmp[5]
        tmp = pat1.search(data)
        if tmp:
            link = tmp.group(1)
            if chapter not in chapters:
                chapters[chapter] = {}
                page = 0

            page += 1
            if type(chapter) == int:
                chapters[chapter][page] = {"link": tmp.group(2)}
            else:
                l = tmp.group(2)
                n = re.sub("\s+"," ",re.sub("<.*?>","",data.split("\n")[98]))
                ext = l.split("/")[-1].split(".")[-1].split("?")[0]
                chapters[chapter][page] = {"link": l,
                    "name": "special/%s/%03d.%s" % (n,page,ext)}

            if link.endswith("end"):
                break

    return name
