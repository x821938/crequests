import shutil
import os
import crequests
from pathlib import Path

cacheDir = "tests/cachedir"


def test_cacheDirCreation():
    shutil.rmtree(
        cacheDir, ignore_errors=True
    )  # Remove the cache dir if it exists... We want to start from fresh

    crs = crequests.Session(cacheDir)  # Create an instance of "Session" that we are testing
    assert os.path.isdir(cacheDir)  # An instance of crequest should create a cachedir


def test_cacheMiss():
    shutil.rmtree(cacheDir, ignore_errors=True)  # Clear cache first

    crs = crequests.Session(cacheDir)
    response = crs.get("http://httpbin.org/get")  # A good testsite for http requests
    assert response.status_code == 200  # Should get without https errors
    assert os.path.isfile(f"{cacheDir}/httpbin.org/80/80af113bc0b984440da4125b41e838dd13b0969e")  # hash good?
    assert not crs.lastReqWasCashed  # We should have an empty cache
    assert not crs.lastCacheReqHadErrors  # We dont want errors

    response = crs.put("http://httpbin.org/put")  # Another URL and PUT method instead of GET.
    assert response.status_code == 200
    assert os.path.isfile(f"{cacheDir}/httpbin.org/f9/f95ddf5314999705631f79c27c305df9deb74f7e")
    assert not crs.lastReqWasCashed  # Shoul also not be in cache
    assert not crs.lastCacheReqHadErrors  # We dont want errors


def test_cacheHit():
    test_cacheMiss()  # Make sure something is in our cache

    # Second time we get the URL, it should be in the cache
    crs = crequests.Session(cacheDir)
    response = crs.get("http://httpbin.org/get")
    assert response.status_code == 200
    assert crs.lastReqWasCashed
    assert not crs.lastCacheReqHadErrors  # We dont want errors

    # Second time we get the other URL, it should be in the cache
    response = crs.put("http://httpbin.org/put")
    assert response.status_code == 200
    assert crs.lastReqWasCashed
    assert not crs.lastCacheReqHadErrors  # We dont want errors


def test_cacheSameAsOriginal():
    shutil.rmtree(cacheDir, ignore_errors=True)  # Clear cache first

    # Get an uncached response
    crs1 = crequests.Session(cacheDir)
    response1 = crs1.get("http://github.com")
    assert not crs1.lastReqWasCashed

    # Get a cached response
    crs2 = crequests.Session(cacheDir)
    response2 = crs2.get("http://github.com")
    assert crs2.lastReqWasCashed

    # The content of those 2 should be the same
    assert response1.content == response2.content


def test_damagedCache():
    shutil.rmtree(cacheDir, ignore_errors=True)  # Clear cache first

    crs = crequests.Session(cacheDir)
    response = crs.get("http://httpbin.org/get")  # A good testsite for http requests

    response = crs.get("http://httpbin.org/get")  # Get the content again - should get cached version
    assert crs.lastReqWasCashed

    # Now we damage the cachefile
    with open(f"{cacheDir}/httpbin.org/80/80af113bc0b984440da4125b41e838dd13b0969e", "r+") as fp:
        fp.seek(0, 0)
        fp.write("garbage")

    response = crs.get("http://httpbin.org/get")  # Get the content again - should try the cache and fail
    assert not crs.lastReqWasCashed

    response = crs.get("http://httpbin.org/get")  # Now we should have a good cache entry again
    assert crs.lastReqWasCashed


def test_writeCacheError():
    shutil.rmtree(cacheDir, ignore_errors=True)  # Clear cache first

    # We make a directory in order to make the following caching fail.
    Path(f"{cacheDir}/httpbin.org/80/80af113bc0b984440da4125b41e838dd13b0969e").mkdir(
        parents=True, exist_ok=True
    )

    crs = crequests.Session(cacheDir)
    response = crs.get("http://httpbin.org/get")  # A good testsite for https requests
    assert crs.lastCacheReqHadErrors
