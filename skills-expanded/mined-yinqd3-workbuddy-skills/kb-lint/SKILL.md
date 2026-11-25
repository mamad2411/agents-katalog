---
name: kb-lint
description: Run comprehensive health checks on the Obsidian knowledge base including broken wikilinks, orphan pages, stale status, concept page completeness, and status consistency. Trigger phrases: lint knowledge base, knowledge base health check, kb check, run lint, 知识库检查, 健康检查.
agent_created: true
---

# Knowledge Base Lint (kb-lint)

Run health checks on an Obsidian knowledge base using the `lint_kb.py` script. Configure your vault path in the script or pass it as an argument.

## When to Use

- User says "检查知识库", "跑一下 lint", "健康检查", "看看有没有断裂链接"
- After any significant ingest session (adding multiple new papers/projects)
- Before weekly or monthly maintenance
- When troubleshooting `[[wikilink]]` issues

## Available Script

`<your-vault-path>/工具脚本/lint_kb.py` — the comprehensive lint tool. Update `VAULT_PATH` in the script to point to your Obsidian vault.

## Running Checks

> ⚠️ lint 报告**仅输出到终端**，不会写知识库文件。

### Full check (all 5 categories)

```bash
cd "<your-vault-path>" && python "工具脚本/lint_kb.py"
```

### Single category check

```bash
cd "<your-vault-path>" && python "工具脚本/lint_kb.py" --check broken-links
cd "<your-vault-path>" && python "工具脚本/lint_kb.py" --check orphans
cd "<your-vault-path>" && python "工具脚本/lint_kb.py" --check stale
cd "<your-vault-path>" && python "工具脚本/lint_kb.py" --check concept
cd "<your-vault-path>" && python "工具脚本/lint_kb.py" --check consistency
```

### Verbose mode (show detailed progress)

```bash
cd "<your-vault-path>" && python "工具脚本/lint_kb.py" --verbose
```

## Understanding Results

### 5 Check Categories

| Check | What it detects | Typical fixes |
|-------|----------------|--------------|
| Broken wikilinks | `[[目标]]` pointing to non-existent files | Fix filename in link, or create missing card |
| Orphan pages | Pages with zero inbound `[[wikilink]]` | Add cross-references from related cards |
| Stale status | Cards with old `status` (e.g., "投稿中" unmodified >90 days) | Update status field in frontmatter |
| Concept completeness | Concept pages missing linked papers, or papers with matching tags not linked from concept page | Add `related_papers` to concept page frontmatter |
| Status consistency | Projects past end_date still "进行中", students past graduation without update | Update status or date in frontmatter |

### Common Fix Patterns

1. **Broken `[[wikilink]]`**: The target uses `[[../子目录/文件]]` relative paths. Use `Obsidian → Files & Links → Always update internal links: true` to auto-heal on rename.

2. **Stale status**: Check the paper/project status against `日志.md` — if status changed per log but frontmatter wasn't updated, correct it.

3. **Concept page missing refs**: Add the paper's `[[wikilink]]` to the concept page's `related_papers` frontmatter list.

## Maintenance Workflow

**Weekly (recommended)**: Run full lint after each `scan_vault.py` weekly scan.
**Post-ingest**: Run lint after batch-adding 3+ new cards.
**Monthly deep-clean**: Run full lint and fix all issues.
