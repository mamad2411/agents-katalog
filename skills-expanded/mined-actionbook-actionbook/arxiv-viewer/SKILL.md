---
name: arxiv-viewer
description: View, search, and download academic papers from arXiv. Supports API queries, web scraping via Actionbook, and HTML paper reading via ar5iv. Use when user asks about arxiv papers, academic papers, research papers, paper summaries, latest papers, or wants to search/download/read papers.
---

# arXiv Viewer

Access, search, download, and read academic papers from arXiv using a hybrid API + Actionbook approach.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     arxiv-viewer                            │
├─────────────────┬─────────────────┬─────────────────────────┤
│   arXiv API     │  arxiv.org Web  │      ar5iv.org          │
│   (WebFetch)    │  (Actionbook)   │    (Actionbook)         │
├─────────────────┼─────────────────┼─────────────────────────┤
│ • Metadata      │ • Latest list   │ • Read sections         │
│ • Search        │ • Trending      │ • Extract figures       │
│ • By ID lookup  │ • Advanced      │ • Extract citations     │
│                 │   search form   │ • Get outline           │
└─────────────────┴─────────────────┴─────────────────────────┘
```

## Tool Priority

**By Feature:**

| Feature | Primary Tool | Fallback |
|---------|--------------|----------|
| Paper metadata | WebFetch (API) | browser-fetcher |
| Search | WebFetch (API) | browser-fetcher |
| Latest papers | browser-fetcher (Actionbook) | WebFetch (API) |
| Trending | browser-fetcher (Actionbook) | - |
| Advanced search | browser-fetcher (Actionbook) | WebFetch (API) |
| Read HTML section | html-reader (Actionbook) | Read (PDF) |
| Download PDF | Bash (curl) | - |

## Workflow Rules

### ⚠️ Agent Waiting Rule

**After launching browser-fetcher or html-reader agents:**
1. ✅ **MUST wait for ALL agents to complete**
2. ⛔ **DO NOT** use WebFetch/WebSearch while waiting
3. ✅ Only use fallback tools after agents have failed

---

## Data Sources

### 1. arXiv API (WebFetch)

**Best for:** Quick metadata lookup, simple search

```
Base URL: http://export.arxiv.org/api/query
```

| Parameter | Description |
|-----------|-------------|
| search_query | Search with field prefixes (ti:, au:, abs:, cat:) |
| id_list | Comma-separated arXiv IDs |
| max_results | 1-2000 (default: 10) |
| sortBy | relevance / submittedDate / lastUpdatedDate |

**Field Prefixes:** `ti:` (title), `au:` (author), `abs:` (abstract), `cat:` (category), `all:` (all)

**Boolean Operators:** `AND`, `OR`, `ANDNOT` (UPPERCASE)

### 2. arxiv.org Web (Actionbook + agent-browser)

**Best for:** Latest papers, trending, advanced search UI

| Page | Action ID | Use Case |
|------|-----------|----------|
| Latest list | `arxiv.org/list/{category}/recent` | Recent submissions |
| Advanced search | `arxiv.org/search/advanced` | Complex filters |
| Homepage | `arxiv.org/` | Trending/announcements |

**Workflow:**
```
1. search_actions("arxiv list recent")
2. get_action_by_id(action_id) → selectors
3. agent-browser open URL
4. agent-browser get text <selector>
5. Return results
```

### 3. ar5iv.org HTML Papers (Actionbook + agent-browser)

**Best for:** Reading specific sections, extracting figures/citations

```
HTML Paper URL: https://ar5iv.org/html/{arxiv_id}
```

| Element | Selector | Description |
|---------|----------|-------------|
| Title | `.ltx_title` | Paper title |
| Authors | `.ltx_authors` | Author list |
| Abstract | `.ltx_abstract` | Abstract text |
| Sections | `section` | All sections |
| Section title | `h2.ltx_title`, `h3.ltx_title` | Section headings |
| Paragraphs | `.ltx_para` | Paragraph content |
| Figures | `figure.ltx_figure` | Figures with captions |
| Tables | `table.ltx_tabular` | Data tables |
| Equations | `.ltx_equation` | Math equations |
| Bibliography | `.ltx_bibliography` | Reference list |
| Single citation | `.ltx_bibitem` | Individual reference |

**Workflow:**
```
1. search_actions("ar5iv section")
2. get_action_by_id(action_id) → selectors
3. agent-browser open ar5iv.org/html/{id}
4. agent-browser get text <section_selector>
5. Return section content
```

---

## URL Patterns

| Purpose | URL |
|---------|-----|
| arXiv Abstract | `https://arxiv.org/abs/{id}` |
| arXiv PDF | `https://arxiv.org/pdf/{id}.pdf` |
| arXiv API | `http://export.arxiv.org/api/query?id_list={id}` |
| ar5iv HTML | `https://ar5iv.org/html/{id}` |
| ar5iv Abstract | `https://ar5iv.org/abs/{id}` |

