django-public-id
==================

Long non-incremental IDs for public links.

Install:
```
pip install git+https://github.com/shantilabs/django-public-id#egg=public_id
```

settings.py (optional)
```
# use readable uuid by default
# example '831ff937-cb26-4876-ab94-d6cf44ad4ec1'
PUBLIC_ID_ALPHABET = None

# uuid with given alphabet
# example: '14URANtr8RaUTzZS05HIEp'
PUBLIC_ID_ALPHABET = (
    '0123456789'
    'abcdefghijklmnopqrstuvwxyz'
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    '_-.~'
)
```

Usage:
```python
from public_id import PublicIdDbField, PublicIdFormField
```

