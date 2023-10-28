import imagehash
import io
import string
import random

from PIL import Image

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


def compute_image_hash(bytes: bytearray, num_bits: int = 64) -> int:
    """
    TODO
    """
    # Load the image.
    img = Image.open(io.BytesIO(bytes))

    # Compute the hash in form of a hex string.
    hash_hex = str(imagehash.dhash(img))

    # Convert the hex string to an integer.
    hash = int(hash_hex, 16)

    # Convert from unsigned number to signed number with <num_bits>-many bits
    if hash & (1 << (num_bits - 1)):
        hash -= 1 << num_bits

    return hash

# ==================================================================================================


def unique_id(size: int = 7) -> str:
    chars = list(set(string.ascii_uppercase + string.digits).difference('LIO01'))
    return ''.join(random.choices(chars, k=size))