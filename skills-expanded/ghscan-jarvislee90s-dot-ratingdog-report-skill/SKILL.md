# Ratingdog 评级报告抓取 Skill 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 创建一个 skill，从 ratingdog.cn 抓取公司 YY 评级信用分析数据，按三种主体模板（产业/城投/金融）重组文字分段，生成标准化的衡泰评级报告 Markdown 文件。

**Architecture:** Python 脚本 `fetch_ratingdog.py` 负责登录 API→搜索公司→获取 JSON 并保存临时文件。SKILL.md 工作流清单指导 agent 读取 JSON→根据 issuerType 选择模板→按板块顺序和编号规则重组文字→输出 .md 文件。两者通过 JSON 临时文件解耦。

**Tech Stack:** Python 3 + requests 库；SKILL.md（Markdown 指令文档）

**设计文档:** `docs/superpowers/specs/2026-07-02-ratingdog-scraper-skill-design.md`

---

## 文件结构

```
C:/Users/bunny/.agents/skills/ratingdog-report/
├── SKILL.md                    # 工作流清单（指导agent执行）
├── fetch_ratingdog.py          # Python数据获取脚本
└── reference/
    └── 安福县海能实业-衡泰评级报告_2026-06-11.md  # 参考案例
```

---

## Task 1: 创建 skill 目录结构和参考文件

**Files:**
- Create: `C:/Users/bunny/.agents/skills/ratingdog-report/` (目录)
- Copy: `C:/Users/bunny/.agents/skills/ratingdog-report/reference/安福县海能实业-衡泰评级报告_2026-06-11.md`

- [ ] **Step 1: 创建目录结构**

```bash
mkdir -p "C:/Users/bunny/.agents/skills/ratingdog-report/reference"
```

- [ ] **Step 2: 复制参考案例文件到 skill 目录**

```bash
cp "C:/Users/bunny/Desktop/转债/安福县海能实业股份有限公司/安福县海能实业股份有限公司-衡泰评级报告_2026-06-11.md" "C:/Users/bunny/.agents/skills/ratingdog-report/reference/安福县海能实业-衡泰评级报告_2026-06-11.md"
```

- [ ] **Step 3: 确认 .env 文件存在且包含凭据**

确认 `E:/LLMproject/YY-webreport/.env` 文件存在，内容包含：
```
RATINGDOG_PHONE=17891946810
RATINGDOG_PASSWORD=QWEqwe123,
```

- [ ] **Step 4: 验证目录结构**

```bash
ls -la "C:/Users/bunny/.agents/skills/ratingdog-report/"
```
Expected: 显示 `reference/` 目录

---

## Task 2: 编写 Python 数据获取脚本 `fetch_ratingdog.py`

**Files:**
- Create: `C:/Users/bunny/.agents/skills/ratingdog-report/fetch_ratingdog.py`

这是完整的 Python 脚本，负责：从 .env 读取凭据 → 登录 API → 搜索公司 → 获取详情 JSON → 保存临时文件。

- [ ] **Step 1: 编写完整的 fetch_ratingdog.py 脚本**

