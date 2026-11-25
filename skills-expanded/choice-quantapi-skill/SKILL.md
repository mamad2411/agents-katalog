---
name: choice-quantapi-skill
description: 面向有编写量化投资策略、回测程序或研究脚本等需求的用户，提供 Choice 量化 API（EMQuantAPI）的文档检索、指标函数选择和 Python 调用代码生成能力，帮助将自然语言策略需求转成可重复执行的量化取数/回测脚本；覆盖截面、序列、板块、专题报表、交易日工具等接口，并在查询报错时按需安装激活 SDK。当用户意图是通过类似 Choice API、Choice 量化、量化取数、程序化取数、金融数据API、量化接口、数据API调用、调用量化接口、Python取数、命令生成、打印命令、生成代码等方式编写或运行量化/回测/策略研究代码时使用；这些是意向示例，不要求逐字匹配关键词。
version: 1.0.3
---

# Choice 量化 API 使用 Skill（EMQuantAPI · Python）

> 当前文档版本：基于 EMQuantAPI Python `V2.7.2.2`（2026-06-05 发布）整理。含 secucode 等新增函数；各函数页「版本要求」标注的阈值以 `scripts/check_sdk_version.py` 内 `THRESHOLD` 为准（当前 `2.7.2.2`，取所有版本门控函数要求之最大值）。

---

## 技能概述

本 Skill 提供 Choice 量化接口（EMQuantAPI · Python）的完整使用能力，包括：
- 按需安装、激活、诊断 SDK 环境（仅在查询报错时触发，详见「SDK 异常诊断与修复」）
- 使用 EMQuantAPI 进行证券数据查询（截面/序列/板块/专题报表/交易日工具）

---

## 使用约束（对 Agent）

> 以下条目**除特别标注外**均为强制约束，按执行时序分 6 组：① 任务理解与响应 → ② 写代码前的准备 → ③ API 调用规范 → ④ 执行脚本 → ⑤ 输出与展示 → ⑥ 版本校验。

### 1. 任务理解与响应

> **按用户意图分流**
>
> - **【要结果】**（"查 X"、"取 Y"、"现在多少"）→ **必须实际跑** 并把结果贴回。
> - **【要代码】**（"写脚本"、"封装函数"、"写程序"、"写量化代码"）→ 产出 `.py` 文件为交付物；并要求试跑通过。
> - 脚本落盘细则见下方「§4 · 脚本落盘约定」。

> **回复格式约定（查数任务）**：最终回复的**重点是查询出来的数据本身**（结果表/数值）。复用脚本、参数解释、扩展玩法、安装/激活/排错过程默认**不展示**或**压缩为一两句话**，不要堆大段说明把数据淹没。需要时再附一个单行注脚（数据口径、披露日、下次更新时点）即可；脚本已落盘的，告知用户文件名，不要再贴一遍代码。

### 2. 写代码前的准备

**写代码前必须按以下 3 步顺序执行，不可跳步：先定函数（⚠️遵循文档，不可根据历史经验直接选择函数），再定实体，最后读文档**：

