import os
import sys
import stat
import codecs
import shutil
import fnmatch
import datetime


__version__ = "0.0.4"


if sys.version.startswith('3'):
    base_string_class = str
    python3 = True
else:
    base_string_class = unicode
    python3 = False


class pathmeta(type):

    @classmethod
    def str_to_path(cls, func):

        def decorator(*args, **kwargs):
            value = func(*args, **kwargs)

            if isinstance(value, base_string_class):
                return path(value)

            return value
        return decorator

    def __new__(cls, name, bases, local):
        _unicode = bases[0]

        for method_name in _unicode.__dict__:
            value = getattr(_unicode, method_name)
            if all([callable(value),
                    method_name not in ('__new__', '__str__', '__getattribute__'),
                    method_name not in local]):
                local[method_name] = cls.str_to_path(value)

        return type.__new__(cls, name, bases, local)


class path(pathmeta('base_path', (base_string_class, ), {})):
    """

    .. code-block:: bash

       $ ls -la /var/log
       total 20
       drwxrwxr-x 3 root root  4096 Dec 20 22:37 .
       drwxrwxr-x 5 root root  4096 Dec 20 22:38 ..
       drwxrwxr-x 2 root root  4096 Dec 20 22:37 gdm
       -rw-rw-r-- 1 root root 11561 Dec 20 22:37 boot.log
       -rw-rw-r-- 1 root root 11562 Dec 20 22:37 dmesg
       -rw-rw-r-- 1 root root 11563 Dec 20 22:37 faillog
       -rw-rw-r-- 1 root root 11564 Dec 20 22:37 kern.log


    .. code-block:: python

        >>> from osome import path

        >>> path('/var/log')
        /var/log

        >>> path('/var', 'log')
        /var/log

        >>> path('/var', 'log', 'syslog')
        /var/log/syslog

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

    Path is also a instance of basestring so all methods implemented for `string/unicode
    <http://docs.python.org/2/library/stdtypes.html#string-methods>`_ should work as well.

    .. code-block:: python

       >>> path('.').absolute.split('/')
       ['', 'home', 'user', 'Projects', 'osome']

       >>> path('/home/user/test_tmp_directory').replace('_', '-')
       '/home/user/test-tmp-directory'

       >>> location = path('/home/user/test_tmp_directory')
       >>> location.mv(location.replace('_', '-'))


    """

    def __call__(self, *args):
        if args:
            return self / path(*args)
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __new__(cls, *args):
        if len(args) > 1:
            return super(path, cls).__new__(path, cls.join(*args))
        return super(path, cls).__new__(path, *args)

    @property
    def user(self):
        """
        Path attribute, returns name of the user owner of the path.

        >>> path('/home/user').user
        user

        """
        import pwd  # doesn't work on windows
        return pwd.getpwuid(os.stat(self).st_uid).pw_name

    @property
    def group(self):
        """
        Path attribute, returns name of the group owner of the path.

        >>> path('/etc/').group
        root
        """
        import pwd  # doesn't work on windows
        return pwd.getpwuid(os.stat(self).st_gid).pw_name

    @property
    def mod(self):
        """
        To get Unix path permissions.

        >>> path('.').mod
        '0775'
        """

        return oct(stat.S_IMODE(os.stat(self).st_mode))

    @property
    def absolute(self):
        """
        Returns a normalised absolutized version of the pathname path.

        .. code-block:: python

           >>> path('.').absolute
           /home/user/Projects/osome

        :rtype: path
        """
        return path(os.path.abspath(self))

    def relative(self, target):
        return path(os.path.relpath(self, target))

    @property
    def basename(self):
        """
        Returns the path basename.

        .. code-block:: python

           >>> path('/home/user/Projects/osome').basename
           osome

        :rtype: path
        """
        return path(os.path.basename(self))

    @property
    def dir(self):
        """
        Returns the directory path of pathname path.

        .. code-block:: python

           >>> path('/var/log/syslog').dir
           /var/log

        :rtype: path
        """
        return path(os.path.dirname(self))

    @property
    def a_time(self):
        """
        Return the time of last access of path.
        The return value is a number giving the number
        of seconds since the epoch.

        .. code-block:: python

           >>> path('/var/log/syslog').a_time
           1358549788.7512302

        :rtype: float
        """
        return os.path.getatime(self)

    @property
    def a_datetime(self):
        """
        Return the time of last access of path.
        The return value is a datetime object.

        .. code-block:: python

           >>> path('/var/log/syslog').a_datetime
           datetime.datetime(2013, 3, 12, 20, 44, 26, 655954)

        """
        return datetime.datetime.fromtimestamp(self.a_time)

    @property
    def m_time(self):
        """
        Return the time of last modification of path.
        The return value is a number giving the number
        of seconds since the epoch.

        .. code-block:: python

           >>> path('/var/log/syslog').m_time
           1358549788.7512302

        :rtype: float

        """
        return os.path.getmtime(self)

    @property
    def m_datetime(self):
        """
        Return the time of last modification of path.
        The return value is a datetime object.

        .. code-block:: python

           >>> path('/var/log/syslog').m_datetime
           datetime.datetime(2013, 3, 12, 20, 44, 26, 655954)

        """
        return datetime.datetime.fromtimestamp(self.m_time)


    @property
    def size(self):
        """
        Return the size of path in bytes

        .. code-block:: python

           >>> path('.').size
           4096

        :rtype: int
        """
        return os.path.getsize(self)

    @property
    def exists(self):
        """
        Returns True if path refers to an existing path.
        Returns False for broken symbolic links.

        .. code-block:: python

           >>> path('/var/log').exists
           True

        :rtype: bool
        """
        return os.path.exists(self)

    def is_dir(self):
        """
        Return True if path is an existing directory.
        This follows symbolic links, so both is_link() and
        is_dir() can be true for the same path.

        .. code-block:: python

           >>> path('/var/log').is_dir()
           True

        :rtype: bool
        """
        return os.path.isdir(self)

    def is_file(self):
        """
        Return True if path is an existing regular file.
        This follows symbolic links, so both is_link() and
        is_file() can be true for the same path.

        .. code-block:: python

           >>> path('/var/log/syslog').is_file()
           True

        :rtype: bool
        """
        return os.path.isfile(self)

    def is_link(self):
        """
        :rtype: bool
        """
        return os.path.islink(self)

    def mkdir(self, p=False):
        """
        :param p: if changed will behave like mkdir -p, creating all directories recursively.

        >>> path('dir').mkdir().exists
        True

        >>> path('/home/user/another/dir',p=True).mkdir().exists
        True

        :rtype: path

        """
        if p:
            os.makedirs(self)
        else:
            os.mkdir(self)
        return self

    def rm(self, r=False):
        """
        Removing file or directory, **r** parameter needs to be
        applied to remove directory recursively.


        >>> path('file').rm()
        file

        >>> path('/tmp').rm(r=True)
        /tmp

        :rtype: path

        """
        if os.path.isfile(self):
            os.remove(self)
        else:
            if r:
                shutil.rmtree(self)
            else:
                os.rmdir(self)
        return self

    def cp(self, target):
        """

        Copy the file or the contents the directory to **target** destination,
        workrs for files and directories as well.

        >>> path('dir').cp('dir_copy')
        dir_copy

        >>> path('file1').cp('file_copy')
        file_copy
        >>> path('file1').cp('file_copy').exists
        True

        :rtype: path
        """
        if self.is_dir():
            shutil.copytree(self, target)
        else:
            shutil.copy(self, target)
        return path(target)

    def ln(self, target, s=True):
        """
        Create a link pointing to source named link_name,
        default call will create symbolic link, change **s=False**
        to create hard link.

        >>> path('/tmp/').ln('/home/user/tmp')
        '/home/user/tmp'

        :rtype: path
        """
        if s:
            os.symlink(os.path.realpath(self), target)
        else:
            os.link(os.path.realpath(self), target)
        return path(target)

    def unlink(self):
        """
        Unlink path from the poiting location.

        >>> path('/home/user/tmp').is_link()
        True
        >>> path('/home/user/tmp').unlink()
        '/home/user/tmp'

        :rtype: path
        """
        os.unlink(self)
        return self

    def touch(self):
        """
        Imitates call of Unix's **touch**.

        >>> path('file').touch()
        file

        :rtype: path
        """
        open(self, "a")
        return self

    def ls(self, pattern="*", sort=None):
        """

        Display content of the directory, use **pattern** as filtering parameter,
        change order by defining **sort** function.

        >>> path('/var/log').ls()
        [/var/log/boot.log, /var/log/dmesg, /var/log/faillog, /var/log/kern.log, /var/log/gdm]

        >>> path('/var/log/').ls('*log')
        [/var/log/boot.log, /var/log/faillog, /var/log/kern.log]

        path('.').ls(sort=lambda x: not x.startswith('_'))
        [_themes, _build, _static, _templates, Makefile, conf.py, index.rst]

        :rtype: list
        """
        sort = sort or (lambda e: (not e.is_dir(), e))
        content = [
            self / path(e) for e in os.listdir(self) if fnmatch.fnmatch(e, pattern)
        ]
        return sorted(content, key=sort)

    def ls_files(self, patern="*", sort=None):
        """
        Returns files inside given path.

        >>> path('.').ls_files()
        [/var/log/boot.log, /var/log/dmesg, /var/log/faillog, /var/log/kern.log]

        :rtype: list
        """
        return [e for e in self.ls(patern, sort) if e.is_file()]

    def ls_dirs(self, patern="*", sort=None):
        """
        Returns directories inside given path.

        >>> path('.').ls_dirs()
        [/var/log/gdm]]

        :rtype: list
        """
        return [e for e in self.ls(patern, sort) if e.is_dir()]

    def walk(self, pattern="*", r=False, sort=None):
        """

        Location walk generator

        .. code-block:: python

            >>> for element in path('.').walk():
                    print element
            /var/log/boot.log
            /var/log/dmesg
            /var/log/faillog
            /var/log/kern.log
            /var/log/gdm

        :rtype: generator
        """
        sort = sort or (lambda e: (e.is_dir(), e))
        content = self.ls(pattern=pattern, sort=sort)
        for element in content:

            if fnmatch.fnmatch(element, pattern):
                yield element
            if element.is_dir() and r:
                for item in element.walk(pattern="*", sort=sort):
                    yield item

    def chmod(self, mode):
        """
        To change path access permissions

        >>> path('test').chmod('0775')
        >>> path('test').mod
        '0775'
        """
        # ToDo: this is probably not the 'best' implementation

        if isinstance(mode, basestring):
            mode = sum([(8**i * int(e)) for i,e in \
                        enumerate(reversed(mode.lstrip("0")))])
            os.chmod(self, mode)
        else:
            os.chmod(self, mode)
        return self

    def split(self, separator=os.sep):
        return [path(p) for p in super(path, self).split(separator) if p]

    def open(self, mode=None, *args, **kwargs):
        """
        Open a file, returning an object of the File Objects.

        .. code-block:: python

            >>> path('/var/log','syslog').open('r')
            <open file '/var/log/syslog', mode 'r' at 0x294c5d0>

        """
        return open(self, mode, *args, **kwargs)

    @property
    def content(self):
        return codecs.open(self, encoding='utf-8').read()

    def __iter__(self):
        """
        >>> for e in path('/var/log'):
        ...     print e
        /var/log/boot.log
        /var/log/dmesg
        /var/log/faillog
        /var/log/kern.log
        /var/log/gdm
        """
        return self.walk()

    def __div__(self, other):
        """
        >>> path('/var/log') / path('syslog')
        /var/log/syslog
        >>> path('/var/log') / 'syslog'
        /var/log/syslog
        >>> (path('/var/log') / 'syslog').exists
        """

        return path(os.path.join(self, other))

    __truediv__ = __div__

    @classmethod
    def join(cls, *path_list):
        return path(os.path.join(*path_list))


path2 = path
