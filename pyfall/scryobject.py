from urllib.parse import urlsplit
from io import BytesIO
import json

import requests
from PIL import Image
from tqdm import tqdm

import pyfall.errors
from .scryfall.api import SCRYFALL_NETLOC, apiget
from .scryfall.util import validate_standard_params, sizeof_fmt

class scryObject:
    def __init__(self, data: dict):
        for key in data.keys():
            setattr(self, key, data[key])
        setattr(self, "scryfall_attributes", list(data.keys()))
    
    def geturi(self, uri: str, *, sizeof=None, chunksize=1024**2, **kwargs) -> 'bytes | scryObject':
        """Download a URI, or make a call to the API as appropriate.
        
            sizeof is the size of the file we're getting, if we happen to know it
            (as in the case of bulk data)

            Keyword args ignored for non-API URIs.
        """
        if uri in dir(self):
            # geturi('search_uri') will work, if there's a search_uri on this object
            uri = getattr(self, uri)
        if urlsplit(uri).netloc != SCRYFALL_NETLOC:
            buffer = BytesIO()
            with requests.get(uri, stream=True) as r:
                if 'content-length' in r.headers:
                    sizeof = r.headers['content-length']
                for bytes in tqdm(r.iter_content(chunksize),total=(sizeof/chunksize) if sizeof else None):
                    buffer.write(bytes)
                buffer.seek(0)
                #contents = buffer.read()
            return buffer
        else:
            return getscryobject(uri, **kwargs)
    
    def hasscryattr(self, name):
        return name in self.scryfall_attributes
        

class scryList(scryObject):
    # def __new__(cls, data): ...
    def __init__(self, data):
        super().__init__(data)
        self.data = [scryobjectfactory(entry) for entry in self.data]
    
    def __getitem__(self, key):
        return self.data[key]

    def __repr__(self):
        return "<scryList: {0} objects>".format(len(self.data))
     
    def __str__(self):
        return '\n'.join([str(item) for item in self.data])

    def getnext(self):
        if self.has_more:
            return self.geturi('next_page')
        else:
            raise pyfall.errors.RequestError("This list has no more pages.")

class scrySet(scryObject):
    def __repr__(self):
        return "<scrySet: {0} ({1})>".format(self.name, self.id)

    def __str__(self):
        return "{0} ({1})".format(self.name, self.code)

    def getsvgicon(self) -> bytes:
        """Download this set's SVG Icon for manipulation or saving."""
        # TODO: image encoding?
        return self.geturi('icon_svg_uri')
    
    def searchcards(self, **kwargs):
        """Get a paginated list of all of the cards in this set.
        
        Equivalent to a scryfall.cards.search() call"""
        allsetcards = self.geturi('search_uri', **kwargs)
        return allsetcards

class scryCard(scryObject):
    # def __new__(cls, data): ...
    def __init__(self, data):
        super().__init__(data)
        if self.hasscryattr('card_faces'):
            self.card_faces = [scryobjectfactory(face) for face in self.card_faces]
        if self.hasscryattr('all_parts'):
            self.all_parts = [scryobjectfactory(part) for part in self.all_parts]

    def __repr__(self):
        return "<scryCard: {0}-{1}-{2}>".format(self.set, self.collector_number, self.name)

    def __str__(self):
        return "{1:<5} #{2:>3}/{4}. {3}".format(self.set_name, self.set, self.collector_number, self.name)

    def getimage(self, version:str="large") -> bytes:
        """Calls the API with this card's image_uri."""
        payload = {"version":version}
        validate_standard_params(payload)
        if (type(self) == scryCard) and (self.image_status == "missing"):
            raise pyfall.errors.RequestError("This card has no available image.")
        if (type(self) == scryCard) and (self.layout in ["transforming", "modal_dfc", "reversible_card"]):
            raise pyfall.errors.AmbiguityError("This card has faces on both sides. Hint: scryCardFace also has a getimage() method")
        image = BytesIO(self.geturi(self.image_uris[payload["version"]]))
        setattr(self, "image_{}".format(payload["version"]), image)
        return Image.open(image)
    
    def getset(self, **kwargs):
        return self.geturi(self.set_uri, **kwargs)
    
    def searchsetcards(self, **kwargs):
        return self.geturi(self.set_search_uri, **kwargs)

    def getrulings(self, **kwargs):
        return self.geturi(self.rulings_uri, **kwargs)

class scryCardFace(scryObject):
    def getimage(self, version:str='large'):
        return scryCard.getimage(self, version)

class scryRelatedCard(scryObject):
    def getcard(self):
        return self.geturi(self.uri)

class scryRuling(scryObject): ...

class scryCardSymbol(scryObject): ...

class scryCatalog(scryObject): ...

class scryManaCost(scryObject): ...

class scryBulkData(scryObject):
    def __str__(self):
        return "{0:>16}:{1}".format(self.type, sizeof_fmt(self.size))
    

def processapiresponse(response: requests.Response) -> scryObject:
    """Wraps requests.Response from the scryfall api inside an appropriate class for manipulation."""
    if response.headers['content-type'] not in ['application/json; charset=utf-8']:
        raise TypeError("Expected json stream, got {0}".format(response.headers['content-type']))
    return processjson(response.json())

def processjson(jsonlike:dict|list):
    return scryobjectfactory(jsonlike)

def scryobjectfactory(jsonlike: dict) -> scryObject:
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

def getscryobject(call:str, **kwargs):
    return processapiresponse(apiget(call, **kwargs))