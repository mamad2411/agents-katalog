---
name: repo-push-readiness
description: 把本地仓库推向远端（尤其多机协作）前的就绪体检。当用户说「要推远端/多机合作/开源/首次 push/加 remote/换台机器继续」时使用。逐项检查密钥与凭据泄露、大文件、gitignore 正确性、换行符与二进制声明、协作资产是否入库，并给出可执行的修复动作。核心不是写 .gitignore，而是「先扫真相、再改规则、最后验证」——凭据进了历史就得洗，规则写错只是噪音。
agent_created: true
task_type: dev.repo_push_readiness
---

# 仓库推送就绪体检

## 何时用

- 用户说「要推远端」「多机合作」「开源」「首次 push」「加个 remote」
- 换台机器/换人接手前，确认仓库能独立复现
- 仓库长期只在本机用，现在要给别人

**不适用**：已经在协作的仓库日常 push（那是常规 CI 流程的事）。

## 核心原则

1. **先扫真相，再改规则**。不要一上来就写 .gitignore —— 先查清楚现在到底有什么在库里。
2. **凭据泄露是可逆的但很贵**。密钥一旦进过 git 历史，删文件不够，得 `filter-repo`。所以这一步要最严格。
3. **规则改动要控制爆炸半径**。加 `* text=auto` 会重写整个工作区；加 `.gitattributes` 只声明例外则零影响。
4. **区分「必须修」与「看场景」**。密钥必须修；真实账号 ID / 弱密钥属于"私有仓库可留、公开仓库必修"。

---

## 步骤

### 第 0 步 · 摸清现状

```bash
git remote -v                     # 有没有远端？没有则用户是要"首次配置"
git log --oneline -5              # 当前基线
git status --short                # 必须先干净，否则查不准
du -sh .git                       # 仓库本体体积
git ls-files -z | xargs -0 du -ch 2>/dev/null | tail -1   # 入库文件总体积
```

**不要跳过 `git status`**：未提交的改动不在 `git grep` 的范围里（`git grep` 只搜已跟踪文件），会漏检。

### 第 1 步 · 凭据扫描（最重要）

通用模式扫描：

```bash
# 64 位十六进制（密钥、token 常见形态）
git grep -nIE "\b[0-9a-f]{64}\b" -- . | grep -vE "\.lock:|uv\.lock|package-lock"

# 常见前缀/形态
git grep -nIE "(sk-|ghp_|gho_|AKIA|eyJ[A-Za-z0-9_-]{10,}|-----BEGIN [A-Z ]*PRIVATE KEY-----)" -- .

# 32/40 位十六进制（弱一点的密钥、MD5/SHA1 指纹）
git grep -nIE "\b[0-9a-f]{32}\b|\b[0-9a-f]{40}\b" -- . | grep -vE "\.lock:|uv\.lock"
```

**关键技巧：用已知的真实值反查，比通用模式准得多。**

如果你知道项目里用过的真密钥/真 ID，直接搜它：

```bash
git grep -nI "<真实密钥或账号ID>" -- .
```

通用模式会漏掉非十六进制的凭据（如 base64、自定义格式），也可能淹没在 lock 文件的哈希里。
**两者都要做**：先通用扫（发现未知），再精确扫（确认已知）。

命中后的判定分级：

| 级别 | 例子 | 处理 |
|---|---|---|
| P0 必须修 | 数据库密钥、API token、私钥 | 改代码/文档 + 若已进历史则 `filter-repo` |
| P1 看场景 | 真实账号 ID、弱密钥（只解部分数据）、内网地址 | 私有仓库可留，公开仓库必修 |
| P2 噪音 | lock 文件的包哈希、示例/测试假值 | 忽略 |

**P2 的识别**：出现在 `*.lock`、测试文件、`example`/`mock`/`fake`/`YYYY` 上下文里的，基本都是假值。

### 第 2 步 · 大文件与目录检查

```bash
# 大于 1M 的入库文件
git ls-files -z | xargs -0 du -h 2>/dev/null | sort -rh | head -20

# 找已被跟踪但本该忽略的
git ls-files | grep -iE "\.(db|sqlite|log|zip|7z|exe|dll|pth|onnx|pt|bin)$"
```

常见遗漏：产物目录（`output/` `dist/` `build/`）、缓存（`__pycache__` `.pytest_cache`）、
本地配置（`*.local.json`）、导出的数据库。

### 第 3 步 · 验证忽略规则

**不要只看 `.gitignore` 写了什么，要验证它真的生效**：

```bash
git check-ignore -v <该被忽略的路径>       # 有输出 = 被忽略，且会告诉你是哪条规则
```

对被忽略的关键路径逐条验证。这一步能抓出"看起来写了但被 `!` 反向规则覆盖"的情况。

