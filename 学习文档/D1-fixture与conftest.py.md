# pytest fixture 作用域完全指南

## 一、作用域层级总览

```text
session（会话级）← 最大范围，整个测试运行只执行一次
    │
    └── package（包级）← 整个包（目录）执行一次
        │
        └── module（模块级）← 每个测试文件执行一次
            │
            └── class（类级）← 每个测试类执行一次
                │
                └── function（函数级）← 每个测试函数执行一次（默认）
```

* * *

## 二、各作用域详解

### 1\. function（函数级）- 默认作用域

#### 基本定义

```python
import pytest

# 方式1：显式指定
@pytest.fixture(scope="function")
def func_fixture():
    print("\n[前置] 准备工作")
    data = {"name": "test", "value": 100}
    yield data
    print("[后置] 清理工作")

# 方式2：不写scope参数（默认就是function）
@pytest.fixture
def default_fixture():
    yield "默认作用域"
```

#### 执行特点

| 属性 | 说明 |
| :-- | :-- |
| **执行频率** | 每个测试函数执行一次 |
| **隔离性** | 最高，测试之间完全隔离 |
| **默认值** | 是（`scope` 参数可省略） |

#### 使用示例

```python
import pytest

@pytest.fixture
def counter():
    print("\n[前置] 初始化计数器")
    count = 0
    yield count
    print("[后置] 清理计数器")

class TestFunctionScope:
    def test_1(self, counter):
        counter += 1
        print(f"test_1: counter = {counter}")
        assert counter == 1

    def test_2(self, counter):
        counter += 1
        print(f"test_2: counter = {counter}")
        assert counter == 1  # 重新从0开始，不是1
```

**执行输出：**

```text
[前置] 初始化计数器
test_1: counter = 1
[后置] 清理计数器

[前置] 初始化计数器
test_2: counter = 1
[后置] 清理计数器
```

#### 使用场景

| 场景 | 原因 |
| :-- | :-- |
| 测试需要隔离 | 每个测试独立，不互相影响 |
| 临时数据 | 测试数据用完即扔 |
| 可变数据 | 避免测试之间数据污染 |
| 并发测试 | 支持并行执行 |

* * *

### 2\. class（类级）

#### 基本定义

```python
import pytest

@pytest.fixture(scope="class")
def class_fixture():
    print("\n[前置] 类级别初始化（整个类只一次）")
    shared_data = {"users": ["alice", "bob"]}
    yield shared_data
    print("[后置] 类级别清理（整个类只一次）")
```

#### 执行特点

| 属性 | 说明 |
| :-- | :-- |
| **执行频率** | 每个测试类执行一次 |
| **共享范围** | 同一个类中的所有测试方法 |
| **触发时机** | 类中第一个测试执行前初始化，最后一个测试执行后清理 |

##### 使用示例

```python
import pytest

@pytest.fixture(scope="class")
def database():
    print("\n[前置] 连接数据库")
    conn = {"host": "localhost", "connected": True}
    yield conn
    print("[后置] 断开数据库连接")

class TestUserAPI:
    def test_create_user(self, database):
        print(f"创建用户，数据库状态: {database['connected']}")
        assert database["connected"] is True

    def test_delete_user(self, database):
        print(f"删除用户，数据库状态: {database['connected']}")
        assert database["connected"] is True

class TestOrderAPI:
    def test_create_order(self, database):
        print("创建订单（新的数据库连接）")
        assert database["connected"] is True
```

**执行输出：**

```text
[前置] 连接数据库
创建用户，数据库状态: True
删除用户，数据库状态: True
[后置] 断开数据库连接

[前置] 连接数据库
创建订单（新的数据库连接）
[后置] 断开数据库连接
```

#### 使用场景

| 场景 | 原因 |
| :-- | :-- |
| 数据库连接池 | 避免每个测试都创建连接 |
| 类级别配置 | 同一类测试共享配置 |
| 耗时资源初始化 | 减少重复初始化开销 |
| 共享测试数据 | 类内测试使用相同的基础数据 |

* * *

### 3\. module（模块级）

#### 基本定义

