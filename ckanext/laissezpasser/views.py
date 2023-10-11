from flask import Blueprint


laissezpasser = Blueprint(
    "laissezpasser", __name__)


def page():
    return "Hello, laissezpasser!"


laissezpasser.add_url_rule(
    "/laissezpasser/page", view_func=page)


def get_blueprints():
    return [laissezpasser]
