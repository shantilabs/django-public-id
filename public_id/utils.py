import string
import uuid
import random

DEFAULT_CHARS = string.digits + string.ascii_lowercase


def generate_id(chars=None, length=36):
    if chars:
        rng = random.SystemRandom()
        alphabet_length = len(chars)

        indexes = [rng.randrange(alphabet_length) for _ in range(length)]

        return ''.join(chars[i] for i in indexes)
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
    if not 2 <= base <= len(chars):
        raise ValueError('Base must be between 2-%d' % len(chars))
    left_digits = num // base
    if left_digits == 0:
        return chars[num % base]
    else:
        return base_n(left_digits, base, chars) + chars[num % base]