```python
#!/usr/bin/env python3
"""fetch_ratingdog.py - 从 ratingdog.cn 获取公司信用分析 JSON 数据

用法:
    python fetch_ratingdog.py --company "公司名" --output-dir "输出目录" [--year 2025]

输出:
    - 原始 JSON 保存到 {output-dir}/.ratingdog_raw.json
    - stdout 打印关键信息（公司名、主体类型、更新日期、JSON文件路径）
"""

import argparse
import json
import os
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    print("错误: 需要 requests 库，请运行 pip install requests", file=sys.stderr)
    sys.exit(1)


# --- API 端点 ---
AUTH_URL = "https://auth.ratingdog.cn/api/TokenAuth/Authenticate"
SEARCH_URL = "https://host.ratingdog.cn/api/services/app/CommonLookup/GetAutoCompletesForFilter"
DETAIL_URL = "https://host.ratingdog.cn/api/services/app/Issuer/GetIssuerDetail"


def load_env(env_path):
    """从 .env 文件读取凭据"""
    if not os.path.exists(env_path):
        # 尝试当前工作目录
        env_path = os.path.join(os.getcwd(), ".env")
    if not os.path.exists(env_path):
        print(f"错误: 未找到 .env 文件 (查找路径: {env_path})", file=sys.stderr)
        sys.exit(1)

    phone = None
    password = None
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("RATINGDOG_PHONE="):
                phone = line.split("=", 1)[1]
            elif line.startswith("RATINGDOG_PASSWORD="):
                password = line.split("=", 1)[1]

    if not phone or not password:
        print("错误: .env 文件中缺少 RATINGDOG_PHONE 或 RATINGDOG_PASSWORD", file=sys.stderr)
        sys.exit(1)

    return phone, password


def login(phone, password):
    """登录 API，返回 accessToken"""
    payload = {
        "tenancyName": "",
        "usernameOrEmailAddress": phone,
        "password": password,
    }
    headers = {
        "Content-Type": "application/json",
        "Origin": "https://www.ratingdog.cn",
        "Referer": "https://www.ratingdog.cn/",
    }
    try:
        resp = requests.post(AUTH_URL, json=payload, headers=headers, timeout=15)
    except requests.exceptions.RequestException as e:
        print(f"错误: 登录请求失败 - {e}", file=sys.stderr)
        sys.exit(1)

    if resp.status_code != 200:
        print(f"错误: 登录失败 (HTTP {resp.status_code})", file=sys.stderr)
        sys.exit(1)

    data = resp.json()
    if not data.get("success"):
        msg = data.get("error", {}).get("message", "未知错误")
        details = data.get("error", {}).get("details", "")
        print(f"错误: 登录失败 - {msg} ({details})", file=sys.stderr)
        sys.exit(1)

    return data["result"]["accessToken"]


def search_issuer(token, company_name):
    """搜索公司，返回 issuerId"""
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "filter": company_name,
        "AutoCompleteTypes": 1001,
    }
    try:
        resp = requests.get(SEARCH_URL, headers=headers, params=params, timeout=15)
    except requests.exceptions.RequestException as e:
        print(f"错误: 搜索请求失败 - {e}", file=sys.stderr)
        sys.exit(1)

    if resp.status_code != 200:
        print(f"错误: 搜索失败 (HTTP {resp.status_code})", file=sys.stderr)
        sys.exit(1)

    data = resp.json()
    issuers = data.get("result", {}).get("issuers", [])

    if not issuers:
        print(f'错误: 未找到公司 "{company_name}"', file=sys.stderr)
        sys.exit(1)

    # 优先精确匹配
    for issuer in issuers:
        if issuer["label"] == company_name:
            return issuer["value"], issuer["label"]

    # 取第一个结果，提示用户
    issuer = issuers[0]
    print(f'提示: 未精确匹配，取第一个结果: {issuer["label"]} (搜索词: {company_name})', file=sys.stderr)
    return issuer["value"], issuer["label"]


def get_issuer_detail(token, issuer_id):
    """获取主体详情 JSON"""
    headers = {"Authorization": f"Bearer {token}"}
    params = {"id": issuer_id}
    try:
        resp = requests.get(DETAIL_URL, headers=headers, params=params, timeout=30)
    except requests.exceptions.RequestException as e:
        print(f"错误: 获取详情失败 - {e}", file=sys.stderr)
        sys.exit(1)

    if resp.status_code != 200:
        print(f"错误: 获取详情失败 (HTTP {resp.status_code})", file=sys.stderr)
        sys.exit(1)

    data = resp.json()
    if not data.get("success"):
        print(f"错误: 获取详情失败 - {data.get('error', {}).get('message', '未知错误')}", file=sys.stderr)
        sys.exit(1)

    return data["result"]


def select_credit_analysis(detail, year=None):
    """从详情 JSON 中选取指定年份的信用分析，默认取最新"""
    analyses = detail.get("creditAnalyses", [])
    if not analyses:
        return None

    if year:
        for a in analyses:
            if a.get("financialYear") == year:
                return a
        print(f"警告: 未找到 {year} 年报数据，回退到最新年份", file=sys.stderr)

    # 按 financialYear 降序，取最新
    analyses.sort(key=lambda x: x.get("financialYear", 0), reverse=True)
    return analyses[0]


def main():
    parser = argparse.ArgumentParser(description="从 ratingdog.cn 获取公司信用分析 JSON")
    parser.add_argument("--company", required=True, help="公司名称")
    parser.add_argument("--output-dir", required=True, help="输出目录（JSON临时文件存放于此）")
    parser.add_argument("--year", type=int, default=None, help="指定年报年份（可选，默认最新）")
    args = parser.parse_args()

    # 1. 加载凭据
    # 优先从 output-dir 的上级查找 .env，再从当前工作目录查找
    env_candidates = [
        os.path.join(os.path.dirname(args.output_dir.rstrip("/\\")), ".env"),
        os.path.join(os.getcwd(), ".env"),
    ]
    env_path = None
    for candidate in env_candidates:
        if os.path.exists(candidate):
            env_path = candidate
            break
    if not env_path:
        # 默认用项目根目录
        env_path = "E:/LLMproject/YY-webreport/.env"

    phone, password = load_env(env_path)

    # 2. 登录
    token = login(phone, password)

    # 3. 搜索公司
    issuer_id, issuer_label = search_issuer(token, args.company)

    # 4. 获取详情
    detail = get_issuer_detail(token, issuer_id)

    # 5. 选取信用分析
    analysis = select_credit_analysis(detail, args.year)
    if not analysis:
        print(f'错误: {issuer_label} 暂无信用分析数据', file=sys.stderr)
        sys.exit(1)

    # 6. 准备输出
    issuer_type = detail.get("issuerType")
    issuer_type_name = detail.get("issuerTypeName", "未知")
    public_date = analysis.get("publicDate", "未知日期")

    # 将选取的 analysis 信息追加到 detail 中，方便 agent 读取
    detail["_selectedAnalysis"] = {
        "financialYear": analysis.get("financialYear"),
        "publicDate": public_date,
        "creditAnalysis": analysis.get("creditAnalysis"),
        "basicTypes": analysis.get("basicTypes", []),
    }

    # 7. 保存 JSON
    output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)
    json_path = os.path.join(output_dir, ".ratingdog_raw.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(detail, f, ensure_ascii=False, indent=2)

    # 8. 打印关键信息到 stdout
    print(f"公司名: {detail.get('issuerName', issuer_label)}")
    print(f"主体类型: {issuer_type_name} (issuerType={issuer_type})")
    print(f"更新日期: {public_date}")
    print(f"JSON文件: {json_path}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: 验证脚本语法正确**

Run: `python -c "import py_compile; py_compile.compile('C:/Users/bunny/.agents/skills/ratingdog-report/fetch_ratingdog.py', doraise=True)"`
Expected: 无输出（语法正确）

- [ ] **Step 3: 用产业主体测试脚本**

Run:
```bash
python "C:/Users/bunny/.agents/skills/ratingdog-report/fetch_ratingdog.py" --company "广州洁特生物过滤股份有限公司" --output-dir "E:/LLMproject/YY-webreport"
```
Expected: stdout 打印4行（公司名、主体类型、更新日期、JSON文件路径），生成 `.ratingdog_raw.json` 文件

- [ ] **Step 4: 验证 JSON 文件内容正确**

Run:
```bash
python -c "import json; d=json.load(open('E:/LLMproject/YY-webreport/.ratingdog_raw.json','r',encoding='utf-8')); print(d['issuerName']); print(d['issuerType']); print(d['_selectedAnalysis']['publicDate']); print(len(d['_selectedAnalysis']['basicTypes']))"
```
Expected:
```
广州洁特生物过滤股份有限公司
1001
2026-07-01
5
```

- [ ] **Step 5: 用城投主体测试脚本**

Run:
```bash
python "C:/Users/bunny/.agents/skills/ratingdog-report/fetch_ratingdog.py" --company "上海城投（集团）有限公司" --output-dir "E:/LLMproject/YY-webreport"
```
Expected: stdout 打印主体类型为"城投 (issuerType=1002)"

- [ ] **Step 6: 用金融主体测试脚本**

Run:
```bash
python "C:/Users/bunny/.agents/skills/ratingdog-report/fetch_ratingdog.py" --company "齐商银行股份有限公司" --output-dir "E:/LLMproject/YY-webreport"
```
Expected: stdout 打印主体类型为"金融 (issuerType=1003)"

- [ ] **Step 7: 清理测试产生的临时文件**

Run:
```bash
rm -f "E:/LLMproject/YY-webreport/.ratingdog_raw.json"
```

---

## Task 3: 编写 SKILL.md 工作流清单

**Files:**
- Create: `C:/Users/bunny/.agents/skills/ratingdog-report/SKILL.md`

这是 SKILL.md 文件，指导 agent 如何执行整个工作流。需要明确区分哪些步骤是脚本职责、哪些是 agent 职责。

- [ ] **Step 1: 编写完整的 SKILL.md 文件**

```markdown
# Ratingdog 评级报告抓取

