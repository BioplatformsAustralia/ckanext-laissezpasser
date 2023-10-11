import ckan.plugins.toolkit as tk
import ckanext.laissezpasser.logic.schema as schema


@tk.side_effect_free
def laissezpasser_get_sum(context, data_dict):
    tk.check_access(
        "laissezpasser_get_sum", context, data_dict)
    data, errors = tk.navl_validate(
        data_dict, schema.laissezpasser_get_sum(), context)

    if errors:
        raise tk.ValidationError(errors)

    return {
        "left": data["left"],
        "right": data["right"],
        "sum": data["left"] + data["right"]
    }


def get_actions():
    return {
        'laissezpasser_get_sum': laissezpasser_get_sum,
    }
