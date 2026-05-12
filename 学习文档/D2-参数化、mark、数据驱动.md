## 学习路线图

```text
第1步：理解参数化 → 第2步：理解mark标签 → 第3步：理解数据驱动 → 第4步：综合实战
```

* * *

# 第一阶段：参数化（Parametrize）

## 1.1 什么是参数化？

**通俗理解**：同一个测试逻辑，换不同的数据反复执行。

```python
# 没有参数化 - 代码重复
def test_login_1():
 assert login("admin", "123") == "成功"

def test_login_2():
 assert login("user1", "456") == "成功"

# 有参数化 - 一份代码，多组数据
@pytest.mark.parametrize("username,password", [
 ("admin", "123"),
 ("user1", "456"),
])
def test_login(username, password):
 assert login(username, password) == "成功"
```

## 1.2 第一个参数化练习

**步骤1：创建项目和虚拟环境**

```bash
# 创建项目文件夹
mkdir pytest_learning
cd pytest_learning

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境 (Windows Git Bash)
source venv/Scripts/activate

# 安装pytest
pip install pytest
```

**步骤2：创建第一个测试文件**

创建 `test_param.py`：

```python
import pytest

# 最简单的参数化 - 单参数
@pytest.mark.parametrize("city", ["北京", "上海", "广州", "深圳"])
def test_city(city):
 """测试城市名称不为空"""
 print(f"\n测试城市: {city}")
 assert len(city) > 0
```

**步骤3：运行测试**

```bash
pytest test_param.py -v -s
```

**输出效果**：

```text
test_param.py::test_city[北京] 
测试城市: 北京
PASSED
test_param.py::test_city[上海] 
测试城市: 上海
PASSED
test_param.py::test_city[广州] 
测试城市: 广州
PASSED
test_param.py::test_city[深圳] 
测试城市: 深圳
PASSED
```

✅ **知识点掌握**：参数化让一个测试函数自动执行了4次，每次传入不同的值。

## 1.3 多参数参数化

```python
import pytest

# 多参数 - 每组数据有多个值
@pytest.mark.parametrize("username,password,expected", [
 ("admin", "123456", "成功"),
 ("admin", "wrong", "失败"),
 ("", "123456", "用户名不能为空"),
 ("admin", "", "密码不能为空"),
])
def test_login(username, password, expected):
 """测试登录功能"""
 print(f"\n测试登录: {username} / {password} -> 期望: {expected}")

 # 模拟登录逻辑
 result = mock_login(username, password)

 assert result == expected

def mock_login(username, password):
 """模拟登录函数"""
 if not username:
 return "用户名不能为空"
 if not password:
 return "密码不能为空"
 if username == "admin" and password == "123456":
 return "成功"
 return "失败"
```

运行：

```bash
pytest test_param.py -v -s
```

**练习任务**：

1.  修改上面的数据，添加第5组数据 `("test", "test", "用户不存在")`
2.  运行看看结果

* * *

# 第二阶段：mark标签（Marker）

## 2.1 什么是mark标签？

**通俗理解**：给测试用例贴标签，想运行哪类就运行哪类。

```python
@pytest.mark.smoke      # 贴"冒烟测试"标签
@pytest.mark.regression # 贴"回归测试"标签
def test_login():
 pass
```

## 2.2 第一个标签练习

**创建 `test_mark.py`**：

```python
import pytest

class TestUser:

 @pytest.mark.smoke
 def test_login_success(self):
 """冒烟测试-登录成功"""
 print("\n执行冒烟测试: 登录成功")
 assert True

 @pytest.mark.smoke
 def test_login_fail(self):
 """冒烟测试-登录失败"""
 print("\n执行冒烟测试: 登录失败")
 assert True

 @pytest.mark.regression
 def test_register(self):
 """回归测试-注册功能"""
 print("\n执行回归测试: 用户注册")
 assert True

 @pytest.mark.regression
 def test_forgot_password(self):
 """回归测试-忘记密码"""
 print("\n执行回归测试: 忘记密码")
 assert True

 @pytest.mark.slow
 def test_large_data(self):
 """慢速测试-大数据处理"""
 print("\n执行慢速测试: 大数据处理")
 assert True
```

**运行不同标签**：