从 ratingdog.cn 抓取公司 YY 评级信用分析数据，按标准化板块顺序和内部分段结构，生成 `XX公司-衡泰评级报告_更新日期.md` 文件。

## 触发条件

用户提供公司名 + 输出目录，要求从 ratingdog 生成衡泰评级报告。

## 输入参数

- **公司名**: 要抓取的公司全称或简称
- **输出目录**: 生成的 .md 文件保存目录

## 工作流程

### Step 1: 数据获取【脚本职责 — agent 只需执行命令，不介入数据获取过程】

执行 Python 脚本获取原始 JSON 数据：

```bash
python "C:/Users/bunny/.agents/skills/ratingdog-report/fetch_ratingdog.py" --company "{公司名}" --output-dir "{输出目录}"
```

脚本会自动完成以下操作（agent 不需要关心细节）：
1. 从 `.env` 文件读取 ratingdog 账号密码
2. 调用登录 API 获取 token
3. 搜索公司名获取 issuerId
4. 调用 GetIssuerDetail API 获取完整 JSON
5. 将原始 JSON 保存到 `{输出目录}/.ratingdog_raw.json`

脚本执行后，读取 stdout 输出的 4 行信息：
- `公司名`: 主体全称
- `主体类型`: 产业/城投/金融 (issuerType=1001/1002/1003)
- `更新日期`: 报告更新日期（用于输出文件名）
- `JSON文件`: 临时 JSON 文件路径

