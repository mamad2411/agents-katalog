---
name: docx-content-patching
description: "Surgical text/image replacement in existing .docx files using python-docx run.text and ZIP-level image swap. Never alter paragraph/run structure or formatting."
tags: [docx, python, word, editing, office]
---

# DOCX Content Patching

Surgical text replacement and image swap in existing `.docx` files — only changes `run.text`, never modifies paragraph/run structure or formatting.

## First Principles

- A `.docx` is ZIP of XML files. Paragraphs and runs are structural — never delete/create them.
- **Only change `run.text`**. Never `p.clear()`, `p.add_run()`, merge paragraphs, or modify fonts/sizes.
- For images: modify the ZIP archive directly (python-docx cannot replace existing images).

## Text Replacement Workflow

### 1. Diagnose — read run structure

```python
from docx import Document

doc = Document("file.docx")
for pi, p in enumerate(doc.tables[0].rows[15].cells[3].paragraphs):
    for ri, run in enumerate(p.runs):
        print(f"P{pi} run[{ri}]: '{run.text}'")
```

### 2. Patch — replace text within runs only

**Simple (all in one run):**
```python
for p in cell.paragraphs:
    for run in p.runs:
        if "old" in run.text:
            run.text = run.text.replace("old", "new")
```

**Text split across multiple runs** (common with Chinese):
```python
runs = p.runs
for i in range(len(runs) - 3):
    if runs[i].text == '3' and runs[i+1].text == '月' and runs[i+2].text == '31' and runs[i+3].text == '日':
        runs[i].text = '6'
        runs[i+2].text = '30'
```

**Checking every adjacent pair** (for `一` + `季度` pattern):
```python
for i in range(len(runs) - 1):
    if runs[i].text == '一' and '季度' in runs[i+1].text[:4]:
        runs[i].text = '二'
```

### 3. Verify

```python
old_kw = [kw for kw in ["2026年3月", "一季度"] if kw in cell.text]
assert not old_kw, f"Old content remains: {old_kw}"
```

## Chinese Text Run Splitting Reference

Word splits CJK characters aggressively — don't assume text is whole in one run:

| Expected | Likely Runs |
|----------|-------------|
| `2026年3月31日` | `20` `2` `6` `年` `3` `月` `3` `1` `日` or `31` |
| `一季度` | `一` `季度权益市场E` (merged with next words) |
| `本季度末权益资产仓位占比为0` | `本季度` `末` `权益` `资产` `仓位占比为` `0` `。` |
| `检查时间` | `检查` `时间` `：` |
| `20` `26` `年` | `20` `2` `6` `年` |

Always inspect run structure with the diagnose step before attempting replacement.

## Image Replacement

python-docx cannot replace images. Modify the ZIP directly. **Always verify which image is which before coding the replacement:**

```python
import zipfile
with zipfile.ZipFile(docx_path, 'r') as zf:
    for name in zf.namelist():
        if 'media' in name:
            data = zf.read(name)
            with open(f'/tmp/{name.replace("/", "_")}', 'wb') as f:
                f.write(data)
```

Use vision_analyze on each extracted image to confirm identity (image1 vs image2). **Do not guess by filesize or name order** — practical experience shows this is error-prone.

Then replace:
```python
import zipfile, shutil

docx_path = "file.docx"
new_img = open("new_screenshot.png", "rb").read()

with zipfile.ZipFile(docx_path, 'r') as zin:
    data = {name: (new_img if name == 'word/media/image1.png' else zin.read(name))
            for name in zin.namelist()}

tmp = docx_path + '.tmp'
with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zout:
    for name, content in data.items():
        zout.writestr(name, content)
shutil.move(tmp, docx_path)
```

## Pitfalls

