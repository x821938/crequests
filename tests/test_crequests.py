import shutil
import os
from crequests import CRequests

cacheDir = "tests/cachedir"


def test_cacheDirCreation():
    shutil.rmtree(cacheDir)  # Remove the cache dir if it exists... We want to start from fresh

    crs = CRequests(cacheDir)  # Create an instance of "crequests" that we are testing
    assert os.path.isdir(cacheDir)  # An instance of crequest should create a cachedir


def test_cacheMiss():
    shutil.rmtree(cacheDir)  # Clear cache first

    crs = CRequests(cacheDir)
    response = crs.get("http://httpbin.org/get")  # A good testsite for https requests
    assert response.status_code == 200  # Should get without https errors
    assert os.path.isfile(f"{cacheDir}/httpbin.org/80/80af113bc0b984440da4125b41e838dd13b0969e")  # hash good?
    assert not crs.lastReqWasCashed  # We should have an empty cache

    response = crs.put("http://httpbin.org/put")  # Another URL and PUT method instead of GET.
    assert response.status_code == 200
    assert os.path.isfile(f"{cacheDir}/httpbin.org/f9/f95ddf5314999705631f79c27c305df9deb74f7e")
    assert not crs.lastReqWasCashed  # Shoul also not be in cache


def test_cacheHit():
    test_cacheMiss()  # Make sure something is in our cache

    # Second time we get the URL, it should be in the cache
    crs = CRequests(cacheDir)
    response = crs.get("http://httpbin.org/get")
    assert response.status_code == 200
    assert crs.lastReqWasCashed

    # Second time we get the other URL, it should be in the cache
    response = crs.put("http://httpbin.org/put")
    assert response.status_code == 200
    assert crs.lastReqWasCashed


def test_cacheSameAsOriginal():
    shutil.rmtree(cacheDir)  # Clear cache first

    # Get an uncached response
    crs1 = CRequests(cacheDir)
    response1 = crs1.get("http://github.com")
    assert not crs1.lastReqWasCashed

    # Get a cached response
    crs2 = CRequests(cacheDir)
    response2 = crs2.get("http://github.com")
    assert crs2.lastReqWasCashed

    # The content of those 2 should be the same
    assert response1.content == response2.content
