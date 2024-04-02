# coding: utf8
import ckan.plugins.toolkit as tk
import ckan.logic.auth as logic_auth
import ckan.authz as authz
from ckan.common import g, _

from ckanext.laissezpasser.logic import (
    authpass,
)

from logging import getLogger

log = getLogger(__name__)

@tk.auth_allow_anonymous_access
def laissezpasser_check_package(context, data_dict):
    return {"success": True}


@tk.auth_allow_anonymous_access
def laissezpasser_check_resource(context, data_dict):
    return {"success": True}

def _sysadmin_only(context, data_dict):
    """ Only allowed to sysadmins or organization admins """
    if not g.userobj:
        return {'success': False, 'msg': _('Only sysadmins can create or remove passes')}

    if authz.is_sysadmin(g.user):
        return {'success': True}

    return {"success": False, 'msg': _('Only sysadmins can create or remove passes')}

def laissezpasser_create(context, data_dict):
    return _sysadmin_only(context, data_dict)


def laissezpasser_remove(context, data_dict):
    return _sysadmin_only(context, data_dict)


@tk.auth_allow_anonymous_access
@tk.chained_auth_function
def laissezpasser_resource_show(next_auth, context, data_dict=None):
    # no user, fall through
    if not g.userobj:
        return next_auth(context, data_dict)

    resource = data_dict.get("resource", context.get("resource", {}))
    if not resource:
        resource = logic_auth.get_resource_object(context, data_dict)
    if not isinstance(resource, dict):
        resource = resource.as_dict()

    user_name = _get_username_from_context(context)

    package = data_dict.get("package", {})
    if not package:
        model = context["model"]
        package = model.Package.get(resource.get("package_id"))
        package = package.as_dict()

    check_pass = authpass.laissezpasser_check_user_resource_access(user_name, resource, package)

    # if we have a pass return that result
    if check_pass:
        return check_pass

    # fall through otherwise
    return next_auth(context, data_dict)


def get_auth_functions():
    return {
        "laissezpasser_check_package": laissezpasser_check_package,
        "laissezpasser_check_resource": laissezpasser_check_resource,
        "laissezpasser_create": laissezpasser_create,
        "laissezpasser_remove": laissezpasser_create,
        "resource_show": laissezpasser_resource_show,
        "resource_view_show": laissezpasser_resource_show
    }

# internal functions

def _get_username_from_context(context):
    auth_user_obj = context.get("auth_user_obj", None)
    user_name = ""
    if auth_user_obj:
        user_name = auth_user_obj.as_dict().get("name", "")
    else:
        if authz.get_user_id_for_username(context.get("user"), allow_none=True):
            user_name = context.get("user", "")
    return user_name

