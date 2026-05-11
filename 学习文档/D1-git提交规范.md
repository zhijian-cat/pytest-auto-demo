# Git 提交信息规范教程：Conventional Commits 完全指南

> 本教程基于行业广泛采用的 **Angular 提交规范（Conventional Commits）** 编写，适用于个人项目与团队协作。掌握后可大幅提升代码可维护性、自动化效率与协作体验。

* * *

## 🎯 教程导读

*   **适合人群**：Git 初学者、前端/后端开发者、DevOps 工程师、技术团队负责人
*   **学习目标**：掌握规范提交格式、熟练编写各类提交信息、配置团队模板与自动化校验
*   **阅读建议**：按顺序阅读 → 重点记忆 `类型表` 与 `格式模板` → 实战练习 → 配置团队规范

* * *

## 一、 为什么需要规范提交信息？

规范的提交信息不仅是“写给人看的注释”，更是**自动化工具的输入源**。

| 好处 | 说明 |
| :-- | :-- |
| 🔍 **快速定位** | 一眼看出本次提交属于功能、修复还是重构 |
| 🤖 **自动生成** | 工具可自动解析类型，生成 `CHANGELOG.md` 或发布说明 |
| 🤝 **规范协作** | 统一团队语言，降低沟通成本，Code Review 更高效 |
| 🎛️ **筛选过滤** | 可通过 `git log --grep` 快速过滤特定类型提交 |

```bash
# 示例：仅查看新功能提交
git log --oneline --grep="^feat"
```

* * *

## 二、 核心提交类型速查表

| 类型 | 英文全称 | 含义 | 示例 |
| :-- | :-- | :-- | :-- |
| `feat` | feature | 新增功能 | `feat: 添加用户登录功能` |
| `fix` | bug fix | 修复缺陷 | `fix: 修复登录超时问题` |
| `docs` | documentation | 文档更新 | `docs: 更新 README 安装说明` |
| `style` | code style | 代码格式（不影响逻辑） | `style: 统一缩进与分号` |
| `refactor` | refactor | 代码重构（功能不变） | `refactor: 优化用户验证逻辑` |
| `test` | testing | 测试用例增改 | `test: 添加登录模块单元测试` |
| `chore` | chore | 构建/工具/依赖配置 | `chore: 升级 eslint 依赖` |
| `perf` | performance | 性能优化 | `perf: 优化数据库查询语句` |
| `ci` | ci | CI/CD 配置修改 | `ci: 调整 GitHub Actions 缓存策略` |

💡 **提示**：`type` 必须为小写英文，且严格使用上述关键词。

* * *

## 三、 标准格式详解（Angular / Conventional Commits）

### 📐 基础格式（日常最常用）

```bash
<type>: <简短描述>
```

### 📐 完整格式（行业标准）

```bash
<type>(<scope>): <subject>

<body>

<footer>
```

| 字段 | 必填 | 说明 | 示例 |
| :-- | :-: | :-- | :-- |
| `type` | ✅ | 提交类型（见上表） | `feat`, `fix` |
| `scope` | ❌ | 影响范围（模块/文件/功能） | `auth`, `api`, `ui` |
| `subject` | ✅ | 简短描述（动词开头，≤50字符） | `添加JWT token认证` |
| `body` | ❌ | 详细描述（为什么改、怎么改） | 多行说明，用 `-` 列表 |
| `footer` | ❌ | 关联 Issue/破坏性变更 | `Closes #123`, `BREAKING CHANGE: ...` |

### 📝 完整示例

```bash
feat(auth): 添加JWT token认证

- 实现token生成和验证逻辑
- 添加登录/登出接口
- 增加token过期自动刷新机制

Closes #123
```

* * *

## 四、 实战操作指南

### 1️⃣ 单行提交（推荐日常使用）