**注意 gitignore 的陷阱**：
- `dir/` 忽略目录，`dir` 忽略目录或文件
- `!` 取反只对"父目录未被忽略"的文件有效
- 有 `.gitkeep` 但整个目录被忽略 = 目录存在但内容不入库（这是模板常见设计，要确认是否符合意图）

### 第 4 步 · 换行符与二进制声明

```bash
ls .gitattributes 2>/dev/null || echo "无 .gitattributes"
git config --get core.autocrlf
git ls-files --eol | awk '{print $1, $2}' | sort | uniq -c    # 分布是否一致
git ls-files --eol -- '*.bat' '*.sh'                          # 平台相关脚本
```

**`git ls-files --eol` 的读法**：`i/<eol>` 是索引里的，`w/<eol>` 是工作区的。
`i/lf w/crlf` 是 Windows + `autocrlf=true` 的正常状态。

需要 `.gitattributes` 的信号：
- 有 `.bat` / `.cmd`（必须 CRLF，LF 在部分 cmd.exe 场景解析失败）
- 有 `.sh`（必须 LF，Windows checkout 成 CRLF 后无法执行）
- 有二进制文件被当文本（看 `attr/` 列为空且 diff 异常）

**关键：不要写 `* text=auto`**。会按新规则重写整个工作区，制造巨大无意义的 diff。
（**例外**：全新仓库、或已决定全库统一的情况——此时写 `* text=auto eol=lf` 是好的，
因为它让 index 一次到位；本机 spotlight 项目就是这么做的。）
**只声明必须偏离默认的**：

```gitattributes
*.bat text eol=crlf
*.cmd text eol=crlf
*.sh text eol=lf
*.png binary
*.db binary
# ... 按项目实际补
```

写完验证爆炸半径：

```bash
git add .gitattributes && git status --short | wc -l    # 看有没有一堆文件冒出来
```

**⛔ 批量改换行的唯一安全做法（2026-10-04 本机踩过）**：

**不要自己写脚本 `data.replace(b"\r\n", b"\n")`** —— **二进制文件里也含 `0x0D 0x0A`**。
实测把工具链的 `gdmcp.exe`（4.6 MB）改坏：`MZ` 头还在、`git status` 也看不出来，
但内容已经损坏。同类高风险的还有 `.png` / `.zip` / `.pyd`。

```bash
git checkout -- .                # 正解①：工作区回到 index 字节，git 按 eol= 属性写出
git add --renormalize .          # 正解②：历史已提交且要统一行尾时
```

判据：**只动 `git check-attr text` 为 `set` / `auto` 的文件**；为 `unset`（binary）的一律跳过。
另：`git ls-files` 对**非 ASCII 路径会加双引号**，脚本里用 `git ls-files -z` 按 `\0` 读，
否则会拼出 `"docs/<中文文件名>.md"` 这种带引号的假路径。

**`w/crlf` 但 `i/lf` 且 `git status` 干净**是正常状态（文件是拷进来的、没走过 checkout）——
想统一就让 `git checkout -- .` 写一遍，不要手改字节。

### 第 5 步 · 协作资产是否入库

多机协作最怕「A 机踩过的坑 B 机再踩一遍」。检查这些是否入库：

- Agent 记忆（`.agents/memory/` `.claude/memory/` 等）—— 跨会话结论
- 未完成任务留档（`wip/`）—— 中断交接
- Skill / 规则定义 —— 工作流
- 设计与决策文档（`docs/`）—— 为什么这么做
- 环境自检脚本 —— 「怎么验证它是对的」

**这些常被 gitignore 掉**（模板默认排除），因为单人开发时不重要。
多机协作时它们是最有价值的资产，值得专门确认一次。

**但入库前必须脱敏**：这些文件最常含密钥（本地路径、账号、调试时的密钥粘贴）。
先过第 1 步的扫描，再放开 gitignore。

### 第 5.5 步 · 断链检查（**最容易漏，代价最大**）

第 5 步查的是「协作资产有没有入库」，这一步查的是**「下一个任务依赖的输入在不在库里」**。

换个说法：**假设对方 clone 下来要接着做下一步，他需要的东西齐吗？**

做法是把「待办清单」逐条拆成输入依赖，然后反查每个输入在哪：

```bash
# 对每个待办，问：它的输入是什么？输入在哪？被 ignore 了吗？
git check-ignore -v <输入路径>      # 有输出 = 对方拿不到
```

典型断链（都真实发生过）：

| 断链 | 表现 |
|---|---|
| 研究产出 / 调研结论在 `temp/` | `temp/` 常年被 gitignore。对方只有代码，没有"为什么这么写" |
| 待办依赖的规范文档、数据表、脚本在本地临时目录 | 下一步直接无法开工，等于从零重做 |
| 只入库了「生产代码」，没入库「怎么验证」 | 对方不知道通过标准，只能猜 |
| 密钥台账/配置文件 | ⚠️ 这类**不能直接入**——先脱敏（见第 1 步），或只入"结构说明 + 指纹" |

