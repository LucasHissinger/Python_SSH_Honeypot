from src import sys_func


def test_check_binary_exists():
    assert sys_func.check_binary("python") == True


def test_check_binary_does_not_exist():
    assert sys_func.check_binary("nonexistent") == False

def test_check_binary_is_not_a_file():
    assert sys_func.check_binary("bin") == False
