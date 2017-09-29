from .fields import PublicIdField, PublicIdFormField, generate_id

# for backwards compatibility
PublicIdDbField = PublicIdField
gen_code = generate_id

VERSION = (2, 2, 0)
__version__ = '.'.join(map(str, VERSION))
