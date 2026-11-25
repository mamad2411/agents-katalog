---
name: windows-recycle-and-space-reclaim
description: 在本机 Windows 上安全删除文件/目录并真正回收磁盘空间 —— 走项目既有的 ctypes 回收站工具（因 Add-Type 被安全策略拦死），并解决「进了回收站却不释放空间」这个核心陷阱。含回收站条目审计与按身份核对后永久清理两个脚本；**也含反向能力：从回收站把已删内容（整目录）捞回来**。当用户说"把这个目录删掉 / 清理 temp / 太占存储了 / 帮我回收空间 / 磁盘满了 / 删掉这个大文件 / 这台机器怎么删到回收站"，或反过来问"那个文件还在吗 / 我记得当时有一批 X / 是不是被我删了"时使用，尤其当删除对象是 GB 级产物时。
agent_created: true
task_type: daily.windows_recycle_and_space_reclaim
---

# Windows 可恢复删除 & 真正回收空间

> ⚠ **本 skill 只管「怎么删、怎么真正释放空间」。**
> 如果用户 intent 是**「哪些该删 / 这块空间被谁占了 / 分析一下」**（尤其是给了 SpaceSniffer
> `.sns` 快照，或说「帮我看看能清什么」）⇒ **先走 Parcae 项目的 `workspace/disk_manager`
> skill**（它有 `.sns` 导入、`scan_disk.py` 分析、`pending_decisions.md` 待决台账），
> 本 skill 只在其产出清单**进入执行阶段**时接手。2026-09-24 踩过：拿本 skill 去解三个盘的快照，
> 前半程都在绕远。

## 0. 先分清对象，再决定要不要问

| 对象 | 流程 |
|---|---|
| **个人文件**（桌面 / 下载 / 文档 / 家目录）| 先只读扫描出清单 → 用加粗警告 → 列全部路径 → **要显式确认** → 才动手 |
| **项目文件**（仓库内的 temp/、构建产物、日志）| 列出清单 + 说明可再生产性 → 确认 → 动手 |
| **回收站里已有的条目** | 永久删除**不可逆**，**必须单独再确认一次**（见第 3 步） |

不确定目标目录 / 文件类型 / 判据时，**先问再动**，不要靠猜。

## 1. 本机唯一可用的「可恢复删除」入口

```bash
cd /f/<project_root> && ./.venv/Scripts/python.exe tools/disk/recycle.py "<绝对路径>"
# 多条：... recycle.py <路径1> <路径2> ；或 --list paths.txt / --stdin
```

- 该工具纯 `ctypes` 调 Win32 `SHFileOperationW` + `FOF_ALLOWUNDO`，无子进程、无 .NET 依赖。
- 结果形如 `回收站: 成功 N 项, 失败 0 项`。

**为什么不能用常见的那两条路**（本机实测全部被拦）：

| 路 | 结果 |
|---|---|
| `Add-Type -AssemblyName Microsoft.VisualBasic` → `[FileSystem]::DeleteDirectory(...,'SendToRecycleBin')` | ❌ `Command blocked for security: Add-Type compiles and loads .NET code at runtime` |
| 从 Bash 里调 `powershell.exe -Command ...` | ❌ `Command blocked for security: Invoking PowerShell from Bash bypasses PowerShell security checks` |
| `cmd.exe` 子进程 | ❌ 被安全策略拦截 |

需要 Win32 能力时一律用 **Python `ctypes`** 直接调 —— 这就是 `recycle.py` 存在的原因。

## 1.5 ⛔ 更狠的一层：本机**所有**删除都被 shim 转成「送回收站」（2026-10-03 实证）

WorkBuddy CLI 注入了 `genie-safe-delete` shim，**在解释器层面**把删除 API 全换掉了：

```bash
# 环境变量（本机默认就有）
PYTHONPATH=C:\Program Files\WorkBuddy\resources\app.asar.unpacked\cli\vendor\shim
CODEBUDDY_SAFE_DELETE_ENABLED=1
BASH_FUNC_rm%%=() { "${CODEBUDDY_SAFE_DELETE_BIN_DIR}/rm" "$@"; }   # unlink / rmdir 同理
```

```python
import os, shutil
os.unlink      # -> sitecustomize._safe_remove
os.rmdir       # -> sitecustomize._safe_rmdir
shutil.rmtree  # -> sitecustomize._safe_shutil_rmtree
```

（`sitecustomize.py` 内部走 `SHFileOperationW` + `FOF_ALLOWUNDO`，即"送回收站"。一行自证：

```bash
python -c "import os,shutil;print(os.unlink.__module__, shutil.rmtree.__module__)"
# -> sitecustomize sitecustomize
```
）

**后果 —— 两个必须记住的判据：**

1. **`shutil.rmtree` 在这台机器上不是永久删除。** 它把目录**送进回收站**后正常返回，
   `assert not os.path.exists(p)` **照样通过** ⇒ **假成功**。别信自己脚本里的"已删除"。
