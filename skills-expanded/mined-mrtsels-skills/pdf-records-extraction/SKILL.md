---
name: pdf-records-extraction
description: Extract structured records (name, ID number, etc.) from repetitive paginated PDFs like exam seating charts, registration forms, or class rosters. Includes page deduplication via connected-components, greedy set cover, CSV output with utf-8-sig BOM, and a CLI search tool with wildcard support.
version: 1.0.0
author: Hermes Agent
tags: [PDF, extraction, dedup, search, csv, education]
---

# PDF Structured Records Extraction

Extract person records (姓名 + 证件号 patterns) from repetitive paginated PDFs, deduplicate, and generate a searchable CSV.

Common use cases: exam seating charts (座次表), class rosters, registration lists where each student appears in two or more exam sessions on different pages.

## Workflow

### 1. Text Extraction & Record Parsing

Use PyMuPDF (fitz) to extract text, then regex for structured records:

```python
import fitz, re

# Match mainland 18-digit ID
pattern_m = re.compile(r'姓名[：:]\s*(\S+)\s*身份证[：:]\s*(\d{17}[\dXx])')
# Match HK/Macau/Taiwan travel permit (H-prefix)
pattern_hk = re.compile(r'姓名[：:]\s*(\S+)\s*港澳台居民来往内地通行证[：:]\s*(\S+)')
```

Store in: `student_info[idnum] = {"name": name, "pages": []}`

### 2. Page Deduplication

Students appear on paired pages (same students in different exam sessions). Build page groups using **connected components** (BFS over shared-students graph):

```python
from collections import defaultdict

page_pairs = defaultdict(set)
for idnum, info in student_info.items():
    for p in info["pages"]:
        for q in info["pages"]:
            if p != q:
                page_pairs[p].add(q)

groups = defaultdict(set)
assigned = set()
gid = 0
for pg in range(1, merged.page_count + 1):
    if pg in assigned: continue
    queue = [pg]
    while queue:
        cur = queue.pop(0)
        if cur in assigned: continue
        assigned.add(cur)
        groups[gid].add(cur)
        for nxt in page_pairs.get(cur, set()):
            if nxt not in assigned: queue.append(nxt)
    gid += 1
```

For each group:
- **Groups with 2 pages** (perfect pairing): keep 1 (identical content).
- **Groups with 4+ pages** (imperfect overlap — some students appear in only one session): use greedy set cover to pick the minimal pages covering all students.

```python
# Greedy set cover for complex groups
uncovered = set(group_students)
group_selected = set()
while uncovered:
    best_pg = max(pages, key=lambda p: len(page_students[p] & uncovered))
    group_selected.add(best_pg)
    uncovered -= page_students[best_pg]
```

### 3. Build Deduped PDF

```python
reduced = fitz.open()
for pg in sorted(selected_pages):
    reduced.insert_pdf(merged, from_page=pg-1, to_page=pg-1)
reduced.save("output.pdf")
```

### 4. CSV Output (utf-8-sig for Excel)

```python
import csv
with open("output.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["姓名", "身份证号", "类型", "页码"])
    writer.writerow([name, idnum, id_type, pages_str])
```

### 5. CLI Search Tool

Build a `search.py` with three modes:
- **Name partial match**: `query in name.lower()`
- **ID wildcard**: replace `*` with `.*` regex, anchor with `^...$`
- **ID substring**: `query in idnum`

## Key Regex Patterns for Chinese Education Documents

| Pattern | Target |
|---------|--------|
| `姓名[：:]\s*(\S+)\s*身份证[：:]\s*(\d{17}[\dXx])` | Mainland ID (18 digits) |
| `姓名[：:]\s*(\S+)\s*港澳台居民来往内地通行证[：:]\s*(\S+)` | HK/Macau/Taiwan permit (H prefixed) |
| `班级[：:]\s*(\S+)` | Class name (e.g., G203) |
| `场次:第(\d+)场` | Exam session number |
| `考场号:(\d+)` | Exam room number |

## Pitfalls

- **HK/Macau students**: use travel permits (H-prefix), not mainland IDs. Always use two separate regexes.
- **utf-8-sig BOM**: required for Excel to recognize Chinese characters in CSV.
- **Duplicate students across sessions**: use ID (not name) as the unique key — names can repeat.
- **Page pairing**: students often appear in two exam sessions (morning/afternoon of different days). The pages are always paired (same content on 2 pages for most, imperfect for last sessions).
- **Single-appearance students**: some students may only appear in one session (e.g., left early on the other day). These force keeping 2+ pages from the last group.
- **Empty pages**: some pages in merged PDF may have 0 extracted students (e.g., divider pages or pages with different document structures). Verify before building output.
