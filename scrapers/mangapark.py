################################################################
# File: mangapark.py
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

_type = ["1","6"]

def scrap_manga(link, chapters):
	def everything_between(start, end):
		idx1 = data.find(start)
		idx2 = data.find(end,tmp)
		return data[idx1+len(var):idx2]

	data = misc.download_page(link)
	name = everything_between("var _manga_name = '","';")

	# the version of the manga
	s = link.split("/")[5]
	while True:
		if "File Not Found" in data: break
		manga_id = everything_between("var _manga_id = '","';")
		book_id = everything_between("var _book_id = '","';")

		tmp = re.search("var _book_link = '/s\d+?/(?:v\d+?/)?c(\d+?)';",data)
		if tmp:
			chapter = int(tmp.group(1))
		else:
			# try to catch crazy x.5 chapter
			chapter = float(re.search("var _book_link = '/s\d+?/(?:v\d+?/)?c(\d+?.?\d+?)';",data).group(1))
			print("found crazy chapter number: %s"%(chapter))
			tmp = input("awaiting input: ")
			if not tmp:
				import sys
				sys.exit()

		link = "http://2.p.mpcdn.net/%s/%s" % (manga_id,book_id)
		data = misc.download_page(link)
		files = re.findall('href="([^/]*?)"',data)
		chapters[chapter] = {page:{"link":"%s/%s" % (link,tmp)} for page,tmp in enumerate(sorted(files,key=lambda x: int(x.split(".")[0])))}

		tmp = re.search('<p><span>Next Chapter:</span> <a href="(.*?)">.*?</a></p>',data)
		if not tmp: break

		link = "http://mangapark.com"+tmp.group(1)
		# check version
		if s != link.split("/")[5]: break
		data = misc.download_page(link)

	return name
