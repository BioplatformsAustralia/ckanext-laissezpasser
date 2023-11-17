import ckan.plugins.toolkit as tk
import ckanext.laissezpasser.logic.schema as schema
import ckan.authz as authz

from ckanext.laissezpasser import laissezpasser

def _get_plugin_extras(user):
    if 'plugin_extras' in user and user.get('plugin_extras') is not None:
        return user.get('plugin_extras')
    else:
        return {}


@tk.side_effect_free
def laissezpasser_check_package(context, data_dict):
    tk.check_access(
        "laissezpasser_check_package", context, data_dict)
    return {}


@tk.side_effect_free
def laissezpasser_check_resource(context, data_dict):
    tk.check_access(
        "laissezpasser_check_resource", context, data_dict)
def laissezpasser_create(context, data_dict):
    tk.check_access(
        "laissezpasser_create", context, data_dict)
    # Arguments
    #  user_id (string)
    #  package_id (string)
    #  valid_until (iso date string) - (optional)

    data, errors = tk.navl_validate(
        data_dict, schema.laissezpasser_create(), context)

    if errors:
        raise tk.ValidationError(errors)

    # Raise an error if the user is a sysadmin
    if data.get("user_id") and authz.is_sysadmin(data.get("user_id")):
            raise tk.ValidationError({
                'user_id': ['User is already a sysadmin.']
            })

    # look at resource_create
    log.warn(context)
    log.warn(data_dict)

    lp_dict = {
        "user_id": data.get("user_id"),
    }
    log.warn(lp_dict)

    l = laissezpasser.get_laissezpasser(None,lp_dict)
    l.restore()

    # get the package and then it's name
    package_id = data.get("package_id")
    
    package_dict = tk.get_action("package_show")(
        dict(context, return_type="dict"), {"id": package_id}
    )

    package_name = package_dict.get("name")

    # logic for valid_until

    valid_until = None

    l.add(package_name, valid_until)

    l.save()

    # return package name and date valid until
    return {
        "package_name": package_name,
        "valid_until": l.check(package_name),
    }


def laissezpasser_remove(context, data_dict):
    tk.check_access(
        "laissezpasser_remove", context, data_dict)
    data, errors = tk.navl_validate(
        data_dict, schema.laissezpasser_remove(), context)

    if errors:
        raise tk.ValidationError(errors)
    return {}


def get_actions():
    return {
        #'laissezpasser_get_sum': laissezpasser_get_sum,
        'laissezpasser_check_package': laissezpasser_check_package,
        'laissezpasser_check_resource': laissezpasser_check_resource,
        'laissezpasser_create': laissezpasser_create,
        'laissezpasser_remove': laissezpasser_remove,
    }
