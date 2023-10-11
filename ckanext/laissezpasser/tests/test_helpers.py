"""Tests for helpers.py."""

import ckanext.laissezpasser.helpers as helpers


def test_laissezpasser_hello():
    assert helpers.laissezpasser_hello() == "Hello, laissezpasser!"
