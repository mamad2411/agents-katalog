---
name: cross-machine-delivery-bundle
description: 把一个工作区的文件从 A 机（真机）打包交付到 B 机（VM/另一台机），产出「压缩包 + 完整性清单 + 交付说明 + 落地脚本」四件套。核心是先判"自己在哪台机"（盘符判据），再把报告里出现的每个路径当断言逐条验，最后按"项目 temp/ 内 staging + sha256 清单 + 7z -tzip"打包。当用户说"把缺的东西打包给我 / 帮我打包传进去 / 跨机交接 / 虚拟机缺的补一下"时使用。
agent_created: true
task_type: daily.cross_machine_delivery_bundle
---

# 跨机交付包（真机 → VM / 另一台机）

## 0. 先判自己在哪台机（不做这步后面全白干）

同一份对话可能一会儿在真机、一会儿在 VM，**不要靠记忆或上下文猜**。查盘符与路径：

```bash
hostname                                        # 真机 <dev_machine> / VM DESKTOP-CCP7OFC
ls -d /e/<data_drive>:/<system_data_root>/Desktop         # 只有真机有 E: 数据根
ls -d /c/<user_home>/localAgent                 # VM 的仓库在这里
ls -d "/e/System_Programes/VMware"              # 有 VMware = 宿主机（真机）
```

判据：**只有进了 git 的两台机器都有**。仓库外（`temp/sdd/`、E: 数据根）与被 gitignore 的
（`data/llm/keys.json`、`data/secret/`、`…/cache/bundles/`、`chrome_debug/`、`.venv/`）
只能随整目录拷贝碰运气 —— 用户报「XX 不见了」时先套这条，别急着归因给清理轮。

## 1. 定清单：把路径当断言，别凭印象

从需求方给的那份「缺件报告」出发，但**逐条复核**（报告常有抄错的名字/层级）：

```python
# 全量引用审计思路：文档里出现的每个路径 → 去文件系统验存在
# glob 搜疑似文件名（比 find/grep 稳，不受 30s 超时限制）：
#   Path(r"<root>").rglob("*关键字*")
```

实测两类假信号，别当成缺口：
- **名字对不上层级**：`references/site_index.md` 可能是 skill 相对路径，不是项目根；
  `jsd_research` 常在 `workspace/homework/tools/` 而不是 `workspace/<项目名>/`。
- **"记忆 key" 其实是字段**：`memory_get('multimachine_20260919_d14')` → 404 说明它只是
  `project_jsd_format_cracked` 里的一个字段。查记忆先 `memory_list` 看真 key。

## 2. staging 放**当前项目的 `temp/`**（不要写到项目外）

⛔ **用户明令（2026-09-19）**：「临时产出不要乱扔，不知道放哪的统一放到 `temp/` 里面，**不要往外放**！」

