---
name: pdf-bib-import
version: 1.0.0
description: "将一个文件夹中的多篇 PDF 论文批量提取题录信息（标题、作者、年份、期刊、卷期页码、DOI、摘要），并导入飞书多维表格。当用户需要把一批 PDF 论文的书目信息、题录信息汇总到飞书 Base / 多维表格时触发。关键词：PDF、论文、题录、书目、批量导入、飞书多维表格。"
metadata:
  requires:
    bins: ["lark-cli", "pdftotext", "pdfinfo", "python3"]
---

# PDF 题录批量导入飞书多维表格

## 核心原则（必须遵守）

> **成本控制**：数据提取必须用脚本完成，禁止用 AI 逐篇读取 PDF——每次 AI 读取都消耗大量 token。
>
> 正确流程：**写脚本提取 → 人工/脚本校对 → 脚本批量写入飞书**，AI 只负责生成脚本和配置飞书结构。

---

## Step 1：脚本提取 PDF 题录

### 1.1 生成提取脚本

在 `/tmp` 下生成 `extract_bib.py`，利用 `pdftotext`（`/opt/homebrew/bin/pdftotext`）批量提取：

```python
#!/usr/bin/env python3
"""
extract_bib.py — 从 PDF 目录批量提取题录，输出 bib_data.json
用法：python3 extract_bib.py <pdf_dir>
"""
import os, sys, json, subprocess, re

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True).stdout.strip()

def extract_pdf_meta(path):
    info = run(["/opt/homebrew/bin/pdfinfo", path])
    meta = {}
    for line in info.splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            meta[k.strip()] = v.strip()
    text = run(["/opt/homebrew/bin/pdftotext", "-l", "2", path, "-"])
    return meta, text

def guess_fields(meta, text):
    """从 pdfinfo + 前两页文字中猜测题录字段，返回 dict。"""
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    return {
        "论文题目": meta.get("Title", ""),
        "作者":     meta.get("Author", ""),
        "发表年份": None,
        "期刊名称": "",
        "卷期页码": "",
        "DOI":      "",
        "摘要":     "",
        "_raw_text_preview": "\n".join(lines[:40]),  # 供人工核查
    }

def main():
    pdf_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    results = []
    for fname in sorted(os.listdir(pdf_dir)):
        if not fname.lower().endswith(".pdf"):
            continue
        fpath = os.path.join(pdf_dir, fname)
        meta, text = extract_pdf_meta(fpath)
        rec = guess_fields(meta, text)
        rec["_filename"] = fname
        results.append(rec)
        print(f"  ✓ {fname}")

    out = "/tmp/bib_data.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n已写出 {len(results)} 条记录 → {out}")
    print("请检查 bib_data.json，补全缺失字段后再执行 Step 3 导入。")

if __name__ == "__main__":
    main()
```

运行：

```bash
python3 /tmp/extract_bib.py "/path/to/pdf_folder"
```

### 1.2 校对 JSON（关键步骤）

pdftotext 能提取机器可读 PDF 的文字，但有些 PDF：
- **扫描件**：文字为空，需手动填写
- **元数据为空**：需从 `_raw_text_preview` 字段中判断并手动补全

打开 `/tmp/bib_data.json`，检查并补全各字段，删除 `_raw_text_preview` 和 `_filename`。

---

## Step 2：创建飞书 Base 结构

> **前置条件：** 先阅读 [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md) 了解认证规则。

### 2.1 创建 Base

```bash
lark-cli base +base-create --name "论文题录数据库"
# 记录返回的 base_token
```

### 2.2 获取默认表并重命名

```bash
lark-cli base +table-list --base-token <BASE_TOKEN>
lark-cli base +table-update --base-token <BASE_TOKEN> --table-id <TABLE_ID> --json '{"name":"论文题录"}'
```

### 2.3 配置字段

先重命名默认"文本"字段，再删除多余默认字段，最后创建所需字段：