- **Never use `cell.paragraphs[0].clear()`** — destroys formatting of all runs in that paragraph.
- **Never `cell.paragraphs[-1]._element.getparent().remove(...)`** — deletes paragraph structure.
- **After replacing text in split runs, verify by re-reading the full paragraph text**, not individual runs.
- **Multi-paragraph cells (18-23 paragraphs)** — never merge or delete paragraphs. To replace content across all paragraphs while preserving structure: replace P0 run[0].text with the new full text, then set run.text="" for all runs in subsequent paragraphs. **`len(cell.paragraphs)` must be unchanged after editing.**

## Complete Cell Content Replacement (Multi-Paragraph)

When the NEW content is completely different from old (not just find-and-replace), use this full-replacement pattern:

```python
# Step 1: Put all content in P0's first run
cell.paragraphs[0].runs[0].text = new_full_content

# Step 2: Clear all subsequent paragraphs (keep structure)
for pi in range(1, len(cell.paragraphs)):
    for run in cell.paragraphs[pi].runs:
        run.text = ""

# Step 3: Verify
old_kw = [kw for kw in ["旧日期", "一季度", "旧内容"] if kw in cell.text]
assert not old_kw, f"Old content remains: {old_kw}"
print(f"Paragraphs: {len(cell.paragraphs)} (unchanged)")
```

## Chinese Quote Character Encoding

Chinese left/right double quotes (\u201c \u201d) break Python source code when embedded in `terminal()` heredocs. **Always write scripts containing Chinese quotes as .py files** and execute via `terminal("python3 script.py")`.

```python
# ⛔ WRONG — SyntaxError in heredoc
terminal("""
run.text = run.text.replace("foo", "管理期货(CTA)策略成为一季度最大赢家。")
""")

# ✅ RIGHT — write to .py file first
write_file("scripts/fix_cta.py", '''\
run.text = run.text.replace("foo", "管理期货(CTA)策略成为一季度最大赢家。")
''')
terminal("python3 scripts/fix_cta.py")
```

## Searching Both Body Paragraphs and Tables

**检查时间** (and other date/period fields) may exist in document body paragraphs, not just table cells. The FOF 1-3a files placed it in P5 (document body), while 附件2 files had it in a table cell R1. Always search both:

```python
from docx import Document
doc = Document(path)

# Search ALL paragraphs
for pi, p in enumerate(doc.paragraphs):
    if "2026年3月" in p.text:
        print(f"Date in body P{pi}: {p.text[:60]}")

# Search ALL table cells
for ti, t in enumerate(doc.tables):
    for ri, row in enumerate(t.rows):
        for ci, cell in enumerate(row.cells):
            if "2026年3月" in cell.text:
                print(f"Date in T{ti}R{ri}C{ci}")
```

## Template Filling (Empty Cell Strategy)

Distinct from find-and-replace patching. When filling an **empty template** with values from a source document, the challenge is merged-cell table layouts where multiple mini-tables share the same table row structure.

### 1. Inspect Cell Structure First

Always dump the cell layout before writing:

```python
from docx import Document
from docx.oxml.ns import qn

doc = Document("template.docx")
t = doc.tables[0]
for ri, row in enumerate(t.rows):
    for ci, cell in enumerate(row.cells):
        text = cell.text.strip().replace('\n', '\\n')
        if text:
            tc = cell._tc
            tcPr = tc.find(qn('w:tcPr'))
            span = ""
            if tcPr is not None:
                gs = tcPr.find(qn('w:gridSpan'))
                if gs is not None:
                    span = f"[s{gs.get(qn('w:val'))}]"
            print(f"R{ri:02d} C{ci}{span}: {text[:50]}")
```

### 2. Identify Actual Value Cells

Chinese financial templates often have complex merged-cell layouts:

- **Simple rows:** Label in C0[s2], value area starts at C2. Write to C2.
- **Sub-table rows (e.g. 牌照信息):** Label in C2[s3], value in C5[s2]. Write to C5.
- **Manager-info rows (R19-R22):** Column headers in C2[s3]=职务, C5[s2]=姓名, C7=联系方式. Row labels (总经理/投资经理) are IN C2 — they're the label AND the 职务 column combined. Only write 姓名 to C5, 联系方式 to C7. Do NOT overwrite C2 with a second job title.
- **Ownership structure (R38-R42):** Shares rows with department list on the left. Labels in C0[s2]=股东名称, C2[s2]=性质, C4[s2]=出资额, C6[s2]=股权比例. Write shareholder data to R40-R41, respecting column positions.

