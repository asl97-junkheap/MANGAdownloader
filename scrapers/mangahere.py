################################################################
# File: mangahere.py
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

def scrap_manga(link, chapters):
	data = misc.download_page(link)
	name = re.search('var series_name = "(.*?)";',self.page_data).group(1)

	tmp = re.search("http://www.mangahere.co/manga/.*?/v.*?/c(\d*)/",link)
	if tmp:
		chapters = int(tmp.group(1))
	else:
		chapters = 1

	page = 0

	while True:
		tmp = re.search('<section class="read_img" id="viewer">.*?<a href="(.*?)" onclick="return next_page\(\);">.*?<img src="(.*?)"',data,re.DOTALL)
		link = tmp.group(1)
		image = tmp.group(2)

		if chapter not in chapters:
			chapters[chapter] = {}
		chapters[chapter][page] = {"link":image}

		if not link.startswith("http"):
			tmp = re.search('<strong>Next Chapter:</strong> <a href="(.*?)">.*?</a></p>',data)
			if not tmp:
				break
			else:
				link = tmp.group(1)
				chapter += 1
				page = 0
		else:
			page += 1

		data = misc.download_page(link)

	return name
