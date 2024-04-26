# coding: utf8

import ckan.model as model
from ckan.lib.dictization import model_dictize
import ckan.lib.dictization as d
from ckan.common import g
from ckanext.laissezpasser import laissezpasser
from ckanext.laissezpasser.models.laissezpasser_passes_table import LaissezpasserPassesTable

from logging import getLogger

log = getLogger(__name__)


def get_lp(user = None):
    if not getattr(g, u'user', None):
        g.user = ''
    context = {'user': user or g.user}

    return laissezpasser.get_laissezpasser(context,None)

def laissezpasser_has_passes(user = None):
    l = get_lp(user)

    return True if l.count() else False


def laissezpasser_has_package_pass(package=None):
    l = get_lp()

    return l.valid(package.get("id",None))


def laissezpasser_check_pass(package=None):
    l = get_lp()

    return l.check(package.get("id",None))


def laissezpasser_default_duration():
    l = get_lp()

    return l.duration


def laissezpasser_package_passes(user = None, filter_valid=False):
    l = get_lp(user)

    package_list = l.passes(valid = filter_valid)

    context = {"model": model, "session": model.Session}

    passes_as_dicts =  [model_dictize.package_dictize(model.Session.query(model.Package).get(pkg_name), context) for pkg_name in package_list]

    return passes_as_dicts


def laissezpasser_held_passes(user = None, filter_valid=False):
    l = get_lp(user)

    metadata_list = l.held(user, filter_valid = filter_valid)

    context = {"model": model, "session": model.Session}

    held_as_dicts = [d.table_dictize(LaissezpasserPassesTable.get_by_package_and_user(metadata.dataset, metadata.user_name)[0], context) for metadata in metadata_list]

    # run through list, add valid flag
    held_as_dicts = [dict(held,**{'valid': l.valid(held.get('dataset'),held.get('user_name'))}) for held in held_as_dicts]

    return held_as_dicts

def laissezpasser_issued_passes(package = None, filter_valid=False):
    l = get_lp()

    metadata_list = l.issued(package, filter_valid = filter_valid)

    context = {"model": model, "session": model.Session}

    issued_as_dicts = [d.table_dictize(LaissezpasserPassesTable.get_by_package_and_user(metadata.dataset, metadata.user_name)[0], context) for metadata in metadata_list]

    # run through list, add valid flag
    issued_as_dicts = [dict(issued,**{'valid': l.valid(issued.get('dataset'),issued.get('user_name'))}) for issued in issued_as_dicts]

    return issued_as_dicts


def get_helpers():
    return {
        "has_passes": laissezpasser_has_passes,
        "has_package_pass": laissezpasser_has_package_pass,
        "check_pass": laissezpasser_check_pass,
        "pass_duration": laissezpasser_default_duration,
        "package_passes": laissezpasser_package_passes,
        "held_passes": laissezpasser_held_passes,
        "issued_passes": laissezpasser_issued_passes,
    }
