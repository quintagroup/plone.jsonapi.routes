# -*- coding: utf-8 -*-

from plone import api as ploneapi
from plone.jsonapi.routes import request as req
from plone.jsonapi.routes import add_plone_route
from plone.jsonapi.routes.api import url_for
from plone.protect.authenticator import createToken

def get_user_info(username=None, short=True):
    """ return the user informations
    """

    # XXX: refactoring needed in this function

    user = None
    anon = ploneapi.user.is_anonymous()
    current = ploneapi.user.get_current()

    # no username, go and get the current user
    if username is None:
        user = current
    else:
        user = ploneapi.user.get(username)

    if not user:
        raise KeyError('User not found')

    info = {
        "id":       user.getId(),
        "username": user.getUserName(),
        "url":      url_for("users", username=user.getUserName())
    }

    # return base info
    if short or anon:
        return info

    # try to get extended infos
    pu = user.getUser()
    properties = {}
    if "mutable_properties" in pu.listPropertysheets():
        mp = pu.getPropertysheet("mutable_properties")
        properties = dict(mp.propertyItems())

    def to_iso8601(dt=None):
        if dt is None:
            return ""
        return dt.ISO8601()

    # include mutable properties if short==False
    info.update({
        "email":           properties.get("email"),
        "fullname":        properties.get("fullname"),
        "login_time":      to_iso8601(properties.get("login_time")),
        "last_login_time": to_iso8601(properties.get("last_login_time")),
        "roles":           user.getRoles(),
        "groups":          pu.getGroups(),
        "authenticated":   current == user and not anon,
    })

    return info


#-----------------------------------------------------------------------------
# API ROUTES
#-----------------------------------------------------------------------------

@add_plone_route("/users", "users", methods=["GET"])
@add_plone_route("/users/<string:username>", "users", methods=["GET"])
def get(context, request, username=None):
    """ Plone users route
    """

    items = []

    if ploneapi.user.is_anonymous():
        raise RuntimeError("Not allowed for anonymous users")

    # list all users if no username was given
    if username is None:
        users = ploneapi.user.get_users()

        for user in users:
            items.append(get_user_info(user.getId()))

    # special user 'current' which retrieves the current user infos
    elif username == "current":
        items.append(get_user_info(short=False))

    # we have a username, go and get the infos for it
    else:
        info = get_user_info(username, short=False)
        items.append(info)

    return {
        "url": url_for("users"),
        "count": len(items),
        "items": items,
        "success": True
    }


@add_plone_route("/auth", "auth", methods=["GET"])
def auth(context, request):
    """ Authenticate
    """

    if ploneapi.user.is_anonymous():
        request.response.setStatus(401)
        request.response.setHeader('WWW-Authenticate', 'basic realm="JSONAPI AUTH"', 1)
    else:
        request.response.setHeader('X-CSRF-TOKEN', createToken())
    return {}


@add_plone_route("/logout", "logout", methods=["POST"])
def logout(context, request):
    """ Authenticate
    """
    portal_membership = ploneapi.portal.get_tool('portal_membership')
    portal_membership.logoutUser(request)
    return {}

# vim: set ft=python ts=4 sw=4 expandtab :
