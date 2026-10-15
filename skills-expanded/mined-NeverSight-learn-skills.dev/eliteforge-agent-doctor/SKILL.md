---
name: eliteforge-agent-doctor
description: 检查开发环境是否配置完成；未完成时先确认重庆/北京办公地，识别当前操作系统、系统工具、包管理器和 eliteforge-* skill 环境变量声明，并按 missing_required、missing_conditional、optional_unset 分类报告，再尝试自动安装必备命令并补齐 hosts、Git 全局配置、Git HTTPS、npm/pip 私有源与 pipx 包。用户提到"检查环境配置""准备开发环境""缺少命令/hosts/私有源/Git配置/包管理工具/skill环境变量"时使用。
metadata:
  version: 1.0.1
---

# EliteForge Agent Doctor

## 目标

只做一件事：判断当前机器能否继续执行相关开发任务；如果不能，就基于当前系统已有能力尽量自动补齐。

## 基础版本要求

- Java/Javac：主版本必须为 25 或以上。
- Maven：必须为 3.9.10 或以上。

## 必须先确认

在写入 hosts 前，必须问清用户的办公地：

- 重庆办公：使用 `references/cq-required-hosts.txt`，脚本参数为 `--office cq`
- 北京办公：使用 `references/bj-required-hosts.txt`，脚本参数为 `--office bj`

如果用户没有确认办公地，只允许做诊断和非 hosts 修复，不要猜测 hosts 配置。

## 工作流

1. 先确认用户是重庆办公还是北京办公。

2. 运行 `report` 模式，只诊断不写入。`report` 返回码为 `2` 表示环境未就绪，不代表脚本异常。

```bash
python3 scripts/bootstrap_env.py --mode report --office cq
python3 scripts/bootstrap_env.py --mode report --office bj
```

3. 如果报告显示环境不完整，向用户确认是否自动修复后，运行 `apply` 模式。

```bash
python3 scripts/bootstrap_env.py --mode apply --office cq
python3 scripts/bootstrap_env.py --mode apply --office bj
```

4. 如果自动安装被系统权限阻塞，报告缺失项和需要用户处理的权限条件。不要伪造安装成功。

5. 只有后续任务确实要操作内部平台时，才安装内部 CLI。

```bash
python3 scripts/bootstrap_env.py --mode apply --office cq --install-internal-clis
```

6. 修复后再运行一次 `report`，输出最终状态。

## 脚本负责的内容

- 识别系统信息：操作系统、平台、架构、Shell、PATH、home 目录、hosts 文件路径。
- 识别系统工具：`git`、`python3`、`node`、`npm`、`npx`、`pipx`、`jq`、`rg`、`mvn`、`pnpm`、`java`、`javac`、`curl`、`wget`、`sudo` 等。
- 识别 SDKMAN 与包管理器：SDKMAN、`brew`、`apt-get`、`dnf`、`yum`、`pacman`、`zypper`、`winget`、`choco`。
- 默认只扫描每个 `skills/eliteforge-*/SKILL.md` 顶层文件中的 `## Environment Variables` 章节，并按 `eliteforge-skill-spec` 规定的 `` `ELITEFORGE_SKILL_<ABBR>_<PURPOSE>` [optional|required|conditional] desc `` 格式识别 skill 环境变量；只报告变量名和缺失状态，不打印变量值。
- 尝试安装必备命令：`git`、`python3`、`node`、`npm`、`npx`、`pipx`、`jq`、`rg`、`pnpm`、Java/Javac 25 及以上、Maven 3.9.10 及以上。
- 自动安装 Java/Javac 与 Maven 时，若当前机器已安装并可初始化 SDKMAN，必须优先通过 SDKMAN 安装；SDKMAN 不可用或安装失败时，再退回系统包管理器。
- 通过 `pipx` 安装必备 Python CLI 包：`pre-commit`。
- 配置 `~/.npmrc` 的 npm 私有源。
- 配置 `~/.pip/pip.conf` 的 pip 私有源。
- 检查 Git 全局配置：
  - `user.name` 必须已配置且不能是占位符；建议使用个人中文姓名，但不以中文字符作为就绪门禁。
  - `user.email` 必须已配置且不能是占位符；建议使用有效的公司邮箱。
  - `init.defaultBranch=master`
  - `color.ui=auto`
  - `pager.branch=false`
  - `pager.status=false`
  - `core.quotePath=false`
  - `http.https://git.cisdigital.cn.proxy=` 空值