>**步骤 1：函数选择**
>
> **步骤 1-A：按实体范围选函数大类**
>
> | 用户查询的实体范围 | 函数 | 说明 |
> | --- | --- | --- |
> | 宏观指标（GDP、CPI、利率等，无具体证券实体） | `edb` | 不涉及证券代码 |
> | 板块维度的聚合指标（板块平均 PE、板块涨跌幅等） | `cses` | 按板块代码查询，不按证券代码 |
> | 获取板块成分列表（"全部 A 股"、"沪深 300 成份"等） | `sector` | 仅取成分代码，不可取板块名称（名称用 `cses`） |
> | 其他实体数据查询（股票/基金/债券/指数等证券数据） | `ctr` / `css` / `csd` | 进入步骤 1-B |
>
> 步骤 1-B：选择 ctr / css / csd，按以下决策顺序选择（**不要仅凭指标类型选函数，必须同时考虑实体数量**）：
>
> **决策规则（按优先级）：**
> 1. **单只或少量（≤50 只）明确证券代码 + 截面/单时间点数据** → **先查 `css` 指标目录**（用 Grep 在 [css-indicator-category-index.md](references/indicators/css-indicator-category-index.md) 中搜索关键词），找到对应指标则用 `css`；找不到再回退 `ctr`。**Why**：`css` 费用成本远低于 `ctr`，且单实体查询无需拉全量数据再过滤。
> 2. **少量明确证券代码 + 跨时间范围数据** → `csd`
> 3. **批量查询一类实体（全部 A 股、全部基金等）或需要报表级多字段明细** → **优先 `ctr`**。`ctr` 聚合一类指标可一次批量查询，但费用成本相对较高。
>
> | 函数                         | 函数特点                            | 优先使用的场景                                                | 注意事项                                                                                                                                                                                                            |
> |----------------------------|---------------------------------|--------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
> | `ctr`                      | 聚合了一类指标，且可一次批量查询一类实体，但是费用成本相对较高 | 1.查询一类实体的情况，如沪深股票、全部基金等<br>2.查询的是某类指标**集合**，如资产负债表等 | 1.ctr指标检索时必须同时检索[ctr-indicator-category-index.md](references/indicators/ctr-indicator-category-index.md)文件和[ctr](references/indicators/ctr/)目录下的所有文件<br>2.报表可能有"证券代码"参数，但是不代表不可以批量查询，有些报表可以不提供该参数来查询报表范围内的全部实体。 |
> | `csd`                      | 费用成本较低，可一次查询时间范围内的多条数据          | 少量明确实体的跨时间范围查询                                         |                                                                                                                                                                                                                 |
> | `css`                      | 费用成本较低，只能查询单实体单指标单时间点的数据        | 少量明确实体、指标的最新截面数据查询<br>**单只/少量股票查截面数据时优先于 ctr** |                                                                                                                                                                                                                 |

> **步骤 2：实体识别（默认跳过，仅兜底）** — **默认不调用 `secucode`**。凡是能直接写出"代码+市场后缀"的标的（如 `301165.SZ`、`00700.HK`、`AAPL.O`、`ATI.N`），直接调 `css` / `csd` / `ctr`。`secucode` 仅在以下场景调用：① `css` / `csd` 返回 `10003008 EQERR_CODE_INVALIED`； ② 不熟悉的市场（伦股、日股、新交所等 后缀约定拿不准）。**A 股、港股、美股的主流股票一律先直查，不要"为了稳妥"先跑 `secucode`。**

> **步骤 3：函数文档读取（前置硬约束）** — 决定使用 `css` / `csd` / `cses` / `ctr` / `sector` / `tradedates` / `getdate` / `tradedatesnum` / `edb` / `datastatistics` 任一函数时，**必须先用 `Read` 工具读取 `./references/functions/<函数名>.md` 再写代码**。禁止凭记忆或从其他文档推断函数调用方法。
>
> **Why**：凭记忆写常见踩坑——`ctr` 把 `Ispandas=1` 放首位会返回 `EmQuantData` 而非 `DataFrame`；`csd` 用 `.at[code, indicator]` 会因 index 重复报错；`cses` 漏传 `IsHistory` 导致空值。

### 3. API 调用规范

> **指标特有参数一律必填**：指标详情页「参数说明」表中列出的所有参数**均为必填**，必须在 `options` 中显式赋值。省略时 API 不报错但返回 None/空值。

> **相对时间必须基于系统实际时间计算**：用户使用"上个季度"、"今年一季报"、"去年三季报"等相对时间描述时，**禁止凭模型自身知识推断当前日期**，必须从运行环境获取真实当前时间后再做换算。

> **默认 `Ispandas=1`**：除非用户明确要求 EmQuantData / 嵌套 dict 结构，所有 `css` / `csd` / `cses` / `ctr` / `sector` / `edb` / `datastatistics` 调用 **默认在 options 末尾追加 `Ispandas=1`**。**Why**：DataFrame 对 Agent 读取、切片、导出 CSV/Excel 都更直接，比 `Data[code][i][j]` 三层 dict 可读性高得多；下面两条约束（`isinstance` 兜底、`pd.to_numeric` 兜底）也建立在这个默认值之上。**How to apply**：函数页样例已默认带 `Ispandas=1`；只有以下场景才退回 `Ispandas=0`——① 用户显式要 EmQuantData；② 函数本身不支持 Ispandas（`tradedates` / `getdate` / `tradedatesnum`）；③ `ctr` 必须把 `Ispandas=1` 放在 options **非首位**（SDK 用 `options.upper().find("ISPANDAS=1") > 0` 判定，子串查找、大小写不敏感、严格大于 0）。