**如果脚本失败**（退出码非零）：
- 按 stderr 错误信息提示用户
- 如果是登录失败，提示用户检查 `.env` 文件中的 `RATINGDOG_PHONE` 和 `RATINGDOG_PASSWORD`
- 如果是搜索无结果，提示用户检查公司名
- 不自动重试（避免账号锁定）

### Step 2: 读取 JSON 并选择模板【agent 职责】

1. 读取 `{输出目录}/.ratingdog_raw.json` 文件
2. 读取 `_selectedAnalysis` 字段中的数据：
   - `publicDate` — 记录此日期，用于输出文件名
   - `creditAnalysis` — 总览段落（城投主体中含全部内容）
   - `basicTypes[]` — 分块内容（产业5块/金融4块/城投为空）
3. 读取 `issuerType` 字段选择模板：
   - `1001` → 产业主体模板
   - `1002` → 城投主体模板
   - `1003` → 金融主体模板
4. 如果 `creditAnalyses` 为空或 `_selectedAnalysis` 不存在，提示"该公司暂无信用分析数据"，不生成文件，终止流程

### Step 3: 文字重组【agent 职责 — 核心步骤】

根据所选模板，按以下规则重组文字。**务必区分规则处理和 LLM 判断处理**。

#### 通用格式规则（所有模板共用）

