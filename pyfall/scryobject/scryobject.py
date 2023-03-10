"""scryobject module is a single interface point between the Scryfall Object
Classes and the rest of the library. So we pull in stuff the classes need,
and we export all of the classes as well as our own factory functionality.

For the classes and the scryfall module, this is where API calls go through.
For the classes and the scryfall module, this is where API calls go through.

Mostly this is to resolve weird circular dependencies; should make maintenance
easier too."""

from urllib.parse import urlsplit
from io import BufferedRandom

import requests

# These are used by the classes.
from pyfall.util import validate_standard_params, sizeof_fmt
from pyfall.errors import RequestError, AmbiguityError, APIError

# These are used by this module.
import pyfall.api
import pyfall.errors

# Pulling in the classes for export and for factory purposes.
from pyfall.scryobject.scryclasses import *
from pyfall.scryobject.scrycard import *

__all__ = [
    'scryObject',
    'scryList',
    'scrySet',
    'scryCard',
    'scryCardFace',
    'scryRelatedCard',
    'scryRuling',
    'scryCardSymbol',
    'scryCatalog',
    'scryManaCost',
    'scryBulkData',
    'processapiresponse',
    'processjson',
#    'scryobjectfactory',
    'getapiuri',
    'getapiuri',
]

def processapiresponse(response: requests.Response) -> scryObject:
    """Wraps requests.Response from the scryfall api inside an appropriate class for manipulation."""
    if response.headers['content-type'] not in ['application/json; charset=utf-8']:
        raise TypeError("Expected json stream, got {0}".format(response.headers['content-type']))
    return processjson(response.json())

def processjson(jsonlike: dict) -> scryObject:
    """Takes a json dict from scryfall api output and wraps it in an appropriate class."""
    scry_classes = {
        "list":scryList,
        "set":scrySet,
        "card":scryCard,
        "card_face":scryCardFace,
        "related_card":scryRelatedCard,
        "ruling":scryRuling,
        "card_symbol":scryCardSymbol,
        "catalog":scryCatalog,
        "mana_cost":scryManaCost,
        "bulk_data":scryBulkData,
    }

    if jsonlike["object"] == "error":
        raise pyfall.errors.APIError(jsonlike)
    return scry_classes[jsonlike["object"]](jsonlike)

"""scryobjectfactory is equivalent to scryobjectfactory."""
scryobjectfactory = processjson

def getapiuri(call:str, **kwargs) -> scryObject:
    """Makes a call to the API, and processes it into the right class."""
    return processapiresponse(pyfall.api.getapiresponse(call, **kwargs))

def geturi(uri:str, *, sizeof:int=None, chunksize:int=1024**2, **kwargs) -> BufferedRandom:
    """Downloads bytes to a temp file."""
    return pyfall.api.getcontents(uri, sizeof=sizeof, chunksize=chunksize, **kwargs)