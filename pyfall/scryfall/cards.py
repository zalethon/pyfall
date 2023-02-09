import pyfall.errors
import pyfall.scryobject
from .API import callapi
from .util import validate_kwargs, validate_param_value

def search(q, **kwargs) -> pyfall.scryobject.scryList:
    valid_keywords = [
        'q',
        'unique',
        'order',
        'dir',
        'include_extras',
        'include_multilingual',
        'include_variations',
        'page',
        'format',
        'pretty'
    ]
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
    
    payload = validate_kwargs(kwargs, valid_keywords)
    payload.update({"q":q})

    validate_param_value("unique", payload, valid_unique)
    validate_param_value("order", payload, valid_order)
    validate_param_value("dir", payload, valid_dir)

    return pyfall.scryobject.processapiresponse(callapi("/cards/search", **payload))

def named(**kwargs):
    valid_keywords = ['exact', 'fuzzy', 'set', 'face', 'version', 'pretty']
    payload = validate_kwargs(kwargs, valid_keywords)

    return pyfall.scryobject.processapiresponse(callapi("/cards/named", **payload))

def random(**kwargs):
    valid_keywords = ['q', 'format', 'face', 'version', 'pretty']
    payload = validate_kwargs(kwargs, valid_keywords)
    return pyfall.scryobject.processapiresponse(callapi("/cards/random", **payload))

def code(code, number, lang=None, **kwargs):
    valid_keywords = ['format', 'face', 'version', 'pretty']
    payload = validate_kwargs(kwargs, valid_keywords)
    if lang != None:
        path = '/cards/{}/{}/{}'.format(code, number, lang)
    else:
        path = '/cards/{}/{}'.format(code, number)
    return pyfall.scryobject.processapiresponse(callapi(path, **payload))