1. **`#` 分隔处理**: JSON 中 `content` 和 `creditAnalysis` 使用 `#` 分隔摘要句和详细内容。输出时保留摘要句作为段落首句，紧接详细内容，去掉 `#` 符号。如果内容中有多个 `#`，每个 `#` 后的内容紧接前文，不另起段落
2. **编号统一**: 输出统一使用 `（1）（2）（3）` 全角括号格式。无论 JSON 中是 `1）2）` 还是 `（1）（2）` 或 `(1)(2)`，输出时统一为 `（1）（2）（3）`
3. **空行分隔**: 各板块之间用一个空行分隔，板块内子段连续无空行
4. **文件首行**: 公司全称，不加任何前缀，不加 `#` 标题标记

#### 产业主体模板 (issuerType=1001)

`_selectedAnalysis.basicTypes[]` 含5个分块，按 basicType 编号查找。

**输出板块顺序**（注意与 API 原始顺序不同）：

| 顺序 | 输出板块 | 数据来源 (basicType) | 重组规则 |
|-----|---------|---------------------|---------|
| 1 | 【股东背景】 | basicType=1002 的 content | 去掉 `#`，摘要句+正文合并为连续一段 |
| 2 | 【所处行业】 | basicType=1001 的 content | 同上 |
| 3 | 【经营情况】 | basicType=1003 的 content | 去掉 `#`。正文中的编号子段（`1）2）` 或 `（1）（2）` 等）拆分后，由 agent（LLM）判断每个子段属于哪个维度（生产/采购/销售/其他），按 生产→采购→销售→其他 排序，编号统一为 `（1）（2）（3）`。也可能按业务板块分段，同样由 agent 判断 |
| 4 | 【财务情况】 | basicType=1004 的 content | 去掉 `#`。正文中的编号子段拆分后，按 盈利→资产→负债→其他 排序，编号统一为 `（1）（2）（3）` |
| 5 | 【总结】 | `_selectedAnalysis.creditAnalysis` | 直接取总览段落，不加编号 |
| 6 | 【重点关注】 | basicType=1005 的 content | 按 `（1）（2）` 或 `1）2）` 拆分为列表项，编号统一为 `（1）（2）（3）` |

#### 城投主体模板 (issuerType=1002)

`_selectedAnalysis.basicTypes` 为空数组，全部内容在 `_selectedAnalysis.creditAnalysis` 一个字段中。

**输出板块顺序**：

| 顺序 | 输出板块 | 重组规则 |
|-----|---------|---------|
| 1 | 【股东背景】 | 从 `creditAnalysis` 中识别含"实控人""国资委""股东""控股"等关键词的句子，提取组成一段。由 agent（LLM）判断哪些内容属于股东背景 |
| 2 | 【区域环境】 | 从 JSON 的 `ctExtendInfo.regionalAnalysis.regionalAnalysis` 字段直接取全文 |
| 3 | 【经营情况】 | 从 `creditAnalysis` 中识别"经营方面"开头的段落，或按业务板块（如水务/环境/置业/路桥）描述的内容。按 `（1）（2）（3）（4）` 拆分子段，编号统一为全角括号。由 agent（LLM）判断如何分段 |
| 4 | 【财务情况】 | 从 `creditAnalysis` 中识别"财务方面"开头的段落。按资产/负债/或有负债/授信等维度分段子段，编号统一为 `（1）（2）（3）`。由 agent（LLM）判断 |
| 5 | 【总结】 | 从 `creditAnalysis` 中提取 `#...#` 包裹的总结句，或末尾的总结性语句 |
| 6 | 【重点关注】 | 如果原文无此板块，由 agent（LLM）从全文内容中提取 3-4 条主要风险点，用 `（1）（2）（3）` 编号 |

