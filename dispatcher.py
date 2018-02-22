from MyCapytain.resources.prototypes.cts.inventory import CtsTextInventoryCollection, CtsTextInventoryMetadata
from MyCapytain.resolvers.utils import CollectionDispatcher


tic = CtsTextInventoryCollection()
positions = CtsTextInventoryMetadata("urn:cts:frenchLit", parent=tic)
positions.set_label("Positions de thèse", "fr")

dispatcher = CollectionDispatcher(tic)


@dispatcher.inventory("urn:cts:frenchLit")
def dispatchFrenchLit(collection, path=None, **kwargs):
    if collection.id.startswith("urn:cts:frenchLit:"):
        return True
    return False