```python
import pytest

@pytest.fixture(scope="module")
def module_fixture():
    print("\n[前置] 模块级别初始化（整个文件只一次）")
    config = load_config()
    yield config
    print("[后置] 模块级别清理")
```

#### 执行特点

| 属性 | 说明 |
| :-- | :-- |
| **执行频率** | 每个测试文件执行一次 |
| **共享范围** | 同一个文件中的所有测试 |
| **触发时机** | 文件中第一个测试执行前初始化，最后一个测试执行后清理 |

#### 使用示例

```python
# test_config.py
import pytest
import json

@pytest.fixture(scope="module")
def app_config():
    print("\n[前置] 读取配置文件")
    with open("config.json", "r") as f:
        config = json.load(f)
    yield config
    print("[后置] 释放配置资源")

class TestDatabaseConfig:
    def test_host(self, app_config):
        print(f"测试数据库主机: {app_config['db']['host']}")
        assert "host" in app_config["db"]

    def test_port(self, app_config):
        print(f"测试数据库端口: {app_config['db']['port']}")
        assert "port" in app_config["db"]

class TestAPIConfig:
    def test_api_key(self, app_config):
        print(f"测试API密钥存在性")
        assert "api_key" in app_config
```

**执行输出：**

```text
[前置] 读取配置文件
测试数据库主机: localhost
测试数据库端口: 5432
测试API密钥存在性
[后置] 释放配置资源
```

#### 使用场景

| 场景 | 原因 |
| :-- | :-- |
| 读取配置文件 | 文件只读一次，全部测试复用 |
| 加载大文件 | 避免重复IO操作 |
| 模块级日志 | 统一日志配置 |
| 环境变量设置 | 所有测试共享相同环境 |

* * *

### 4\. package（包级）

#### 基本定义

```python
# tests/conftest.py 或包内任何文件
import pytest

@pytest.fixture(scope="package")
def package_fixture():
    print("\n[前置] 包级别初始化（整个包只一次）")
    resources = initialize_package_resources()
    yield resources
    print("[后置] 包级别清理")
```

#### 执行特点

| 属性 | 说明 |
| :-- | :-- |
| **执行频率** | 整个包（目录）执行一次 |
| **共享范围** | 包内所有测试文件 |
| **触发时机** | 包中第一个测试执行前初始化，最后一个测试执行后清理 |

#### 文件结构

```text
tests/
├── __init__.py           # 使tests成为Python包
├── conftest.py           # 定义package级别的fixture
├── test_user.py          # 同一个包下的测试文件
└── test_order.py         # 同一个包下的测试文件
```

#### 使用示例

```python
# tests/conftest.py
import pytest

@pytest.fixture(scope="package")
def global_test_data():
    print("\n[前置] 初始化全局测试数据")
    users = ["admin", "tester", "guest"]
    yield {"users": users, "env": "testing"}
    print("[后置] 清理全局测试数据")
```

```python
# tests/test_user.py
def test_user_list(global_test_data):
    print(f"用户列表: {global_test_data['users']}")
    assert len(global_test_data["users"]) == 3

def test_user_role(global_test_data):
    print("测试用户角色")
    assert global_test_data["env"] == "testing"
```

```python
# tests/test_order.py
def test_order_creation(global_test_data):
    print(f"创建订单，环境: {global_test_data['env']}")
    assert global_test_data["env"] == "testing"

def test_order_query(global_test_data):
    print("查询订单依赖全局数据")
    assert "admin" in global_test_data["users"]
```

**执行命令：** `pytest tests/`
**输出：**

```text
[前置] 初始化全局测试数据
用户列表: ['admin', 'tester', 'guest']
测试用户角色
创建订单，环境: testing
查询订单依赖全局数据
[后置] 清理全局测试数据
```

#### 使用场景

| 场景 | 原因 |
| :-- | :-- |
| 集成测试 | 多个模块测试共享同一个测试环境 |
| 端到端测试 | 整个功能模块的测试共享状态 |
| 数据库种子数据 | 包内所有测试使用相同的基础数据 |
| 服务启动/停止 | Mock服务在整个包测试期间运行 |

* * *

### 5\. session（会话级）

#### 基本定义