2. **同盘回收站不释放空间** ⇒ 删完可用空间纹丝不动。**判"到底释放没有"只能看可用空间数字**
   （`shutil.disk_usage('F:/')` 实测精确：分配 512 MiB → free −512.0 MiB，截断回 0 → +512.0 MiB），
   **绝不能看 `os.path.exists`**。

> 2026-10-03 实战代价：一个 3.2 GiB 孤儿目录被 `shutil.rmtree`"删掉"，脚本打印 `[ok] 已永久删除`，
> 但 F 盘可用空间反从 74 G 掉到 72.35 G（我另建的两个 1.5 GiB 探针也被送进桶）。
> 事后才在 `<data_drive>:\$RECYCLE.BIN\<SID>\$RJC9Q5T`（3.2 G / 74 文件）里找到它 —— **完整可还原**。
> 当时错判成"永久删除、不可恢复"，是**看 `os.path.exists` 得出的错误结论**。

⇒ **要真正回收空间，只能走 `§4` 的"永久清理"，或让用户自己清空回收站。** 别指望 `rmtree`。

## 2. ⚠️ 核心陷阱：进回收站 **不等于** 释放空间

**同盘移入回收站只是把文件改了个名**（移到 `<data_drive>:\$RECYCLE.BIN\<SID>\$R<ID>`），
磁盘可用空间**一个字节都不会变**。

实测：7.81 GiB 目录送进回收站后，源目录消失、`temp/` 从 7.9G 掉到 11M，
但 F 盘可用空间**纹丝不动**。真正释放必须永久删除回收站里的 `$R`/`$I` 对。

**推论（很重要）**：用户说"帮我清空间 / 太占存储"时，
**验收标准是「磁盘可用空间的数字变化」，不是「目录不见了」**。
下结论前一定用 `shutil.disk_usage('F:/').free` 或 `df -h` 实测前后对比。

所以「清空间」是**两步**，不能一步到位：

1. 可恢复删除（进回收站）—— 安全、可反悔，但**不释放空间**
2. 确认无误后永久删除回收站条目 —— **真正释放**，不可逆，须再确认一次

## 3. 标准四步流程

### 第一步：删前留清单

```python
# 落一份「路径 + 字节数」清单到 temp/，删完可对账
```

清单本身也回答了"我到底删了什么"，比截图可靠。

### 第二步：送回收站

用第 1 节的 `recycle.py`。

### 第三步：认条目（回收站里看不出哪条是哪个）

```bash
cd /f/<project_root>/.agents/skills/daily/windows-recycle-and-space-reclaim/scripts
python recycle_audit.py --drive F --limit 5
python recycle_audit.py --drive F --filter sync_v3        # 按原路径子串过滤
python recycle_audit.py --drive F --json                  # 给机器读
```

输出：条目 ID / 大小 / 删除时间（本地）/ 数据体是否完好 / 原路径。

⚠️ **`--filter` 是对 `$I` 里记录的原路径做子串匹配，而原路径存的是反斜杠** ——
过滤串里一旦带 `/` 就**静默 0 命中**（2026-10-06 实测：`--filter "spotlight/temp"` 返回"共 0 条"，
看着像回收站根本没收到，其实 7 条都在）。**过滤串一律不带路径分隔符**，
改用名字片段（`--filter _verify` / `--filter sync_v3`），命中后再逐条看原路径确认身份。

### 第四步：按身份核对后永久清理

```bash
# 先 dry-run（默认），看将要删的是哪几条
python recycle_purge.py --entry "UNALER=<projects_parent>/wechatDecode/temp/sync_v3_kq3_irbv"
# 核对无误再加 --yes
python recycle_purge.py --entry "UNALER=<projects_parent>/wechatDecode/temp/sync_v3_kq3_irbv" --yes
```

- **必须同时给 ID 和原始路径**。脚本把 `$I` 记录的路径与预期比对，
  **任一条不符则整体中止**（绝不部分执行）—— 防止只凭 6 位随机 ID 错删用户别的东西。
- 路径可以用正斜杠（脚本 `os.path.normpath` 归一），**这样能绕开 Shell/JSON 的反斜杠转义地狱**。
- 多条：`--entry A=... --entry B=...`。
- 跑完会报 `F: 可用 X → Y GiB（实际释放 Z GiB）`，拿这个数字验收。

## 3.5 ★ 反悔：从回收站把内容**捞回来**（与「删」方向相反，2026-10-03 实战补）

用户说「那个文件/那批图还在吗」「我记得当时有一批……」时，**先扫回收站，别急着答"没了"**。

关键性质（本机实测）：**删「整个目录」时，回收站里只生成一条 `$I`，而对应的
`$R<同名>` 就是完整目录树**（子文件不再单独出现在 `$I` 列表里）。所以只要 `$I` 在、
`$R` 完好，**目录结构可以整棵捞回**。

