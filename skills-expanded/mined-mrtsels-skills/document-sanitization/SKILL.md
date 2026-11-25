---
name: document-sanitization
description: >
  Extract sensitive data (passwords, IPs, API keys, domains, connection strings)
  from project documentation into a single centralized file, replacing inline
  values with cross-references. Includes verification via grep to catch leaks.
trigger:
  - "User wants to strip sensitive info from docs before open-sourcing, handover, or audit"
  - "clean up confidential data"
  - "extract secrets from docs"
  - "sanitize documentation"
  - "move sensitive info to one place"
---

# Document Sanitization Workflow

## Goal

Consolidate all sensitive information scattered across project documentation into
a single authoritative file (`docs/CONFIDENTIAL.md` or equivalent), then replace
each inline occurrence with a cross-reference. Every piece of sensitive data
appears in exactly one place.

## Step 1 — Identify all documents

Start by listing every `.md` / `.txt` / documentation file in the project:

```bash
find . -name '*.md' -not -path './.git/*' -not -path './node_modules/*' | sort
```

Also check `docker/` subdirectories, `README.md`, `CLAUDE.md`, `HANDBOOK.md`, etc.

## Step 2 — Read and catalog sensitive data

Read each file and extract ALL of the following categories:

| Category | Examples to look for |
|----------|---------------------|
| Server addresses | `exeye.info`, `192.168.x.x`, `/opt/...` |
| Login credentials | `admin/admin123`, inline `username/password` pairs |
| Database | DB name, user, password, port, JDBC URL |
| AI / API | API endpoint URL, model name, env var name, IP whitelist |
| Auth / JWT | algorithm, key description, token fields, expiry |
| Deployment paths | install paths, compose file locations |

Write down each occurrence's **exact value** and **source file** — you'll need both
to replace later.

## Step 3 — Create `docs/CONFIDENTIAL.md`

Structure:

```markdown
# 敏感配置信息

> ⚠️ 本文件集中记录所有敏感配置项，其他文档已移除具体值，改为引用本文件。

## 服务器
| 项目 | 值 |
| ...  | ... |

## 登录账号
| 用户名 | 密码 | 角色 |
| ...   | ...  | ...  |

## 数据库
| 项目 | 值 |

## AI / API
| 项目 | 值 |

## JWT / 认证
| 项目 | 说明 |
```

One section per category. Include **all** values — this is now the single source of truth.

## Step 4 — Patch each source document

For each document file, replace every occurrence of a sensitive value with a
reference to the corresponding section in `CONFIDENTIAL.md`.

**Reference format:**
```
参见 [CONFIDENTIAL.md](CONFIDENTIAL.md#服务器)
参见 [CONFIDENTIAL.md](CONFIDENTIAL.md#登录账号)
```

**In code blocks** (shell commands, curl samples), replace literal passwords with
`***` and add a trailing comment:
```bash
mysql -u enterprise -p*** -e "SELECT 1"  # 密码参见 CONFIDENTIAL.md
```

**In section titles** that embed credentials (e.g. `演示（jinpeng/jinpeng123）`),
rewrite to:
```
演示（jinpeng，密码参见 CONFIDENTIAL.md）
```

**PATCHING STRATEGY — batch by tool:**
- Use `patch` (replace mode) for straightforward find-and-replace in each file.
- For files with many replacements in one region, use `execute_code` with a Python
  script that calls `patch()` repeatedly — the tool batches multiple patches
  per execution efficiently.

## Step 5 — Full grep verification (CRITICAL)

After all patches are applied, run a comprehensive scan. **Do not skip this step —
it always catches at least one missed occurrence.**

```bash
cd /path/to/project

for pattern in "admin123" "jinpeng123" "enterprise123" "root123" \
               "192.168." "exeye.info" "dashscope.aliyuncs.com" \
               "8.152.159.24" "39.96.198.249" "8.140.217.18" "39.96.213.166"; do
  grep -rn "$pattern" --include="*.md" . \
    | grep -v "CONFIDENTIAL.md" \
    | grep -v "references/" \
    | head -5
done
```

Scan all passwords, IPs, domains, API URLs you found in Step 2. Use
`grep -v "CONFIDENTIAL.md"` to exclude the centralized file itself.

## Step 6 — Fix remaining leaks (iterative)

If verification finds anything, patch those specific occurrences (often in section
titles, debug tables, or code examples) and re-verify. Repeat until clean.

## Pitfalls

- **Section titles with inline passwords** are easy to miss — grep checks the
  literal password string, not the section header format, so they show up.
- **Code-block examples** (bash commands, curl samples, SQL) often embed DB
  passwords or API keys — replace with `***` + comment, not a bare reference.
- **Debug/troubleshooting tables** frequently contain `mysql -u enterprise -penterprise123`
  commands — these are inside table cells, not code fences, and easy to overlook.
- **`grep` finds the pattern in the CONFIDENTIAL.md file itself** — always pipe
  through `grep -v "CONFIDENTIAL.md"` to avoid false positives.
- **The reference/ archive directory** may also contain sensitive data — decide
  upfront whether to sanitize it too or flag it as historical/excluded.
- **After mass-patching, re-read key files** to verify patches applied correctly
  (flat replace-mode patches can mis-match tab/space indentation).
- **The CONFIDENTIAL.md itself must not be committed to a public repo** — add
  it to `.gitignore` or warn prominently at the top of the file.
