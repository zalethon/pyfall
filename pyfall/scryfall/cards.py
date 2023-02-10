from pyfall.scryobject import scryList, scryCard, getscryobject
from pyfall.util import validate_param_value, validate_standard_params
import pyfall.errors

def search(q:str,
           unique:str="cards",
           order:str="name",
           dir:str="auto",
           include_extras:bool=False,
           include_multilingual:bool=False,
           include_variations:bool=False,
           page:int=1,
           format:str='json',
           pretty:bool=False) -> scryList:
    valid_unique = [None, '', 'cards', 'art', 'prints']
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
    valid_format = ['json', 'csv']
    payload = {
        "q":q,
        "unique":unique,
        "order":order,
        "dir":dir,
        "include_extras":include_extras,
        "include_multilingual":include_multilingual,
        "include_variations":include_variations,
        "page":page,
        "format":format,
        "pretty":pretty,
    }
    validate_standard_params(payload, valid_format)
    validate_param_value("unique", payload, valid_unique)
    validate_param_value("order", payload, valid_order)
    validate_param_value("dir", payload, valid_dir)

    return getscryobject("/cards/search", **payload)

def named(exact:str=None,
          fuzzy:str=None,
          set:str=None,
          format:str='json',
          face:str=None,
          version:str='large',
          pretty:bool=False) -> scryCard:
    valid_format = ['json', 'text', 'image']
    payload = {
        "exact":exact,
        "fuzzy":fuzzy,
        "set":set,
        "format":format,
        "face":face,
        "version":version,
        "pretty":pretty,
    }
    if exact == None and fuzzy == None:
        raise pyfall.errors.RequestError("Either `exact` or `fuzzy` need to be set.")
    validate_standard_params(payload, valid_format)
    return getscryobject("/cards/named", **payload)

def autocomplete(q:str,
                 format:str='json',
                 pretty:bool=False,
                 include_extras:bool=False,):
    valid_format = ['json']
    payload = {
        "q":q,
        "format":format,
        "pretty":pretty,
        "include_extras":include_extras
    }
    validate_standard_params(payload, valid_format)
    return getscryobject("/cards/autocomplete", **payload)

def random(q:str=None,
           format:str='json',
           face:str=None,
           version:str='large',
           pretty:bool=False) -> scryCard:
    valid_format = 'json', 'text', 'image'
    payload = {
        "q":q,
        "format":format,
        "face":face,
        "version":version,
        "pretty":pretty,
    }
    validate_standard_params(payload, valid_format)
    return getscryobject("/cards/random", **payload)

def collection(*args, **kwargs):
# /cards/collection is a POST method -- will probably do this later
    raise pyfall.errors.RequestError("/cards/collection is a POST method, and not yet implemented here.")

def code(code:str,
         number:str|int,
         lang:str=None,
         format:str='json',
         face:bool=None,
         version:str='large',
         pretty:bool=None) -> scryCard:
    valid_format = ['json', 'text', 'image']
    payload = {
        "code":code,
        "number":number,
        "lang":lang,
        "format":format,
        "face":face,
        "version":version,
        "pretty":pretty,
    }
    validate_standard_params(payload, valid_format)
    if lang != None:
        path = '/cards/{}/{}/{}'.format(code, number, lang)
    else:
        path = '/cards/{}/{}'.format(code, number)
    return getscryobject(path, **payload)

def typeid(id:str,
           type:str=None,
           format:str='json',
           face:str=None,
           version:str='large',
           pretty:bool=False):
    valid_types = [None, '', 'multiverse', 'mtgo', 'arena', 'tcgplayer', 'cardmarket']
    valid_format = ['json', 'text', 'image']
    payload = {
        "format":format,
        "face":face,
        "version":version,
        "pretty":pretty
    }
    validate_standard_params(payload,valid_format)
    validate_param_value("type", {"type":type}, valid_types)

    if type in [None, '']:
        path = '/cards/{}'.format(id)
    else:
        path = '/cards/{}/{}'.format(type, id)
    return getscryobject(path, **payload)

def multiverse(id:str, format:str='json', face:str=None, version:str='large', pretty:bool=False):
    return typeid(id, 'multiverse', format, face, version, pretty)

def mtgo(id:str, format:str='json', face:str=None, version:str='large', pretty:bool=False):
    return typeid(id, 'mtgo', format, face, version, pretty)

def arena(id:str, format:str='json', face:str=None, version:str='large', pretty:bool=False):
    return typeid(id, 'arena', format, face, version, pretty)

def tcgplayer(id:str, format:str='json', face:str=None, version:str='large', pretty:bool=False):
    return typeid(id, 'tcgplayer', format, face, version, pretty)

def cardmarket(id:str, format:str='json', face:str=None, version:str='large', pretty:bool=False):
    return typeid(id, 'cardmarket', format, face, version, pretty)

def id(id:str, format:str='json', face:str=None, version:str='large', pretty:bool=False):
    return typeid(id, None, format, face, version, pretty)

