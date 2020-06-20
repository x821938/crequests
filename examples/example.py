import crequests
import logging
from bs4 import BeautifulSoup

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(name)s] %(levelname)7s: %(message)s", datefmt="%H:%M:%S",
)

url = "http://httpbin.org/html"

crs = crequests.Session("cachedata")
for _ in range(3):  # Do the same over and over... Check that we get cache hits - this should be fast
    rawHtml = crs.get(url).content
    if rawHtml:
        soup = BeautifulSoup(rawHtml, "html.parser")
        print(soup.body.h1)
