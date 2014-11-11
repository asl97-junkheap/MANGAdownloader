################################################################
# File: e621.py
# Title: MANGAdownloader's site scraper
# Author: ASL97/ASL <asl97@outlook.com>
# Version: 1
# Notes : DON'T EMAIL ME UNLESS YOU NEED TO
# TODO: *blank*
################################################################

import misc

# used in __main__, download using id is currently not implemented yet
id_supported = False

_type = ["1","10"]

def scrap_manga(link, chapter):
    chapter[1] = {}
    tmp = link.split("/")[-1]
    if tmp.isdigit():
        id_ = tmp
        link = "http://e621.net/pool/show.json?id=%s"%(id_)
        j = misc.download_json(link)
        name = j["name"]
        total = j["post_count"]
        page_ = 1
        page = 0

        for d in j["posts"]:
            chapter[1][page] = {"link": d['file_url'],
                                "name": d['file_url'].split("/")[-1]}
            page += 1

        while page < total:
            page_ += 1
            link = "http://e621.net/pool/show.json?id=%s&page=%d"%(id_,page_)
            j = misc.download_json(link)
            for d in j["posts"]:
                chapter[1][page] = {"link": d['file_url'],
                                    "name": d['file_url'].split("/")[-1]}
                page += 1
        return name
    else:
        misc.Exit("fail to get id")
