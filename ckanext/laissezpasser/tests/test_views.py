"""Tests for views.py."""

import pytest

import ckanext.laissezpasser.validators as validators


import ckan.plugins.toolkit as tk


@pytest.mark.ckan_config("ckan.plugins", "laissezpasser")
@pytest.mark.usefixtures("with_plugins")
def test_laissezpasser_blueprint(app, reset_db):
    resp = app.get(tk.h.url_for("laissezpasser.page"))
    assert resp.status_code == 200
    assert resp.body == "Hello, laissezpasser!"