- 正解：`<仓库根>/temp/<任务名>_<日期>/`（`temp/` 已被各项目 `.gitignore` 忽略，既不入库也不污染项目根）。
- **反面教材（本技能初版就写错了）**：写到 `<projects_parent>\` **根**上 —— 那是**多个项目共用的父目录**，
  对当前仓库而言就是"外面"。用户会直接看到一堆散落的 zip / py。
- 同理别散在仓库根：临时脚本、中间产物一律进 `temp/`，长期复用的才迁 `tools/`。

```
<仓库>/temp/<任务名>_<日期>/
├── <staging目录>/          ← zip 的源，目录名 = 解压后的顶层名（保持稳定）
│   ├── 交付说明.md          ← 主交付物
│   ├── MANIFEST.sha256.txt  ← 包内（清单自身不自我哈希）
│   ├── 01_<大块数据>/
│   ├── 02_配置与密钥/
│   ├── 03_<文档/计划书>/
│   ├── 04_记忆导出/         ← *.json + IMPORT.md + import_memories.py
│   └── 05_<可选大件>/
├── <staging目录>.zip        ← 与 staging 同级 → 原地即可重新打包
└── _build/                 ← 生成用脚本（staging / 记忆导出等）
```

排他规则（照 `HANDOFF.md §2` 一类文档走，别自创）：
- **明确不入库的也别拷机**：`samples/`（截图含账户名等 PII）、`cache/*.json`（派生物）、`.venv/`、`chrome_debug/`（登录态）。
- **能在 VM 重装的客户端安装包别装**（写进 §3 说明，省几十~上百 MB）。
- **已在 git 里的文本层不要重复携带**（`git status` 干净 + `git ls-files | grep <名字>` 确认）→ 制造分叉。

## 3. 四件套的产出方式

> **别做过头**：用户原话「就是传文件，不用做那么好，sha256 不用」（2026-09-19）。
> **必备 = 压缩包 + 交付说明**；`MANIFEST.sha256` / 校验和 / 抽样复验属**可选强化**，除非用户要或
> 包内含密钥/大件、跨网络中转 —— 默认不做，别自己加戏。

| 步骤 | 怎么做 | 要点 |
|---|---|---|
| staging | 写一份 python 脚本（unicode 路径比 bash 稳），`shutil.copy2` 保 mtime | 跳过规则写成 `SKIP_NAME_SUBSTR` 常量，打印跳过了几个 |
| 记忆导出 | `GET http://127.0.0.1:8766/memory/{key}`（后端在跑时）；失败回退 sqlite **只读** `file:data/memory/memory.db?mode=ro` 读 `facts.value` | 导出的是原始 fact JSON，不是 wrapper |
| manifest | 逐文件 `sha256` + 字节；**>8MB 只记尺寸**（字体包等已压缩，哈希耗时无收益） | 写成 `sha256  字节 相对路径`，别用 `sha256sum` 格式以免路径含中文出错 |
| 交付说明 | 见 §4 模板 | 用表格给「真机来源 → VM 目标位置 → 为什么」 |
| 打包 | `"/c/Program Files/7-Zip/7z.exe" a -tzip -mx=3 -y "<名>.zip" "<staging目录名>"` | **用 -tzip 不用 .7z**：Windows 资源管理器原生能解；中文名自动带 UTF-8 标志，实测无损。251MiB/327MiB ≈ -mx3，7 秒 |
| 校验和 | 打完包再 `sha256(zip)`，写 `<zip>.sha256.txt` 放**包外** | **别把 zip 自己的哈希写进包内的说明**（循环依赖）；包内说明只写"见同目录 xxx.sha256.txt" |

## 4. 交付说明模板（就这几节，别写散文）

1. **头部元信息表**：生成时间 / 生成机器 / 目标机器 / 对应哪份报告 / 包内合计
2. **§0 一句话**：缺件是否全带、有无例外
3. **§1 包里有什么**：表 = 编号 | 内容 | 真机来源 | VM 目标位置 | 为什么（挂到具体 ticket）
4. **§2 怎么用**：可直接粘的 `robocopy /E /COPY:DAT`、`copy /Y` 落位命令（占位 `X:\解压目录`）
   + **落位后怎么验**（字节数/哈希/健康检查/项目自带自检顺序）
5. **§3 明确没装进去的 / 理由**（省得用户以为漏了）
6. **§4 只有用户能做的**（人工登录、只有人能造的样本——**列成表，别含糊**）
7. **§5 安全提醒**（密钥文件不要上传/进 git/放同步盘）
8. **§6 对上一轮报告的修正**（若有）+ **§7 传输校验**

## 5. 坑（都实测踩过）

- **`memory_get` 的 key 未必存在**：报告里的"结构化记忆名"可能只是别的记忆里的字段 → 先 `memory_list`。
- **bash 里不要出现 PowerShell cmdlet 字样**：把 `Get-FileHash` 之类写进 heredoc 会被安全策略拦
  （报「Invoking PowerShell from Bash」）→ 改写成 python 哈希，或把命令交给 PowerShell 工具。
- **登录态跨机必然失效**：Chromium cookie / `Local State` 用 DPAPI 绑「Windows 用户 + 机器」，
  拷过去也解不开 → 在新机人工首登是**省不掉的**，别当成疏漏去排障。
- **git 用用户二进制**：`export PATH="/e/System_Programes/Git/cmd:$PATH"`，且 `git -C` 要传 **Windows 路径**
  （`<projects_parent>/...`），MSYS 的 `/f/...` 会让它报 `cannot change to`。
- **追加含中文的 .md 记忆文件用 bytes 追加**（检测原 EOL 后 `write_bytes`），不要用 Edit 工具
  （会把 CRLF 文件整体重写成 LF）。
- **计划书在 `temp/sdd/` 的会被清理轮回收**：交付时**整目录拷**，别只拷 tickets；并提醒用户落位后只留一份。
