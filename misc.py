################################################################
# File: misc.py
# Title: MANGAdownloader's misc function
# Author: ASL97/ASL <asl97@outlook.com>
# Version: 4
# Notes : DON'T EMAIL ME UNLESS YOU NEED TO
# TODO: *blank*
################################################################

import requests
import tempfile
import time
import sys
import os

_exit = sys.exit

types = {
	"0":"template",
	"1":"single threaded",
	"2":"multi-threaded",
	"3":"reserve",
	"4":"reserve",
	"5":"page by page",
	"6":"chapter by chapter",
	"7":"volume by volume",
	"8":"reserve",
	"9":"reserve",
	"10":"pool"
}

def type_to_str(_type):
	return ", ".join([types[l] for l in _type if l in types])

def get_bool_input(msg):
	while True:
		print("please type ether y or n")
		tmp = input(msg)
		#print("\n")
		if tmp == "y":
			return True
		elif tmp == "n":
			return False

def get_int_input(msg):
	while True:
		print("please type a number")
		tmp = input(msg)
		#print("\n")
		if tmp.isdigit():
			return tmp

def get_id_input():
	tmp = input("site: ")
	if tmp in self.id_supported_sites:
		num = self.get_int_input("id: ")
		return num, tmp
	else:
		sys.exit("site not supported")

def make_folder(name):
	if not os.path.exists(name):
		os.mkdir(name)
	else:
		if not os.path.isdir(name):
			sys.exit("%s isn't a directory" % self.manga_name)

def get_url_input():
	"""
	return link and 2rd level domain
	http://www.google.com  >  google
	http://asl97.uk.to > uk
	"""
	link = input("enter url: ")
	try:
		# need find better re, temporary using split
		#self.bottom_domain = re.search("(?:https?\://)?(?:www\.)?(.*?)\.?",link)
		second_top_domain = link.split("/")[2].split(".")[-2]
		return link, second_top_domain
	except Exception as e:
		sys.exit(repr(e))

def download_image(link):
	last = 0
	times = 0
	while True:
		try:
			print("downloading image: %s"%(link))
			r = requests.get(link, timeout=10)
			data = r.content
			now = len(data)
			if ('content-length' not in r.headers or int(r.headers['content-length']) == now) and now != 0:
				return data
			elif now == last:
				times += 1
				if times > 5:
					tmp = input("awaiting input: ")
					if tmp:
						link = tmp
			else:
				last = now
				print("error, file download size is %d while content-length say %s"%(len(data),r.headers['content-length']))
				#print("retrying in 5 seconds")
		except Exception as e:
			print("error: "+str(e))

		#finally:
		#	time.sleep(5)

def download_page(link):
	while True:
		try:
			print("downloading page: %s"%(link))
			r = requests.get(link, timeout=10)
			data = r.text
			if "</html>" in data.lower():
				return data
			else:
				print("error, the page doesn't have `</html>` in it, possible fault in download")
				#tmp = tempfile.gettempdir() + "/mangadownloader_error.html"
				#print("saving page in %s"%(tmp))
				#with open(tmp,"w") as f:
				#	f.write(data)
				print("redownloading page") # print("retrying in 5 seconds")
		except Exception as e:
			print("error: "+str(e))

		#finally:
		#	time.sleep(5)

def download_json(link):
	while True:
		try:
			print("downloading page: %s"%(link))
			r = requests.get(link, timeout=10)
			try:
				return r.json()
			except Exception as e:
				print("error: "+str(e))
				print("redownloading page") # print("retrying in 5 seconds")
		except Exception as e:
			print("error: "+str(e))
