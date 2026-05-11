import pytest 

class TestUser:

    @pytest.mark.smoke
    @pytest.mark.p0
    def test_login_success(self):
        print("\n执行冒烟测试:登录成功")
        assert True

    @pytest.mark.smoke
    def test_login_fail(self):
        print("\n执行冒烟测试:登录失败")
        assert True

    @pytest.mark.regression
    def test_register_success(self):
        print("执行回归测试：注册成功")
        assert True

    @pytest.mark.regression
    def test_register_fail(self):
        print("执行回归测试：注册识别")
        assert True

    @pytest.mark.regression
    def test_forgot_password(self):
        print("执行回归测试：忘记密码")
        assert True

    @pytest.mark.slow
    def test_large_data(self):
        print("执行慢速测试: 大数据处理")
        assert True