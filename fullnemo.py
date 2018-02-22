from collections import Callable

from lxml import etree
import html

from flask import render_template, Blueprint, abort, Markup, send_from_directory, Flask, url_for, redirect, request

from flask_nemo import Nemo
from MyCapytain.resources.prototypes.cts.inventory import CtsWorkMetadata, CtsEditionMetadata
from MyCapytain.errors import UnknownCollection
from MyCapytain.common.constants import Mimetypes


class FullNemo(Nemo):

    ROUTES = Nemo.ROUTES + [
        ("/text/<objectId>/fulltext", "r_full_text", ["GET"])
    ]

    CACHED = Nemo.CACHED + [
        "r_full_text"
    ]

    def r_full_text(self, objectId, subreference=None, lang=None):
        """ Retrieve the text of the passage

        :param objectId: Collection identifier
        :type objectId: str
        :param lang: Lang in which to express main data
        :type lang: str
        :param subreference: Reference identifier
        :type subreference: str
        :return: Template, collections metadata and Markup object representing the text
        :rtype: {str: Any}
        """
        collection = self.get_collection(objectId)
        if isinstance(collection, CtsWorkMetadata):
            editions = [t for t in collection.children.values() if isinstance(t, CtsEditionMetadata)]
            if len(editions) == 0:
                raise UnknownCollection("This work has no default edition")
            return redirect(url_for(".r_passage", objectId=str(editions[0].id), subreference=subreference))
        text = self.get_passage(objectId=objectId, subreference=None)

        text_etree = text.export(Mimetypes.PYTHON.ETREE)
        fulltext = self.transform(text, text_etree, objectId)

        return {
            "template": "main::text.html",
            "objectId": objectId,
            "subreference": subreference,
            "collections": {
                "current": {
                    "label": collection.get_label(lang),
                    "id": collection.id,
                    "model": str(collection.model),
                    "type": str(collection.type),
                    "author": text.get_creator(lang),
                    "title": text.get_title(lang),
                    "description": collection.get_description(lang),
                    "citation": collection.citation,
                    "coins": self.make_coins(collection, text, "", lang=lang)
                },
                "parents": self.make_parents(collection, lang=lang)
            },
            "text_passage": fulltext,
            "prev": None,
            "next": None
        }