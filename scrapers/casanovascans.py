################################################################
# File: casanovascans.py
# Title: MANGAdownloader's site scraper
# Author: ASL97/ASL <asl97@outlook.com>
# Version: 1
# Notes : DON'T EMAIL ME UNLESS YOU NEED TO
# TODO: *blank*
################################################################

import re
import json
import misc

# used in __main__, download using id is currently not implemented yet
id_supported = False

def note():
    print("the casanovascans scraper require you to input the chapter page")
    print("or else it would just crash with an error")
    print("eg: http://manga.casanovascans.com/read/name_here/en/0/85/2/page/1")

_type = ["1","6"]

def scrap_manga(link, chapters):
    tmp = link.split("/")
    name = tmp[4]

    if len(tmp) > 7 and type(tmp[7]) == int:
        chapter = int(tmp[7])
    else:
        chapter = 1

    while True:
        data = misc.download_page(link)
        links = json.loads(data.split("\n")[189].split(" = ")[-1].split(";")[0])
        chapters[chapter] = {page:{"link":f["url"]} for
                                page,f in enumerate(links)}
        tmp = re.search('(http://.*?/read/.*)"',data.split("\n")[191])
        if tmp:
            link = tmp.group(1)
            tmp = link.split("/")
            if len(tmp) == 10:
                chapter = float(tmp[7]) + float("0."+tmp[8])
            elif len(tmp) == 9:
                chapter = int(tmp[7]) # += 1
            else:
                break
        else:
            break

    return name