```bash
# 查看现有字段（记录各字段 id）
lark-cli base +field-list --base-token <BASE_TOKEN> --table-id <TABLE_ID>

# 将默认文本字段重命名为"论文题目"
lark-cli base +field-update --base-token <BASE_TOKEN> --table-id <TABLE_ID> \
  --field-id <TEXT_FIELD_ID> --json '{"type":"text","name":"论文题目","style":{"type":"plain"}}'

# 删除多余默认字段（日期、附件、单选）
lark-cli base +field-delete --base-token <BASE_TOKEN> --table-id <TABLE_ID> --field-id <ID> --yes

# 创建其余字段（串行执行）
cd /tmp
for field in \
  '{"type":"text","name":"作者","style":{"type":"plain"}}' \
  '{"type":"number","name":"发表年份"}' \
  '{"type":"text","name":"期刊名称","style":{"type":"plain"}}' \
  '{"type":"text","name":"卷期页码","style":{"type":"plain"}}' \
  '{"type":"text","name":"DOI","style":{"type":"plain"}}' \
  '{"type":"text","name":"摘要","style":{"type":"plain"}}'; do
  echo "$field" > field.json
  lark-cli base +field-create --base-token <BASE_TOKEN> --table-id <TABLE_ID> --json @field.json
  sleep 0.3
done
```

---

## Step 3：脚本批量写入记录

### 3.1 生成导入脚本

生成 `/tmp/import_to_lark.sh`，从 `/tmp/bib_data.json` 读取记录并逐条写入：

```bash
cat << 'PYEOF' > /tmp/import_to_lark.py
#!/usr/bin/env python3
"""
import_to_lark.py — 从 bib_data.json 批量写入飞书 Base
用法：python3 import_to_lark.py <BASE_TOKEN> <TABLE_ID> [bib_data.json]
"""
import json, sys, subprocess, time, os

def upsert(base_token, table_id, record):
    tmp = "/tmp/_rec.json"
    # 去除空值字段（避免写入空字符串覆盖）
    payload = {k: v for k, v in record.items()
               if not k.startswith("_") and v not in (None, "", 0)}
    # 年份是数字，0 代表未知，保持过滤
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False)
    result = subprocess.run(
        ["lark-cli", "base", "+record-upsert",
         "--base-token", base_token,
         "--table-id", table_id,
         "--json", "@_rec.json"],
        capture_output=True, text=True, cwd="/tmp"
    )
    return json.loads(result.stdout)

def main():
    base_token = sys.argv[1]
    table_id   = sys.argv[2]
    data_file  = sys.argv[3] if len(sys.argv) > 3 else "/tmp/bib_data.json"

    with open(data_file, encoding="utf-8") as f:
        records = json.load(f)

    ok, fail = 0, 0
    for i, rec in enumerate(records, 1):
        title = rec.get("论文题目", rec.get("_filename", f"record-{i}"))
        resp = upsert(base_token, table_id, rec)
        if resp.get("ok"):
            ok += 1
            print(f"  [{i}/{len(records)}] ✓ {title[:60]}")
        else:
            fail += 1
            print(f"  [{i}/{len(records)}] ✗ {title[:60]}: {resp}")
        time.sleep(0.5)   # 避免写入冲突

    print(f"\n完成：{ok} 成功 / {fail} 失败")

if __name__ == "__main__":
    main()
PYEOF

python3 /tmp/import_to_lark.py <BASE_TOKEN> <TABLE_ID> /tmp/bib_data.json
```

---

## 常见问题

| 问题 | 解决方案 |
|------|----------|
| pdftotext 提取为空（扫描件） | 手动填写 bib_data.json，或用 OCR 工具 |
| PDF 元数据乱码 / 错误 | 忽略 meta，从 `_raw_text_preview` 手工提取 |
| lark-cli `--json @file` 报路径错误 | 必须 `cd /tmp` 后再执行，使用相对路径 `@_rec.json` |
| 写入冲突 1254291 | 增大 `time.sleep()` 到 1 秒 |
| 字段不存在 1254045 | 检查字段名拼写，与 `+field-list` 返回结果一致 |

## 成本控制提示

- **不要用 AI 逐篇读取 PDF**：49 篇 PDF 用 AI 提取 ≈ $10，用脚本 ≈ $0
- **数据提取 → 人工校对 → 脚本写入**，AI 只生成脚本
- 遇到 pdftotext 无法提取的字段，集中人工补全 JSON，再统一导入
