################################################################
# File: __main__.py
# Title: MANGAdownloader
# Author: ASL97/ASL <asl97@outlook.com>
# Version: 4
# Notes : DON'T EMAIL ME UNLESS YOU NEED TO
# TODO: *blank*
################################################################
import threading
import scrapers
import queue
import types
import json
import misc
import time
import os

class main:

    def __init__(self):
        # basic setup
        self.scrapers = {name:obj.id_supported
            for name,obj in vars(scrapers).items()
                if isinstance(obj, types.ModuleType)
            }
        self.done = False
        self.chapters = {}
        self.startup_msg()
        self.load_settings()
        self.check_setup()

    def startup_msg(self):
        print("\n".join([
            "ASL97 Online Manga Ripper Version 4",
            "This is a very simple fast downloader for downloading",
            "manga from read manga online sites",
            "",
            "supported sites: %s" % ", ".join(self.scrapers),
            ""
            ]))

    def load_settings(self):
        if not os.path.exists("./asl97_manga_downloader.ini"):
            self.settings = {}
        else:
            with open("./asl97_manga_downloader.ini","r") as f:
                self.settings = json.load(f)

    def setup(self):
        print("asl97_manga_downloader.ini not found, running setup")
        print()
        self.settings["zip"] = misc.get_bool_input("zip manga folder: ")
        print()
        self.settings["thread_number"] = misc.get_int_input(
                                                    "number of threads: ")
        print()
        with open("./asl97_manga_downloader.ini","w") as f:
            json.dump(self.settings,f)

    def check_setup(self):
        # check if all setting is set/exists
        if not set(self.settings) == {"zip","thread_number"}:
            self.setup()

    def predownload(self):
        misc.make_folder(self.name)
        self.image_queue = queue.Queue()
        self.lock = threading.Lock()
        for chapter in sorted(self.chapters):
            for page in sorted(self.chapters[chapter]):
                tmp = self.chapters[chapter][page]
                self.image_queue.put({
                    "chapter":chapter,
                    "link":tmp["link"],
                    "page":page,
                    "name":tmp["name"] if "name" in tmp else False
                })

    def worker(self):
        while True:
            tmp = self.image_queue.get()
            if tmp is False:
                self.image_queue.task_done()
                break

            link = tmp["link"]
            page = tmp["page"]
            chapter = tmp["chapter"]

            ext = tmp["link"].split("/")[-1].split(".")[-1].split("?")[0]
            if tmp["name"]:
                file_name = "%s/%s" % (self.name,tmp["name"])
            else:
                file_name = "%s/chapter_%s/%03d.%s" % (self.name,
                                                       chapter,page,ext)

            if os.path.exists(file_name):
                print("%s already exists"%(file_name))

            else:
                f = misc.download_image(link)
                print("downloaded page %d of chapter %s" % (page+1,chapter))
                with self.lock:
                    self.chapters[chapter][page]["image"] = f
                    self.chapters[chapter][page]["name"] = file_name

            self.chapters[chapter][page]["done"] = True
            self.image_queue.task_done()

        print("Thread Ended")

    def saver(self):
        while self.chapters: # check if there are still chapter to save
            with self.lock:
                # get the top chapter number
                chapter_num = sorted(self.chapters)[0]

                # get the top chapter (dict)
                chapter = self.chapters[chapter_num]

                # check if every single image is downloaded
                if all("done" in chapter[page] for page in chapter):
                    print("Saving Chapter: %s"%(chapter_num))

                    # save the images/pages
                    for page in sorted(chapter):
                        tmp = chapter[page]
                        if "image" in tmp:

                            # if the directory name doesn't exists, make it
                            directory = os.path.dirname(tmp["name"])
                            if not os.path.exists(directory):
                                os.makedirs(directory)

                            with open(tmp["name"],"wb") as f:
                                f.write(tmp["image"])

                    # finally free up the ram taken by the image
                    del self.chapters[chapter_num]

            time.sleep(0.2)
        print("Finish Saving")
        # i don't remember if any code depend on this variable
        # so i am leaving it here as backward compatibility
        self.done = True

    def download_finish_msg(self):
        self.image_queue.join()
        print("Finish Downloading")

    def download_thread(self):
        # download threads
        for _ in range(0,int(self.settings["thread_number"])):
            t = threading.Thread(target=self.worker)
            t.daemon = True
            t.start()
            self.image_queue.put(False)

        t = threading.Thread(target=self.download_finish_msg)
        t.daemon = True
        t.start()

    def run(self):
        link, domain = misc.get_url_input()
        if hasattr(scrapers,domain):
            self.scraper = getattr(scrapers,domain)
            if hasattr(self.scraper,"_type"):
                print()
                print("the scraper for %s is a %s scraper" % (domain,
                        misc.type_to_str(getattr(self.scraper,"_type"))))
                print()
            if hasattr(self.scraper,"note"):
                getattr(self.scraper,"note")()
                print()
            self.name = self.scraper.scrap_manga(link, self.chapters)
            self.predownload()
            self.download_thread()
            self.saver()
        else:
            print("%s is not supported!"%(domain))


if __name__ == "__main__":
    m = main()
    m.run()
