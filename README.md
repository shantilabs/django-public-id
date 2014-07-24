django-public-id
==================

Long non-incremental IDs for public links.

Install:
```
pip install git+https://github.com/shantilabs/django-public-id#egg=public_id
```

settings.py (optional)
```

# all sybmols allowed in URLs
PUBLIC_ID_ALPHABET = (
    '0123456789'
    'abcdefghijklmnopqrstuvwxyz'
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    '_-.~'
)

# backward compatibility
PUBLIC_ID_MAX_LENGTH = 36  

```

Usage:
```python
from public_id import PublicIdDbField, PublicIdFormField
```

