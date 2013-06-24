============================
from os import path2 as path
============================

The **os.path** library replacement with simple API.


.. code-block:: python

    >>> from os import path2 as path

    >>> path('/var/log')
    /var/log

    >>> path('/var', 'log')
    /var/log

    >>> path('/home/you/file').user
    'you'

    >>> [(element.user, element.group, element.mod) for element in path('.')]
    [('user', 'user', '0664'),
     ('user', 'user', '0664'),
     ('user', 'user', '0664'),
     ('user', 'user', '0664'),
     ('user', 'user', '0664'),
     ('user', 'user', '0664'),
     ('user', 'user', '0664'),
     ('user', 'user', '0775'),
     ('user', 'user', '0664')]


Status
------

Library seems to be pretty stable. Feel free to use it as you want.
But I think this no the final version of API.


Install
-------

You can install it from PyPi, by simply **pip**:

.. code-block:: bash

   $ pip install os.path2

only if you don't have pip installed, an alternative method is **easy_install**:

.. code-block:: bash

   $ easy_install os.path2

to test it, launch **python**

.. code-block:: python

   >>> from os import path2 as path


Supported platforms
-------------------

* Python2.6
* Python2.7
* Python3.3
* PyPy1.9


Tests
-----

.. image:: https://api.travis-ci.org/xando/os.path2.png?branch=master
   :target: https://travis-ci.org/xando/os.path2


.. code-block:: bash

   >>> python setup.py test

