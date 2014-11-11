# The MIT License (MIT)
#
# Copyright (c) 2014 Koroshiya
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# https://github.com/koroshiya/batoto-downloader-py/

# Foreign comics haven't been tested and may not work at all.
# Only comics translated into English have been tested.

import re
import misc

def findChapters(url):
    web_pg = misc.download_page(url)
    pattern = "http://bato.to/read/\S*\""
    chapters = []
    lang = None
    for line in web_pg:
        if lang == "English":
            m = re.search(pattern, line)
            if m:
                inputLine = m.group(0)[:-1]
                if "/" not in inputLine[-4]:
                    chapters.append(inputLine)
                lang = None
        else:
            try:
                if "lang_English" in line:
                    lang = "English"
                else:
                    lang = None
            except UnicodeDecodeError:
                lang = None
    
    return chapters

def LastFolderInPath(path):
    start = path.rindex('/')
    newPath = path[:start]
    start = newPath.rindex('/')
    return newPath[start + 1:]

def get_name(path):
    if (not path[-1] == "/" and not path[-1] == "/1"): path += "/1"
    return LastFolderInPath(path)