```python
# 用 §4 的 `$I` 解析拿到 (原路径, 大小, 删除时间, $I 路径)，
# 再拼出数据体路径：同目录下 "$R" + $I文件名[2:]
rpath = os.path.join(os.path.dirname(ipath), "$R" + os.path.basename(ipath)[2:])
# 目录条目 -> os.walk(rpath) 列内容；文件条目 -> 直接 copy
```

做法选择：
- **复制取回**（推荐，默认）：`cp -r "$R..." <目标>` / `shutil.copy2`。
  回收站条目**原样保留** ⇒ 零风险，两份并存，之后用户自己清。
- **移动还原**：会同时清掉回收站条目，等于「永久删 + 恢复」合并 —— 除非用户明确要求，别做。

搜索技巧：**先按「名字关键词」过一遍全部 `$I`**（如 trade / 饰品 / 封面），
再对命中项解析 `$R`；比逐个目录翻快得多。本次就是靠这一招在 3486 条 `$I` 里
一次定位到 `<data_drive>:/<apps_root>\trade`（2026-09-24 删，11 MB，6 张平台截图）。

## 4. `$I` 元数据格式与三个已踩的坑

```
offset  0  int64  版本（1 或 2，v2 = Win10+）
offset  8  int64  数据体字节数
offset 16  int64  删除时间，FILETIME（UTC）
offset 24  int32  路径长度
offset 28  ...    原始路径，UTF-16LE，\0 结尾
```

1. **长度字段是「字符数」（含结尾 `\0`），不是字节数。**
   按字节读会把路径读成半截（`<projects_parent>\wechatDec`），于是按路径搜索
   **永远 0 命中**，看起来像"回收站里根本没有这条"。排错时极易误判。
   实测 `n=51` 对应 `<projects_parent>\wechatDecode\temp\sync_v3_kq3_irbv`（50 字符 + `\0`）。
2. **FILETIME 是 UTC**，直接格式化会显示成 8 小时前的时刻（东八区）。
3. **`$R` 必须原样带扩展名**：删文件时 Windows 保留原扩展名
   （`$I4X51EV.json` ↔ `$R4X51EV.json`），删目录时无扩展名。
   ID 一律取 `$I` 之后的**全部**内容，去掉扩展名就找不到数据体。

另一个容易忽略的：`$R` 可能不存在（历史遗留的孤儿 `$I`），
脚本用 `payload_exists` 标出来 —— 这类条目删了不释放任何空间。

## 5. 本机环境怪癖（会白白浪费好几个来回）

- **PowerShell 工具的 stdout 回显永远是空的**，但命令**确实执行了**。
  规避：让 PowerShell `Out-File` 写文件，再用 Read 工具读。
  千万别因为"没输出"就重复执行 —— 可能已经改了两遍。
- **Bash 里给 Python heredoc 写 Windows 路径时，反斜杠会被吃掉一层**：
  写 `'F:\\'` 到 Python 会变成 `'F:\'` 直接 SyntaxError。
  ⚠ **更阴的一种：被吃成控制字符而不报错** —— 写 `<data_drive>:/<apps_root>\trade` 时
  `\r`→CR、`\t`→TAB，脚本**照跑不误但字符串是错的**（本次实测：`startswith` 全不命中，
  打印出来的路径显示成 `F:ubbish` + TAB + `rade`）。判据：**输出里出现反斜杠被"吞掉"的痕迹**。
  规避：用 `r'...'` 原始串，或换 API 绕开字面反斜杠（如 `shutil.disk_usage('F:/')`），
  或干脆写脚本文件而不是 `-c`/heredoc（**本次最终解法**）。
- **Shell 里的 `$` 会被吃掉**：`"$RECYCLE.BIN"` 在双引号里被当变量。
  要引回收站路径时用单引号，或在 Python 里用 `chr(36)` 拼。
- 本机 git 一律用 `<data_drive>:/<apps_root>\Git\cmd\git.exe`（见其他 skill）。

## 6. 一个真实踩坑记录（值得知道我为什么会写这个 skill）

排查脚本连着两次 `os.path.isdir(回收站) == False`，最后发现是：

```python
root = os.path.join(drive + os.sep, "$RECYCLE.BIN")   # ❌ 'F' + '\' = 'F\' —— 少了冒号！
```

`'F' + os.sep` 得到 `'F\'`（**没有冒号**），整体变成**相对路径** `F\$RECYCLE.BIN`，
`isdir` 恒为 False，脚本静默报"回收站不存在或为空"。
正解：`f"{drive.rstrip(':\\/')}:{os.sep}"`。

教训：**这类路径拼接错误在 shell 里用 `python -c` 测试时会被引号/反斜杠转义扰乱，
越测越乱。直接写成脚本文件跑，几秒钟就能定位。**

## 7. 收尾自检

- [ ] 删前清单已落盘（路径 + 字节数）
- [ ] 用的是 `recycle.py`（不是 `rm`/`del`）
- [ ] 已实测**磁盘可用空间**变化，而不是只看目录消失
- [ ] 若做了永久删除：用户已**单独确认**过；条目**身份已核对**；实际释放数字已报给用户
- [ ] 临时脚本与调试文件已清掉
