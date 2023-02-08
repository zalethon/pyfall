import pyfall.errors
import pyfall.scryobject
from pyfall.scryfall.API import StrPrototypes, callapi

def search(*, q: str,
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
        raise ValueError(StrPrototypes.VALUEERROR.format("unique",valid_unique,unique))
    if order not in valid_order:
        raise ValueError(StrPrototypes.VALUEERROR.format("order", valid_order, order))
    if dir not in valid_dir:
        raise ValueError(StrPrototypes.VALUEERROR.format("dir", valid_dir, dir))
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

    return pyfall.scryobject.processapiresponse(callapi("/cards/search", **payload))
