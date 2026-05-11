## 🛠 阶段一：环境配置与身份认证

### 1\. 配置 Git 提交身份

```bash
git config --global user.name "你的GitHub用户名"
git config --global user.email "你的GitHub注册邮箱"
```

🔍 **指令深度解析**

| 组件 | 说明 |
| --- | --- |
| **作用** | 设置全局提交者信息，所有 `commit` 都会携带此身份 |
| `--global` | 作用于用户级配置文件 `~/.gitconfig`。若省略，则仅作用于当前仓库的 `.git/config` |
| `user.name/email` | Git 分布式架构无中央服务器，需靠此字段追溯代码归属与生成贡献图 |

### 2\. 生成 SSH 密钥（推荐）

```bash
ssh-keygen -t ed25519 -C "你的GitHub注册邮箱"
```

🔍 **指令深度解析**

| 组件 | 说明 |
| --- | --- |
| **作用** | 生成非对称加密密钥对（私钥留本地，公钥传 GitHub） |
| `-t ed25519` | 指定加密算法。`ed25519` 比传统 `rsa` 更安全、更快、密钥更短 |
| `-C "邮箱"` | 添加注释标签，仅用于标识密钥来源，不影响加密逻辑 |
| **交互提示** | 连续按 3 次回车：① 默认保存路径 `~/.ssh/` ② 不设置密码短语 ③ 确认 |

### 3\. 查看并复制公钥

```bash
# macOS/Linux
cat ~/.ssh/id_ed25519.pub
# Windows (CMD/PowerShell)
type %USERPROFILE%\.ssh\id_ed25519.pub
```

🔍 **指令深度解析**

*   `cat` / `type`：读取文件内容并输出到终端
*   `~/.ssh/`：Linux/macOS 家目录下的隐藏 SSH 配置文件夹
*   `%USERPROFILE%\.ssh\`：Windows 用户目录下的等效路径
*   ⚠️ **注意**：仅复制 `.pub`（公钥）文件内容，**绝对不要泄露私钥**（无后缀文件）

### 4\. 验证 SSH 连通性

```bash
ssh -T git@github.com
```

🔍 **指令深度解析**

| 组件 | 说明 |
| --- | --- |
| **作用** | 测试本地私钥能否通过 GitHub 公钥验证 |
| `-T` | 禁用伪终端分配。GitHub SSH 不提供 Shell 交互，加 `-T` 可避免 `PTY allocation request failed` 警告 |
| `git@github.com` | GitHub 的 SSH 服务入口，固定格式 |
| **成功标志** | `Hi 用户名! You've successfully authenticated...` |

* * *

## 🌐 阶段二：GitHub 创建仓库

1.  登录 GitHub → 右上角 `+` → `New repository`
2.  关键配置：
    *   ✅ `Add a README file`：**必选**。自动生成首次提交，避免空仓库导致默认分支名混乱。
    *   ✅ `Add .gitignore` → 选 `Python`。自动忽略 `__pycache__/`、`.venv/` 等垃圾文件。
    *   `License`：开源项目必选（如 MIT），声明代码使用权限。

* * *

## 📥 阶段三：克隆到本地

```bash
git clone git@github.com:你的用户名/python-data-analysis.git
cd python-data-analysis
```

🔍 **指令深度解析**

| 组件 | 说明 |
| --- | --- |
| **作用** | 完整下载远程仓库到本地，并初始化工作区 |
| `git clone <URL>` | 执行三件事：① 下载 `.git` 目录（完整历史） ② 创建同名文件夹 ③ **自动绑定远程别名 `origin`** |
| `cd` | 切换工作目录。后续所有 Git 命令必须在此目录下执行 |
| ⚠️ **注意** | 克隆后 **无需** 再执行 `git remote add`，否则会导致 `remote origin already exists` 报错 |

* * *

## 💻 阶段四：VSCode 打开项目 & 虚拟环境配置

### 1\. 创建虚拟环境

```bash
python -m venv .venv
```

🔍 **指令深度解析**

