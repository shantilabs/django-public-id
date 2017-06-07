def base_n(num, base, numerals='0123456789abcdefghijklmnopqrstuvwxyz'):
    """
    >>> base_n(42, 10)
    '42'
    >>> base_n(42, 2)
    '101010'
    """
    if num == 0:
        return '0'
    if num < 0:
        return '-' + base_n((-1) * num, base, numerals)
    if not 2 <= base <= len(numerals):
        raise ValueError('Base must be between 2-%d' % len(numerals))
    left_digits = num // base
    if left_digits == 0:
        return numerals[num % base]
    else:
        return base_n(left_digits, base, numerals) + numerals[num % base]
