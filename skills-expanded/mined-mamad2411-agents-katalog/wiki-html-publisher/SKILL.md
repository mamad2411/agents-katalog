---
name: wiki-html-publisher
description: >
  Publishes any Markdown document to GitHub Wiki and generates a standalone HTML file with
  rendered Mermaid diagrams. Use when the user asks to: publish to wiki, generate HTML from
  markdown, export docs to HTML, push documentation to GitHub Wiki, create standalone HTML
  documentation, or any variant of "publish/export this markdown". Works with any .md file
  — technical documentation, ADRs, changelogs, runbooks, API docs, etc.
compatibility: >
  Python 3.x with 'markdown' pip package required for HTML export.
  Git CLI required for Wiki publishing.
allowed-tools:
  - read_file
  - grep_search
  - find_by_name
  - run_command
  - write_to_file
  - edit
---

# Wiki & HTML Publisher

Publishes Markdown documents to **GitHub Wiki** and generates **standalone HTML** with Mermaid diagram rendering.

This skill is designed to be **composable** — any other skill that produces a `.md` file can delegate publishing to this skill.

---

## INPUT

This skill expects:

1. **A Markdown file** (`.md`) to publish — typically in `docs/` but any path works
2. **A Git repository** as context — to determine the GitHub org/repo for the Wiki

The skill will ask for the input file path if not provided.

---

## PHASE 1: WIKI PUBLISHING — Publish to GitHub Wiki

### Step 1: Detect wiki repository

Look for `{repo-name}.wiki` or `{repo-name}.wiki/` in the parent directory of the main repo.

If it does not exist, clone it:
```
git clone https://github.com/{org}/{repo}.wiki.git
```

To determine `{org}` and `{repo}`:
- Read the Git remote: `git remote get-url origin`
- Parse the org and repo name from the URL

### Step 2: Analyze the input Markdown

Read the input `.md` file and extract:
- **Title**: first `# H1` heading
- **Metadata**: project name, version, date (from header tables or bold fields)
- **Section headings**: all `## H2` sections for the sidebar
- **Language**: detect the language of the document content (Spanish, English, etc.) and use the SAME language for all Wiki outputs

### Step 3: Generate `Home.md`

Wiki landing page with:

```markdown
# {Project Title}

**Project**: `{artifact-id}`
**Version**: {version}

{Brief description extracted from the first paragraph of the input document.}

---

## Documentation

| Page | Description |
|---|---|
| **[[Technical-Documentation]]** | {Description based on input document content} |

## Technology Stack

{Extract from the input document if available, otherwise omit this section.}
```

> **LANGUAGE RULE**: Generate `Home.md` in the **same language** as the input Markdown. Do NOT translate to English unless the input is already in English.

### Step 4: Generate `_Sidebar.md`

Sidebar navigation with links to all `## H2` sections:

```markdown
**[[Home]]**

---

**[[{Page-Name}]]**

- [{Section 1 Title}]({Page-Name}#{anchor-1})
- [{Section 2 Title}]({Page-Name}#{anchor-2})
- [{Section 3 Title}]({Page-Name}#{anchor-3})
```

#### Anchor generation rules (GitHub Wiki)

1. Convert heading to lowercase
2. Replace spaces with hyphens `-`
3. Remove special characters except hyphens
4. Accents are removed (e.g., `Vision` stays `vision`)
5. Examples:
   - `## 1. Architecture Overview` → `#1-architecture-overview`
   - `## 3. Sistema 1 — GBO Entities` → `#3-sistema-1--gbo-entities`

#### Rules for _Sidebar.md

1. Each main page as a bold heading with `[[Wiki Link]]`
2. `---` separator between pages
3. Maximum 2 indentation levels for readability
4. Only include `##` sections, not `###` or deeper

### Step 5: Copy content page

Copy the input Markdown file to the wiki directory as the content page:
- Default name: `Technical-Documentation.md`
- If the input file has a different semantic (e.g., ADR, changelog), use an appropriate page name

### Step 6: Publish

