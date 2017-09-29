import string
import random


def generate_sequence(alphabet, length):
    rng = random.SystemRandom()
    alphabet_length = len(alphabet)

    indexes = [rng.randrange(alphabet_length) for _ in range(length)]

    return ''.join(alphabet[i] for i in indexes)


def base_n(num, base, chars):
    """
    >>> base_n(42, 10, '0123456789')
    '42'
    >>> base_n(42, 2, '01')
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
