import ckan.plugins.toolkit as tk
from six import text_type

def laissezpasser_create():
    #  user_id (string)
    #  package_id (string)
    #  valid_until (iso date string) - (optional)
    not_empty = tk.get_validator("not_empty")
    ignore_missing = tk.get_validator("ignore_missing")
    user_id_or_name_exists = tk.get_validator("user_id_or_name_exists")
    package_id_or_name_exists = tk.get_validator("package_id_or_name_exists")
    convert_user_name_or_id_to_id = tk.get_validator("convert_user_name_or_id_to_id")
    convert_package_name_or_id_to_id = tk.get_validator("convert_package_name_or_id_to_id")
    isodate = tk.get_validator("isodate")

    return {
        "user_id": [not_empty, text_type, user_id_or_name_exists, convert_user_name_or_id_to_id],
        "package_id": [not_empty, text_type, package_id_or_name_exists, convert_package_name_or_id_to_id],
        "valid_until": [ignore_missing, isodate],
    }


def laissezpasser_remove():
    #  user_id (string)
    #  package_id (string)
    #  valid_until (iso date string) - (optional)
    not_empty = tk.get_validator("not_empty")
    ignore_missing = tk.get_validator("ignore_missing")
    user_id_or_name_exists = tk.get_validator("user_id_or_name_exists")
    package_id_or_name_exists = tk.get_validator("package_id_or_name_exists")
    convert_user_name_or_id_to_id = tk.get_validator("convert_user_name_or_id_to_id")
    convert_package_name_or_id_to_id = tk.get_validator("convert_package_name_or_id_to_id")

    return {
        "user_id": [not_empty, text_type, user_id_or_name_exists, convert_user_name_or_id_to_id],
        "package_id": [not_empty, text_type, package_id_or_name_exists, convert_package_name_or_id_to_id],
    }
