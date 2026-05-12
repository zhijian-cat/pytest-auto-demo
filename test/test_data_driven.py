import pytest
from utils.data_loader import DataLoader

#加载测试数据（数据与代码分离！）
test_cases = DataLoader.get_test_cases('data/login_data.yaml', 'login_cases')

def mock_login(username, password):
    """模拟登录函数"""
    if not username:
        return "用户名不能为空"
    if not password:
        return "密码不能为空"
    if username == "admin" and password == "123456":
        return "成功"
    return "失败"

#参数化 + 数据驱动
@pytest.mark.parametrize("case", test_cases)
def test_login(case):
    """测试登录——数据从YAML文件来"""
    print(f"\n执行用例：{case['name']}")
    print(f"\n请求的数据：username={case['username']}, password={case['password']}")
    print(f"期待的结果：{case['expected']}")

    result = mock_login(case['username'], case['password'])

    assert result == case['expected']
    print (f"测试实际结果：{result}")