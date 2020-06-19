from crequests import CRequests
import logging
from bs4 import BeautifulSoup

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s [%(name)s] %(levelname)7s: %(message)s", datefmt="%H:%M:%S",
)

url = "http://www.github.com"

crs = CRequests("cachedata")
for _ in range(3):  # Do the same over and over... Check that we get cache hits - this should be fast
    rawHtml = crs.put(url).content
    if rawHtml:
        soup = BeautifulSoup(rawHtml, "html.parser")
        print(soup.title.text)
