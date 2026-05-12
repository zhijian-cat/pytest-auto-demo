# 高频词汇
词汇的标准读法整理，已严格按您要求的格式统一排版：

**session** 音标：英 /ˈseʃ.ən/ ｜ 美 /ˈseʃ.ən/ 音节/重音：ses-sion（2音节），重音在 SES 中文谐音参考：“赛申”（“赛”短促，“申”带轻微鼻音，连读）

**module** 音标：英 /ˈmɒd.juːl/ ｜ 美 /ˈmɑː.dʒuːl/ 音节/重音：mod-ule（2音节），重音在 MOD 中文谐音参考：“莫杰欧”（英式）/“妈杰欧”（美式，du 同化为 /dʒ/ 音）

**yield** 音标：英 /jiːld/ ｜ 美 /jiːld/ 音节/重音：单音节，重音在整体 中文谐音参考：“耶-ld”（连贯单音节，ld 舌尖连贯动作，切勿拆读）

**pytest.raises** 音标：英 /ˈpaɪ.test ˈreɪ.zɪz/ ｜ 美 /ˈpaɪ.test ˈreɪ.zɪz/ 音节/重音：py-test dot rai-ses（组合标识符），重音在 PY 和 RAI 中文谐音参考：“派-test 点 瑞-ziz”（dot 轻读，raises 结尾发浊音 /z/）

**exc_info** 音标：英 /ɪkˈsep ˈɪn.fəʊ/ ｜ 美 /ɪkˈsep ˈɪn.foʊ/ 音节/重音：exc in-fo（日常省略下划线连读），重音在 SEP 和 IN 中文谐音参考：“ik-SEP IN-foh”（exc 为 exception 缩写，info 重音在前）

**traceback** 音标：英 /ˈtreɪs.bæk/ ｜ 美 /ˈtreɪs.bæk/ 音节/重音：trace-back（2音节），重音在 TRACE 中文谐音参考：“追斯-拜克”（两个词清晰连读，不要吞音）

**assert** 音标：英 /əˈsɜːt/ ｜ 美 /əˈsɜːrt/ 音节/重音：as-sert（2音节），重音在 SERT 中文谐音参考：“额-SERT”（“额”极轻，“瑟特”重读且清晰）

**fixture** 音标：英 /ˈfɪk.stʃə/ ｜ 美 /ˈfɪk.stʃər/ 音节/重音：fix-ture（2音节），重音在 FIX 中文谐音参考：“菲克斯-彻”（美音带轻微卷舌“彻儿”）

**scope** 音标：英 /skəʊp/ ｜ 美 /skoʊp/ 音节/重音：单音节，重音在整体 中文谐音参考：“斯-寇普”（“斯”与“寇”紧密连读无停顿，/oʊ/ 嘴型由圆滑向两侧收拢，结尾 /p/ 轻触双唇即止，不送气）

**conftest.py** 音标：英 /ˈkɒn.fest dɒt paɪ/ ｜ 美 /ˈkɑːn.fest dɑːt paɪ/ 音节/重音：con-fest dot py（组合标识符），重音在 CON 和 PY 中文谐音参考：“康-test 点 派”（conf 发音同 conference 首音节，test 正常读，dot 轻读弱化，py 读作“派”）

**autouse**：在 `pytest` 社区中，开发者通常直接按字面拆读为 **`auto-use`**（自动使用），语速快时会自然连读成“奥透尤兹”。你只需记住：**重音在开头，结尾发 `z` 音**，即可被全球开发者准确理解。

**enumerate**：不要和 `enum`（枚举类型，读 `/ˈiːnʌm/` 或 “伊-纳姆”）混淆， Python 中 `enumerate()` 的作用是 **“带索引遍历”**，读音重音落在 `nu` 上即可被全球开发者准确理解，📌 **一句话总结**：重音在第二个音节，读作 **伊-努-么-瑞特**，记住“努”字加重，就是最地道的开发者发音。

**YAML** 在技术会议、代码评审或面试中，读作 **“雅姆”** 或 **“YAM-ul”** 更显专业。日常交流中按字母读 `Y-A-M-L` 也能被理解，但建议逐步习惯标准读法。

**hookimpl***是 pytest 源码中的一个标识符，由两个部分缩写组成：**`hook` + `impl`**。在技术社区中，开发者通常这样读：**胡克-印普尔** ，它不是自然语言单词，而是编程标识符，不需要追求绝对标准发音，按 `hook` + `impl` 拆分读最自然。

**parametrize**：普-**瑞姆**-呃-踹兹（第二个音节重读）  

**regression** 的标准读音如下：  **中文谐音**：瑞-**格瑞**-申

**priority（优先权）**：`普赖 - **奥** - 若 - 提`
（拼音：`pǔ lài - **ào** - ruò - tí`）*   `**奥**`：**重读+拉长**
**priority 高频搭配**

*   `top / highest priority` 最高优先级
*   `low / medium / high priority` 低/中/高优先级
*   `give priority to...` 优先考虑…
*   `set / adjust / reprioritize priorities` 设定/调整优先级
*   `out of priority` 优先级错乱/未排序

