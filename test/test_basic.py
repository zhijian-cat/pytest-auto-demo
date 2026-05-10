import pytest

# ========== 用例1：基础断言 ==========
def test_addition():
    """测试加法运算"""
    assert 1 + 1 == 2
    assert 3 * 4 == 12

# ========== 用例2：字符串断言 ==========
def test_string_operations():
    """测试字符串操作"""
    name = "pytest"
    assert "test" in name           # 成员检查
    assert len(name) == 6           # 长度检查
    assert name.upper() == "PYTEST" # 方法调用

# ========== 用例3：异常断言 ==========
def test_division_by_zero():
    """测试是否抛出指定异常"""
    with pytest.raises(ZeroDivisionError):
        result = 1 / 0

# ========== 用例4：使用fixture（function作用域）==========
@pytest.fixture
def sample_data():
    """function级别fixture，每个测试用例独立调用"""
    print("\n[fixture] 准备测试数据...")
    data = {"name": "pytest", "version": 8.0}
    return data

def test_fixture_demo(sample_data):
    """测试fixture传入的数据"""
    assert sample_data["name"] == "pytest"
    assert sample_data["version"] == 8.0

# ========== 用例5：使用autouse的fixture ==========
@pytest.fixture(autouse=True)
def auto_timer():
    """自动执行的fixture，记录测试耗时"""
    import time
    start = time.time()
    print(f"\n[自动fixture] 测试开始...")
    yield
    elapsed = time.time() - start
    print(f"[自动fixture] 测试结束，耗时: {elapsed:.4f}秒")

def test_auto_fixture_demo():
    """验证autouse fixture会自动执行"""
    assert 2 * 2 == 4