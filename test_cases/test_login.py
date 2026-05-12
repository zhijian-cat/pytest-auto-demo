import pytest
from apis.login_api import login_api
from utils.data_loader import DataLoader

#加载10组测试数据（数据与代码分离）
test_cases = DataLoader.get_test_cases('data/login_data.yaml', 'login_cases_10')

class TestLogin:
    """登录测试类"""

    #综合测试
    @pytest.mark.parametrize("case", test_cases)
    def test_all_cases(self, case):
        """测试所有10组用例"""
        print(f"\n{'='*50}")
        print(f"用例: {case['name']}")
        print(f"请求: username={case['username']}, password={case['password']}")
        print(f"期望: code={case['expected_code']}, msg={case['expected_msg']}")

        #执行测试
        result = login_api(case['username'], case['password'])
        
        print(f"实际：code={result.get('code')}, msg={result.get('message')}")

        #断言
        assert result.get('code') == case['expected_code']
        assert result.get('message') == case['expected_msg']

    # 按照优先级筛选测试
    @pytest.mark.parametrize("case", [c for c in test_cases if c['priority'] == 'p0'])
    @pytest.mark.p0
    @pytest.mark.smoke
    def test_p0_cases(self, case):
         """测试P0优先级用例"""
         print(f"\n[P0高优先级] {case['name']}")
         result = login_api(case['username'], case['password'])
         assert result.get('code') == case['expected_code']

    #只测试正常场景
    @pytest.mark.parametrize("case", [c for c in test_cases if c['expected_code'] == 200])
    @pytest.mark.smoke
    def test_success_cases(self, case):
        """只测试登录成功的场景"""
        print(f"\n[正常场景]：{case['name']}")
        result = login_api(case['username'], case['password'])
        assert result.get('code') == 200
        assert 'token' in result
    
    @pytest.mark.parametrize("case", [c for c in test_cases if c['expected_code'] != 200])
    @pytest.mark.regression
    def test_failure_cases(self, case):
        print(f"\n[异常场景]:{case['username']}")
        result = login_api(case['username'], case['password'])
        assert result.get('code') != 200