| 组件 | 说明 |
| --- | --- |
| **作用** | 创建隔离的 Python 运行环境，避免依赖冲突 |
| `-m venv` | `-m` 表示以脚本方式运行标准库模块 `venv` |
| `.venv` | 目标文件夹名。以 `.` 开头表示隐藏目录，符合行业惯例 |
| **为什么必须用？** | ① 隔离项目依赖 ② 避免污染系统 Python ③ 通过清单文件可跨设备重建环境 |

### 2\. VSCode 绑定解释器

*   `Ctrl+Shift+P` → 输入 `Python: Select Interpreter` → 选择含 `.venv` 路径的解释器
*   **验证命令**：

    ```bash
    python -c "import sys; print(sys.executable)"
    ```

🔍 **指令深度解析**

*   `python -c "代码"`：直接在命令行执行 Python 代码，不进入交互模式
*   `sys.executable`：返回当前 Python 解释器的绝对路径，用于确认是否真正使用了虚拟环境

### 3\. 激活环境 & 安装依赖

```bash
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install pandas numpy matplotlib
pip freeze > requirements.txt
```

🔍 **指令深度解析**

| 命令 | 说明 |
| --- | --- |
| `activate` / `source` | 修改当前终端的 `PATH` 环境变量，使 `python`/`pip` 指向 `.venv` 内部 |
| `pip install` | 从 PyPI 下载并安装指定包到当前激活的环境 |
| `pip freeze` | 输出当前环境已安装包的精确版本（格式：`包名==版本号`） |
| `> requirements.txt` | Shell 重定向符号。将 `freeze` 的输出写入文件，若文件存在则覆盖 |

### 4\. 配置 `.gitignore`（关键！）

在项目根目录打开 `.gitignore`，确保包含：

```gitignore
.venv/
__pycache__/
*.pyc
*.pyo
```

💡 **底层逻辑**：`.gitignore` 是 Git 的过滤规则文件。匹配到的文件**永远不会被 `git add` 跟踪**，从而避免提交体积庞大、跨平台不兼容的虚拟环境目录。

* * *

## 📝 阶段五：VSCode 编写代码 & Git 状态管理

1.  创建/编辑文件（如 `main.py`）
2.  点击左侧 **源代码管理** 图标（`Ctrl+Shift+G`）
3.  状态标识：
    *   🔴 `U` (Untracked)：新文件，Git 未跟踪
    *   🟡 `M` (Modified)：已跟踪文件被修改
    *   🟢 `A` (Staged)：已加入暂存区，准备提交
    *   ⚪ 无标记：已提交，与远程同步

* * *

## 🔗 阶段六：连接远程仓库验证

```bash
git remote -v
```

🔍 **指令深度解析**

| 组件 | 说明 |
| --- | --- |
| **作用** | 查看当前仓库绑定的远程仓库地址 |
| `remote` | 管理远程仓库的子命令 |
| `-v` | `--verbose` 的缩写，显示完整 URL 及 `fetch/push` 权限 |
| **正常输出** | `origin git@github.com:用户名/仓库.git (fetch/push)` |
| ⚠️ **仅当本地先 `git init` 时才需手动连接**：`git remote add origin <URL>` |  |

* * *

## 🚀 阶段七：提交与推送代码

### 1\. 暂存更改

```bash
git add .
```

🔍 **指令深度解析**

*   **作用**：将工作区变动移入暂存区（Staging Area）
*   `.`：表示当前目录及所有子目录。Git 会递归扫描，**自动跳过 `.gitignore` 匹配的文件**
*   💡 替代方案：`git add 文件名` 精准控制单个文件

### 2\. 提交到本地仓库

```bash
git commit -m "feat: 初始化数据分析环境，添加依赖"
```

🔍 **指令深度解析**

| 组件 | 说明 |
| --- | --- |
| **作用** | 将暂存区内容打包为不可变快照，生成唯一 Hash ID |
| `-m` | `--message` 缩写。允许直接在命令行输入提交信息，避免打开默认文本编辑器 |
| **提交规范** | `类型: 描述`（如 `feat:`新功能、`fix:`修复、`docs:`文档、`refactor:`重构） |

### 3\. 推送到远程

```bash
git push -u origin main
```

🔍 **指令深度解析**