```bash
# 只运行冒烟测试
pytest test_mark.py -m smoke -v -s

# 只运行回归测试
pytest test_mark.py -m regression -v -s

# 运行冒烟或回归测试
pytest test_mark.py -m "smoke or regression" -v -s

# 排除慢速测试
pytest test_mark.py -m "not slow" -v -s
```

## 2.3 注册标签（消除警告）

创建 `pytest.ini` 文件：

```ini
[pytest]
markers =
 smoke: 冒烟测试-核心功能
 regression: 回归测试-完整验证
 slow: 慢速测试-执行时间长
```

**练习任务**：

1.  运行 `pytest test_mark.py -m smoke`，观察结果
2.  添加一个新标签 `@pytest.mark.p0` 到某个测试
3.  运行 `pytest -m p0` 看看能否运行

* * *

# 第三阶段：数据驱动（Data-Driven）

## 3.1 什么是数据驱动？

**核心思想**：测试数据从代码里分离出来，存在外部文件（YAML/JSON）中。

```text
❌ 错误方式：数据写在代码里
def test_login():
 data = {"username": "admin", "password": "123"}  # 改数据要改代码

✅ 正确方式：数据存在文件里
def test_login(test_data):  # test_data从文件读取
 # 改数据只需改文件，不用改代码
```

## 3.2 安装YAML支持

```bash
pip install pyyaml
```

## 3.3 创建数据文件

**创建 `data/login_data.yaml`**：

```yaml
login_cases:
 - name: "正常登录"
 username: "admin"
 password: "123456"
 expected: "成功"

 - name: "密码错误"
 username: "admin"
 password: "wrong"
 expected: "失败"

 - name: "用户名为空"
 username: ""
 password: "123456"
 expected: "用户名不能为空"
```

## 3.4 创建数据加载器

**创建 `utils/data_loader.py`**：

```python
"""
数据加载器 - 从YAML文件读取测试数据
"""
import yaml
from pathlib import Path

class DataLoader:
 """数据加载器"""

 @staticmethod
 def load_yaml(file_path):
 """加载YAML文件"""
 # 获取项目根目录
 project_root = Path(__file__).parent.parent
 full_path = project_root / file_path

 # 读取文件
 with open(full_path, 'r', encoding='utf-8') as f:
 data = yaml.safe_load(f)

 return data

 @staticmethod
 def get_test_cases(file_path, case_key):
 """获取测试用例列表"""
 data = DataLoader.load_yaml(file_path)
 return data[case_key]
```

## 3.5 使用数据驱动的测试

**创建 `test_data_driven.py`**：

```python
"""
数据驱动测试 - 数据从YAML文件读取
"""
import pytest
from utils.data_loader import DataLoader

# 加载测试数据（数据与代码分离！）
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

# 参数化 + 数据驱动
@pytest.mark.parametrize("case", test_cases)
def test_login(case):
 """测试登录 - 数据从YAML文件来"""
 print(f"\n执行用例: {case['name']}")
 print(f"请求数据: username={case['username']}, password={case['password']}")
 print(f"期望结果: {case['expected']}")

 # 执行测试
 result = mock_login(case['username'], case['password'])

 # 断言
 assert result == case['expected']
 print(f"✅ 实际结果: {result}")
```

**运行测试**：

```bash
pytest test_data_driven.py -v -s
```

**练习任务**：

1.  修改 `data/login_data.yaml`，添加第4组数据：密码为空的情况
2.  不需要改任何代码，重新运行测试，新数据自动生效

✅ **核心收获**：改数据不需要改代码！

* * *

# 第四阶段：综合实战

现在我们把所有知识点结合起来。

## 4.1 完整项目结构

```text
pytest_learning/
│
├── pytest.ini                    # 配置（注册标签）
├── requirements.txt              # 依赖
│
├── data/                         # 数据文件
│   └── login_data.yaml          # 10组测试数据
│
├── utils/                        # 工具
│   └── data_loader.py           # 数据加载器
│
├── apis/                         # API封装
│   └── login_api.py             # 登录API
│
└── test_cases/                   # 测试用例
    └── test_login.py            # 登录测试
```

## 4.2 创建所有文件

**步骤1：创建目录**

```bash
mkdir -p data utils apis test_cases
```

