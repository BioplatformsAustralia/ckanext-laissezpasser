# coding: utf8

from ckanext.laissezpasser import laissezpasser

from logging import getLogger

log = getLogger(__name__)


def access_granted(organization=None):
    retval = {"success": True}

    if organization:
        retval["result"] = organization

    return retval


def laissezpasser_check_user_resource_access(user, resource_dict, package_dict):
    pkg_organization_id = package_dict.get("owner_org", "")

    l = laissezpasser.get_laissezpasser(None, None)

    # if we have a pass
    if l.valid(package_dict.get("id")):
        return access_granted(pkg_organization_id)

    return None