```bash
cd {repo}.wiki/
git add .
git commit -m "Update documentation"
git push origin master
```

### Mermaid in GitHub Wiki

` ```mermaid ` blocks render natively in GitHub Wiki since 2022. No plugins needed.

**Known limitations**:
- Very large diagrams (>50 nodes) may not render
- Use `default` theme for best compatibility

---

## PHASE 2: HTML EXPORT — Standalone HTML generation

### Step 1: Check for Python

Run `python --version`. If Python 3.x is available, use the script approach. Otherwise, generate HTML directly.

### Step 2a: Script approach (preferred)

```bash
pip install markdown
python "{skill-dir}/scripts/md-to-html.py" "{input.md}" "{output.html}" --title "{Title}"
```

The script handles:
- Markdown → HTML conversion (tables, code blocks, lists, etc.)
- Mermaid block conversion (`<pre><code class="language-mermaid">` → `<pre class="mermaid">`)
- GitHub-like CSS injection
- Mermaid JS CDN loading
- Template placeholder substitution

### Step 2b: Direct generation (fallback)

If Python is not available, generate the HTML directly by:

1. Converting each Markdown element to HTML:

   | Markdown | HTML |
   |---|---|
   | `# Heading 1` | `<h1 id="heading-1">Heading 1</h1>` |
   | `## Heading 2` | `<h2 id="heading-2">Heading 2</h2>` |
   | `` `code` `` | `<code>code</code>` |
   | ` ```lang ... ``` ` | `<pre><code class="language-lang">...</code></pre>` |
   | ` ```mermaid ... ``` ` | `<pre class="mermaid">...</pre>` |
   | `\| table \|` | `<table>...</table>` |
   | `> blockquote` | `<blockquote>...</blockquote>` |
   | `---` | `<hr>` |

2. Wrapping in the HTML template (see `assets/html-template.html`)

3. Injecting Mermaid JS:
   ```html
   <script src="https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.min.js"></script>
   <script>mermaid.initialize({startOnLoad: true, theme: 'default', securityLevel: 'loose'});</script>
   ```

> **IMPORTANT**: Mermaid blocks must be `<pre class="mermaid">` — do NOT use `<code>` inside them.

### Step 3: Output file

Save to: `docs/{artifact-id}-documentation.html`

If the artifact ID is not available, derive it from the repo directory name.

### Step 4: Offline option

For environments without CDN access, offer to embed Mermaid JS inline (~2MB):
- Download `https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.min.js`
- Embed inside an inline `<script>` tag
- The HTML becomes heavier but completely self-contained

---

## GENERATED OUTPUTS

| Channel | Location | Audience | Diagrams |
|---|---|---|---|
| **GitHub Wiki** | `{repo}.wiki/` (Home.md + _Sidebar.md + content pages) | Anyone with repo access on GitHub | Mermaid rendered natively |
| **Standalone HTML** | `docs/{artifact-id}-documentation.html` | Anyone (no GitHub needed) | Mermaid rendered as SVG via CDN |

---

## EXPECTED BEHAVIOR

When the user asks to publish or export documentation:

1. **Identify the input file** — If not specified, look for `docs/DOCUMENTACION-TECNICA.md` or any `.md` in `docs/`. If multiple exist, ask the user which one.
2. **Ask what to generate**:
   - GitHub Wiki only
   - HTML standalone only
   - Both
3. **Detect language** — Read the input file and detect its language. Use the SAME language for all generated outputs (Home.md, _Sidebar.md, HTML).
4. **Execute** the requested phases (1, 2, or both).
5. **Report** the generated files and provide the Wiki URL if published.

### Progress Checklist

```
- [ ] Input file identified
- [ ] Output format chosen (Wiki / HTML / Both)
- [ ] Language detected from input
- [ ] Wiki: Home.md generated
- [ ] Wiki: _Sidebar.md generated
- [ ] Wiki: Content page copied
- [ ] Wiki: Committed and pushed
- [ ] HTML: Standalone .html generated with Mermaid rendering
```
