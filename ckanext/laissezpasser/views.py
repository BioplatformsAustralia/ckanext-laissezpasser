from flask import Blueprint
from flask.views import MethodView
from ckan.common import _, g
from ckan.lib.base import render, abort, request
from ckan.logic import get_action, ValidationError, NotFound, NotAuthorized
import ckan.authz as authz
import ckan.logic as logic
import ckan.model as model
import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as h
import ckan.lib.navl.dictization_functions as dict_fns



laissezpasser = Blueprint(
    "laissezpasser", __name__)

# FIXME
class LaissezPasserEditView(MethodView):

    def post(self, id):
    # FIXME model
        context = {u'model': model, u'user': g.user}

        try:
            form_dict = logic.clean_dict(
                dict_fns.unflatten(
                    logic.tuplize_dict(
                        logic.parse_params(request.form))))

            user = get_action(u'user_show')(
                context, {u'id': form_dict[u'username']}
            )

            data_dict = {
                u'package_id': id,
                u'user_id': user[u'id'],
                u'expires_in': form_dict.get(u'expires_in'),
            }

            get_action(u'laissezpasser_create')(
                context, data_dict)

        except dict_fns.DataError:
            return abort(400, _(u'Integrity Error'))
        except NotAuthorized:
            message = _(u'Unauthorized to create pases {}').format(id)
            return abort(401, _(message))
        except NotFound as e:
            h.flash_error(_(u'User not found'))
            return h.redirect_to(u'laissezpasser.new_laissezpasser', id=id)
        except ValidationError as e:
            h.flash_error(e.error_summary)
            return h.redirect_to(u'laissezpasser.new_laissezpasser', id=id)
        else:
            h.flash_success(_(u'User pass to dataset'))

        return h.redirect_to(u'laissezpasser.passes_read', id=id)

    def get(self, id):
        context = {u'model': model, u'user': g.user}
        data_dict = {u'id': id}

        try:
            toolkit.check_access(u'laissezpasser_create', context, data_dict)
            # needed to ckan_extend package/edit_base.html
            pkg_dict = get_action(u'package_show')(context, data_dict)
        except NotAuthorized:
            message = u'Unauthorized to create access passses {}'.format(id)
            return abort(401, _(message))
        except NotFound:
            return abort(404, _(u'Resource not found'))

        user = request.params.get(u'user_id')
        user_capacity = u'member'

        if user:
            user = get_action(u'user_show')(context, {u'id': user})

        extra_vars = {
            u'user': user,
            u'pkg_dict': pkg_dict,
        }

        return render(
            u'ckanext_laissezpasser/package_passes_new.html', extra_vars)


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

    return render("ckanext_laissezpasser/passes.html",extra_vars={ "user_dict": user_dict })

#FIXME 
def passes_read(id):
    # FIXME
    return pass_index(g.userobj.id)

#FIXME 
def passes_delete(id, user_id):
    # FIXME
    return pass_index(g.userobj.id)

laissezpasser.add_url_rule("/passes/<target_user>", view_func=pass_index)

laissezpasser.add_url_rule(
    rule=u'/<id>/passes',
    view_func=passes_read,
    methods=['GET', ]
)

laissezpasser.add_url_rule(
    rule=u'/<id>/passes/new',
    view_func=LaissezPasserEditView.as_view(str(u'new_laissezpasser')),
    methods=[u'GET', u'POST', ]
)

laissezpasser.add_url_rule(
    rule=u'/<id>/passes/delete/<user_id>',
    view_func=passes_delete, methods=['POST', ]
)


def get_blueprints():
    return [laissezpasser]
