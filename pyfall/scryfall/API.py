import requests
import urllib.parse
import pyfall.errors
import pyfall.scryobject
from enum import Enum

SCRYFALL_SCHEME = "https"
SCRYFALL_NETLOC = "api.scryfall.com"
class StrPrototypes(Enum):
    VALUEERROR = "{} must be one of {}; we got {}."

# def choosecall(*, passed_keys, valid_keywords, keyword_calls):
#     if len(passed_keys.keys()) == 0:
#         call = keyword_calls[None]
#     else:
#         if list(passed_keys.keys())[0] not in valid_keywords:
#             raise ValueError(string_valueerror_notinlist.format("First keyword", valid_keywords, *passed_keys.keys()))
#         else:
#             call = keyword_calls[passed_keys.keys()[0]]
#     return call

def callapi(call: str | urllib.parse.SplitResult="/cards/random", **kwargs) -> requests.Response:
    """Uses a SplitResult, or a string, to make a call to the API.
    
    This eturns an open stream! Be sure to close it, or use the result as
    a context manager.

    Will only make calls to https://api.scryfall.com -- any other scheme or
    netloc will be overwritten.
    
    kwargs will be treated as parameters to send with the API request.
    If a parameter is included in both the call and the kwargs, the
    one from kwargs will generally overrule the one from the call.
    (this is HTTP or API behaviour; kwargs are appended to the end of params)"""
    if type(call) == str:
        call = urllib.parse.urlsplit(call)
    if call.netloc not in [SCRYFALL_NETLOC, ""]:
        raise pyfall.errors.RequestError("The attempted call included netloc {} -- this isn't the API.".format(call.netloc))
    pathquery = call._replace(scheme=SCRYFALL_SCHEME, netloc=SCRYFALL_NETLOC).geturl()
    
    # Set default parameters -- the API sets these of course, but let's do it here
    # too for visibility.
    payload = {"format":"json","version":"large","face":""}
    payload.update(kwargs)
    return requests.get(pathquery, params=payload)