> **`Ispandas=1` 访问红线**：① **禁止 `.iloc[i, j]` 按位置取值**——一律用 `.at[code, indicator]` 或 `.loc[code, indicator]` 按列名访问；**例外**：序列函数 `csd` 的 DataFrame index（`CODES`）有重复，必须用 `.loc` 或 `pivot`，不能用 `.at`；`ctr`中可以使用`df.iloc[0]['列名']`获取首行内容，必须使用列名，不能按序号取值。② **禁止 `.ErrorCode` 判错**——`Ispandas=1` 成功时返回 `DataFrame`、**失败时仍返回 `EmQuantData`**，必须用 `isinstance(result, pd.DataFrame)` 先分流再判错。各函数返回结构与样板见各自函数页「返回结构」节。

> **`Ispandas=1` 返回值 dtype 须转数值**：API 返回的 DataFrame 各指标列 dtype **通常**为 `object`（只要列里出现缺失值或 `'--'` 等占位字符串，pandas 就会把整列推断成 `object`），**禁止直接做算术运算**。**一律先 `pd.to_numeric(col, errors="coerce")` 转为 float**。

### 4. 执行脚本

> **脚本落盘约定**：按用户意图区分（见 §1 · 按用户意图分流）：
>
> - **【要结果】**：**能不落就不落**——短脚本一律走 `python -c "..."` 直接跑，避免在用户仓库里留一堆一次性 `query_xxx.py`。**仅当最终脚本确实过长**（>100行，多函数、长 SQL、几十行循环等用 `-c` 写起来不可读）时才落盘。
> - **【要代码】**：**最终交付脚本必须落盘**（作为交付物）；调试/探索过程中的中间脚本尽量不落盘，走 `python -c` 试跑。
>
> 落盘路径见「§5 · 输出目录约定」；落盘后须告知用户文件名（见「§1 · 回复格式约定」）。

> **python 输出字符集约定**：Windows 下中文输出易乱码，统一设置 `PYTHONIOENCODING=utf-8`。按 shell 选写法：PowerShell `$env:PYTHONIOENCODING="utf-8"`；cmd `set PYTHONIOENCODING=utf-8`；bash `export PYTHONIOENCODING=utf-8`。也可在脚本首行加 `sys.stdout.reconfigure(encoding="utf-8")`（Python 3.7+）。

> **致命错误拦截**：遇到 `AttributeError: type object 'c' has no attribute` 时，**唯一动作**是执行 [check_sdk_version.py](scripts/check_sdk_version.py)，**禁止任何其他尝试**（不要换写法、不要换函数、不要"修 typo"、不要重启解释器、不要绕过）。执行后按脚本 `RESULT=` 输出分流：① `RESULT=VERSION_TOO_LOW` → 运行 `python scripts/install.py`（**默认参数，禁止加 `--force-reinstall`**，理由见 [sdk-setup](references/sdk-setup.md) §1）覆盖升级 SDK，再跑 `activate.py`（见 [sdk-setup](references/sdk-setup.md) §2），完成后**重跑原查询**继续任务；② `RESULT=VERSION_OK` → 版本足够，AttributeError 另有原因（如函数名拼写），排查他因，**不要**升级；③ `RESULT=VERSION_UNKNOWN` → 无法判定，回退报用户对齐。

