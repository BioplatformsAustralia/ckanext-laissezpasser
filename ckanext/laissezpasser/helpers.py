# coding: utf8

import ckan.model as model
from ckan.lib.dictization import model_dictize
from ckan.common import g
from ckanext.laissezpasser import laissezpasser

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


def laissezpasser_package_passes(user = None):
    l = get_lp(user)

    package_list = l.passes()

    context = {"model": model, "session": model.Session}

    return [model_dictize.package_dictize(model.Session.query(model.Package).get(pkg_name), context) for pkg_name in package_list]

def get_helpers():
    return {
        "has_passes": laissezpasser_has_passes,
        "has_package_pass": laissezpasser_has_package_pass,
        "check_pass": laissezpasser_check_pass,
        "pass_duration": laissezpasser_default_duration,
        "package_passes": laissezpasser_package_passes,
    }
