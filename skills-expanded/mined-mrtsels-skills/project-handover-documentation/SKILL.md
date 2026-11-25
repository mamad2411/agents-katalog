---
name: project-handover-documentation
description: "Structure and write comprehensive project handover / README documents — single source of truth, not scattered. Covers architecture, deployment, database, API, flows, known issues, demo guides."
tags: [documentation, handover, readme, onboarding, deployment-guide]
---

# Project Handover Documentation

> 本技能为交接文档类技能的伞(umbrella),已吸收以下技能(2026-08 合并):
> `handover-document`(面向中国企业甲方,总分结构)、`project-handover-doc`(单文件 README 交接)。
> 完整原文见 `references/absorbed-*.md`。

When writing a handover document or comprehensive README for a project being passed to another developer, follow this structure:

## Principles

- **One document, not scattered** — All information in a single file. Avoid "see docs/XX for details" references to other files.
- **Handover doc is a SEPARATE file** — Write as `HANDBOOK.md`, not a rewrite of `README.md`. README stays as the quick-start overview. The handover doc is the deep-dive companion.
- **Table of contents at top** — Every section numbered, reader can jump to what they need.
- **From-scratch instructions** — Write steps as if the reader has nothing set up. Database creation, config files, the full chain.
- **Facts, not conditions** — Don't say "if the server has no network." The environment is what it is — state it as fact.
- **Pre-configure, don't document as manual steps** — If a setting is known at authoring time (e.g. API IPs), put it in the code/config. The reader should not need to edit files post-deployment.
- **Prioritize: the most important info goes first** — SSH access, service management commands, known issues at the top.

## User-Requested 7-Question Structure

When the user requests a handover doc with the phrase "补充以下内容" or lists numbered requirements, they want the following 7 sections addressed (in this order):