#### 金融主体模板 (issuerType=1003)

`_selectedAnalysis.basicTypes[]` 含4个分块。

**输出板块顺序**：

| 顺序 | 输出板块 | 数据来源 (basicType) | 重组规则 |
|-----|---------|---------------------|---------|
| 1 | 【公司治理】 | basicType=1006 的 content | 去掉 `#`，摘要句+正文合并为连续一段 |
| 2 | 【经营情况】 | basicType=1003 的 content | 去掉 `#`。正文按资产/贷款质量/盈利等维度分段，由 agent（LLM）判断维度归属，编号统一为 `（1）（2）（3）` |
| 3 | 【财务情况】 | basicType=1004 的 content | 去掉 `#`。正文按负债/存款结构等分段，编号统一为 `（1）（2）（3）` |
| 4 | 【监管指标】 | basicType=1007 的 content | 去掉 `#`。正文按资本充足率/拨备覆盖率等分段，编号统一为 `（1）（2）（3）` |
| 5 | 【总结】 | `_selectedAnalysis.creditAnalysis` | 直接取总览段落 |
| 6 | 【重点关注】 | 原文无此板块 | 由 agent（LLM）从全文内容中提取 3-4 条主要风险点，用 `（1）（2）（3）` 编号 |

### Step 4: 文件输出【agent 职责】

1. **文件名**: `{公司名}-衡泰评级报告_{publicDate}.md`
   - `公司名` = JSON 中的 `issuerName` 字段
   - `publicDate` = `_selectedAnalysis.publicDate`（即 ratingdog 页面上的"更新日期"）
2. **保存路径**: 用户指定的输出目录
3. **清理**: 生成 .md 文件后，删除临时 JSON 文件 `{输出目录}/.ratingdog_raw.json`
4. **验证**: 读取生成的 .md 文件，确认首行为公司全称、各板块标题格式正确、编号统一为全角括号

## 输出文件格式参考

参见 `reference/安福县海能实业-衡泰评级报告_2026-06-11.md`。格式如下：

```
{公司全称}

【股东背景】
{摘要句}{正文内容}

【所处行业】
{摘要句}{正文内容}

【经营情况】
{摘要句}{正文内容}
（1）{维度1内容}
（2）{维度2内容}
（3）{维度3内容}

【财务情况】
{摘要句}{正文内容}
（1）{盈利内容}
（2）{资产内容}
（3）{负债内容}

【总结】
{总览段落}

【重点关注】
（1）{风险点1}
（2）{风险点2}
（3）{风险点3}
```

## 错误处理

- **脚本失败**（退出码非零）: 按 stderr 提示用户，不生成文件
- **creditAnalyses 为空**: 提示"该公司暂无信用分析数据"，不生成文件
- **内容无法识别段落归属**: 保留原文不强行分段，保持内容完整

## 关键 API 字段速查

```
.ratingdog_raw.json
├── issuerName                    # 公司全称
├── issuerType / issuerTypeName   # 主体类型 (1001产业/1002城投/1003金融)
├── holder                        # 第一大股东
├── nature                        # 企业性质
├── yyRating                      # YY评级
├── externalCreditRatingDisplay   # 外部评级
├── _selectedAnalysis             # 脚本选定的信用分析（按年份）
│   ├── financialYear             # 年份
│   ├── publicDate               # 更新日期（用于文件名）
│   ├── creditAnalysis            # 总览段落（城投主体含全部内容）
│   └── basicTypes[]              # 分块内容（产业5块/金融4块/城投为空）
│       ├── basicType             # 类型编号
│       ├── basicTypeName         # 类型名称
│       └── content               # 内容（#分隔摘要和正文）
├── ctExtendInfo                  # 城投扩展
│   └── regionalAnalysis
│       ├── regionalAnalysis      # 区域分析全文
│       └── datas[]               # 区域经济数据
├── cyExtendInfo                  # 产业扩展
│   └── yyIndustry                # YY行业
└── jrExtendInfo                  # 金融扩展
    └── yyIndustry                # YY行业
```
```

- [ ] **Step 2: 验证 SKILL.md 格式正确**

Run: `head -5 "C:/Users/bunny/.agents/skills/ratingdog-report/SKILL.md"`
Expected: 显示前5行内容，以 `# Ratingdog 评级报告抓取` 开头

