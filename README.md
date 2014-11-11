MANGAdownloader V4
====

this is a very old downloader that i make long ago

it is make with hard-coded linux path separator, it most likely would
need a little clean up for it to work on windows

it is also not really just a manga downloader anymore, it could be make to work
with almost every site to download post or even feed

version 1,2 and 3 are very horrible so i wouldn't be releasing them

for the license, see LICENSE

for versioning, see VERSION

note
----
this is the root of the package, you just run it as it is without importing it

`python3 MANGAdownloader`

____

credit:
----

[koroshiya's batoto downloader](https://github.com/koroshiya/batoto-downloader-py/)

let's just say i was lazy and decided to use the `findChapters` from it,
i also retrieve the name of the comic the same way as it in the `third_party_scraper`.

although, it is only use to scrape the comic page*

i did wrote my own scraper to handle the read page.

\* start with something like this: http://bato.to/comic/_/comics/