1. **Operation flowcharts** for each user role — show the complete request chain (frontend page → API endpoint → database table → response)
2. **Final AI prompts** — the exact prompts used in production, organized by material type
3. **Complete local startup guide** — from Zero, every command, every dependency
4. **Detailed server deployment** — Step 1, Step 2, ... from blank server to running service
5. **Core database schema** — table relationships, key fields, permission model (how each role's access is enforced)
6. **Demo walkthrough** — step-by-step per role, where the demo data comes from, how to modify it
7. **Known issues** — P0/P1/P2 sorted by severity, with workarounds for demo-day failures

Embed these as numbered sections in a single `HANDBOOK.md`. Use text-based flowcharts (PlantUML or ASCII) inline — PNG images from external tools are not available in most environments.

## Document Structure

```
1. Project Overview (one-liner, tech stack, accounts)
2. From-Scratch Local Startup (Step 1, Step 2, ...)
3. From-Scratch Server Deployment (Step 1, Step 2, ...)
4. Production Environment & Ops (architecture diagram, service commands, log paths)
5. Operation Flowcharts (one per user role — rendered as PNG images)
6. Database Tables & Relationships (entity diagram + key fields table)
7. AI Prompts (final versions)
8. Demo Guide (step-by-step per role, what data to use)
9. Known Issues & Risks (sorted P0→P2 by severity, each with workaround)
10. FAQ / Troubleshooting (common failures and their fix)
```

## Writing Style (user preferences)

This user values directness and hates "AI味":

- **State facts directly.** "服务器无网络" — not "如服务器无网络".
- **Do things in code, not in instructions.** Write `extra_hosts` into docker-compose.yml; don't tell the reader to add it later.
- **Use variables for deploy-time config.** `SERVER_IP="${SERVER_IP:-<内网IP>}"` — don't hardcode IPs.
- **Support all standard flag variations.** `-h`, `--help`, `help` all work. `-v`, `--version`.
- **Auto-detect paths.** CLI tools should find the project root, not assume `/opt/enterprise`.
- **Be concise.** No unnecessary explanation. After a summary, let the user decide if they want details.
- **Documentation vs Mechanism.** When writing deployment docs for a non-technical audience, describe the USER-facing workflow (e.g. "copy to USB"), not the underlying tooling (SSH/SCP). The tool can still use SSH/SCP behind the scenes — the docs just present the workflow the user sees.

## Flowcharts (Existing Images)

If the project already has PNG flowchart images (e.g. in a `references/` directory), reference them directly with standard Markdown image syntax — don't regenerate them or switch to text-only diagrams:

```markdown
![企业端流程图](../references/03-演示汇报/diagrams/enterprise-flow.png)
图下方紧跟一段文字说明：覆盖的流程、涉及的后端接口和数据库表。
```

Prefer existing images over inline ASCII diagrams. Only fall back to PlantUML/ASCII when no images exist.

## Mermaid Diagrams (Recommended over standalone HTML/SVG)

Prefer Mermaid diagrams (`erDiagram`, `classDiagram`, `flowchart TD`) embedded directly in markdown over standalone HTML/SVG files. Mermaid renders natively on GitHub/GitLab and eliminates the "open a separate file" step for readers.

### Mermaid ER Diagram Syntax Pitfalls

Mermaid's ER diagram parser breaks on `/` (slash) in quoted comment strings. Replace with `-`:

```
# BAD — parse error
varchar_32 status "DRAFT/SUBMITTED"
# GOOD
varchar_32 status "DRAFT-SUBMITTED"
```

### Mermaid Verification Protocol

Markdown previewers silently fail on broken Mermaid — always verify syntax before committing.

1. Write a minimal test HTML loading mermaid from CDN:

```html
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
```

2. Open in browser, then run in console:

```js
mermaid.parse(`erDiagram
    table1 ||--o{ table2 : "fk"
`)
// Returns true if valid, throws with line number if invalid
```

3. Fix the reported line (usually `/` in comments, sometimes unclosed braces), re-test

4. Only after parse succeeds, embed the diagram in the markdown file

The `/` restriction also applies to `flowchart` node labels — any `"/"` inside quoted strings causes parse failure.

### Architecture Flowcharts

Use `flowchart TD` with `subgraph` blocks for each layer; keep node text concise and add layer descriptions in plain text below the diagram.

### Three-Diagram Pattern for Database Docs

| Diagram | Type | Where |
|---------|------|-------|
| ER diagram (relationships + fields) | `erDiagram` | DATABASE.md |
| Entity class diagram (inheritance) | `classDiagram` | DATABASE.md |
| Brief table overview (no fields) | `erDiagram` (lines only) | README/HANDBOOK |

### Mermaid Verification Protocol

1. Load `mermaid@10` from CDN in a test HTML page
2. Open in browser — check for "Syntax error in text"
3. Use `mermaid.parse()` in console to find exact failure line
4. Fix (usually `/` in comments), re-test

```html
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
```

## Cross-Document CLI Consistency

When docs span multiple files (README, HANDBOOK, DEPLOY, CLAUDE), ensure the CLI command table is **identical** across all of them. Diverge once and each file becomes a time capsule of an old state.

### Audit Procedure

1. `grep -rn "enterprise " *.md docs/*.md` — collect all references
2. Compare against the CLI's `usage()` function — that's the source of truth
3. Add missing commands, remove stale ones
4. Verify descriptions match what the CLI actually does, not what it used to do

```markdown
enterprise start       # 启动
enterprise status      # 状态
enterprise stop        # 停止
enterprise restart     # 重启
enterprise update      # 代码热更新
enterprise setup       # 配置 AI
enterprise check-ai    # 测试 AI
enterprise logs        # 查看日志
enterprise logs -f     # 实时跟踪
enterprise logs backend   # 只看后端日志
enterprise logs nginx     # 只看 Nginx 日志
enterprise logs frontend  # 只看前端上报日志
enterprise logs search <词> # 跨文件搜索
enterprise ssh          # SSH 连接信息
enterprise uninstall    # 卸载
```

## Deployment Update Documentation Pitfalls

When documenting code update workflows, the docs must match the **actual CLI behavior**, not an idealised workflow.

### Common Mismatches

| Doc says | CLI actually does |
|----------|------------------|
| "rebuild the Docker image" | `docker cp` JAR/HTML into running container |
| "rename JAR to app.jar" | CLI greps `backend/target/enterprise-mvp-*.jar` directly |
| "restart with systemctl" | `enterprise update` handles stop/copy/start/verify |

### Keep the Real Filename (no app.jar)

The Maven build artifact at `backend/target/enterprise-mvp-0.1.0-SNAPSHOT.jar` is the only correct path. **Never rename it to `app.jar`** or any other name. Copy it to the server with its original name, and the CLI should glob for `backend/target/enterprise-mvp-*.jar` directly.

This applies to any Maven/Gradle project: `update` commands should find the build artifact at its standard path, not require a manual rename step.

### Don't Delete Compile Artifacts

`enterprise update` should not `rm` the JAR after update — the file is needed for incremental compilation on the next build cycle.

## Flowcharts (Existing Images)

If the project already has PNG flowchart images (e.g. in a `references/` directory), reference them directly with standard Markdown image syntax — don't regenerate them or switch to text-only diagrams:

```markdown
![企业端流程图](../references/03-演示汇报/diagrams/enterprise-flow.png)
```

Prefer existing images over inline ASCII diagrams. Only fall back to Mermaid/PlantUML/ASCII when no images exist.

## Database Schema Documentation & Verification

When the handover doc needs a database section — or when the user asks to audit/update existing database docs — follow this four-step pipeline:

### Step 1: Extract the schema

Read both sides:
- **SQL DDL**: `init.sql` (production source of truth if Flyway is not used) + `{migration-dir}/*.sql` (chronological changes)
- **Java entities**: `@Entity` + `@Table(name=...)` classes in the domain package

### Step 2: Cross-reference entities against SQL

Map each Java field to its SQL column:
- Plain field `private String creditCode;` → snake_case → `credit_code`
- Custom `@Column(name="group_name")` — use the explicit name, not the convention
- BaseEntity fields (`id`, `createdAt`, `updatedAt`) are inherited — skip them on both sides

Flag discrepancies:
- **Java fields with no SQL column** — missing column in DDL
- **SQL columns with no Java field** — dead/legacy columns (common after migrations)
- **Near-duplicate columns** (`ip_class1self` vs `ip_class1_self`) — a migration added a second column instead of reusing the first

### Step 3: Audit the migration chain

Flyway migrations need to work IN ORDER from a blank database. Check for:
- Two migrations that `CREATE TABLE` with the same name — the second one fails
- `ALTER TABLE ADD COLUMN` without `IF NOT EXISTS` on re-runnable scripts
- Chinese characters in column names — accidental, not intentional
- DROP of a table that a later migration references

If the project uses `init.sql` (single DDL snapshot) in production instead of Flyway, note that migration errors are latent — they affect fresh Flyway rebuilds but not production deployments.

### Step 4: Generate documentation artifacts

1. **DATABASE.md** — full field reference: every table with every column (name, type, constraint, business meaning)
2. **ER diagram** — standalone HTML with inline SVG, color-coded by table type, entity class name annotated on each table header
3. **Deduplicate**: one authoritative location (DATABASE.md); other docs (HANDBOOK.md, SCHEMA.md, README.md) redirect or summarize

Full working pipeline (Python cross-reference code, migration audit commands, ER diagram template) → `references/database-schema-verification.md`

## Sensitive Info Consolidation

Before handing over a project, consolidate all secrets into a single authoritative file and cross-reference everywhere else. This prevents the next maintainer from hunting through 12 files for the production password.

**Pattern:** `docs/CONFIDENTIAL.md`

```
# 敏感配置信息
> ⚠️ 本文件集中记录所有敏感配置项，其他文档已移除具体值，改为引用本文件。

## 服务器
| 公网入口 | `https://...` |
## 登录账号
## 数据库
## API / 第三方服务
## JWT / 认证
## 已知安全风险
```

**Procedure:**
1. Inventory every doc, script, and config file that contains a password, IP, domain, API key, or connection string
2. Copy each value into the appropriate section of CONFIDENTIAL.md (deduplicate: each fact appears once)
3. In each source file, replace the inline value with a `参见 CONFIDENTIAL.md` link/note
4. For credentials needed in scripts (curl, docker exec, mysql), use `***` placeholders with a comment referencing CONFIDENTIAL.md
5. For config files with env-var overrides (application.yml), use env vars as the primary mechanism and only reference CONFIDENTIAL.md for the defaults
6. Verify: `grep -rn` for every known password/IP across all files — zero hits outside CONFIDENTIAL.md

## Cross-File Path Consistency Audit

When maintaining a project with multiple scripts, configs, and dockfiles, paths can silently diverge. Always audit the full pipeline before a handover.

**Common divergence patterns:**

| Pattern | How it breaks |
|---------|---------------|
| Docker compose volume path vs CLI log dir | Compose writes to `docker/logs/`, CLI reads from `logs/` — never the twain meet |
| Nginx location vs backend endpoint | `nginx` proxies `/files/` to backend, but backend serves at `/api/documents/files/{id}` — dead config |
| `cp` vs `Copy-Item` behavior | `cp -r dir /Volumes/U盘/` copies the dir; `Copy-Item $ROOT F:\target -Recurse` copies the contents. Install script expects one, deploy script produces the other |
| Relative paths in `docker-compose.yml` | `./logs` resolves relative to the **compose file's directory**, not the working directory. If compose is in `docker/`, `./logs` → `docker/logs/` |

**Audit checklist:**

1. **Script paths** — For every `.sh`, `.ps1`, `Dockerfile`: trace each path reference. Is it relative or absolute? Does the target file/dir actually exist at that resolution? Do `dirname $0` and `$(pwd)` resolve as expected?

2. **Config paths** — application.yml, .env, nginx.conf: do the volumes, roots, upstreams, and data-source URLs match what the containers actually expose?

3. **Doc paths** — Every `cp -r /Volumes/U盘/`, `cd /path/to/enterprise`, `-f docker/docker-compose.yml`: are they consistent with the actual project structure? Do the deploy, install, and update sequences agree?

4. **Log path alignment** — Verify that:
   - `docker-compose.yml` volumes use `../logs` (not `./logs`) when the compose file is in a `docker/` subdirectory
   - The CLI tool's LOG_DIR matches where compose writes logs
   - Log cleanup scripts (`logclean.sh`) target the same directory

5. **Nginx upstreams** — Every `location` block should map to an actual backend endpoint. Dead locations (no matching controller or service endpoint) accumulate silently.

## PlantUML Flowcharts

Render sequence/activity diagrams as PNG and embed in the document:

```python
# Python encoding for PlantUML web API
import zlib

ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"

def puml_encode(text):
    raw = zlib.compressobj(9, zlib.DEFLATED, -zlib.MAX_WBITS)
    compressed = raw.compress(text.encode('utf-8')) + raw.flush()
    # PlantUML custom base64
    result = []
    i = 0
    data = compressed
    while i < len(data):
        if len(data) - i >= 3:
            b = (data[i] << 16) | (data[i+1] << 8) | data[i+2]
            result += [ALPHABET[(b >> 18) & 0x3F], ALPHABET[(b >> 12) & 0x3F],
                       ALPHABET[(b >> 6) & 0x3F], ALPHABET[b & 0x3F]]
            i += 3
        elif len(data) - i == 2:
            b = (data[i] << 16) | (data[i+1] << 8)
            result += [ALPHABET[(b >> 18) & 0x3F], ALPHABET[(b >> 12) & 0x3F],
                       ALPHABET[(b >> 6) & 0x3F]]
            i += 2
        else:
            b = (data[i] << 16)
            result += [ALPHABET[(b >> 18) & 0x3F], ALPHABET[(b >> 12) & 0x3F]]
            i += 1
    return '~1' + ''.join(result)

# Usage:
url = 'https://www.plantuml.com/plantuml/png/' + puml_encode(plantuml_source)
```

## Deployment CLI Tool Pattern

When creating a management CLI for a project:

```bash
# Auto-detect project root (don't hardcode)
find_project_root() {
  for dir in "$APP_HOME" /opt/app /srv/app ~/app; do
    [ -f "$dir/docker-compose.yml" ] && echo "$dir" && return 0
  done
  # Fallback: script location
  dirname "$(readlink -f "$0")"
}
```

- Support `start`, `stop`, `restart`, `status`, `logs` commands
- `enterprise -h`, `enterprise --help`, `enterprise help` all work
- `enterprise -v`, `enterprise --version` show version
- `enterprise logs -f` tails

### Interactive Prompts in set -euo pipefail Scripts

When using `read -p` in a script with `set -euo pipefail`, `read` returns non-zero on EOF (non-TTY input or piped input), which kills the script. The safe pattern:

```bash
# ❌ BAD — crashes on non-TTY
read -p "Enter value: " VAR

# ✅ GOOD — survives non-TTY
INPUT_VAR=""; read -p "Enter value [${DEFAULT}]: " INPUT_VAR || true
VAR="${INPUT_VAR:-$DEFAULT}"
```

This pattern is required for all `enterprise setup`-style interactive commands that might be tested in automated environments.

### Setup & Uninstall Commands

Add `setup` and `uninstall` to any deployment CLI:

- **`setup`**: interactively prompt for config values (URL, API Key, model) with defaults; write to `.env` AND runtime config file
- **`uninstall`**: stop containers (`down -v`), delete Docker images, clean logs/uploads/.env, remove systemd service; ask for confirmation first (`[y/N]`)

## Incorporating Code Review into Documentation

When a code review document is provided, incorporate its findings into the "Known Issues" section:
- Rate issues P0 (security/critical), P1 (robustness), P2 (maintainability)
- For each issue: source file:line, impact, and a specific workaround
- Preserve the reviewer's original severity labels