**判定标准**：把待办里最靠前的那一条，交给一个只有这份仓库的人 —— 他能不能独立开工？
不能就是断链。

> 这一步要**在第 5 步之后做**：先确认常规资产，再逐条对照待办。顺序反了容易只补常规项就收工。

### 第 6 步 · 基线自检

```bash
<项目的测试命令>          # pytest / npm test / go test ./...
<项目的自检脚本>          # 如果有 scripts/verify_*.py 这类
```

**通过标准**：测试全绿 + 工作区干净。测试不过说明仓库处于中间状态，不适合作为协作起点。

### 第 7 步 · 出报告

给用户的报告要包含：

1. **现状**：有无 remote、当前 HEAD、体积
2. **风险分级**：P0/P1/P2 各命中了什么
3. **已修 vs 待决策**：我直接改了什么（无争议的），什么是需要用户拍板的（场景相关）
4. **推送前仍需做的**：剩余动作清单

### 第 8 步 · 建仓 + 推送 + 克隆验证

前七步都是"查"，这一步是"做"。**做完必须克隆验证**——这是"对方能接手"的唯一可信证据。

**8.1 建远端**（有 gh 时最快）：

```bash
gh auth status                                    # 确认已登录、有 repo scope
gh repo create <名字> --private --description "..."   # 先建空仓，不与本地关联
# 或一步到位：gh repo create <名字> --private --source=. --remote=origin --push
```

**8.2 让 git 用 gh 的凭据**（否则 push 可能弹交互窗）：

```bash
gh auth setup-git      # 写入 credential.https://github.com.helper = !gh auth git-credential
git config --global --get-regexp credential      # 验证写入成功
```

> 本机有多套 git 时（PortableGit + 自装 Git），**PATH 里前置要用哪套就在前置后跑 setup-git**，
> 否则配置写到另一套的全局配置里，push 时仍弹窗。

**8.3 加入 remote 并推**：

```bash
git remote add origin <url>
git push -u origin <分支>
gh repo edit --default-branch <分支>     # 本地分支名不是 main 时，别忘了设默认分支
```

**8.4 克隆验证（不可跳过）**：

```bash
cd <临时目录> && git clone --depth 1 <url> _clone_verify && cd _clone_verify
git ls-files | wc -l                      # 与本地对比，数量应一致
for f in <关键资产清单>; do [ -e "$f" ] || echo "✗ 缺失 $f"; done
for d in output temp logs .venv; do [ -e "$d" ] && echo "⚠️ 泄漏 $d"; done
git grep -nIE "\b[0-9a-f]{64}\b" -- . | grep -v uv.lock    # 密钥复扫
```

然后**用克隆副本的源码跑测试**（依赖可以借用本机已装好的环境）：

```bash
# src-layout 项目：PYTHONPATH 指向克隆的 src，解释器用本机装好依赖的 venv
PYTHONPATH="<绝对路径>/_clone_verify/src" <本机venv>/python.exe -m pytest tests/ -q
```

**这一步的价值**：它同时验证了「文件真的推上去了」「忽略规则真的生效」
「代码在干净环境下能跑」三件事。前面所有检查都只是"应该没问题"，这一步是实证。

验证完删掉临时副本。

### 第 8.5 步 · 首次推送的三个高频陷阱

**① `.gitignore` 中间含斜杠的模式会锚定到仓库根 —— 会漏排除几十个文件**

`addons/foo/` 这种**中间带斜杠**的模式，git 视为相对于 `.gitignore` 所在目录（通常就是仓库根），
**匹配不到** `game/addons/foo/`。必须加 `**`：

```gitignore
**/addons/foo/         # ✅ 任意深度
_toolchain/**/data/    # ✅
```

规律：只有**不带斜杠**（`node_modules`）或**仅末尾带斜杠**（`.godot/`）才匹配任意层级。
验证：`git status --short --untracked-files=all | grep -c "<本该排除的路径>"` 必须为 0。

**② 嵌套的 `.git` 会变成 gitlink —— 只有引用、内容不入库**

工作区里放了**另一个 git 仓库的副本**（工具链、参考项目、vendor 来的子项目）时，
主仓库只记录一个 commit 引用（mode `160000`）。**`git status` 完全看不出来**，
但别人 clone 下来那个目录是空的 —— 最难发现的故障。

```bash
find . -maxdepth 4 -name .git                        # 找嵌套仓库
git ls-files -s | awk '$1=="160000"{print $4}'        # 列 gitlink，应为空
# 信号：git add 时出现 "adding embedded git repository" 警告
```