# pytest 官方命名规范（默认收集规则）

| 对象 | 必须格式 | 示例 | 说明 |
| :-- | :-- | :-- | :-- |
| **测试文件** | `test_*.py` 或 `*_test.py` | `test_login.py` / `auth_test.py` | 文件名不匹配则直接跳过 |
| **测试类** | `Test*`（**大写 T**） | `class TestLogin:` | ❌ `test_login`、`Test_login` 均不会被收集 |
| **测试方法/函数** | `test_*`（小写 t + 下划线） | `def test_valid_user():` | 类内外均适用 |

类名加 `Test` 只是告诉 pytest “请进这个类里找测试方法”，但具体哪些方法是测试用例，**仍然严格依赖方法名以 `test_` 开头**。

* * *

### 🔍 底层收集逻辑

pytest 的测试发现机制是**两级过滤**，两者独立且必须同时满足：

| 层级 | 标识 | 作用 | 不满足的后果 |
| :-- | :-- | :-- | :-- |
| **1\. 类级** | `Test*`（大写T） | 告诉 pytest：“这个类是测试容器，请扫描它” | 整个类被忽略，内部方法一个都不会看 |
| **2\. 方法级** | `test_*`（小写t+下划线） | 告诉 pytest：“这个方法是具体测试用例，请执行它” | 方法被当作普通辅助函数，**不执行、不报错、不计入报告** |

* * *

### ✅ 正确 vs ❌ 错误示例

```python
class TestUserAuth:  # ✅ 类名符合 Test*

    def test_login_success(self):  # ✅ 会被收集并执行
        assert True

    def validate_token(self):  # ❌ 辅助方法，pytest 直接跳过
        return "valid"

    def setup_method(self):  # ⚠️ 特殊钩子（非测试用例），pytest 自动识别
        pass
```

🔍 验证命令：`pytest --collect-only -q`
输出只会显示 `test_login_success`，`validate_token` 不会出现。

* * *

### 💡 为什么这样设计？

1.  **隔离辅助代码**：测试类中常包含数据构造、Mock 封装、断言辅助等方法。如果类名带 `Test` 就自动执行所有方法，会导致大量非测试逻辑被误跑。
2.  **精准控制粒度**：你可以自由在 `Test*` 类中写任意数量的 `test_*` 用例，同时保留私有/辅助方法，互不干扰。
3.  **框架生态兼容**：Allure、pytest-html、覆盖率工具、IDE 测试面板均依赖 `test_` 前缀进行用例映射与报告生成。

# 常用钩子按生命周期分类

| 阶段 | 钩子名称 | 典型用途 |
| --- | --- | --- |
| **启动/配置** | `pytest_addoption` | 添加自定义命令行参数（如 `--env`） |
|  | `pytest_configure` | 初始化插件、注册标记、修改配置 |
| **收集阶段** | `pytest_collection` | 干预测试文件发现过程 |
|  | `pytest_collection_modifyitems` | 用例收集后排序、过滤、打标签 |
|  | `pytest_generate_tests` | 动态参数化（替代 `@pytest.mark.parametrize`） |
| **执行阶段** | `pytest_runtest_setup` | 每个用例执行前（Fixture 之前） |
|  | `pytest_runtest_call` | 执行测试函数本身 |
|  | `pytest_runtest_teardown` | 每个用例执行后（Fixture 之后） |
| **报告/结束** | `pytest_terminal_summary` | 自定义终端输出报告 |
|  | `pytest_sessionfinish` | 整个测试会话结束，清理资源 |

* * *

### ⚠️ 常见踩坑场景

| 错误写法 | 结果 | 正确写法 |
| --- | --- | --- |
| `def pytest_runtest_setp(item):` | 静默忽略，钩子不执行 | `pytest_runtest_setup` |
| `def pytest_collection_modifyitems(config, items, **kwargs):` | 可能失效或报参数错误 | `def pytest_collection_modifyitems(config, items):` |
| 钩子写在普通 `.py` 文件而非 `conftest.py` | pytest 不会自动加载 | 移至 `conftest.py` 或注册为插件 |
| 使用 `@pytest.hookimpl` 但拼错钩子名 | 装饰器不生效，无警告 | 严格对照官方文档 |

* * *

### 💡 最佳实践建议

1.  **永远不要发明钩子名**：pytest 的钩子体系是封闭的，扩展应通过组合现有钩子或开发独立插件实现。
2.  **使用 `@pytest.hookimpl` 明确意图**：

    ```python
    @pytest.hookimpl(tryfirst=True)  # 优先执行
    def pytest_collection_modifyitems(config, items):
        ...
    ```

3.  **参数名必须一字不差**：pytest 底层使用 `pluggy` 按**参数名**匹配，不是按位置。
4.  **需要自定义行为时**：通过 `pytest_addoption` + 钩子组合实现，而非新建钩子。

> ✅ 验证钩子是否生效的快捷命令：
> `pytest --collect-only -q` 查看用例收集过程是否触发你的钩子逻辑。

如需某个具体钩子的完整参数签名、执行顺序图或企业级封装模板，可提供钩子名称，我为你拆解。