```python
# tests/conftest.py
import pytest

@pytest.fixture(scope="session")
def session_fixture():
    print("\n[前置] 会话级别初始化（整个测试运行只一次）")
    global_resource = setup_global_resource()
    yield global_resource
    print("[后置] 会话级别清理")
```

#### 执行特点

| 属性 | 说明 |
| :-- | :-- |
| **执行频率** | 整个 pytest 运行过程只执行一次 |
| **共享范围** | 所有测试文件、所有包 |
| **触发时机** | 测试会话开始时初始化，所有测试完成后清理 |

#### 使用示例

```python
# tests/conftest.py
import pytest
from selenium import webdriver

@pytest.fixture(scope="session")
def browser():
    print("\n[前置] 启动浏览器（所有测试共享）")
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    print("[后置] 关闭浏览器")
```

```python
# tests/test_login.py
def test_login_page(browser):
    browser.get("https://example.com/login")
    assert "Login" in browser.title

def test_login_submit(browser):
    browser.get("https://example.com/login")
    browser.find_element(...).click()
    # 复用同一个浏览器会话
```

```python
# tests/test_profile.py
def test_profile_page(browser):
    browser.get("https://example.com/profile")
    assert "Profile" in browser.title
```

**执行命令：** `pytest tests/`
**输出：**

```text
[前置] 启动浏览器（所有测试共享）
测试登录页面
测试登录提交
测试个人资料页面
[后置] 关闭浏览器
```

> 💡 **重要**：整个测试过程只启动一次浏览器，所有测试共用一个会话。

#### 使用场景

| 场景 | 原因 |
| :-- | :-- |
| Web测试 | 启动一次浏览器，所有测试复用 |
| 数据库连接池 | 整个测试会话共享连接 |
| 全局配置加载 | 配置文件只读一次 |
| 日志系统 | 统一的日志配置 |
| 性能测试 | 避免重复初始化影响测试结果 |

* * *

## 三、作用域对比总结表

| 作用域 | 执行次数 | 共享范围 | 触发时机 | 推荐场景 |
| :-- | :-- | :-- | :-- | :-- |
| `function` | 每个测试函数 1 次 | 单个测试函数 | 每个测试前后 | 隔离测试、临时数据 |
| `class` | 每个测试类 1 次 | 同一个类的所有方法 | 类开始前/结束后 | 类级别共享资源 |
| `module` | 每个文件 1 次 | 同一个文件的所有测试 | 文件开始前/结束后 | 配置文件、模块级数据 |
| `package` | 每个包 1 次 | 整个包的所有测试 | 包开始前/结束后 | 包级集成测试 |
| `session` | 整个会话 1 次 | 所有测试 | 测试会话开始前/结束后 | 全局资源、浏览器驱动 |

* * *

## 四、执行顺序图

```text
pytest 启动
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│ session 初始化（只1次）                                      │
│     │                                                       │
│     ▼                                                       │
│ ┌───────────────────────────────────────────────────────┐   │
│ │ package A 初始化（第一个执行的包）                      │   │
│ │     │                                                 │   │
│ │     ▼                                                 │   │
│ │ ┌─────────────────────────────────────────────────┐   │   │
│ │ │ module A1 初始化                                  │   │   │
│ │ │     │                                           │   │   │
│ │ │     ├── class A1 初始化                         │   │   │
│ │ │     │     ├── test_1 初始化 → 执行 → 清理        │   │   │
│ │ │     │     ├── test_2 初始化 → 执行 → 清理        │   │   │
│ │ │     │     └── class A1 清理                     │   │   │
│ │ │     │                                           │   │   │
│ │ │     ├── class A2 初始化                         │   │   │
│ │ │     │     ├── test_3 初始化 → 执行 → 清理        │   │   │
│ │ │     │     └── class A2 清理                     │   │   │
│ │ │     │                                           │   │   │
│ │ │     └── module A1 清理                           │   │   │
│ │ └─────────────────────────────────────────────────┘   │   │
│ │                                                       │   │
│ │ ┌─────────────────────────────────────────────────┐   │   │
│ │ │ module A2 初始化                                  │   │   │
│ │ │     └── ...                                      │   │   │
│ │ │     └── module A2 清理                           │   │   │
│ │ └─────────────────────────────────────────────────┘   │   │
│ │                                                       │   │
│ └── package A 清理                                       │
│                                                         │
│ ┌───────────────────────────────────────────────────────┐   │
│ │ package B 初始化                                       │   │
│ │     └── ...                                          │   │
│ └── package B 清理                                       │
└─────────────────────────────────────────────────────────────┘
    │
    ▼
session 清理
```

