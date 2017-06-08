import string
import uuid

DEFAULT_CHARS = string.digits + string.ascii_lowercase


def generate_id(chars=None):
    if chars:
        max_base = len(chars)
        return base_n(uuid.uuid4().int, max_base, chars)
    else:
        return str(uuid.uuid4())


def base_n(num, base, chars=DEFAULT_CHARS):
    """
    >>> base_n(42, 10)
    '42'
    >>> base_n(42, 2)
    '101010'
    """
    if num == 0:
        return '0'
    if num < 0:
        return '-' + base_n((-1) * num, base, chars)
    if not 2 <= base <= len(chars):
        raise ValueError('Base must be between 2-%d' % len(chars))
    left_digits = num // base
    if left_digits == 0:
        return chars[num % base]
    else:
        return base_n(left_digits, base, chars) + chars[num % base]
