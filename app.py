# -*- coding: utf-8 -*-
from flask import Flask
from capitains_nautilus.cts.resolver import NautilusCTSResolver
from capitains_nautilus.flask_ext import FlaskNautilus
from fullnemo import FullNemo
#from flask_nemo.fullnemo import FullNemo
from dispatcher import dispatcher

flask_app = Flask("Flask Application for Nemo")
resolver = NautilusCTSResolver(["/usr/share/dh-data/theses"], dispatcher=dispatcher)
#resolver.parse()

nautilus_api = FlaskNautilus(prefix="/nemo/api", app=flask_app, resolver=resolver)

nemo = FullNemo(
    name="Positions de thèse",
    app=flask_app,
    resolver=resolver,
    base_url="/nemo",
    css=["assets/css/html.css", "assets/css/postprod.css"],
    js=["assets/js/Tree.js", "assets/js/postprod.js"],
    statics=["assets/images/logo.png"],
    transform={"default": "assets/xsl/tei2html.xsl", "common" : "assets/xsl/common.xsl"},
    templates={"main": "templates/main"}
)

if __name__ == "__main__":
    flask_app.run(debug=True)