> **禁止首次查询前主动自检 SDK**：自检脚本仅用于查询脚本报错后的诊断回退，禁止在首次查询前主动运行。**Why**：首次查询若 SDK 缺失会立刻 `ModuleNotFoundError`/`ImportError`；若 SDK 已装但版本低（如 secucode 需 ≥2.7.2.2 而旧版没有），调用时立刻 `AttributeError: type object 'c' has no attribute`——两种异常都会在首次调用时直接暴露，预检不会更早发现问题，反而多浪费一轮交互。**How to apply**：直接跑查询脚本；只有当脚本报 `ModuleNotFoundError`/`ImportError`、API 返回异常、或 `AttributeError: type object 'c' has no attribute` 时，才参照 [SDK 异常诊断与修复](#sdk-异常诊断与修复)流程执行。

### 5. 输出与展示

> **输出目录约定**：用户在上下文中未明确指定路径时，**脚本默认落 `scripts/`，结果文件（Markdown / CSV / Excel / 图表 / JSON 等）默认落 `results/`**。用户明确指定路径时以用户指定为准。脚本落盘判定见「§4 · 脚本落盘约定」。

> **相同查询禁止重复调用**：禁止因为输出被 pandas 截断成 `...`、想换个展示方式、想多看几列，就把**相同参数、相同指标**的查询重跑一遍。**默认所有 DataFrame 输出一律用 `print(df.to_string())`**——它忽略 `display.max_rows/max_columns/width`，直接打全。**只有首次请求本身报错或返回空数据**时才允许带修正参数重发。

### 6. 版本校验（强制执行）

> **⚠️ 这是强制步骤，不可跳过 ⚠️**
>
> **版本校验是"输出与展示"环节的一部分，必须附加在返回结果末尾，不可单独分开或省略。**
>
> 执行流程：
> ① 执行查询脚本，获取数据结果。
> ② 调用 `GET https://mxapi.eastmoney.com/quantapi/skill/version` 获取最新版本号。
> ③ 读取本地 `VERSION` 文件（位于 skill 根目录）获取当前版本号，按语义化版本逐段对比（如 `1.0.11` > `1.0.2`）。
> ④ 将版本信息附加在查询结果末尾，格式如下：
> ```
> [版本校验] 当前版本：X.X.X，最新版本：X.X.X
> ```
> ⑤ 若本地版本低于最新版本，在版本信息后追加：**「⚠ 当前 skill 版本已过时，是否更新？」**，用户确认后先阅读 `https://mxapi.eastmoney.com/quantapi/doc/quick-start.md`，再按其 §1–§4 重新安装。
> ⑥ 将最终结果（含版本信息）一起返回给用户。
>
> **违反后果**：返回结果中缺少版本信息，**由 Agent 承担全部责任**。

## 最小可运行示例

完整流程：**登录 → 取板块成分 → 取截面/序列数据 → 退出**。本示例默认走 `Ispandas=1`（DataFrame 路径，本 Skill 默认值）。

```python
import pandas as pd
from EmQuantAPI import *

# 1) 登录
login = c.start()
if login.ErrorCode != 0:
    raise RuntimeError(f"login failed: {login.ErrorCode} {login.ErrorMsg}")

# 2) 取板块成分代码（以"全部 A 股"为例），演示用只取前 5 只
sec = c.sector("001004", "2024-12-31", "Ispandas=1")
if not isinstance(sec, pd.DataFrame):
    raise RuntimeError(f"sector error: {sec.ErrorCode} {sec.ErrorMsg}")
codes = ",".join(sec.index.tolist()[:5])   # 演示用前 5 只；生产场景按业务过滤，不要直接全量

# 3) 截面：取总股本（EndDate 是 TOTALSHARE 的指标特有参数，详见 css.md / 指标详情页）
css_df = c.css(codes, "TOTALSHARE", "EndDate=20241231,Ispandas=1")
if not isinstance(css_df, pd.DataFrame):
    raise RuntimeError(f"css error: {css_df.ErrorCode} {css_df.ErrorMsg}")
print(css_df.to_string())

# 4) 序列：同 5 只标的的日线收盘价（后复权）
csd_df = c.csd(codes, "CLOSE",
               "2024-12-01", "2024-12-31",
               "Period=1,AdjustFlag=2,Order=1,Ispandas=1")
if not isinstance(csd_df, pd.DataFrame):
    raise RuntimeError(f"csd error: {csd_df.ErrorCode} {csd_df.ErrorMsg}")
print(csd_df.to_string())

# 5) 退出
c.stop()
```

> 用户**显式要嵌套 dict 结构**时，去掉 options 末尾的 `,Ispandas=1` 即可退回 `EmQuantData`——访问范式见各函数页「返回结构」节。

---

## SDK 异常诊断与修复

> **本节仅在查询脚本报错后才需查阅，不是使用前流程。** 首次查询前禁止主动自检 SDK（见 §4 · 执行脚本）。

### 触发分流

按报错信号分流（不要混用）：

| 报错信号                                                                                               | 含义                    | 路径                                                                                                                         |
|----------------------------------------------------------------------------------------------------|-----------------------|----------------------------------------------------------------------------------------------------------------------------|
| `ModuleNotFoundError` / `ImportError`（`from EmQuantAPI import *` 失败）                               | SDK 未安装 / 未注册         | 走 [sdk-setup](references/sdk-setup.md) **完整剧本**：先 `install.py` 再 `activate.py`。`install.py` 重注册 `.pth` 并校验版本：版本够则不重下，版本低则自动升级重下（均保留 userInfo 及同目录 defineCode）；`activate.py` 随即返回 `ALREADY_ACTIVATED`、无需重激活 |
| `c.start()` 或查询返回的 `ErrorCode` 命中下方账号错误码表（`10001020` / `10001019` / `10001009`），或 API 明确提示需激活 / 凭据失效 | SDK 已装但账号 / 凭据异常      | 见下方「账号相关错误码速查」——**只需重跑 `activate.py`，不要重装**                                                                                |
| `AttributeError: type object 'c' has no attribute`                                                | 调用的函数不存在，通常是 SDK 版本过低（如 secucode 需 ≥2.7.2.2） | 执行 [check_sdk_version.py](scripts/check_sdk_version.py) 按 `RESULT=` 分流：`VERSION_TOO_LOW` → 按 [sdk-setup](references/sdk-setup.md) 剧本重新安装**并激活** SDK 后重跑原查询；`VERSION_OK` → 排查函数名拼写等他因，**不要**升级；`VERSION_UNKNOWN` → 回退报用户对齐 |

> **如何取 ErrorCode**：`c.start()` 的返回值直接有 `.ErrorCode` / `.ErrorMsg`；`Ispandas=1` 的查询失败时返回的是 `EmQuantData`（不是 DataFrame），按 §3 红线先 `isinstance(result, pd.DataFrame)` 分流，再从 `result.ErrorCode` / `result.ErrorMsg` 读取后对照下表。**未命中下表的不是账号问题，改查 [error-codes.md](references/help/error-codes.md)，不要重跑 `activate.py`。**

### 账号相关错误码速查

> 命中下表时按对应处理；未列出的错误码见 [error-codes.md](references/help/error-codes.md)。

> **强制阅读激活剧本（前置硬约束）**：执行 `activate.py` 前**必须先用 `Read` 工具读取 [sdk-setup.md §2](references/sdk-setup.md#2-第二步激活)** 并照此执行。`activate.py` 默认模式**只探测并输出 `RESULT=`**（`NEED_GUI_TWO_STEP` / `NEED_SMS` / `ALREADY_ACTIVATED`），**不会自动完成激活**——必须按 §2 根据 `RESULT=` 走完 GUI 两步（`--gui-launch` → 发指引 → `--gui-poll`）或 SMS（发指引拿手机号 → `--sms <phone>`）流程。**禁止跑一次 `activate.py` 见到 `NEED_*` 就停下当作已处理。**

| 错误码 | 含义 | 处理 |
| --- | --- | --- |
| `10001020 EQERR_USERINFO_EXPIRED` | userInfo 失效（通常是改了账号密码） | 以 `python scripts/activate.py` 为入口，按 [sdk-setup.md §2](references/sdk-setup.md#2-第二步激活) 剧本重新激活。 |
| `10001019 EQERR_DIFFRENT_DEVICE` | 激活设备与当前设备不一致 | 在当前设备以 `python scripts/activate.py` 为入口，按 [sdk-setup.md §2](references/sdk-setup.md#2-第二步激活) 剧本重新激活。 |
| `10001009 EQERR_LOGIN_COUNT_LIMIT` | 账号已在其他设备登录 | **必须先问用户**「该账号已在其他设备登录，是否踢掉其它设备改在本机激活？」用户确认后再以 `python scripts/activate.py --force-login` 为入口按 [sdk-setup.md §2](references/sdk-setup.md#2-第二步激活) 剧本执行。**不要不问直接加 `--force-login`**——它会踢掉该账号在其他设备的登录。 |

> - `--force-login` 影响说明见 [sdk-setup.md §3](references/sdk-setup.md#3-常见激活错误码)。
> - **登录失败不要反复重试 `c.start()`**：脚本已内置重试，超限后停下和用户对齐原因（见 [sdk-setup.md §4 禁区](references/sdk-setup.md#4-禁区agent-必须遵守)）。

---


## 常用函数索引

每个函数页包含：函数类型介绍 · 公共参数 · Python 命令示例 · 命令拼接教程；并指向对应的"指标/报表主索引页"。

### 登录 / 退出

| 函数 | 用途 |
| --- | --- |
| `c.start()` | 启动并登录 Choice 量化服务。 |
| `c.stop()` | 退出登录、释放资源。 |

### 取证券代码

| 函数 | 介绍页 | 指标主索引 | 用途 |
| --- | --- | --- | --- |
| `sector` | [functions/sector.md](references/functions/sector.md) | [indicators/sector-indicator-category-index.md](references/indicators/sector-indicator-category-index.md) | 取系统板块的成分证券代码列表（**不知道成分代码时，先用 sector 取**；已有证券代码可直接调用查询函数）。 |

### 取数据（截面/序列/宏观/板块截面/专题报表）

| 函数 | 介绍页 | 指标主索引 | 简要说明 |
| --- | --- | --- | --- |
| `css` 截面函数 | [functions/css.md](references/functions/css.md) | [indicators/css-indicator-category-index.md](references/indicators/css-indicator-category-index.md) | 获取单个时间点上的多证券、多指标的截面数据。 |
| `csd` 序列函数 | [functions/csd.md](references/functions/csd.md) | [indicators/csd-indicator-category-index.md](references/indicators/csd-indicator-category-index.md) | 获取一段时间区间内多证券、多指标的时间序列数据。 |
| `edb` 宏观数据函数 | [functions/edb.md](references/functions/edb.md) | 动态指标搜索（调用流程见介绍页） | 先按用户需求动态检索宏观指标 ID，再获取中国经济、地区宏观、利率和行业经济等宏观指标数据。 |
| `cses` 板块截面函数 | [functions/cses.md](references/functions/cses.md) | [indicators/cses-indicator-category-index.md](references/indicators/cses-indicator-category-index.md) | 在板块维度计算的截面数据；仅支持沪深京股票和养老保障两大类板块。 |
| `ctr` 专题报表 | [functions/ctr.md](references/functions/ctr.md) | [indicators/ctr-indicator-category-index.md](references/indicators/ctr-indicator-category-index.md) | 取专题报表（如 `StockInfo`、`RptXxx` 等 ctrName）。 |

### 交易日工具

| 函数 | 介绍页 | 简要说明 |
| --- | --- | --- |
| `tradedates` 交易日历 | [functions/tradedates.md](references/functions/tradedates.md) | 获取指定交易市场、指定时间区间的交易日序列。 |
| `getdate` 交易日偏移 | [functions/getdate.md](references/functions/getdate.md) | 从基准日按指定市场的交易日历向前/向后偏移 N 个交易日。 |
| `tradedatesnum` 区间交易日数 | [functions/tradedatesnum.md](references/functions/tradedatesnum.md) | 计算指定交易市场在指定时间区间内的交易日个数。 |

### 其他工具

| 函数 | 介绍页 | 简要说明 |
| --- | --- | --- |
| `datastatistics` 流量查询 | [functions/datastatistics.md](references/functions/datastatistics.md) | 查询指定量化接口函数的使用量情况（流量阈值、已使用量、剩余流量等）。 |

---

## 指标/报表索引

按函数分组的"指标目录主索引"和"目录指标详情页"。

| 入口 | 简要说明 |
| --- | --- |
| [indicators/css-indicator-category-index.md](references/indicators/css-indicator-category-index.md) | css 函数支持的指标目录路径与详情页地址。 |
| [indicators/csd-indicator-category-index.md](references/indicators/csd-indicator-category-index.md) | csd 函数支持的指标目录路径与详情页地址。 |
| [indicators/cses-indicator-category-index.md](references/indicators/cses-indicator-category-index.md) | cses 板块截面函数支持的指标目录路径与详情页地址。 |
| [indicators/sector-indicator-category-index.md](references/indicators/sector-indicator-category-index.md) | sector 函数的板块清单导航。 |
| [indicators/ctr-indicator-category-index.md](references/indicators/ctr-indicator-category-index.md) | ctr 函数的报表清单导航。 |

---

## 错误码速查

API 调用返回 `ErrorCode != 0` 时，查阅 [error-codes.md](references/help/error-codes.md) 按含义定位原因；激活相关错误码（`10001020` / `10001019` / `10001009`）的处理见下方「账号相关错误码速查」与 [sdk-setup.md §3](references/sdk-setup.md#3-常见激活错误码)。

---

## 文档约定

- 文档内引用其他文档统一使用**相对链接**，便于离线浏览。
- "可选参数列表"使用 `key=value`，多个参数用半角逗号 `,` 拼接；详见各函数页的「命令拼接教程」段落。