**步骤2：requirements.txt**

```txt
pytest==7.4.3
pytest-html==4.1.1
pyyaml==6.0.1
requests==2.31.0
```

安装：`pip install -r requirements.txt`

**步骤3：pytest.ini**

```ini
[pytest]
markers =
 smoke: 冒烟测试-核心功能
 regression: 回归测试-完整验证
 p0: 最高优先级
 p1: 高优先级
 login: 登录模块

addopts = -v -s --html=reports/report.html
testpaths = test_cases
```

**步骤4：data/login_data.yaml（10组数据）**

```yaml
login_cases:
 - name: "TC001_正常登录_管理员"
 username: "admin"
 password: "admin123"
 expected_code: 200
 expected_msg: "登录成功"
 priority: "p0"
 markers: ["smoke", "login"]

 - name: "TC002_正常登录_普通用户"
 username: "user001"
 password: "pass123"
 expected_code: 200
 expected_msg: "登录成功"
 priority: "p1"
 markers: ["smoke", "login"]

 - name: "TC003_密码错误"
 username: "admin"
 password: "wrong"
 expected_code: 401
 expected_msg: "用户名或密码错误"
 priority: "p0"
 markers: ["regression", "login"]

 - name: "TC004_用户名为空"
 username: ""
 password: "admin123"
 expected_code: 400
 expected_msg: "用户名不能为空"
 priority: "p0"
 markers: ["regression", "login"]

 - name: "TC005_密码为空"
 username: "admin"
 password: ""
 expected_code: 400
 expected_msg: "密码不能为空"
 priority: "p0"
 markers: ["regression", "login"]

 - name: "TC006_用户名不存在"
 username: "notexist"
 password: "123456"
 expected_code: 404
 expected_msg: "用户不存在"
 priority: "p1"
 markers: ["regression", "login"]

 - name: "TC007_SQL注入测试"
 username: "' OR '1'='1"
 password: "123456"
 expected_code: 401
 expected_msg: "用户名或密码错误"
 priority: "p1"
 markers: ["regression", "login"]

 - name: "TC008_XSS攻击测试"
 username: "<script>alert('xss')</script>"
 password: "123456"
 expected_code: 400
 expected_msg: "用户名包含非法字符"
 priority: "p1"
 markers: ["regression", "login"]

 - name: "TC009_超长用户名"
 username: "a" * 101
 password: "123456"
 expected_code: 400
 expected_msg: "用户名长度超出限制"
 priority: "p2"
 markers: ["regression", "login"]

 - name: "TC010_特殊字符测试"
 username: "test@#$%"
 password: "123456"
 expected_code: 401
 expected_msg: "用户名或密码错误"
 priority: "p2"
 markers: ["regression", "login"]
```

**步骤5：utils/data_loader.py**

```python
import yaml
from pathlib import Path
from typing import List, Dict

class DataLoader:
 """数据加载器"""

 PROJECT_ROOT = Path(__file__).parent.parent

 @classmethod
 def load_yaml(cls, file_path: str) -> Dict:
 full_path = cls.PROJECT_ROOT / file_path
 with open(full_path, 'r', encoding='utf-8') as f:
 return yaml.safe_load(f)

 @classmethod
 def get_test_cases(cls, file_path: str, case_key: str) -> List[Dict]:
 data = cls.load_yaml(file_path)
 return data.get(case_key, [])
```

**步骤6：apis/login_api.py**

```python
from typing import Dict

class LoginAPI:
 """登录API"""

 @staticmethod
 def login(username: str, password: str) -> Dict:
 """执行登录 - 模拟实现"""
 # 参数校验
 if not username:
 return {"code": 400, "message": "用户名不能为空"}
 if not password:
 return {"code": 400, "message": "密码不能为空"}

 # 长度校验
 if len(username) > 100:
 return {"code": 400, "message": "用户名长度超出限制"}

 # 非法字符检测
 if '<' in username or '>' in username or 'script' in username.lower():
 return {"code": 400, "message": "用户名包含非法字符"}

 # SQL注入检测
 if "'" in username or '"' in username:
 return {"code": 401, "message": "用户名或密码错误"}

 # 用户验证
 valid_users = {
 "admin": "admin123",
 "user001": "pass123"
 }

 if username in valid_users:
 if valid_users[username] == password:
 return {"code": 200, "message": "登录成功", "token": f"token_{username}"}
 return {"code": 401, "message": "用户名或密码错误"}

 if username == "notexist":
 return {"code": 404, "message": "用户不存在"}

 return {"code": 401, "message": "用户名或密码错误"}

# 便捷函数
def login_api(username: str, password: str) -> Dict:
 return LoginAPI.login(username, password)
```