---

## Task 4: 端到端测试 — 产业主体

用产业主体（广州洁特生物过滤股份有限公司）做完整端到端测试，验证从脚本到 agent 重组到输出文件的完整流程。

**Files:**
- Test output: `E:/LLMproject/YY-webreport/test_洁特生物-衡泰评级报告_2026-07-01.md`

- [ ] **Step 1: 运行 Python 脚本获取数据**

Run:
```bash
python "C:/Users/bunny/.agents/skills/ratingdog-report/fetch_ratingdog.py" --company "广州洁特生物过滤股份有限公司" --output-dir "E:/LLMproject/YY-webreport"
```
Expected: stdout 打印4行信息，生成 `.ratingdog_raw.json`

- [ ] **Step 2: 按 SKILL.md Step 2-3 执行 agent 重组**

按产业主体模板重组文字：
1. 读取 JSON 中的 `_selectedAnalysis.basicTypes[]`
2. 按 股东背景→所处行业→经营情况→财务情况→总结→重点关注 顺序输出
3. 经营情况按 生产→采购→销售 排序子段
4. 财务情况按 盈利→资产→负债 排序子段
5. 编号统一为 `（1）（2）（3）`
6. 去掉所有 `#` 符号

- [ ] **Step 3: 生成输出文件**

写入 `E:/LLMproject/YY-webreport/test_洁特生物-衡泰评级报告_2026-07-01.md`

- [ ] **Step 4: 验证输出文件格式**

Run: `head -20 "E:/LLMproject/YY-webreport/test_洁特生物-衡泰评级报告_2026-07-01.md"`
Expected:
- 第1行为 `广州洁特生物过滤股份有限公司`
- 包含 `【股东背景】`、`【所处行业】`、`【经营情况】`、`【财务情况】`、`【总结】`、`【重点关注】` 六个板块
- 编号使用 `（1）（2）（3）` 全角括号
- 无 `#` 符号残留

- [ ] **Step 5: 清理测试文件**

```bash
rm -f "E:/LLMproject/YY-webreport/.ratingdog_raw.json" "E:/LLMproject/YY-webreport/test_洁特生物-衡泰评级报告_2026-07-01.md"
```

---

## Task 5: 端到端测试 — 城投主体

用城投主体（上海城投（集团）有限公司）测试，验证城投模板的 creditAnalysis 整段拆分逻辑。

**Files:**
- Test output: `E:/LLMproject/YY-webreport/test_上海城投-衡泰评级报告_2025-08-28.md`

- [ ] **Step 1: 运行 Python 脚本获取数据**

Run:
```bash
python "C:/Users/bunny/.agents/skills/ratingdog-report/fetch_ratingdog.py" --company "上海城投（集团）有限公司" --output-dir "E:/LLMproject/YY-webreport"
```
Expected: stdout 打印主体类型为"城投 (issuerType=1002)"

- [ ] **Step 2: 按城投模板重组**

从 `creditAnalysis` 整段中识别并提取：
1. 股东背景（识别"实控人""国资委"相关内容）
2. 区域环境（从 `ctExtendInfo.regionalAnalysis.regionalAnalysis` 取全文）
3. 经营情况（识别"经营方面"段落，按业务板块分段）
4. 财务情况（识别"财务方面"段落，按资产/负债/或有负债/授信分段）
5. 总结（提取 `#...#` 包裹的总结句）
6. 重点关注（LLM 提取 3-4 条风险点）