- 把 `git.cisdigital.cn` 的 SSH 地址重写为 HTTPS。
- 按已确认办公地维护 `/etc/hosts`。

## 安全规则

- 不要把密码、Token、共享凭据硬编码、提交入仓或直接打印。
- 私有源凭据以在线“必知必会”文档为准，脚本只维护非敏感的源地址配置，不要求也不读取本地私有源凭据环境变量。
- Git 个人身份配置必须由用户手动执行 `git config --global user.name "你的姓名"` 与 `git config --global user.email "公司邮箱"` 完成；脚本不自动写入。`user.name`/`user.email` 的就绪判断以"已配置且非占位符"为准；非中文姓名或非标准邮箱只作为建议提示，不作为阻塞项。
- 需要私有源认证信息时，提示用户按在线“必知必会”文档自行写入本地配置；不要要求用户在对话中明文发送密码或 Token。
- 如果 `/etc/hosts` 中同一域名已指向其他 IP，不要覆盖，必须报告冲突。
- 写 hosts 只维护脚本标记块，不要清空用户已有内容。
- 系统安装和 hosts 写入只做“可自动完成”的尝试；需要交互式 sudo、管理员权限、账号开通或项目授权时，报告阻塞。
- `git.cisdigital.cn` 优先使用 HTTPS，禁止要求用户改用 SSH 克隆。

## 脚本参数

- `--mode report|apply`：`report` 只检查；`apply` 写入安全修复并尝试安装缺失依赖。
- `--office cq|bj`：必填业务参数，由用户确认；重庆用 `cq`，北京用 `bj`。
- `--package-manager auto|brew|apt-get|dnf|yum|pacman|zypper|winget|choco`：自动探测不准时强制指定。该参数只控制系统包管理器回退路径；Java/Javac 与 Maven 仍优先尝试 SDKMAN。
- `--home-dir` 与 `--hosts-file`：可指向临时路径做验证，不污染真实机器。
- `--skills-root`：指定 `eliteforge-*` skill 所在目录；默认按脚本位置推断为仓库 `skills` 目录。
- `--skip-install`：跳过工具安装，但仍应用配置文件修复。
- `--install-internal-clis`：通过 `pipx` 安装或升级内部 Python CLI。

## 输出规则

- 汇总要短、可执行，至少覆盖：`system`、`SDKMAN`、`package manager`、`tools`、`hosts`、`npm/pip mirrors`、`git global config`、`git https rewrite`、`pipx packages`、`skill_env_vars`、`remaining blockers`。
- 如果运行了 `apply`，必须明确说明改了哪些文件、执行了哪些安装命令、哪些项被权限或账号阻塞。
- `skill_env_vars` 必须拆分报告 `missing_required`、`missing_conditional`、`optional_unset` 三类；只有 `missing_required` 与已触发的 `missing_conditional` 是环境就绪阻塞项。
- 如果 `skill_env_vars.missing_required` 或 `skill_env_vars.missing_conditional` 非空，必须提示用户配置对应环境变量；不要要求用户在对话中明文发送密码或 Token。
- 对仍需人处理的事项，指出具体条件或文件，不要整段转抄参考资料。

## 参考资料

- `references/onboarding-checklist.md`：人类前置项、私有源凭据、安全边界。
- `references/cq-required-hosts.txt`：重庆办公 hosts。
- `references/bj-required-hosts.txt`：北京办公 hosts。
