---
name: gh-issues-to-doc
description: 將 GitHub Issues 轉換為 Obsidian 筆記文件。支援取得 issue 內容、留言、sub-issues、附圖下載（含 private repo），並產生結構化的 Obsidian Markdown 文件。觸發關鍵詞：「issue 整理」、「issue 轉文件」、「issue to doc」、「整理 issue」。
metadata:
  version: 1.0.0
---

# GitHub Issues to Obsidian Document

Convert GitHub issues (including sub-issues, comments, and images) into structured Obsidian Markdown notes.

## Overview

This skill fetches GitHub issue data via `gh` CLI and creates well-structured Obsidian documents with:
- Issue content and comments
- Sub-issues hierarchy
- Locally saved images (supports private repos)
- Obsidian wikilinks between related documents
- Proper frontmatter tags and metadata

## Input

User provides one or more of:
- GitHub issue URL: `https://github.com/owner/repo/issues/123`
- Repo + issue number: `owner/repo#123`
- Multiple issues to organize together

User should also specify:
- **Target directory**: where to save the documents (e.g., `Projects/aml/`)
- **Parent project** (optional): an existing note to link back to

## Workflow

### Phase 1: Data Collection

1. **Fetch issue details** via `gh` CLI:
   ```bash
   gh issue view <number> --repo <owner/repo> --json title,body,state,labels,comments,createdAt,closedAt
   ```

2. **Fetch sub-issues** via GraphQL:
   ```bash
   gh api graphql -f query='{
     repository(owner: "<owner>", name: "<repo>") {
       issue(number: <number>) {
         subIssues(first: 20) {
           nodes { number title state }
         }
       }
     }
   }'
   ```

3. **For each sub-issue**, recursively fetch details and comments.

4. **Map the timeline**: identify which months each issue's work spans (based on comment dates) for monthly report updates.

### Phase 2: Image Download

**CRITICAL**: GitHub private repo images require special handling.

1. **DO NOT** use `https://github.com/user-attachments/assets/...` URLs directly — they return 404 for private repos.

2. **Get signed CDN URLs** via the GitHub API HTML render:
   ```bash
   # For issue body images:
   gh api "repos/<owner>/<repo>/issues/<number>" \
     -H "Accept: application/vnd.github.html+json" 2>/dev/null | \
     grep -oE 'https://private-user-images\.githubusercontent\.com/[^"\\]+'

   # For comment images:
   gh api "repos/<owner>/<repo>/issues/<number>/comments" \
     -H "Accept: application/vnd.github.html+json" 2>/dev/null | \
     grep -oE 'https://private-user-images\.githubusercontent\.com/[^"\\]+'
   ```

3. **Download images** using the signed URLs (they expire in ~5 minutes):
   ```bash
   curl -sL "<signed_url>" -o "<output_path>"
   ```

4. **Verify downloads**: check file size > 100 bytes. Files of 9 bytes or `Not Found` content indicate failed downloads.

5. **Save images** to `<target_dir>/assets/` with descriptive names:
   - Format: `issue<N>-<description>.png`
   - Match asset UUID to determine which image is which by cross-referencing with the issue markdown body.

6. **Helper script** available at:
   ```bash
   uv run .claude/skills/gh-issues-to-doc/tools/download-issue-images.py <owner/repo> <issue_number> <output_dir> [--prefix PREFIX]
   ```

### Phase 3: Document Generation

For each issue (or group of related issues), create an Obsidian Markdown file.

#### Document Structure

```markdown
# <Issue Title>

> **標籤**: #project/<project> #<topic> #<technology>
> **來源**: [Issue #<N>](https://github.com/<owner>/<repo>/issues/<N>)
> **狀態**: #status/completed | #status/active
> **父項目**: [[<path>|<parent title>]]

---

## <Section from issue body>

<Content converted from GitHub Markdown to Obsidian Markdown>

![[<path>/assets/<image-file>.png]]

---

## Comments / Progress

<Organized content from issue comments>

---

## 參考資料

- [Link](url)

---

*最後更新：<date> — 從 GitHub Issue #<N> 整理*
```

#### Conversion Rules

1. **Images**: Use Obsidian embed syntax `![[path/to/image.png]]` (NOT standard markdown `![]()`).
2. **Internal links**: Use wikilinks `[[path|display text]]` for cross-references between generated documents.
3. **GitHub-specific elements**:
   - Task lists (`- [x]`, `- [ ]`) — keep as-is
   - `<details>/<summary>` — convert to Obsidian callouts or keep as-is
   - HTML `<img>` tags — convert to `![[]]` embeds with local images
4. **Comments**: Organize chronologically. If comments represent progress updates, group by date. If they contain research content, integrate into the main document sections.
5. **Code blocks**: Preserve language identifiers.
6. **Tables**: Keep GitHub Flavored Markdown table syntax.

### Phase 4: Index Updates

If the target directory has an `index.md`:
1. Add links to new documents under the appropriate section.
2. Update the directory structure listing.

### Phase 5: Monthly Report Updates (if requested)

If the user asks to update monthly reports:

1. **Map activities to months** based on:
   - Issue creation date
   - Comment dates (these indicate when work was done)
   - Issue close date

2. **For each month**, create or update `Reports/Monthly/YYYY-MM.md`:
   - Add items to Objectives table
   - Add Key Achievements from completed work
   - Add Issues/Blockers
   - Add Learned insights
   - Link to relevant project documents

3. **Use the template** at `./Templates/Monthly Report Template.md` for new reports.

4. **Objective Status values**:
   - `✅ Done` — completed in this month
   - `🔄 In Progress` — started but not finished
   - `📋 Planned` — planned but not started

## Important Notes

### Private Repo Image Handling

The most common failure point. Remember:
- `https://github.com/user-attachments/assets/<uuid>` → **404 for private repos** via curl
- Must use `gh api` with `-H "Accept: application/vnd.github.html+json"` to get signed CDN URLs
- Signed URLs contain JWT tokens and expire in ~5 minutes
- Download all images in one batch before tokens expire
- Always verify file size after download

### Content Organization Principles

- **Merge related issues** into single documents when they cover the same topic (e.g., dataset overview + feature analysis)
- **Separate concerns**: infrastructure, data pipeline, research, experiments → different files
- **Preserve technical detail**: keep code blocks, SQL schemas, benchmark results, configuration examples
- **Add context**: include progress timeline, decisions made, and lessons learned from comments

### Obsidian Compatibility

- Use `![[path]]` NOT `![](path)` for image embeds
- Use `[[path|display text]]` for internal links
- Tags format: `#project/<name>`, `#status/<state>`, `#<technology>`
- Frontmatter uses `>` blockquote style (not YAML frontmatter) for tags/metadata in this vault