### 3. Handle Vertical Merges

python-docx reports all cells in a vertical merge group with the same text as the top cell. **The cells below ARE distinct — writing to them only changes that specific cell, not the merged header.**

```python
# R20 C5 is merged vertically from R19's "姓名" header
# Writing here correctly sets the 姓名 value for 总经理 row
t.rows[20].cells[5].paragraphs[0].text = "莫敏秋（法定代表人）"
```

### 4. Label Overwrite Pitfall

**Do NOT write to a cell that contains a row label unless you intend to replace the label.** In Chinese templates, row labels (总经理, 投资经理, 风控/合规主管) often live in C2-C4, which is also where a 职务 value would go. The template treats the label AS the 职务 — there's no separate cell. Writing a second title here destroys the row identity.

✅ Correct: `w(21, 5, "王志滨")` — writes 姓名 for 投资经理 row
❌ Wrong: `w(21, 2, "资产管理部负责人兼投资经理")` — overwrites "投资经理" label

### 5. Template Sub-Table Patterns (Chinese Financial Forms)

Chinese financial DD templates often pack multiple sub-tables into one large table sharing the same rows. Common patterns:

**Pattern A — License info (R11-R14):**
```
R11: C0[s2]=取得牌照信息 | C2[s3]=牌照类型 | C5[s2]=取得牌照时间
R12: C0[s2]=取得牌照信息 | C2[s3]=私募基金管理人牌照 | C5[s2]=不涉及
```
Write C5 for time value. Leave C2 (label) alone.

**Pattern B — Manager info (R19-R22):**
```
R19: C0[s2]=主要管理人信息 | C2[s3]=职务 | C5[s2]=姓名 | C7=联系方式
R20: C0[s2]=(vMerge)       | C2[s3]=总经理 | C5[s2]=(vMerge) | C7=(vMerge)
```
- C2 already has the row label(=职务). **Write 姓名 to C5 only.**
- C0-C1 are vertically merged from R19 — writing there changes the header, not the row label.
- **Before writing, check:** which cell has the row label? If it's C2, that's also where 职务 would go. The label IS the 职务 — don't write another one.

**Pattern C — Departments + Ownership side-by-side (R31-R42):**
```
Left (C0-C3): dept table         Right (C4-C7): ownership table
R32: 部门名称(C0) | 人数(C2)      R39: 股东名称(C4) | 股权比例(C6)
```
Both sub-tables share the same row indices. Write dept names to C0, counts to C2. Write shareholder names to C4, percentages to C6. Same rows, different columns.

**Pattern D — Simple label→value (R01-R17):**
```
R01: C0[s2]=公司法定中文名称：
```
Write value to C2. Verify C2 is not merged with anything above/below.

### 5. Backup Discipline

**Always back up before ANY write.** Use `shutil.copy2` via Python (handles Unicode filenames safely):

```python
from shutil import copy2
from pathlib import Path

src = Path("template.docx")
bak = src.with_suffix(".bak")
copy2(src, bak)
assert bak.exists(), f"Backup failed: {bak}"
```

Shell `cp` may fail silently on filenames with non-breaking spaces or special Unicode characters. Always verify the backup exists before proceeding.

If backup fails or the `.bak` is missing when you need to restore, **ask the user for a fresh template** — do not attempt to reverse-engineer the damage.

### 6. Sequential Fix Protocol

If the first fill attempt has misaligned cells:

1. **Stop patching immediately.** Don't try to fix individual cells in the damaged file — each patch risks breaking more merged cells.
2. **Restore from backup** — if `.bak` exists: `shutil.copy2(bak, src)`. If it doesn't (Unicode filename issue, encoding failure): **ask the user for a fresh template**. Never attempt damage reversal.
3. **Re-inspect** — dump the clean cell structure with gridSpan and vMerge info (see §1).
4. **Write to value cells only** — use the patterns in §2-4.
5. **Verify immediately** — check no row labels were overwritten:

