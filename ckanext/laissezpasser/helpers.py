# coding: utf8

from ckan.common import g
from ckanext.laissezpasser import laissezpasser

from logging import getLogger

log = getLogger(__name__)


def get_lp():
    if not getattr(g, u'user', None):
        g.user = ''
    context = {'user': g.user}

    return laissezpasser.get_laissezpasser(context,None)

def laissezpasser_has_passes():
    l = get_lp()
    l.restore()

    return True if l.count() else False


def laissezpasser_has_package_pass(package=None):
    l = get_lp()
    l.restore()

    return l.valid(package.get("id",None))


def laissezpasser_check_pass(package=None):
    l = get_lp()
    l.restore()

    return l.check(package.get("id",None))


def laissezpasser_default_duration():
    l = get_lp()

    return l.duration

def get_helpers():
    return {
        "has_passes": laissezpasser_has_passes,
        "has_package_pass": laissezpasser_has_package_pass,
        "check_pass": laissezpasser_check_pass,
        "pass_duration": laissezpasser_default_duration,
    }