* * *

## 五、嵌套使用示例

### 高级示例：多级依赖

```python
import pytest

# session级：全局配置
@pytest.fixture(scope="session")
def global_config():
    print("\n[session] 加载全局配置")
    yield {"env": "test", "version": "2.0"}

# package级：包级资源
@pytest.fixture(scope="package")
def package_resource(global_config):
    print(f"[package] 初始化包资源，依赖 {global_config['env']}")
    resource = {"name": "package_data", "config": global_config}
    yield resource
    print("[package] 清理包资源")

# module级：模块数据
@pytest.fixture(scope="module")
def module_data(package_resource):
    print(f"[module] 准备模块数据，依赖 {package_resource['name']}")
    data = {"module": "test_module", "parent": package_resource}
    yield data
    print("[module] 清理模块数据")

# class级：类实例
@pytest.fixture(scope="class")
def class_instance(module_data):
    print(f"[class] 创建类实例，依赖 {module_data['module']}")
    instance = {"id": 123, "module_data": module_data}
    yield instance
    print("[class] 销毁类实例")

# function级：测试数据
@pytest.fixture
def test_data(class_instance):
    print(f"[function] 生成测试数据，依赖 {class_instance['id']}")
    yield {"value": 42, "instance": class_instance}
    print("[function] 清理测试数据")

class TestIntegration:
    def test_1(self, test_data):
        print(f"执行 test_1: {test_data['value']}")
        assert test_data["value"] == 42

    def test_2(self, test_data):
        print(f"执行 test_2: {test_data['instance']['id']}")
        assert test_data["instance"]["id"] == 123
```

**执行顺序：**

```text
[session] 加载全局配置
[package] 初始化包资源，依赖 test
[module] 准备模块数据，依赖 package_data
[class] 创建类实例，依赖 test_module
[function] 生成测试数据，依赖 123
执行 test_1: 42
[function] 清理测试数据
[function] 生成测试数据，依赖 123
执行 test_2: 123
[function] 清理测试数据
[class] 销毁类实例
[module] 清理模块数据
[package] 清理包资源
```

* * *

## 六、实际应用场景模板

### 场景1：Web自动化测试

```python
# conftest.py
import pytest
from selenium import webdriver

# session：所有测试共享浏览器
@pytest.fixture(scope="session")
def driver():
    print("启动浏览器")
    driver = webdriver.Chrome()
    yield driver
    print("关闭浏览器")

# function：每个测试独立清理cookies
@pytest.fixture
def clean_driver(driver):
    driver.delete_all_cookies()
    yield driver
    driver.delete_all_cookies()
```

### 场景2：数据库测试

```python
# conftest.py
import pytest
import psycopg2

# module：每个测试文件独立的数据库连接
@pytest.fixture(scope="module")
def db_connection():
    print("连接数据库")
    conn = psycopg2.connect("dbname=test")
    yield conn
    print("断开连接")
    conn.close()

# function：每个测试独立的事务回滚
@pytest.fixture
def db_transaction(db_connection):
    print("开启事务")
    transaction = db_connection.cursor()
    yield transaction
    print("回滚事务")
    db_connection.rollback()
```

### 场景3：API测试

```python
# conftest.py
import pytest
import requests

# package：整个测试包共享的会话
@pytest.fixture(scope="package")
def api_session():
    print("创建API会话")
    session = requests.Session()
    session.headers.update({"Authorization": "Bearer token"})
    yield session
    print("关闭API会话")
    session.close()

# class：同一类测试共享的用户
@pytest.fixture(scope="class")
def test_user(api_session):
    print("创建测试用户")
    user = {"id": 1, "name": "tester"}
    yield user
    print("删除测试用户")
    api_session.delete(f"/users/{user['id']}")
```

