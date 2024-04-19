from typing import Any, Iterable, Optional, OrderedDict
import datetime

import ckan.plugins.toolkit as tk
from ckan.common import g
from ckan.model import Package, User

from ckanext.laissezpasser.models.laissezpasser_passes_table import LaissezpasserPassesTable

CONFIG_PASS_DURATION = "ckanext.laissezpasser.duration"
CONFIG_PASS_DURATION_DEFAULT = "1"

def get_laissezpasser(context: dict[str, Any], data_dict):
    laissezpasser = LaissezPasser()

    laissezpasser.data_dict = data_dict
    laissezpasser.context = context
    return laissezpasser


class LaissezPasser():
    def __init__(self):
        self.key = 'laissezpasser'
        self.duration = int(tk.config.get(CONFIG_PASS_DURATION, CONFIG_PASS_DURATION_DEFAULT))
        self.site_user = tk.get_action("get_site_user")({'ignore_auth': True}, {})["name"]
        self.admin_ctx = {"ignore_auth": True, "user": self.site_user }
        self.context = None
        self.data_dict = None

    def count(self, user = None):
        # Returns the number of passes for a user
        if not user:
            user = self._get_user()

        result = LaissezpasserPassesTable.get_by_user(user)
        if not result:
            return 0
        return len(result)

    def add(self, item: str, passdatetime = None, user = None):
        # return True on success of adding pass

        # remove old pass
        if self.check(item):
            self.remove(item)

        now = datetime.datetime.utcnow()

        if passdatetime:
           if isinstance(passdatetime, datetime.datetime):
               passvaliduntil = passdatetime
           else:
               try:
                   passvaliduntil = datetime.datetime.strptime(passdatetime, '%Y-%m-%dT%H:%M:%S.%f')
               except (ValueError, TypeError):
                   return False
        else:
           stale_after = datetime.timedelta(days=self.duration)
           passvaliduntil = now + stale_after

        if not user:
            user = self._get_user()

        db_model = LaissezpasserPassesTable(
            dataset_name = item,
            user = User.by_name(user),
            created_at = now,
            created_by = g.userobj.name,
            valid_until = passvaliduntil,
        )

        db_model.save()
        return True

    def passes(self, valid = True, user = None):
        # Returns a list of packages that have passes
        # By default, only return the ones that are valid

        if not user:
            user = self._get_user()

        result = LaissezpasserPassesTable.get_by_user(user)
        if not result:
            return []

        packages = [p.dataset for p in result]
        if valid:
           return list(filter(self.valid, packages))

        return packages

    def issued(self, item: str, filter_valid = True):
        # Returns the metadata for passes associated with a package
        # By default, only return the ones that are valid

        result = LaissezpasserPassesTable.get_by_package(item)

        if not result:
            return []

        if filter_valid:
           log.warn("filtering list")
           return list(filter(lambda m: self.valid(m.dataset, user=m.user_name), result))

        # unfiltered
        return result


    def check(self, item: str, user = None):
        # Returns datetime of pass if present otherwise None
        if not user:
            user = self._get_user()

        result = LaissezpasserPassesTable.get_by_package_and_user(item, user)

        if not result:
            return None

        return result[0].valid_until

    def valid(self, item: str, user = None):
        # Returns True if contains a valid pass
        # Returns False otherwise
        if not self.check(item, user=user): return False
        try:
            timeofpass = self.check(item, user=user)
        except ValueError:
            return False
        
        assume_stale_after = datetime.timedelta(days=self.duration)
        passdelta = datetime.datetime.utcnow() - timeofpass

        return passdelta < assume_stale_after

    def remove(self, item: str, user = None):
        # Returns True if removed
        # Returns False otherwise
        if not self.check(item,user=user): return False

        if not user:
            user = self._get_user()

        result = LaissezpasserPassesTable.get_by_package_and_user(item, user)
        for res in result:
            res.delete()
            res.commit()

        return True

    def _get_user(self):
        # Default to own user
        user_id = g.userobj.id

        # if data_dict is not None, use user_id from there
        # otherwise use the global context
        if self.data_dict:
            if self.data_dict.get("user_id"):
                user_id = self.data_dict.get("user_id")

        if self.context:
            if self.context.get("user"):
                user_id = self.context.get("user")

        user_dict = { "id": user_id, "include_plugin_extras": True }
        user = tk.get_action('user_show')(self.admin_ctx, user_dict)
        return user.get('name')
