import pyfall.errors

import urllib.parse
import requests
import time

SCRYFALL_SCHEME = "https"
SCRYFALL_NETLOC = "api.scryfall.com"

# class StrPrototypes(Enum):
#     VALUEERROR = "{} must be one of {}; we got {}."

#     def format(self, *args, **kwargs):
#         return self.value.format(*args, **kwargs)

# def choosecall(*, passed_keys, valid_keywords, keyword_calls):
#     if len(passed_keys.keys()) == 0:
#         call = keyword_calls[None]
#     else:
#         if list(passed_keys.keys())[0] not in valid_keywords:
#             raise ValueError(string_valueerror_notinlist.format("First keyword", valid_keywords, *passed_keys.keys()))
#         else:
#             call = keyword_calls[passed_keys.keys()[0]]
#     return call

def apiget(call: str | urllib.parse.SplitResult="/cards/random", **kwargs) -> requests.Response:
    """Uses a SplitResult, or a string, to make a call to the API.
        
        This eturns an open stream! Be sure to close it, or use the result as
        a context manager.

        Will only make calls to https://api.scryfall.com -- any other scheme or
        netloc will be overwritten.
        
        kwargs will be treated as parameters to send with the API request.
        'format' and 'pretty' parameters will be ignored.
        If a parameter is included in both the call and the kwargs, the
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
    # I'm not planning on doing async stuff rn, and figuring out timing seems like a headache.
    # For my purposes, as not to overwhelm scryfall, this is enough...
    time.sleep(0.1)
    # TODO: does requests do URL encoding automatically? We should encode it if not
    return requests.get(pathquery, params=payload)