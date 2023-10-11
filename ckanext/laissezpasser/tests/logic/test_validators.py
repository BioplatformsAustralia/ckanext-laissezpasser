"""Tests for validators.py."""

import pytest

import ckan.plugins.toolkit as tk

from ckanext.laissezpasser.logic import validators


def test_laissezpasser_reauired_with_valid_value():
    assert validators.laissezpasser_required("value") == "value"


def test_laissezpasser_reauired_with_invalid_value():
    with pytest.raises(tk.Invalid):
        validators.laissezpasser_required(None)