**步骤7：test_cases/test_login.py**

```python
"""
登录接口测试 - 综合运用参数化、mark标签、数据驱动
"""
import pytest
from apis.login_api import login_api
from utils.data_loader import DataLoader

# 加载10组测试数据（数据与代码分离！）
test_cases = DataLoader.get_test_cases('data/login_data.yaml', 'login_cases')

class TestLogin:
 """登录测试类"""

 # ========== 综合测试 ==========
 @pytest.mark.parametrize("case", test_cases)
 def test_all_cases(self, case):
 """测试所有10组用例"""
 print(f"\n{'='*50}")
 print(f"用例: {case['name']}")
 print(f"请求: username={case['username']}, password={case['password']}")
 print(f"期望: code={case['expected_code']}, msg={case['expected_msg']}")

 # 执行测试
 result = login_api(case['username'], case['password'])

 print(f"实际: code={result.get('code')}, msg={result.get('message')}")

 # 断言
 assert result.get('code') == case['expected_code']
 assert result.get('message') == case['expected_msg']

 # ========== 按优先级筛选测试 ==========
 @pytest.mark.parametrize("case", [c for c in test_cases if c['priority'] == 'p0'])
 @pytest.mark.p0
 @pytest.mark.smoke
 def test_p0_cases(self, case):
 """测试P0优先级用例"""
 print(f"\n[P0高优先级] {case['name']}")
 result = login_api(case['username'], case['password'])
 assert result.get('code') == case['expected_code']

 # ========== 只测试正常场景 ==========
 @pytest.mark.parametrize("case", [c for c in test_cases if c['expected_code'] == 200])
 @pytest.mark.smoke
 def test_success_cases(self, case):
 """只测试登录成功的场景"""
 print(f"\n[正常场景] {case['name']}")
 result = login_api(case['username'], case['password'])
 assert result.get('code') == 200
 assert 'token' in result

 # ========== 只测试异常场景 ==========
 @pytest.mark.parametrize("case", [c for c in test_cases if c['expected_code'] != 200])
 @pytest.mark.regression
 def test_failure_cases(self, case):
 """只测试登录失败的场景"""
 print(f"\n[异常场景] {case['name']}")
 result = login_api(case['username'], case['password'])
 assert result.get('code') != 200
```

## 4.3 运行测试

```bash
# 1\. 运行所有测试
pytest test_cases/test_login.py

# 2\. 只运行P0优先级测试
pytest -m p0

# 3\. 只运行冒烟测试
pytest -m smoke

# 4\. 生成HTML报告
pytest --html=reports/report.html

# 5\. 查看详细输出
pytest -v -s
```

## 4.4 总结检查清单

完成以下任务，证明你已掌握：

*   **参数化**：能用一个测试函数执行10组不同数据
*   **mark标签**：能用 `-m smoke` 只运行冒烟测试
*   **数据驱动**：能修改YAML文件而不改代码
*   **数据分离**：数据文件在 `data/`，代码在 `test_cases/`
*   **结构**：项目有清晰的目录结构

## 4.5 扩展练习

1.  **添加新数据**：在YAML中添加第11组数据，不改代码，测试自动执行
2.  **新建标签**：创建 `@pytest.mark.p2`，标记几个用例
3.  **改用JSON**：把YAML数据改成JSON格式，修改加载器支持JSON
4.  **真实接口**：把 `login_api` 改成调用真实HTTP接口

* * *

**恭喜！你已完成新手教程！** 🎉

现在你掌握了：

*   ✅ 参数化 - 一份代码多组数据
*   ✅ mark标签 - 灵活选择执行哪些测试
*   ✅ 数据驱动 - 数据与代码分离
*   ✅ 10组接口参数化
*   ✅ 完整的项目结构