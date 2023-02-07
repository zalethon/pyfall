import requests
import urllib.parse
import pyfall.errors
import pyfall.scryobject

scryfall_scheme = "https"
scryfall_netloc = "api.scryfall.com"
string_valueerror_notinlist = "{} must be one of {}; we got {}."

def choosecall(*, passed_keys, valid_keywords, keyword_calls):
    if len(passed_keys.keys()) == 0:
        call = keyword_calls[None]
    else:
        if list(passed_keys.keys())[0] not in valid_keywords:
            raise ValueError(string_valueerror_notinlist.format("First keyword", valid_keywords, *passed_keys.keys()))
        else:
            call = keyword_calls[passed_keys.keys()[0]]
    return call

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
    if call.netloc not in [scryfall_netloc, ""]:
        raise pyfall.errors.RequestError("The attempted call included netloc {} -- this isn't the API.".format(call.netloc))
    pathquery = call._replace(scheme=scryfall_scheme, netloc=scryfall_netloc).geturl()
    
    # Set default parameters -- the API sets these of course, but let's do it here
    # too for visibility.
    payload = {"format":"json","version":"large","face":""}
    payload.update(kwargs)
    return requests.get(pathquery, params=payload)

def callsets(code:str|None=None, type:str|None=None, **kwargs) -> pyfall.scryobject.scryObject:
    """Calls /sets, /sets/:code, /sets/:id, or /sets/tcgplayer/:id
    
    With no code or type argument, calls /sets and returns a scryList of scrySet objects
    
    type can be one of 'setcode', 'tcgplayerid', or 'scryfallid'
    
    For setcode, code should be the 3-5 character set code. For tcgplayerid, code should
    be the relevant set's tcgplayer id. For scryfallid, code should be the set's scryfall id.
    In all cases, this returns a scryList or a scrySet.
    """
    valid_types = [None, 'setcode', 'tcgplayerid', 'scryfallid']
    type_calls = {
        None:'/sets',
        'setcode':'/sets/{}',
        'tcgplayerid':'/sets/tcgplayer/{}',
        'scryfallid':'/sets/{}'
    }
    if type not in valid_types:
        raise ValueError(string_valueerror_notinlist.format("type", valid_types, type))
    
    call = type_calls[type].format(code)

    return pyfall.scryobject.processapiresponse(callapi(call, **kwargs))

def callcardssearch(*, q: str,
                   unique: str='cards',
                   order: str='name',
                   dir: str='auto',
                   include_extras: bool=False,
                   include_multilingual: bool=False,
                   include_variations: bool=False,
                   page: int=1,
                   **kwargs
                   ) -> pyfall.scryobject.scryList:
    valid_unique = ['cards', 'art', 'prints']
    valid_order = [
        'name',
        'set',
        'released',
        'rarity',
        'color',
        'usd',
        'tix',
        'eur',
        'cmc',
        'power',
        'toughness',
        'edhrec',
        'penny',
        'artist',
        'review',
    ]
    valid_dir = ['auto', 'asc', 'desc']
    if unique not in valid_unique:
        raise ValueError(string_valueerror_notinlist.format("unique",valid_unique,unique))
    if order not in valid_order:
        raise ValueError(string_valueerror_notinlist.format("order", valid_order, order))
    if dir not in valid_dir:
        raise ValueError(string_valueerror_notinlist.format("dir", valid_dir, dir))
    payload = {
        'q':q,
        'unique':unique,
        'order':order,
        'dir':dir,
        'include_extras':include_extras,
        'include_multilingual':include_multilingual,
        'include_variations':include_variations,
        'page':page,
    }
