import os
import shutil

import pytest

from path2 import path

root = 'xxx'

dir_1 = 'dir_1'
dir_2 = 'dir_2'
dir_1_path = os.path.join(root, dir_1)
dir_2_path = os.path.join(root, dir_2)
dir_list = [dir_1, dir_2]

file_1 = 'file_1'
file_2 = 'file_2'
file_1_path = os.path.join(root, file_1)
file_2_path = os.path.join(root, file_2)
file_list = [file_1, file_2]

file_3 = 'file_3'
file_4 = 'file_4'
file_3_path = os.path.join(root, dir_1, file_3)
file_4_path = os.path.join(root, dir_2, file_4)


def setup_function(function):
    os.mkdir(root)

    for dir in dir_list:
        os.mkdir(os.path.join(root, dir))

    for file in file_list:
        open(os.path.join(root, file), "w").write("")


def teardown_function(function):
    shutil.rmtree(root)


def test_path():
    assert path(root, file_1).exists
    assert not path(root, file_1, 'xxxss').exists


def test_exists():
    assert path(dir_1_path).exists
    assert path(file_1_path).exists


def test_absolute():
    assert os.path.abspath(file_1_path) == path(file_1_path).absolute


def test_is_dir():
    assert path(dir_1_path).is_dir()
    assert path(dir_2_path).is_dir()

    assert not path(file_1_path).is_dir()
    assert not path(file_2_path).is_dir()


def test_is_file():
    assert path(file_1_path).is_file()
    assert path(file_2_path).is_file()

    assert not path(dir_1_path).is_file()
    assert not path(dir_2_path).is_file()


def test_ln_s():
    symlink = path(file_1_path).ln(os.path.join('xxx', 'symlink'))

    assert symlink.exists
    assert symlink.is_link()


def test_ln_hard():
    symlink = path(file_1_path).ln(os.path.join('xxx', 'symlink'), s=False)

    assert symlink.exists
    assert not symlink.is_link()


def test_unlink():
    target = os.path.join('xxx', 'symlink')

    os.symlink(
        os.path.realpath(file_1_path),
        target
    )

    assert path(target).exists
    path(target).unlink()
    assert not path(target).exists


def test_mkdir():
    path_string = os.path.join(root, "test")
    path(path_string).mkdir()

    assert os.path.exists(path_string)
    assert os.path.isdir(path_string)


def test_mkdir_p():
    path_string = os.path.join(root, "level1", "level2")
    path(path_string).mkdir(p=True)

    assert os.path.exists(path_string)
    assert os.path.isdir(path_string)


def test_rm():
    path(file_1_path).rm()
    assert not os.path.exists(file_1_path)

    path(dir_1_path).rm()
    assert not os.path.exists(dir_1_path)

    file_location = os.path.join(dir_2_path, 'xxx')
    open(file_location, "w")

    with pytest.raises(OSError):
        path(dir_2_path).rm()
    assert os.path.exists(dir_2_path)

    path(dir_2_path).rm(r=True)
    assert not os.path.exists(dir_2_path)


def test_cp():
    file_copy = path(file_1_path).cp(os.path.join(root, 'file_copy'))
    assert os.path.exists(file_copy)

    dir_copy = path(dir_1_path).cp(os.path.join(root, 'dir_copy'))
    assert os.path.exists(dir_copy)


def test_touch():
    path_string = os.path.join(root, "test")
    path(path_string).touch()

    assert os.path.exists(path_string)
    assert os.path.isfile(path_string)


def test_ls():
    dir_content = path(root).ls()

    names_only = [a.basename for a in dir_content]

    assert len(dir_content) == len(dir_list + file_list)
    assert set(dir_list).issubset(names_only)
    assert set(file_list).issubset(names_only)


def test_ls_files():
    dir_content = path(root).ls_files()

    names_only = [a.basename for a in dir_content]

    assert len(dir_content) == len(file_list)
    assert not set(dir_list).issubset(names_only)
    assert set(file_list).issubset(names_only)


def test_ls_dirs():
    dir_content = path(root).ls_dirs()

    names_only = [a.basename for a in dir_content]

    assert len(dir_content) == len(dir_list)
    assert set(dir_list).issubset(names_only)
    assert not set(file_list).issubset(names_only)


def test_walk():
    dir_content = path(root).walk()
    assert len([e for e in dir_content]) == len(dir_list + file_list)


def test_iter():
    dir_content = path(root)
    assert len([e for e in dir_content]) == len(dir_list + file_list)


def test__div__():
    joined_path = path(root) / path(file_1)
    assert joined_path.exists

    joined_path = path(root) / file_1
    assert joined_path.exists

    joined_path = path(root) / path(file_1) / path("xxx")
    assert not joined_path.exists

    joined_path = path(root) / path(file_1) / "xxx"
    assert not joined_path.exists


def test_join():
    assert path.join(root, file_1).exists
    assert not path.join(root, file_1, 'xxx').exists


def test_split():
    path_1 = path('/tmp/directory/file')
    assert all([isinstance(p, path) for p in path_1.split()])


def test_base_methods():

    path_1 = path("/tmp/file with spaces").replace(" ", "-")
    assert isinstance(path_1, path)
    assert path_1 == '/tmp/file-with-spaces'

    path_2 = path("smallfile").upper()
    assert isinstance(path_2, path)
    assert path_2 == 'SMALLFILE'

    path_3 = path("/tmp/file.txt")[:5]
    assert isinstance(path_3, path)
    assert path_3 == '/tmp/'
