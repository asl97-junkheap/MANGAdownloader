################################################################
# File: wildcritters.py
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
		link = "http://wildcritters.ws/pool/show.json?id=%s"%(id_)
		j = misc.download_json(link)
		name = j["pool"]["name"]
		total = j["pool"]["post_count"]
		page_ = 1
		page = 0

		for d in j["posts"]:
			chapter[1][page] = {"link": d['file_url'], "name": d['file_url'].split("/")[-1]}
			page += 1

		while page < total:
			page_ += 1
			link = "http://wildcritters.ws/pool/show.json?id=%s&page=%d"%(id_,page_)
			j = misc.download_json(link)
			for d in j["posts"]:
				chapter[1][page] = {"link": d['file_url'], "name": d['file_url'].split("/")[-1]}
				page += 1
		return name
	else:
		misc._exit("fail to get id")