## arXiv ID Formats

| Format | Example |
|--------|---------|
| New (2007+) | `2301.07041` |
| With version | `2301.07041v2` |
| Old | `cs.AI/0612345` |

## Common Categories

| Code | Field |
|------|-------|
| `cs.AI` | Artificial Intelligence |
| `cs.CL` | Computation and Language (NLP) |
| `cs.CV` | Computer Vision |
| `cs.LG` | Machine Learning |
| `cs.SE` | Software Engineering |
| `stat.ML` | Statistical ML |

---

## Feature Matrix

| Command | Data Source | Agent |
|---------|-------------|-------|
| `/arxiv-viewer:paper` | API | paper-fetcher |
| `/arxiv-viewer:search` | API | search-executor |
| `/arxiv-viewer:download` | Direct URL | - |
| `/arxiv-viewer:latest` | arxiv.org | browser-fetcher |
| `/arxiv-viewer:trending` | arxiv.org | browser-fetcher |
| `/arxiv-viewer:read` | ar5iv.org | html-reader |
| `/arxiv-viewer:outline` | ar5iv.org | html-reader |
| `/arxiv-viewer:figures` | ar5iv.org | html-reader |
| `/arxiv-viewer:citations` | ar5iv.org | html-reader |
| `/arxiv-viewer:report` | API + ar5iv | paper-summarizer |

---

## Output Formats

### Paper Info
```
## {Title}

**arXiv:** {id}
**Authors:** {author1}, {author2}, ...
**Categories:** {cat1}, {cat2}
**Published:** {date}

### Abstract
{abstract}

**Links:** [Abstract]({abs_url}) | [PDF]({pdf_url}) | [HTML]({ar5iv_url})
```

### Section Content
```
## {Section Title}

{section content}

---
*Source: ar5iv.org/html/{id}*
```

### Paper Report (AI Generated)

**Command:** `/arxiv-viewer:report {arxiv_id}` or `/arxiv-viewer:report {paper_title}`

**Purpose:** Generate a comprehensive, well-formatted paper report with AI-generated analysis.

**Output Format:**
```markdown
---
> **🤖 AI Generated Content**
> Author: Powered by ActionBook
---

# {Paper Title}

**Paper Information**
| Field | Content |
|-------|---------|
| arXiv ID | {id} |
| Authors | {authors} |
| Affiliations | {affiliations} |
| Published | {date} |
| Categories | {categories} |

---

## 📋 Abstract

{abstract_summary}

---

## 🎯 Problem Statement

{problem_statement}

---

## 💡 Key Contributions

1. {contribution_1}
2. {contribution_2}
3. {contribution_3}

---

## 🔬 Method Overview

{method_summary}

---

## 📊 Experimental Results

{experimental_results}

---

## 🌟 Why It Matters

{significance}

---

## 🔗 Links

- [arXiv Abstract](https://arxiv.org/abs/{id})
- [PDF Download](https://arxiv.org/pdf/{id}.pdf)
- [HTML Version](https://ar5iv.org/html/{id})

---
> This report was automatically generated by AI based on the original paper content.
> **Powered by ActionBook** | Generated: {timestamp}
```

**Workflow:**
```
1. Fetch paper metadata via arXiv API
2. Read full paper content from ar5iv.org HTML
3. Extract key sections (abstract, intro, method, results)
4. Generate structured report with AI analysis
5. Add ActionBook branding header and footer
```

**Report Sections:**
| Section | Source | Description |
|---------|--------|-------------|
| Paper Information | API metadata | Basic paper information |
| Abstract | Abstract | Summary of abstract |
| Problem Statement | Introduction | Problem statement extracted |
| Key Contributions | Introduction | Key contributions listed |
| Method Overview | Method section | Technical approach summary |
| Experimental Results | Experiments | Key results and metrics |
| Why It Matters | Analysis | AI-generated significance |

## Rate Limiting

- arXiv API: 3 second delay between requests
- ar5iv.org: Respect server load
- agent-browser: One page at a time
