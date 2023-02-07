from urllib.parse import urlsplit

import requests

import pyfall.errors
import pyfall.scryapi

class scryObject:
    def __init__(self, data: dict):
        for key in data.keys():
            setattr(self, key, data[key])
        setattr(self, "scryfall_attributes", list(data.keys()))
    
    def geturi(self, uri: str) -> 'bytes | scryObject':
        """Download a URI, or make a call to the API as appropriate."""
        if uri in dir(self):
            # geturi('search_uri') will work, if there's a search_uri on this object
            uri = getattr(self, uri)
        if urlsplit(uri).netloc != pyfall.scryapi.scryfall_netloc:
            return requests.get(uri).content
        else:
            return processapiresponse(pyfall.scryapi.callapi(uri))
    
    def hasscryattr(self, name):
        return name in self.scryfall_attributes
        

class scryList(scryObject):
    # def __new__(cls, data): ...
    def __init__(self, data):
        super().__init__(data)
        self.data = [scryobjectfactory(entry) for entry in self.data]
    
    def getnext(self):
        if self.has_more:
            return self.geturi('next_page')
        else:
            raise pyfall.errors.RequestError("This list has no more pages.")

class scrySet(scryObject):
    # def __new__(cls, data): ...
    def getsvgicon(self) -> bytes:
        """Download this set's SVG Icon for manipulation or saving."""
        return self.geturi('icon_svg_uri')
    
    def listallcards(self):
        """Get a paginated list of all of the cards in this set."""
        allsetcards = self.geturi('search_uri')
        return allsetcards

class scryCard(scryObject):
    # def __new__(cls, data): ...
    def __init__(self, data):
        super().__init__(data)
        if getattr(self, 'card_faces', None) != None:
            self.card_faces = [scryobjectfactory(face) for face in self.card_faces]

    def getimage(self, type:str = 'large') -> bytes:
        valid_types = ['png', 'border_crop', 'art_crop', 'large', 'normal', 'small']
        if type.lower() not in valid_types:
            raise ValueError("Specified type must be one of {0}".format(valid_types))
        if self.image_status == "missing":
            raise pyfall.errors.RequestError("This card has no available image.")
        try:
            image = self.geturi(self.image_uris[type])
        except AttributeError:
            if getattr(self, 'card_faces', None) != None:
                raise pyfall.errors.RequestError("This card has multiple faces.")
            raise
        return image

class scryCardFace(scryCard):
    # def __new__(cls, data): ...
    pass

class scryRelatedCard(scryCard):
    # def __new__(cls, data): ...
    pass

class scryRuling(scryObject):
    # def __new__(cls, data): ...
    pass

class scryCardSymbol(scryObject):
    # def __new__(cls, data): ...
    pass

class scryCatalog(scryObject):
    # def __new__(cls, data): ...
    pass

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
    }

    if scryjson["object"] == "error":
        raise pyfall.errors.APIError(scryjson)
    return scry_classes[scryjson["object"]](scryjson)