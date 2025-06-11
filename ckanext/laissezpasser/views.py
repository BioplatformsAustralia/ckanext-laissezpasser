from flask import Blueprint
from flask.views import MethodView
from ckan.common import _, g
from ckan.lib.base import render, abort, request
from ckan.logic import get_action, ValidationError, NotFound, NotAuthorized
import datetime
import ckan.authz as authz
import ckan.logic as logic
import ckan.model as model
import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as h
import ckan.lib.navl.dictization_functions as dict_fns


laissezpasser = Blueprint("laissezpasser", __name__)


class LaissezPasserEditView(MethodView):
    def post(self, id):
        context = {"model": model, "user": g.user}

        try:
            form_dict = logic.clean_dict(
                dict_fns.unflatten(logic.tuplize_dict(logic.parse_params(request.form)))
            )

            user = get_action("user_show")(context, {"id": form_dict["username"]})

            data_dict = {
                "package_id": id,
                "user_id": user["id"],
                "expires_in": form_dict.get("expires_in"),
            }

            get_action("laissezpasser_create")(context, data_dict)

        except dict_fns.DataError:
            return abort(400, _("Integrity Error"))
        except NotAuthorized:
            message = _("Unauthorized to create pass {}").format(id)
            return abort(401, _(message))
        except NotFound as e:
            h.flash_error(_("User not found"))
            return h.redirect_to("laissezpasser.new_laissezpasser", id=id)
        except ValidationError as e:
            h.flash_error(e.error_summary)
            return h.redirect_to("laissezpasser.new_laissezpasser", id=id)
        else:
            h.flash_success(_("User pass to dataset"))

        return h.redirect_to("laissezpasser.passes_read", id=id)

    def get(self, id):
        context = {"model": model, "user": g.user}
        data_dict = {"id": id}

        try:
            toolkit.check_access("laissezpasser_create", context, data_dict)
            # needed to ckan_extend package/edit_base.html
            pkg_dict = get_action("package_show")(context, data_dict)
        except NotAuthorized:
            message = "Unauthorized to create access passses {}".format(id)
            return abort(401, _(message))
        except NotFound:
            return abort(404, _("Resource not found"))

        user = request.args.get("user_id")
        user_capacity = "member"

        if user:
            user = get_action("user_show")(context, {"id": user})

        extra_vars = {
            "user": user,
            "pkg_dict": pkg_dict,
        }

        return render("ckanext_laissezpasser/package_passes_new.html", extra_vars)


def pass_index(target_user):
    if g.userobj is None:
        return h.redirect_to("user.login")

    site_user = logic.get_action("get_site_user")({"ignore_auth": True}, {})["name"]
    ctx = {"ignore_auth": True, "user": site_user}
    # Only admins can view another user's cart
    username = g.userobj.name

    if g.userobj.name != target_user:
        if g.userobj.sysadmin is True:
            username = target_user
        else:
            return toolkit.redirect_to(f"/passes/{username}")

    try:
        user_dict = logic.get_action("user_show")(
            ctx,
            {
                "include_num_followers": True,
                "include_plugin_extras": True,
                "id": username,
            },
        )
    except logic.NotFound:
        return toolkit.redirect_to(f"/passes/{g.userobj.name}")

    return render(
        "ckanext_laissezpasser/passes.html", extra_vars={"user_dict": user_dict}
    )


def passes_read(id):
    return h.redirect_to("laissezpasser.new_laissezpasser", id=id)


def passes_expire(id, user_id):
    context = {"model": model, "user": g.user}

    try:
        form_dict = logic.clean_dict(
            dict_fns.unflatten(logic.tuplize_dict(logic.parse_params(request.form)))
        )

        # This should set the pass to now explicitly expiring
        now = datetime.datetime.utcnow()

        data_dict = {
            "package_id": id,
            "user_id": user_id,
            "valid_until": now,
        }

        # this will overwrite the existing pass for the user
        get_action("laissezpasser_create")(context, data_dict)

    except dict_fns.DataError:
        return abort(400, _("Integrity Error"))
    except NotAuthorized:
        message = _("Unauthorized to create pass {}").format(id)
        return abort(401, _(message))
    except NotFound as e:
        h.flash_error(_("User not found"))
        return h.redirect_to("laissezpasser.new_laissezpasser", id=id)
    except ValidationError as e:
        h.flash_error(e.error_summary)
        return h.redirect_to("laissezpasser.new_laissezpasser", id=id)
    else:
        h.flash_success(_("Pass expired"))

    return h.redirect_to("laissezpasser.passes_read", id=id)


def passes_delete(id, user_id):
    context = {"model": model, "user": g.user}

    try:
        form_dict = logic.clean_dict(
            dict_fns.unflatten(logic.tuplize_dict(logic.parse_params(request.form)))
        )

        data_dict = {
            "package_id": id,
            "user_id": user_id,
        }

        get_action("laissezpasser_remove")(context, data_dict)

    except dict_fns.DataError:
        return abort(400, _("Integrity Error"))
    except NotAuthorized:
        message = _("Unauthorized to delete pass {}").format(id)
        return abort(401, _(message))
    except NotFound as e:
        h.flash_error(_("User not found"))
    except ValidationError as e:
        h.flash_error(e.error_summary)
    else:
        h.flash_success(_("Pass deleted"))

    return h.redirect_to("laissezpasser.passes_read", id=id)


laissezpasser.add_url_rule("/passes/<target_user>", view_func=pass_index)

laissezpasser.add_url_rule(
    rule="/<id>/passes",
    view_func=passes_read,
    methods=[
        "GET",
    ],
)

laissezpasser.add_url_rule(
    rule="/<id>/passes/new",
    view_func=LaissezPasserEditView.as_view(str("new_laissezpasser")),
    methods=[
        "GET",
        "POST",
    ],
)

laissezpasser.add_url_rule(
    rule="/<id>/passes/delete/<user_id>",
    view_func=passes_delete,
    methods=[
        "POST",
    ],
)

laissezpasser.add_url_rule(
    rule="/<id>/passes/expire/<user_id>",
    view_func=passes_expire,
    methods=[
        "POST",
    ],
)


def get_blueprints():
    return [laissezpasser]
