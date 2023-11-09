from flask import Blueprint
from ckan.common import g
from ckan.lib.base import render, abort, request
import ckan.logic as logic
import ckan.plugins.toolkit as toolkit



laissezpasser = Blueprint(
    "laissezpasser", __name__)


def pass_index(target_user):
    if g.userobj is None:
        return h.redirect_to('user.login')

    site_user = logic.get_action("get_site_user")({'ignore_auth': True}, {})["name"]
    ctx = {"ignore_auth": True, "user": site_user }
    # Only admins can view another user's cart
    username = g.userobj.name
    if g.userobj.name != target_user:
        if g.userobj.sysadmin is True:
            username = target_user
        else:
            return toolkit.redirect_to(f"/passes/{username}")

    try:
        user_dict = logic.get_action("user_show")(ctx, {"include_num_followers":True, "include_plugin_extras": True, "id": username})
    except logic.NotFound:
        return toolkit.redirect_to(f"/passes/{g.userobj.name}")

    return render("laissezpasser/passes.html",extra_vars={ "user_dict": user_dict })


laissezpasser.add_url_rule("/passes/<target_user>", view_func=pass_index)


def get_blueprints():
    return [laissezpasser]
