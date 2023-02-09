# pyfall
Another python interface for the Scryfall REST API.
 
I wrote this library as part of another project. I think I will keep working on it after the other project is done, it has been a fun exercise.
 
It currently exists in a state suitable to my needs, but I've done my best to write it in a way to be reusable and easily-maintained and updated. I will publish it properly someday.
 
For now, consider this to be version 0.0.2. It needs some polishing and the rest of the API added.
 
# usage
You'll need Python 3.10, probably. I haven't tested it with older versions.
`pip install -r requirements.txt`

    >>> # Import the module
    >>> from pyfall import scryfall
    
    >>> # I tried to match the API calls as closely as I could--why fix what ain't broke?
    >>> # So https://api.scryfall.com/search?q=c%3Ared+pow%3D3&order=cmc, you can use this:
    >>> results = scryfall.cards.search(q="c:red pow=3", order='cmc')
    >>> results
    ... <scryList: 175 objects>
    
    >>> # For what it's worth, the list is actually much longer.
    >>> # You can access properties of objects returned by the API through normal addressing.
    >>> results.total_cards
    ... 669
    
    >>> # These lists you can also index and slice. I'll be implementing more of this kind of thing.
    >>> results[25:30]
    ... [<scryCard: gs1-23-Leopard-Spotted Jiao>, <scryCard: m19-151-Lightning Mare>, <scryCard: frf-108-Mardu Scout>, <scryCard: ody-206-Minotaur Explorer>, <scryCard: a25-143-Mogg Flunkies>]
    
So far only the /cards and /set API are implemented this way; the exception is /cards/collections, which is a POST method so I haven't bothered to implement it yet. I have no need for it right now.

I'll write more thorough documentation, or see if I can't generate it. It's not bad to look at though if I can say that; it shouldn't be hard to figure out how to use it if you know a bit of Python.
