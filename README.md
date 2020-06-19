# A python library for caching data while scraping using the famous requests-module

Often when scraping, something goes wrong. In order to minimize the burden on the website you are scraping, its a good idea to cache the data. This library does all this transparently. 

With this module you can create an instance of `Crequests` (which inherits from `requests.Session`). With this instance you can use all the standard methods of `requests.Session`. In the background all the magic caching happens, while you use all the well known methods of the requests library

## Normal use of requests
A normal way to do a get request with the requests-module goes like this:

```python
import requests
html = requests.get("http://httpbin.org/html").content
```

If you need to run your program several times in a test or development phase, the content will be fetched from the website every time, putting a strain on the website. It can also be slow.

In this small example it's probably not a big problem, but if your program is traversing hundreds of pages, it's not nice to start all over.

## crequests to the rescue

First install `Crequests`:

```bash
pip install crequests
```

You can now achieve the same request like this:

```python
from crequests import CRequests
crs = CRequests("cachedata")
html = crs.get("http://httpbin.org/html").content
```

Running this program will create a cache folder in the current working directory called "cachedata". The raw html will be extracted and returned in the same way as before. But besides this, a local cache copy is stored.

Next time you run the code, the exact same data will be retrieved from disk instead.

You can delete the cache by deleting the folder

## Technical info

The `Crequests` class extends the [requests.Session](https://requests.readthedocs.io/en/master/user/advanced/#session-objects) class.

All methods should be exposed like the original class. The most useful are .get / .put / .post... But have a look in their documentation for more details.

Most cached methods returns an `requests.models.Response` object.



------

Have fun...

*Alex Skov Jensen*