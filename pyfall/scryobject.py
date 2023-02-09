from urllib.parse import urlsplit

import requests

import pyfall.errors
import pyfall.scryfall
from pyfall.scryfall.API import StrPrototypes

class scryObject:
    def __init__(self, data: dict):
        for key in data.keys():
            setattr(self, key, data[key])
        setattr(self, "scryfall_attributes", list(data.keys()))
    
    def geturi(self, uri: str, **kwargs) -> 'bytes | scryObject':
        """Download a URI, or make a call to the API as appropriate.
        
            Keyword args ignored for non-API URIs.
        """
        if uri in dir(self):
            # geturi('search_uri') will work, if there's a search_uri on this object
            uri = getattr(self, uri)
        if urlsplit(uri).netloc != pyfall.scryfall.API.SCRYFALL_NETLOC:
            return requests.get(uri).content
        else:
            return processapiresponse(pyfall.scryfall.API.callapi(uri, **kwargs))
    
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
        return "{1:<5} #{2:>3}. {3}".format(self.set_name, self.set, self.collector_number, self.name)

    def getimage(self, type:str = 'large', **kwargs) -> bytes:
        valid_types = ['png', 'border_crop', 'art_crop', 'large', 'normal', 'small']
        if type.lower() not in valid_types:
            raise ValueError(StrPrototypes.VALUEERROR.format("type", valid_types, type))
        if self.image_status == "missing":
            raise pyfall.errors.RequestError("This card has no available image.")
        try:
            image = self.geturi(self.image_uris[type], **kwargs)
        except AttributeError:
            if self.layout in ["transforming", "modal_dfc", "reversible_card"]:
                raise pyfall.errors.AmbiguityError("This card has faces on both sides. Hint: scryCardFace is a subclass of scryCard")
        return image
    
    def getset(self, **kwargs):
        return self.geturi(self.set_uri, **kwargs)
    
    def listallsetcards(self, **kwargs):
        return self.geturi(self.set_search_uri, **kwargs)

    def getrulings(self, **kwargs):
        return self.geturi(self.rulings_uri, **kwargs)

class scryCardFace(scryObject):
    def getimage(self, type:str='large', **kwargs):
        return scryCard.getimage(self, **kwargs)

class scryRelatedCard(scryObject):
    def getcard(self):
        return self.geturi(self.uri)

class scryRuling(scryObject): ...

class scryCardSymbol(scryObject): ...

class scryCatalog(scryObject): ...

class scryManaCost(scryObject): ...

def processapiresponse(response: requests.Response) -> scryObject:
    """Wraps requests.Response from the scryfall api inside an appropriate class for manipulation."""
    if response.headers['content-type'] not in ['application/json; charset=utf-8']:
        raise TypeError("Expected json stream, got {0}".format(response.headers['content-type']))
    scryjson = response.json()
    return scryobjectfactory(scryjson)

def scryobjectfactory(scryjson: dict) -> scryObject:
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
    }

    if scryjson["object"] == "error":
        raise pyfall.errors.APIError(scryjson)
    return scry_classes[scryjson["object"]](scryjson)