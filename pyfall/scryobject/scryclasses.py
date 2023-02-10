from io import BufferedRandom
# Need this for class functionality
import pyfall.scryobject.scryobject

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
        self.scryfall_attributes = list(data.keys())
        for key in data.keys():
            setattr(self, key, data[key])
    
    def geturi(self, uri: str, *, sizeof=None, chunksize=1024**2, **kwargs) -> BufferedRandom:
        """Download a URI to a temporary file.
        
            sizeof is the size of the file we're getting, if we happen to know it
            (as in the case of bulk data)
        """
        # geturi('search_uri') will work, if there's a search_uri on this object
        if uri in dir(self):
            uri = getattr(self, uri)
        return pyfall.scryobject.scryobject.geturi(uri, sizeof=sizeof, chunksize=chunksize, **kwargs)
    
    def getapiuri(self, uri: str, **kwargs) -> 'scryObject':
        """Make an API call from a uri, and wrap it in the right class."""
        if uri in dir(self):
            uri = getattr(self, uri)
        return pyfall.scryobject.scryobject.getapiuri(uri, **kwargs)

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
            return self.getapiuri('next_page')
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
        with self.geturi('icon_svg_uri') as fp:
            contents = fp.read()
        return contents
    
    def searchcards(self, **kwargs) -> scryList:
        """Get a paginated list of all of the cards in this set.
        
        Equivalent to a scryfall.cards.search() call"""
        allsetcards = self.getapiuri('search_uri', **kwargs)
        return allsetcards

class scryRuling(scryObject): ...

class scryCardSymbol(scryObject): ...

class scryCatalog(scryObject): ...

class scryManaCost(scryObject): ...

class scryBulkData(scryObject):
    def __str__(self):
        return "{0:>16}:{1}".format(self.type, pyfall.scryobject.scryobject.sizeof_fmt(self.size))