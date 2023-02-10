from io import BytesIO

from PIL import Image

# Need this for class functionality
import pyfall.scryobject.scryobject

# Need this for subclassing and typehinting
from .scryclasses import *

__all__ = [
    'scryCard',
    'scryCardFace',
    'scryRelatedCard',
]

class scryCard(scryObject):
    # def __new__(cls, data): ...
    def __init__(self, data):
        super().__init__(data)
        if self.hasscryattr('card_faces'):
            self.card_faces = [pyfall.scryobject.scryobject.scryobjectfactory(face) for face in self.card_faces]
        if self.hasscryattr('all_parts'):
            self.all_parts = [pyfall.scryobject.scryobject.scryobjectfactory(part) for part in self.all_parts]

    def __repr__(self):
        return "<scryCard: {0}-{1}-{2}>".format(self.set, self.collector_number, self.name)

    def __str__(self):
        return "{1:<5} #{2:>3}/{4}. {3}".format(self.set_name, self.set, self.collector_number, self.name)

    def getimage(self, version:str="large") -> bytes:
        """Calls the API with this card's image_uri."""
        payload = {"version":version}
        pyfall.scryobject.scryobject.validate_standard_params(payload)
        if (type(self) == scryCard) and (self.image_status == "missing"):
            raise pyfall.scryobject.scryobject.RequestError("This card has no available image.")
        if (type(self) == scryCard) and (self.layout in ["transforming", "modal_dfc", "reversible_card"]):
            raise pyfall.scryobject.scryobject.AmbiguityError("This card has faces on both sides. Hint: scryCardFace also has a getimage() method")
        with self.geturi(self.image_uris[payload["version"]]) as fp:
            image = fp.read()
        setattr(self, "image_{}".format(payload["version"]), image)
        return Image.open(BytesIO(image))
    
    def getset(self, **kwargs) -> scrySet:
        return self.getapiuri(self.set_uri, **kwargs)
    
    def searchsetcards(self, **kwargs) -> scryList:
        return self.getapiuri(self.set_search_uri, **kwargs)

    def getrulings(self, **kwargs):
        return self.getapiuri(self.rulings_uri, **kwargs)

class scryCardFace(scryObject):
    def getimage(self, version:str='large') -> bytes:
        return scryCard.getimage(self, version)

class scryRelatedCard(scryObject):
    def getcard(self) -> scryCard:
        return self.getapiuri(self.uri)