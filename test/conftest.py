import pytest

@pytest.hookimpl
def pytest_runtest_setup(item):
    print(f"\n[钩子触发]开始执行测试：{item.name}")