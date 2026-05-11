import pytest

@pytest.fixture(scope = "function")
def init_info():
    info = {"admin": "123", "user": "345"}
    return info


def login_api(username, password, info):
    if not username:
        return 0
    if username in info:
        return 200
    else:
        return 0
        
    if password == info[username]:
        return 200

@pytest.mark.parametrize("username, password, expected", [
    ("admin", "123", 200), 
    ("user", "345", 200),  
    ("", "213", 0)
    ])
def test_fun_login(username, password, expected, init_info):
    result = login_api(username, password, init_info)
    assert result == expected

