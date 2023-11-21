from typing import Any, Iterable, Optional, OrderedDict
import datetime

import ckan.plugins.toolkit as tk
from ckan.common import g

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
        self.clear()

    def clear(self):
        self.content = {}

    def count(self):
        return len(self.content)

    def add(self, item: str, passdatetime = None):
        # return True on success of adding pass
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
           now = datetime.datetime.utcnow()
           passvaliduntil = now + stale_after

        self.content[item] = passvaliduntil.strftime('%Y-%m-%dT%H:%M:%S.%f')
        return True

    def check(self, item: str):
        # Returns date of pass if present otherwise None
        return self.content.get(item, None)

    def valid(self, item: str):
        # Returns True if contains a valid pass
        # Returns False otherwise
        if not self.check(item): return False
        try:
            timeofpass = datetime.datetime.strptime(self.check(item), '%Y-%m-%dT%H:%M:%S.%f')
        except ValueError:
            return False
        
        assume_stale_after = datetime.timedelta(days=self.duration)
        passdelta = datetime.datetime.utcnow() - timeofpass

        return passdelta < assume_stale_after

    def remove(self, item: str):
        # Returns True if removed
        # Returns False otherwise
        if not self.check(item): return False
        del self.content[item]

        return True

    def restore(self):
        user = self._get_user()
        plugin_extras = self._get_plugin_extras(user)
        self.content = self._get_passes(plugin_extras)

    def save(self):
        user = self._get_user()
        plugin_extras = self._get_plugin_extras(user)
        plugin_extras[self.key] = self.content
        user['plugin_extras'] = plugin_extras
        tk.get_action('user_update')(self.admin_ctx, user)

    def _get_user(self):
        # Default to own user
        user_id = g.userobj.id

        # if data_dict is not None, use user_id from there
        # otherwise use the global context
        if self.data_dict:
            if self.data_dict.get("user_id"):
                user_id = self.data_dict.get("user_id")

        user_dict = { "id": user_id, "include_plugin_extras": True }
        user = tk.get_action('user_show')(self.admin_ctx, user_dict)
        return user

    def _get_plugin_extras(self, user):
        if 'plugin_extras' in user and user.get('plugin_extras') is not None:
            return user.get('plugin_extras')
        else:
            return {}
    
    def _get_passes(self, plugin_extras):
        if plugin_extras is not None and self.key in plugin_extras: 
            return plugin_extras[self.key]
        else:
            return {}      

    def drop(self):
        self.clear()
        self.save(key)