| 组件 | 说明 |
| --- | --- |
| **作用** | 将本地提交同步到 GitHub |
| `-u` | `--set-upstream` 缩写。**建立本地分支与远程分支的追踪关系**。首次使用后，后续只需 `git push` |
| `origin` | 远程仓库的默认别名（克隆时自动创建） |
| `main` | 分支名。GitHub 默认主分支已从 `master` 改为 `main` |
| ⚠️ **注意** | 若远程有更新未拉取，推送会报 `rejected`。需先执行 `git pull origin main` |

* * *

## 📊 核心指令参数速查表

| 指令 | 关键参数 | 用途 | 常见替代/补充 |
| --- | --- | --- | --- |
| `git config` | `--global` | 用户级配置 | 省略则仅作用于当前仓库 |
| `ssh-keygen` | `-t ed25519` | 指定现代加密算法 | `-t rsa -b 4096`（旧标准） |
| `git clone` | `<URL>` | 下载仓库+自动配远程 | `--depth 1` 仅拉最新提交（提速） |
| `python -m venv` | `.venv` | 创建隔离环境目录 | `virtualenv`（第三方，更快） |
| `pip freeze` | `> req.txt` | 导出依赖清单 | `pip list --format=freeze` |
| `git add` | `.` | 暂存当前目录所有变更 | `git add -p` 交互式暂存代码块 |
| `git commit` | `-m "msg"` | 内联提交信息 | 省略 `-m` 会打开编辑器 |
| `git push` | `-u origin main` | 首次推送+建立追踪 | 后续直接 `git push` |
| `git rm` | `--cached` | 仅从 Git 索引移除，保留本地文件 | 修复误提交 `.gitignore` 文件必用 |

* * *

## 🛡 最佳实践与高频避坑

### ✅ 必做习惯

1.  **项目初始化顺序**：克隆 → 建虚拟环境 → 配 `.gitignore` → 装依赖 → 生成清单 → 写代码
2.  **提交前自检**：`git status` 确认无 `.venv/`、`__pycache__/`、`.env` 等敏感文件
3.  **推送前同步**：`git pull origin main --rebase` 避免冲突（团队协作必做）
4.  **VSCode 设置同步**：登录 GitHub 账号开启 `Settings Sync`，跨设备保持插件/主题一致

### 🐛 高频问题根因与解法

| 现象 | 根因 | 精准解法 |
| --- | --- | --- |
| `ModuleNotFoundError` | VSCode 未使用虚拟环境解释器 | `Ctrl+Shift+P` → `Python: Select Interpreter` → 选 `.venv` |
| 终端不显示 `(.venv)` | 未激活或终端未继承环境 | 终端右上角 `+` 新建终端，或检查 `python.terminal.activateEnvironment` |
| `.gitignore` 不生效 | 文件已被 Git 历史跟踪 | `git rm -r --cached .venv/` → `git add .` → `git commit -m "fix: 忽略虚拟环境"` |
| `git push` 报 `rejected` | 远程有新提交未拉取 | `git pull origin main` 合并后再推 |
| SSH 报 `Permission denied` | 私钥权限错误或未添加公钥 | `chmod 600 ~/.ssh/id_ed25519` → 重新添加公钥到 GitHub |

* * *

## 🗺 完整流程速查图

```
GitHub 创建仓库 (README + .gitignore)
        ↓
终端: git clone <SSH链接> → cd 项目目录
        ↓
VSCode 打开文件夹 → python -m venv .venv
        ↓
VSCode: Python: Select Interpreter → 选 .venv
        ↓
激活环境 → pip install xxx → pip freeze > requirements.txt
        ↓
编写代码 → VSCode 源代码管理: + 暂存 → 填写信息 → ✓ 提交
        ↓
终端/VSCode: git push -u origin main (首次) → 后续 git push
        ↓
GitHub 刷新，代码已同步 ✅

```

按照此流程操作，你将获得一个**指令透明、环境隔离、依赖清晰、版本可控**的标准化开发工作流。所有命令均已拆解至参数级，可直接作为日常开发手册使用。如需针对特定语言（Node.js/Java/Go）或进阶场景（分支策略/冲突解决/PR 流程）输出定制指南，可随时告知。