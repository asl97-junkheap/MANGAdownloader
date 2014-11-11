there are specially name variables in those scraper files (maintainability)

the meaning of those variables are stated below

* `chapters`: a dict variable that contain all the chapters
* `chapter`: the chapter number
* `image`: the image link
* `data`: the webpage data
* `links`: a list variable that contain all the links for all the chapters
* `link`: the webpage link
* `name`: the name of the manga
* `pages`: a list variable that contain all the links to pages for a chapter
* `page`: the page/image number, note: page always start with 0, it's a design choice
* `tmp`: reusable variables (it become useless most of the time after using it and can be safely ignore)

_______________________________________________________________________

chapters format:

```
{
	chapter (int):
		{
			page (int):
				{
					"link": link (str),
					"image": data (bytes), [optional]
					"name": image name (str) [optional]
				}
		}
}
```