```python
critical_labels = ["总经理", "投资经理", "风控/合规主管"]
found_all = True
for label in critical_labels:
    found = any(label in cell.text for row in doc.tables[0].rows for cell in row.cells)
    if not found:
        print(f"OVERWRITTEN: '{label}' not found anywhere in table")
        found_all = False
if found_all:
    print("All row labels preserved ✓")
```

### 7. Pattern E — "Long Text = Value Cell"

Many Chinese financial templates use the cell's **descriptive placeholder text as the VALUE cell**. Replace the long explanation with actual data — don't look for an adjacent empty cell:

```python
# Table 1, R2 C1 (存续产品情况 → 产品总规模 value cell):
# Before: "含当前在运行产品总规模与历史总管理产品规模"  ← placeholder
# After:  "8495.35亿元（截至2026年6月30日）"           ← actual value

t1.rows[2].cells[1].paragraphs[0].text = "8495.35亿元（截至2026年6月30日）"
```

**Rule:** If a cell contains a detailed instruction/explanation (not just a short label like "产品总规模"), that cell IS where the value goes. The template designer put the placeholder there to show what kind of data belongs.

**Counter-example:** Short labels like "产品总规模" in C0 are pure labels — leave them alone. Write to C1 (the explanation cell) instead.

### 8. Pattern F — Row Label IS the Value Cell

In manager-info sections (R19-R22 of Chinese DD templates), the row label column (C2-C4, span 3) doubles as the 职务 column. There is no separate 职务 cell:

```
R20: C2[s3]="总经理"       ← this IS the label AND the 职务
R21: C2[s3]="投资经理"     ← this IS the label AND the 职务  
R22: C2[s3]="风控/合规主管"
```

**Do NOT write a second job title to C2** — it overwrites the row label and the row becomes unidentifiable. The template intends the label itself to serve as the 职务.

✅ Write 姓名 to C5 only:
```python
w(21, 5, "王志滨")  # 投资经理的姓名
```

❌ Never write to C2 for these rows:
```python
w(21, 2, "资产管理部负责人兼投资经理")  # OVERWRITES "投资经理" label!
```

If the source document has a specific job title that differs from the row label (e.g. source says "资产管理部负责人兼投资经理" but row label is "投资经理"), **keep the row label** — it's the template's category, not a place to put the detailed title.

### Test and Verify (Template Fills)

```python
# Read back and verify
doc = Document(output_path)
t = doc.tables[0]

# Check critical labels preserved
for label in ["总经理", "投资经理", "风控/合规主管"]:
    found = any(label in cell.text for row in t.rows for cell in row.cells)
    assert found, f"Row label '{label}' was overwritten!"

# Check values written
for ri, ci, expected in [(20, 5, "莫敏秋"), (21, 5, "王志滨"), (22, 5, "杜琨")]:
    actual = t.rows[ri].cells[ci].text
    assert expected in actual, f"R{ri}C{ci}: expected '{expected}', got '{actual[:30]}'"

print("All verifications passed ✓")
```

## Verification Checklist

After any docx edit, confirm:
1. `len(cell.paragraphs)` unchanged from before edit
2. No old keywords remain in BOTH `doc.paragraphs` text AND `cell.text` (search dates and period references in all locations)
3. Spot-check 2-3 paragraphs for correct rendering
4. For images: `len(zipfile.ZipFile(path).namelist())` unchanged
5. For dates: check both the month AND day were correctly updated (e.g. "6月31日" is invalid — verify day matches actual month end)
6. **For template fills:** row labels (总经理/投资经理等) were NOT overwritten by 职务 values — verify `cell.text` still contains the label
7. **For template fills:** back up the original template before first write
- ZIP manipulation loses the original file's EXIF/thumbnail data — acceptable for office docs.