```bash
git commit -m "feat: 添加pytest测试框架"
git commit -m "fix: 修复空指针异常"
git commit -m "docs: 添加环境搭建说明"
git commit -m "chore: 更新requirements.txt依赖"
git commit -m "perf: 优化pytest执行速度"
git commit -m "refactor: 重构fixture组织结构"
```

### 2️⃣ 多行提交（推荐复杂变更）

```bash
# 不带 -m 参数，Git 会自动打开默认编辑器
git commit

# 或在终端使用换行符（Windows CMD/PowerShell 用 ^，Linux/macOS 用 \）
git commit -m "feat(auth): 添加JWT认证" ^
  -m "- 实现token生成" ^
  -m "- 添加过期处理" ^
  -m "Closes #45"
```

* * *

## 五、 团队协作与自动化配置

### 🛠️ 1\. 设置全局提交模板

```bash
# 创建模板文件
touch ~/.gitmessage.txt

# 写入模板内容
cat > ~/.gitmessage.txt << 'EOF'
# <type>(<scope>): <subject>
# 类型：feat(新功能) | fix(修复) | docs(文档) | style(格式)
#       refactor(重构) | test(测试) | chore(工具) | perf(性能) | ci(CI配置)
# 示例：feat(auth): 添加登录接口
# 
# <body>（可选，详细说明变更原因与实现方式）
# 
# <footer>（可选，关联Issue或破坏性声明）
EOF

# 应用全局配置
git config --global commit.template ~/.gitmessage.txt
```

### 🤖 2\. 推荐自动化校验工具链

| 工具 | 作用 | 安装命令 |
| :-- | :-- | :-- |
| `commitlint` | 校验提交信息格式 | `npm i -D @commitlint/cli @commitlint/config-conventional` |
| `husky` | Git Hooks 管理 | `npx husky-init && npm install` |
| `standard-version` | 自动生成 CHANGELOG & 版本号 | `npm i -D standard-version` |

> ✅ 配置后，不符合规范的提交将被拦截，从源头保证团队一致性。

* * *

## 六、 规范格式 vs 普通格式对比

| ❌ 普通格式（不推荐） | ✅ 规范格式（推荐） | 问题剖析 |
| :-- | :-- | :-- |
| `修改了代码` | `feat: 添加用户登录功能` | 模糊，无法判断变更性质 |
| `修复问题` | `fix: 修复token过期bug` | 无范围/无具体描述，排查困难 |
| `更新文档` | `docs: 更新API接口说明` | 缺乏模块指向性 |
| `改bug` | `fix: 处理除零异常` | 口语化，不符合工程规范 |
| `优化了一下` | `perf: 优化数据库查询索引` | 无法量化，难以追踪 |

* * *

## 七、 总结与速记口诀

### 📌 核心模式

```bash
feat: 添加xxx功能
fix: 修复xxx问题
docs: 更新xxx文档
refactor: 重构xxx逻辑
test: 补充xxx测试
chore: 维护xxx配置
```

### 🧠 速记口诀

> **类型打头阵，冒号隔描述；**
> **范围可省略，详情换行补；**
> **关联Issue号，规范不迷路。**

* * *

## 🛠️ 附录：常见问题 FAQ

| 问题 | 解答 |
| :-- | :-- |
| `scope` 一定要写吗？ | 非必填。小项目可省略，中大型项目建议写明模块名（如 `api`, `ui`, `db`） |
| 中文描述可以吗？ | 可以。Conventional Commits 不限制语言，但建议团队统一（推荐中文或英文） |
| 提交后写错了怎么办？ | `git commit --amend` 修改最后一次提交信息（未推送前） |
| 如何查看历史规范提交？ | `git log --oneline --grep="^feat|^fix"` |

* * *

📄 **文档版本**：v1.0｜🔄 **适用标准**：Conventional Commits 1.0.0
💡 建议将此文档保存至团队 Wiki 或项目 `CONTRIBUTING.md` 中，作为新人入职必读规范。