* * *

## 七、选择决策树

```text
需要共享的资源初始化开销大吗？
    │
    ├── 是 → 尽量使用更高级的作用域
    │
    └── 否 → 可以使用 function 作用域

资源是否会被测试修改？
    │
    ├── 会被修改 → 使用 function 作用域（隔离）
    │
    └── 只读 → 可以使用更高级作用域

需要跨文件共享吗？
    │
    ├── 需要 → session / package
    │
    └── 不需要 → module / class

需要跨类共享吗？
    │
    ├── 需要 → module
    │
    └── 不需要 → class / function
```

* * *

## 八、一句话总结

| 作用域 | 一句话理解 |
| :-- | :-- |
| `function` | 每个测试独立，用完即扔，互不影响 |
| `class` | 一个类里的测试共享，类与类之间隔离 |
| `module` | 一个文件里的测试共享，文件与文件之间隔离 |
| `package` | 一个目录里的测试共享，目录与目录之间隔离 |
| `session` | 整个测试运行只做一次，所有测试共享 |
# conftest.py 和 fixture 作用域

`conftest.py` 和 `fixture` 作用域之间最容易被混淆的核心。让我们先理清这两个概念，然后看它们是如何关联的。

## 1. 先分别理解：它们是两个完全不同的东西

**`fixture` 作用域**：这是关于 **“一个 fixture 的生命周期有多长”**。
- `function`：每个测试函数执行前都重新创建一次。
- `class`：每个测试类执行前创建一次。
- `module`：每个测试文件执行前创建一次。
- `session`：整个 pytest 运行期间只创建一次。

> 💡 **核心问题**：“这个数据/资源，什么时候创建，什么时候销毁？”

**`conftest.py`**：这是关于 **“一个 fixture 可以给多少个测试文件使用”**。
- 如果把 fixture 写在 `test_a.py` 里，它只能被 `test_a.py` 使用。
- 如果把 fixture 写在 `conftest.py` 里，它就能被 **同级和所有子目录** 中的任意测试文件使用。

> 💡 **核心问题**：“这个 fixture，能放在哪里，让其他文件也能用？”

**`fixture` 作用域 = 时间维度（活多久）**  
**`conftest.py` = 空间维度（能用多广）**  
它们是正交的两个概念，互不冲突。

---

## 2. 一个比喻帮你彻底分清

想象你是餐厅的厨师（`pytest`），你要为客人准备餐前小菜（`fixture`）。

### 🕒 `fixture` 作用域（时间/生命周期）
- **`function`**：每位客人来了我都现做一份小菜（客人 A 和客人 B 的小菜是独立的）。
- **`class`**：每桌客人（一个测试类）共享一份大拼盘（这桌的客人 A 和 B 吃同一盘）。
- **`module`**：每天午餐时段（一个测试文件）只做一份招牌菜，所有午餐客人都吃这个。
- **`session`**：整个餐厅营业期间（一次 pytest 运行）只熬一锅汤，所有客人喝同一锅。

### 🌍 `conftest.py`（空间/共享范围）
- **场景 1：小餐馆（单文件）**  
  你的菜谱（fixture）写在厨房里的一张纸条上（写在 `test_order.py` 文件里）。这张纸条只有管这个厨房的厨师能看到。  
  → 其他测试文件无法使用这个 fixture。
- **场景 2：连锁餐厅（多文件）**  
  你把菜谱（fixture）写在一个中央菜谱库（`conftest.py`）里。然后把它复印给所有分店（不同目录下的测试文件）。  
  → 所有分店（所有同级和子目录的测试文件）都能照着这个菜谱做菜。

### 🔗 现在，让它们两个结合：
你想让整个连锁餐厅（`session` 作用域）的所有分店（`conftest.py` 的共享范围）都使用同一锅老汤（一次创建，全局使用）。

对应的代码就是：

**`conftest.py`**
```python
import pytest

@pytest.fixture(scope="session") # <-- 时间维度：整个测试会话只熬一锅
def master_soup():
    print("\n[老汤] 熬制中...（只一次）")
    return "秘制老汤"
```



