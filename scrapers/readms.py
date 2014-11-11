################################################################
# File: readms.py <mangastream>
# Title: MANGAdownloader's site scraper
# Author: ASL97/ASL <asl97@outlook.com>
# Version: 1
# Notes : DON'T EMAIL ME UNLESS YOU NEED TO
# TODO: *blank*
################################################################

import misc

# used in __main__, download using id is currently not implemented yet
id_supported = False

_type = ["1","5"]

def scrap_manga(link, chapters):
	pat1 = re.compile('<a href="(.*?)"><img id="manga-page" src="(.*?)"/></a>')

	tmp = link.split("/")
	name = tmp[4]

	try:
		chapter = int(tmp[5])
	except:
		chapter = 1

	try:
		manga_id = int(tmp[6])
	except:
		sys.exit("missing id")

	link = "http://readms.com/r/%s/%03d/%d"%(self.manga_name,num,self.manga_id)

	while True:
		data = misc.download_page(link)
		tmp = link.split("/")
		chapter = int(tmp[5])
		tmp = pat1.search(data)
		if tmp:
			link = tmp.group(1)
			if chapter not in chapters:
				chapters[chapter] = {}
				page = 0

			page += 1
			chapters[chapter][page] = {"link": tmp.group(2)}

			if link.endswith("end"):
				break

	return name
