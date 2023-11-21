import ckan.plugins.toolkit as tk
import ckanext.laissezpasser.logic.schema as schema
import ckan.authz as authz

from ckan.common import g
from ckanext.laissezpasser import laissezpasser

def _get_plugin_extras(user):
    if 'plugin_extras' in user and user.get('plugin_extras') is not None:
        return user.get('plugin_extras')
    else:
        return {}


@tk.side_effect_free
def laissezpasser_check_package(context, data_dict):
    # Arguments
    #  package_id (string)
    #  user_id (string) - (optional)
    tk.check_access(
        "laissezpasser_check_package", context, data_dict)

    data, errors = tk.navl_validate(
        data_dict, schema.laissezpasser_check_package(), context)

    if errors:
        raise tk.ValidationError(errors)

    # if user_id is not set, use self
    effective_id = g.userobj.id
    user_id = data.get("user_id",None)

    # Raise an error if the user is not a sysadmin but has user_id set
    if user_id and not authz.is_sysadmin(effective_id):
        raise tk.ValidationError({
            'user_id': ['Only sysadmin admins or self can check.']
        })
    else:
        user_id = effective_id

    lp_dict = {
        "user_id": data.get("user_id"),
    }

    l = laissezpasser.get_laissezpasser(None,lp_dict)
    l.restore()

    # get the package and then it's name
    package_id = data.get("package_id")

    package_dict = tk.get_action("package_show")(
        dict(context, return_type="dict"), {"id": package_id}
    )

    package_name = package_dict.get("name")


    # return package name and date valid until
    return {
        "package_name": package_name,
        "valid": l.valid(package_name),
        "valid_until": l.check(package_name),
    }


@tk.side_effect_free
def laissezpasser_check_resource(context, data_dict):
    tk.check_access(
        "laissezpasser_check_resource", context, data_dict)

    data, errors = tk.navl_validate(
        data_dict, schema.laissezpasser_check_resource(), context)

    if errors:
        raise tk.ValidationError(errors)

    # get package from resource_id
    resource = tk.get_action('resource_show')(context, {'id': data.get("resource_id", "")})

    check_dict = dict(data_dict | { "package_id": resource.get("package_id", None) })

    return laissezpasser_check_package(context, check_dict)


def laissezpasser_create(context, data_dict):
    # Arguments
    #  user_id (string)
    #  package_id (string)
    #  valid_until (iso date string) - (optional)
    tk.check_access(
        "laissezpasser_create", context, data_dict)

    data, errors = tk.navl_validate(
        data_dict, schema.laissezpasser_create(), context)

    if errors:
        raise tk.ValidationError(errors)

    # Raise an error if the user is a sysadmin
    if data.get("user_id") and authz.is_sysadmin(data.get("user_id")):
            raise tk.ValidationError({
                'user_id': ['User is already a sysadmin.']
            })

    lp_dict = {
        "user_id": data.get("user_id"),
    }

    l = laissezpasser.get_laissezpasser(None,lp_dict)
    l.restore()

    # get the package and then it's name
    package_id = data.get("package_id")
    
    package_dict = tk.get_action("package_show")(
        dict(context, return_type="dict"), {"id": package_id}
    )

    package_name = package_dict.get("name")

    # logic for valid_until

    valid_until = data.get("valid_until",None)

    l.add(package_name, valid_until)

    l.save()

    # return package name and date valid until
    return {
        "package_name": package_name,
        "valid_until": l.check(package_name),
    }


def laissezpasser_remove(context, data_dict):
    # Arguments
    #  user_id (string)
    #  package_id (string)

    tk.check_access(
        "laissezpasser_remove", context, data_dict)
    data, errors = tk.navl_validate(
        data_dict, schema.laissezpasser_remove(), context)

    if errors:
        raise tk.ValidationError(errors)

    lp_dict = {
        "user_id": data.get("user_id"),
    }

    l = laissezpasser.get_laissezpasser(None,lp_dict)
    l.restore()

    # get the package and then it's name
    package_id = data.get("package_id")

    package_dict = tk.get_action("package_show")(
        dict(context, return_type="dict"), {"id": package_id}
    )

    package_name = package_dict.get("name")

    l.remove(package_name)

    l.save()

    return {}


def get_actions():
    return {
        'laissezpasser_check_package': laissezpasser_check_package,
        'laissezpasser_check_resource': laissezpasser_check_resource,
        'laissezpasser_create': laissezpasser_create,
        'laissezpasser_remove': laissezpasser_remove,
    }
