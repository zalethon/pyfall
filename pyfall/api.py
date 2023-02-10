import urllib.parse
import time
from io import BufferedRandom
import tempfile

import requests
from tqdm import tqdm

import pyfall.errors


SCRYFALL_SCHEME = "https"
SCRYFALL_NETLOC = "api.scryfall.com"

def geturiresponse(uri:str, **kwargs):
    """Get a response from a particular URI."""
    # I'm not planning on doing async stuff rn, and figuring out timing seems like a headache.
    # For my purposes, as not to overwhelm scryfall, this is enough...
    time.sleep(0.1)
    return requests.get(uri, **kwargs)

def getapiresponse(call: str | urllib.parse.SplitResult="/cards/random", **kwargs) -> requests.Response:
    """Uses a SplitResult, or a string, to make a call to the API.
        
        Will only make calls to https://api.scryfall.com -- any other scheme or
        netloc will be overwritten or raise a RequestError.
        
        `call` can be of either form:
        '[scheme]api.scryfall.com/cards/random' -or-
        '/cards/random'

        kwargs will be treated as parameters to send with the API request.
        'format' and 'pretty' parameters will be ignored.
        If a parameter is included in both the call string and the kwargs, the
        one from kwargs will generally overrule the one from the call.
        (this is HTTP or API behaviour; kwargs are appended to the end of params)
    """
    if type(call) == str:
        call = urllib.parse.urlsplit(call)
    if call.netloc not in [SCRYFALL_NETLOC, ""]:
        raise pyfall.errors.RequestError("The attempted call included netloc {} -- this isn't the API.".format(call.netloc))
    pathquery = call._replace(scheme=SCRYFALL_SCHEME, netloc=SCRYFALL_NETLOC).geturl()
    
    # Set default parameters -- the API sets these of course, but let's do it here
    # too for visibility.
    payload = {"version":"large","face":""}
    # We're never gonna want pretty=TRUE, and for now let's stick with json
    override = {"format":"json", "pretty":False}
    payload.update(kwargs)
    payload.update(override)
    return geturiresponse(pathquery, params=payload)

def getcontents(uri:str, *, chunksize:int=1024**2, sizeof:int, **kwargs) -> BufferedRandom:
    """Get the contents returned by a URI. Meant for use with non-API calls.
    
    `sizeof` should be the size in bytes; `chunksize` should be the desired chunk size.

    Gets the contents buffered on the hard drive in a temporary file, and tries to guess how long it'll take."""
    buffer = tempfile.TemporaryFile()
    with geturiresponse(uri, stream=True, **kwargs) as r:
        if 'content-length' in r.headers:
            sizeof = int(r.headers['content-length'])
        for bytes in tqdm(r.iter_content(chunksize),total=(int(sizeof)/(chunksize*8)) if sizeof else None):
            buffer.write(bytes)
        buffer.seek(0)
        #contents = buffer.read()
    return buffer