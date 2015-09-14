# -*- coding: utf-8 -*-

from plone.jsonapi.routes import add_plone_route

# CRUD
from plone.jsonapi.routes.api import get_batched
from plone.jsonapi.routes.api import create_items
from plone.jsonapi.routes.api import update_items
from plone.jsonapi.routes.api import delete_items
from plone.jsonapi.routes.decorators import returns_plone_items_for

from plone.jsonapi.routes.api import url_for


# GET
@add_plone_route("/cards", "cards", methods=["GET"])
@add_plone_route("/cards/<string:uid>", "cards", methods=["GET"])
@returns_plone_items_for("cards")
def get(context, request, uid=None):
    """ get cards
    """
    return get_batched("shmresearch.card", uid=uid, endpoint="cards")


# CREATE
@add_plone_route("/cards/create", "cards_create", methods=["POST"])
@add_plone_route("/cards/create/<string:uid>", "cards_create", methods=["POST"])
def create(context, request, uid=None):
    """ create cards
    """
    items = create_items("shmresearch.card", uid=uid, endpoint="cards")
    return {
        "url": url_for("cards_create"),
        "count": len(items),
        "items": items,
    }


# UPDATE
@add_plone_route("/cards/update", "cards_update", methods=["POST"])
@add_plone_route("/cards/update/<string:uid>", "cards_update", methods=["POST"])
def update(context, request, uid=None):
    """ update cards
    """
    items = update_items("shmresearch.card", uid=uid, endpoint="cards")
    return {
        "url": url_for("cards_update"),
        "count": len(items),
        "items": items,
    }


# DELETE
@add_plone_route("/cards/delete", "cards_delete", methods=["POST"])
@add_plone_route("/cards/delete/<string:uid>", "cards_delete", methods=["POST"])
def delete(context, request, uid=None):
    """ delete cards
    """
    items = delete_items("shmresearch.card", uid=uid, endpoint="cards")
    return {
        "url": url_for("cards_delete"),
        "count": len(items),
        "items": items,
    }

# vim: set ft=python ts=4 sw=4 expandtab :
