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


Source Code
-----------

https://github.com/xando/os.path2


API
---


.. autoattribute:: path2.path.user
.. autoattribute:: path2.path.group
.. autoattribute:: path2.path.mod
.. autoattribute:: path2.path.absolute
.. autoattribute:: path2.path.basename
.. autoattribute:: path2.path.dir
.. autoattribute:: path2.path.a_time
.. autoattribute:: path2.path.m_time
.. autoattribute:: path2.path.size
.. autoattribute:: path2.path.exists

.. automethod:: path2.path.is_dir
.. automethod:: path2.path.is_file
.. automethod:: path2.path.mkdir
.. automethod:: path2.path.rm
.. automethod:: path2.path.cp
.. automethod:: path2.path.ln
.. automethod:: path2.path.unlink
.. automethod:: path2.path.touch
.. automethod:: path2.path.ls
.. automethod:: path2.path.ls_files
.. automethod:: path2.path.ls_dirs
.. automethod:: path2.path.walk
.. automethod:: path2.path.chmod
.. automethod:: path2.path.open


string/unicode methods
``````````````````````

Path is also a instance of basestring so all methods implemented for `string/unicode
<http://docs.python.org/2/library/stdtypes.html#string-methods>`_ should work as well.

.. code-block:: python

   >>> path('.').absolute().split('/')
   ['', 'home', 'user', 'Projects', 'os.path2']

   >>> path('/home/user/test_tmp_directory').replace('_', '-')
   '/home/user/test-tmp-directory'

   >>> location = path('/home/user/test_tmp_directory')
   >>> location.mv(location.replace('_', '-'))


-----
