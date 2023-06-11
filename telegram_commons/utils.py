import string
import random

# ==================================================================================================

def deep_get(dictionary, keys, default=None):
    """
    TODO
    """
    key_list = keys.split(".")
    value = dictionary
    for key in key_list:
        if isinstance(value, dict) and key in value:
            value = value[key]
        else:
            return default
    return value

# ==================================================================================================

def unique_id(size: int = 7) -> str:
    chars = list(set(string.ascii_uppercase + string.digits).difference('LIO01'))
    return ''.join(random.choices(chars, k=size))