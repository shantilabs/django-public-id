django-public-id |Build Status| |Coverage Status|
=================================================

Long non-incremental IDs for public links.

Install
-------

::

    pip install django-public-id


Requirements
------------

* Python 2.7, 3.5+
* Django 1.9+


Settings
--------

put in `settings.py` (optional):

::

    # use readable uuid by default
    # example '831ff937-cb26-4876-ab94-d6cf44ad4ec1'
    PUBLIC_ID_CHARS = None

    # uuid with given chars (length will be enough to store 128 bits)
    # example: '14URANtr8RaUTzZS05HIEp'
    PUBLIC_ID_CHARS = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


Usage
-----

.. code :: python

    from django.db import models
    from public_id.fields import PublicIdField

    class Post(models.Model):
        public_id = PublicIdField(auto=True)
        title = models.CharField(max_length=255)
        body = models.TextField(blank=True)


.. |Build Status| image:: https://travis-ci.org/shantilabs/django-public-id.svg?branch=master
   :target: https://travis-ci.org/shantilabs/django-public-id
.. |Coverage Status| image:: https://coveralls.io/repos/github/shantilabs/django-public-id/badge.svg?branch=master
   :target: https://coveralls.io/github/shantilabs/django-public-id?branch=master
