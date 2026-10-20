---
name: ges-case-analysis
description: 当用户需要分析已经打开并解析完成的火眼案件数据时使用，包括案件记录、检材文件、手机应用数据、聊天/通话/交易记录、数据库文件和语义检索。
metadata:
  requires:
    bins: ["ges"]
  cliHelp: "ges --help"
allowed-tools: Bash(ges*)
---

# 火眼案件数据分析

用 `ges` 分析已选择且解析完成的单机版或平台版火眼案件数据。不要用本 skill 创建案件、选择案件或导入检材；这些操作使用 `ges-case-management`。如果用户提出新检材路径，只有该路径与当前案件检材路径完全一致时才继续当前上下文。

遇到 `/case/`、`/evidence_mounts/` 等 GES 虚拟路径时，只能用 `ges` 命令访问，不要用本地 `Read`、`Glob`、`Grep` 直接读取。

## 开始前

先读取当前案件上下文：

```bash
ges status
```

如果成功，记录 `status` 返回的当前 `cid`、`GES URL` 和可用路由，再按实际路由继续分析，不要猜测挂载路径。`ges status` 等价于旧命令 `ges context`。

如果失败，按已有信息初始化：

```bash
# 用户已提供 cid、完整案件编号或完整案件名称
ges case open <cid|case_number|case_name>
ges status

# 上游已提供 cid 和 ges_url，或来自 ges case ls 的 ges_url
ges init --cid <cid> --ges-url <ges_url>
ges status
```

单机版 `ges case open <case_number>` 会先复用已打开的同编号案件；未打开时才启动案件并自动初始化。平台版会精确选择远程案件并写入用户级上下文，名称重名时必须使用 `cid` 或完整案件编号。不要因为 `status` 失败就重复导入检材；也不要因为案件名、检材名或路径相似就复用旧检材，必须完整路径一致。

平台只提供 URL/token 而没有案件参数时，切到 `ges-case-management` 执行 `ges case ls` 并询问用户；绝不能默认选择第一个案件。其他缺少上下文的情况也切到该 skill。

## 常用命令

### 查看目录

```bash
ges ls /
ges ls /case/
ges ls /evidence_mounts/
```

### 读取文件

```bash
ges read /case/path/to/data.csv --offset 0 --limit 100
ges read /evidence_mounts/eid-1/path/to/file.txt --offset 0 --limit 100
```

先用较小的 `--limit`，避免输出过大。

读 `/case/` 下可溯源的 `data.csv` / `chat.txt` 时，输出最顶部会多出一行 `〔本文件溯源基址 Goldeneyes://<case_number>/<node_id>〕`。引用记录时只需在该基址后追加 `#<正文行号>`，见下方「溯源引用」。基址行不占行号，正文仍从第 1 行算起。

如果顶部仍是旧格式 `〔本文件溯源句柄 nXXXX〕`，说明 CLI 未能从当前 GES 服务确认案件编号；可以继续分析，但禁止自行补写案件编号或生成溯源链接，也不要为补链接额外执行 `case ls` 或 `evidence ls`。

### 搜索文本

```bash
ges grep "关键词" --path /case/
ges grep "关键词" --path /case/ --start-time "2025-01-01" --end-time "2025-01-31"
```

`grep` 是字面子串匹配，不是正则。`/evidence_mounts/` 可能很大，先 `ls` 或 `glob` 定位文件后再 grep。

### 查找文件

```bash
ges glob -p "**/*.db" --path /evidence_mounts/
ges glob -p "**/*.csv" --path /case/
```

必须传 `-p`/`--pattern`，并尽量用 `--path` 缩小范围。模式相对 `--path` 匹配：`*.db` 只匹配当前目录的直接子文件，`**/*.db` 才会递归匹配任意层级。

### 复制到本地分析

```bash
ges copy /case/path/to/data.csv
ges copy /evidence_mounts/eid-1/path/to/app.db
ges copy /evidence_mounts/eid-1/path/to/databases/ --recursive
ges copy "/evidence_mounts/eid-1/分区4(恢复的文件)/" --recursive --glob "**/*.xls" --glob "**/*.xlsx" --dest ./recovered --max-files 1000 --skip-existing --manifest ./recovered-copy.jsonl --async
ges job status <job-id> --json
```