处理二选一：**移走内层 `.git`**（`mv` 到 temp 而非 `rm`，可恢复）让它扁平入库；
或 `git submodule add` 保留上游关联。
⚠ 扁平化后**内层 `.gitignore`/`.gitattributes` 仍生效于该子树** ——
先 `cat` 一遍确认不会误排要入库的文件（好处是内层规则如 `*.bat eol=crlf` 会保住）。

**③ push 报 `Recv failure: Connection was reset`（小请求正常、大流量被掐）**

`git ls-remote` 能通但 `push` 失败 ⇒ 不是鉴权/网络不通，是**传输中断**：

```bash
git config --local http.version HTTP/1.1       # HTTP/2 在部分网络/中间设备下不稳
git config --local http.postBuffer 524288000   # 默认 1M，超了走 chunked 易被掐
git config --local http.lowSpeedLimit 0        # 别因短暂低速自行中断
git config --local http.lowSpeedTime 999999
```

⚠ **这是本机网络环境的临时故障，不要固化成项目约定**。
`--local` 写进 `.git/config` 只影响这一个仓库副本、不进任何提交，但仍属本机状态；
**更不要写进项目共享文档或项目记忆** —— 别人机器上不需要那两项，写进去就是污染
（而且绝对化的"别删"会把一次网络波动包装成行业规范，比不写更糟）。
先重试一两次往往就好，确认频繁复现再考虑固化为本机全局配置。

---

## 修复动作速查

**密钥进了已提交的文件**（未进历史）：

```bash
# 改文件内容 → 提交
```

**密钥进了 git 历史**（已 push 或已多个提交）：

```bash
# 用 git-filter-repo（比 filter-branch 快且不易错）
git filter-repo --replace-text replacements.txt   # 格式: 旧字符串==>新字符串
# ⚠️ 会重写历史，所有协作者必须重新 clone
```

**在代码里打印密钥**：

```python
# 反例
logger.error(f'key error: {key}')
# 正例：用脱敏属性
logger.error(f'key error: {info.masked_key}')
```

**把密钥写进文档/记忆**：

用不可逆指纹代替 —— `sha256(key)[:16]`。
足以判断"还是不是同一把钥"，且原文可以从原始来源重新获取。

**换行符噪音**：见第 4 步。保守加 `.gitattributes`，别 renormalize 全库。

---

## 常见误区

| 误区 | 实际 |
|---|---|
| `.gitignore` 写了就以为生效 | 必须用 `git check-ignore -v` 验证；`!` 取反规则和父目录忽略会互相干扰 |
| `git grep` 能搜到所有文件 | **只搜已跟踪文件**。未提交的和被忽略的都搜不到 |
| 删掉文件里的密钥就安全了 | 已进历史的仍在 `git log -p` 里。需要 `filter-repo` |
| 加 `* text=auto` 是"最佳实践" | 会让整个工作区被重写，制造巨大 diff。只声明例外更安全 |
| 图片密钥不算敏感 | 看作用域。能解全部聊天记录的必须修；只解部分附件的属 P1 |
| 通用正则扫过就行 | 非十六进制格式的凭据会漏。要用已知真实值反查补充 |
| 只看"协作资产入没入库"就够 | 还要看**下一步的输入**在不在库里。研究产出/规范/数据表常在 `temp/`，一 ignore 就断链 |
| push 成功 = 对方能接手 | push 只证明"传上去了"。要 clone 到干净目录跑一遍测试才算验证 |
| 本地分支 master 也能用 | 能推，但新建空仓的默认分支可能仍是 main，要 `gh repo edit --default-branch` 对齐 |
| 敏感文档"脱敏太麻烦，干脆不入库" | 通常可以只入**结构 + 指纹**：保留研究价值，去掉可直接利用的能力 |

---

## 检查清单（可贴进项目文档）

```markdown
- [ ] 密钥原文没混进仓库：`git grep -nIE "\b[0-9a-f]{64}\b" -- . | grep -v uv.lock` 为空
- [ ] 已知真实凭据的反查也为空（用具体值 grep）
- [ ] 无 >1M 的意外入库文件
- [ ] 忽略规则经 `git check-ignore -v` 验证
- [ ] `.gitattributes` 声明了 bat/sh 与二进制（如果适用）
- [ ] 协作资产（memory/wip/skills/docs）已入库且已脱敏
- [ ] **断链检查**：下一条待办的每个输入依赖都能在库里找到（`git check-ignore -v` 无输出）
- [ ] 测试全绿、工作区干净
- [ ] 若公开：P1 级数据（真实 ID / 弱密钥）也已脱敏
- [ ] 文档里的里程碑提交号是"语义化"的，没有写死 HEAD
- [ ] **推送后做过克隆验证**：干净目录 clone → 关键资产齐全 → 无泄漏 → 跑测试通过
- [ ] 若建了新仓：默认分支已对齐本地分支名
```
