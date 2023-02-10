from urllib.parse import urlsplit
from io import BytesIO

# Need this for class functionality
import pyfall.scryobject.scryobject

import requests
from PIL import Image
from tqdm import tqdm

__all__ = [
    'scryObject',
    'scryList',
    'scrySet',
    'scryRuling',
    'scryCardSymbol',
    'scryCatalog',
    'scryManaCost',
    'scryBulkData',
]

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
        if urlsplit(uri).netloc != pyfall.scryobject.scryobject.SCRYFALL_NETLOC:
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
            return pyfall.scryobject.scryobject.getscryobject(uri, **kwargs)
    
    def hasscryattr(self, name):
        return name in self.scryfall_attributes
        

class scryList(scryObject):
    # def __new__(cls, data): ...
    def __init__(self, data):
        super().__init__(data)
        self.data = [pyfall.scryobject.scryobject.scryobjectfactory(entry) for entry in self.data]
    
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
            raise pyfall.scryobject.scryobject.RequestError("This list has no more pages.")

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

class scryRuling(scryObject): ...

class scryCardSymbol(scryObject): ...

class scryCatalog(scryObject): ...

class scryManaCost(scryObject): ...

class scryBulkData(scryObject):
    def __str__(self):
        return "{0:>16}:{1}".format(self.type, pyfall.scryobject.scryobject.sizeof_fmt(self.size))