需要用 pandas、sqlite3 或其他本地工具分析时，先 `ges copy`。复制 SQLite 数据库时，同名 `-wal`、`-shm` 会一并复制。

目录复制规则：

- 路径包含中文、空格、括号或其他 shell 特殊字符时，必须用引号包住完整路径。
- 复制目录必须传 `--recursive`；只复制部分文件时重复传 `--glob`。`--include` 是完全等价的兼容别名。
- 递归筛选推荐使用 `**/*.xlsx` 这类明确模式。不含 `/` 的模式会匹配任意层级的文件名，含 `/` 的模式匹配相对源目录的路径，匹配不区分大小写。
- 文件数超过默认 200 时，根据已确认的目录规模显式提高 `--max-files`；总大小超过默认 256 MiB 时再提高 `--max-total-bytes`。
- 批量复制应使用一条 `ges copy ... --recursive`，不要先列出文件再逐个循环调用 `ges copy`。
- 长时间批量复制必须加 `--async`，命令会立即返回 `job_id`；之后用 `ges job status <job-id> --json` 轮询，不要重复提交同一个复制命令。
- `queued/running/cancelling` 表示尚未结束；`completed` 且 `result_current` 不是 `false` 后再处理目标目录；`result_current=false` 表示目标后来被其他复制覆盖，旧结果不可再信任；`failed/cancelled/interrupted` 时读取 `error`，不要把部分文件当作完整结果。
- 相同参数的活动任务会返回同一 `job_id`；同一目标目录或其父子目录已被其他任务锁定时，应继续轮询原任务或更换目标，不能绕过锁并发写入。
- 相同参数已完成的任务也会返回原 `job_id`，避免响应丢失导致重复复制；只有用户明确要求重新执行时才加 `--force-new-job`。
- 长时间批量复制应指定 `--manifest <path>.jsonl`。中断后用相同 `--dest` 加 `--skip-existing` 重新提交；`--skip-existing` 与 `--overwrite` 不能同时使用。
- 用户要求停止时运行 `ges job cancel <job-id> --json`，再轮询到 `cancelled`。取消在当前文件下载返回后生效。
- 命令失败时 `ges` 返回非零退出码并把错误写入 stderr；不要把失败当作空结果继续处理。

### 语义搜索

```bash
ges search "转账记录" --max-results 10
ges search "potato 聊天" --timerange 2025-05 --max-results 10
```

返回路径是当前可用的 `/case/...` 路径。需要展开结果时再 `ges read` 或 `ges copy`。

## 路径规则

- `/case/`：已解析案件记录，例如聊天、通话、账号、交易、应用提取结果；检材节点下可能有 `图片分类/{分类名}/data.csv`、`实体分类/{分类名}/data.csv` 和 `检材信息/data.csv`，分别用于查看图片分析、实体聚合结果，以及检材元数据和任务写回的 hash 结果。
- `/evidence_mounts/`：原始检材挂载文件系统，用于查找 `/case/` 未覆盖的数据库、缓存、应用目录和文件。
- `/case/` 不是本地物理目录；`/evidence_mounts/` 也不要绕过 `ges` 直接猜路径。

## 溯源引用

回答里凡是引用 `/case/` 记录的地方，都要在该处紧跟一个角标，让用户能跳回原始记录：

```text
[[N]](Goldeneyes://<case_number>/<node_id>#<行号>)
```

`N` 从 1 递增，像论文引用。必须使用双层方括号的 Markdown 源格式 `[[N]](...)`，使渲染后的可点击链接文字仍显示为 `[N]`；不要写成 `[N](...)`，否则渲染后只会显示 `N`。正文里【只出现带方括号的可点击角标 `[N]`】，不要写 `/case/` 路径、不要写句柄。

### 溯源基址和行号从哪来

溯源基址和行号都来自 `ges read`：

```text
$ ges read <某个 /case/ 下的 data.csv 或 chat.txt>
〔本文件溯源基址 Goldeneyes://20260805123456A/4821〕
     1  字段,值               ← 表头行，不要引用
     2  真实姓名,张三          ← 行号 2
```

回答：

```text
该检材持有人姓名是张三[[1]](Goldeneyes://20260805123456A/4821#2)。
```