- [ ] **Step 3: 生成输出文件并验证**

确认输出文件包含 `【股东背景】`、`【区域环境】`、`【经营情况】`、`【财务情况】`、`【总结】`、`【重点关注】` 六个板块

- [ ] **Step 4: 清理测试文件**

```bash
rm -f "E:/LLMproject/YY-webreport/.ratingdog_raw.json" "E:/LLMproject/YY-webreport/test_上海城投-衡泰评级报告_2025-08-28.md"
```

---

## Task 6: 端到端测试 — 金融主体

用金融主体（齐商银行股份有限公司）测试，验证金融模板的4分块结构和"重点关注"生成逻辑。

**Files:**
- Test output: `E:/LLMproject/YY-webreport/test_齐商银行-衡泰评级报告_2025-09-05.md`

- [ ] **Step 1: 运行 Python 脚本获取数据**

Run:
```bash
python "C:/Users/bunny/.agents/skills/ratingdog-report/fetch_ratingdog.py" --company "齐商银行股份有限公司" --output-dir "E:/LLMproject/YY-webreport"
```
Expected: stdout 打印主体类型为"金融 (issuerType=1003)"

- [ ] **Step 2: 按金融模板重组**

从 `basicTypes[]` 4个分块中提取：
1. 公司治理（basicType=1006）
2. 经营情况（basicType=1003）
3. 财务情况（basicType=1004）
4. 监管指标（basicType=1007）
5. 总结（creditAnalysis 总览段落）
6. 重点关注（LLM 提取 3-4 条风险点）

- [ ] **Step 3: 生成输出文件并验证**

确认输出文件包含 `【公司治理】`、`【经营情况】`、`【财务情况】`、`【监管指标】`、`【总结】`、`【重点关注】` 六个板块

- [ ] **Step 4: 清理测试文件**

```bash
rm -f "E:/LLMproject/YY-webreport/.ratingdog_raw.json" "E:/LLMproject/YY-webreport/test_齐商银行-衡泰评级报告_2025-09-05.md"
```

---

## Self-Review

### Spec coverage 检查

| 设计文档要求 | 对应 Task |
|------------|----------|
| fetch_ratingdog.py（登录→搜索→获取JSON） | Task 2 |
| .env 凭据读取 | Task 2 (load_env 函数) |
| issuerType 搜索匹配策略 | Task 2 (search_issuer 函数) |
| --year 参数及回退逻辑 | Task 2 (select_credit_analysis 函数) |
| stdout 输出关键信息 | Task 2 (main 函数) |
| JSON 临时文件保存 | Task 2 (main 函数) |
| SKILL.md 工作流清单 | Task 3 |
| 脚本/agent 职责区分 | Task 3 (Step 1-4 标注) |
| 产业主体模板 | Task 3 + Task 4 |
| 城投主体模板 | Task 3 + Task 5 |
| 金融主体模板 | Task 3 + Task 6 |
| 通用格式规则（#处理、编号统一、空行、首行） | Task 3 (通用格式规则章节) |
| 错误处理（脚本失败、无数据、无法识别段落） | Task 3 (错误处理章节) |
| 文件名规则（公司名-衡泰评级报告_publicDate.md） | Task 3 (Step 4) |
| 清理临时 JSON | Task 3 (Step 4) |
| 参考案例文件 | Task 1 |

### Placeholder scan

无 TBD/TODO。所有代码和命令都已完整写出。

### Type consistency

- `fetch_ratingdog.py` 中函数名: `load_env`, `login`, `search_issuer`, `get_issuer_detail`, `select_credit_analysis`, `main` — 一致
- SKILL.md 中引用的脚本路径: `C:/Users/bunny/.agents/skills/ratingdog-report/fetch_ratingdog.py` — 一致
- JSON 临时文件路径: `{输出目录}/.ratingdog_raw.json` — 一致
- `_selectedAnalysis` 字段名在脚本和 SKILL.md 中一致