直接复制 `read` 顶部的完整基址，再追加 `#2`。不要拆分、改写、猜测其中的案件编号或节点编号；行号使用 `read` 输出左侧那一列。

> ⚠️ **本节所有示例里的路径、案件编号（20260805123456A）、句柄数字（4821 / 6307）、姓名、行号全部是占位符，只用来示意格式，不是真实值。**
> 案件的目录结构因检材、应用、账号而异，**没有固定路径**——实际路径必须用 `ges ls` / `ges glob` / `ges search` 逐层看出来，
> 实际溯源基址必须来自你自己 `read` 时顶部的真实值。**绝不能照搬示例里的路径、案件编号或数字。**

### 铁律

1. **必须使用 `read` 返回的完整溯源基址。** 没 `read` 过不许标；顶部没有 `Goldeneyes://<case_number>/<node_id>` 基址也不许标。绝不能凭 `ls` / `grep` / `search` 的路径、旧 `nXXXX` 句柄或记忆补造基址。
2. **只对 `/case/` 打角标。** `/evidence_mounts/` 的原始检材文件、`ges copy` 到本地的文件都没有句柄，标了会悬空。
3. **只指向具体记录行。** 不要标 `data.csv` 的表头行（第 1 行），不要标 `chat.txt` 的 `[摘要]` 行（有摘要时正文从第 2 行起）。
4. **一段连续记录只标首行、只给一个角标。** 正文用一句话概括整段，绝不逐行逐笔标。
5. **一个溯源基址只对应一个案件中的一个文件。** 换文件或切换案件后必须重新 `read`，使用新输出的基址。

### 正例与反例

```text
✅ 他从 2025-11-21 到 2026-01-13 共 78 笔彩票投注，每日约 4 元[[1]](Goldeneyes://20260805123456A/6307#2)
   （78 笔连续记录概括成一句话，只标首行一个角标）

❌ 他有投注记录[1](Goldeneyes://20260805123456A/6307#2)
   （只用一层方括号，渲染后只显示 `1`，没有可见的 `[1]`）
❌ 投注[[1]](Goldeneyes://20260805123456A/6307#2)、[[2]](Goldeneyes://20260805123456A/6307#3)……[[78]](Goldeneyes://20260805123456A/6307#79)
   （逐笔标，正文被角标刷屏）
❌ 姓名是张三[[1]](Goldeneyes://6307#2)                         （缺 case_number）
❌ 姓名是张三[[1]](Goldeneyes://40/6307#2)                      （用内部 cid 代替了 case_number）
❌ 姓名是张三[[1]](Goldeneyes://20260805123456A/6307)           （缺 #行号）
❌ 姓名是张三[[1]](Goldeneyes://20260805123456A/6307#1)         （标到了 data.csv 的表头行）
❌ 姓名是张三[[1]](/case/…/data.csv#2)                          （正文写路径，不是案件级句柄）
```

## 工作流

```bash
ges status
ges ls /case/
ges grep "关键词" --path /case/
ges read /case/path/from/result/data.csv --offset 0 --limit 100
ges copy /case/path/from/result/data.csv
```

`grep` 只能定位到文件和记录行。要引用命中的记录，仍需对该文件 `read` 一次，复制顶部完整溯源基址并追加命中记录的正文行号。

如果 `ges status` 显示没有可用数据，或用户要求新增检材，切换到 `ges-case-management`。

## 排障

- 缺少上下文：有案件编号就 `ges case open <case_number>`；有 `cid/ges_url` 就 `ges init --cid <cid> --ges-url <ges_url>`；都没有时切到 `ges-case-management`。
- 缺少完整溯源基址：可以继续分析但不要生成角标；不要用 `case ls`、`evidence ls`、`cid` 或旧 `nXXXX` 句柄手工拼接。先确认 `ges status` 正常；上下文失效时切到 `ges-case-management` 重新打开或初始化案件。
- 输出过大：使用 `--path`、`--glob`、`--timerange`、`--limit`、`--max-results` 缩小范围。
- `/evidence_mounts/` 为空：查看 `ges status` 中被跳过的挂载项。
- 不确定语法：运行 `ges --help` 或 `ges <command> --help`。
