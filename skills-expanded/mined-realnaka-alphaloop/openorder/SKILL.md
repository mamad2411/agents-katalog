---
name: openorder
version: 1.0.0
description: "OpenOrder — Order out of investment chaos. An AI-maintained investment research wiki that compounds your edge across every conversation. Triggers automatically on: (1) any stock ticker (US/HK/A-share/TW/JP) or company name; (2) industry/theme discussions (semiconductors, AI infra, photonics, HBM, energy, biotech, crypto, etc.); (3) investment frameworks/methodology (moats, chokepoints, valuation, portfolio construction, value chain analysis); (4) earnings, guidance, research notes, or news analysis; (5) explicit operations ('ingest', 'lint wiki', 'archive this', 'add to research'). On trigger MUST: Read INDEX.md first → Read relevant sub-files → Answer using wiki content → Update wiki when new insights emerge. This is a cross-session, cross-project, read+write skill. Inspired by Andrej Karpathy's LLM Wiki pattern."
metadata:
  storageRoot: "${OPENORDER_HOME:-$HOME/openorder}"
  homepage: "https://github.com/realnaka/OpenOrder"
  inspiredBy: "https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f"
  domain: "investment-research"
  customizable: true
---

# OpenOrder — Investment Research Wiki Skill

> **Order out of investment chaos.**
> An open AI-maintained research wiki that compounds your edge across every conversation.

## 1. Core Mission

OpenOrder turns scattered investment research into a **persistent, compounding wiki** maintained by your AI agent.

Following the [Karpathy LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f):

- The agent is the **maintainer**; you are the **prompter + source curator**
- Knowledge is **compiled once, kept fresh** — not re-derived on every query
- The wiki is a **persistent, compounding artifact** — every conversation makes it smarter

Every conversation that touches a ticker / industry / earnings / framework MUST execute:

```
READ → REASON → WRITE → LOG → (periodically) LINT
 ↓        ↓        ↓       ↓             ↓
look up  combine  archive  timeline    health-check
existing real-time new       append-only contradictions,
data     + history insights  record       gaps, staleness
```

---

## 2. Three-Layer Architecture

```
${OPENORDER_HOME}/
│
├── raw/                        ← Layer 1: Raw Sources (immutable, read-only)
│   ├── earnings/                  Earnings transcripts / 8-K filings
│   ├── articles/                  Articles, tweets, blog posts
│   ├── filings/                   SEC 10-K/10-Q PDFs
│   ├── research-notes/            Raw research notes from conversations
│   └── README.md
│
├── [Wiki Layer]                 ← Layer 2: Wiki (LLM-owned, continuously maintained)
│   ├── INDEX.md                   📌 Content index (always read first)
│   ├── log.md                     📌 Activity log (append-only timeline)
│   ├── README.md
│   ├── companies/{TICKER}.md      Company profiles
│   ├── industries/{NAME}/         Industry deep-dives
│   ├── frameworks/{NAME}.md       Investment frameworks
│   ├── earnings/{TICKER}-{Q}.md   Earnings deep-dives
│   ├── portfolios/{NAME}.md       Portfolio configurations
│   └── templates/                 Templates for new entries
│
└── [Schema Layer]               ← Layer 3: Schema (this file)
    ~/.claude/skills/openorder/SKILL.md (or equivalent for other agents)
```

**Layer rules**:
- **Raw is immutable**: only append metadata headers; never modify content
- **Raw must produce Wiki updates**: every raw file must trigger at least one wiki page update (otherwise it's dead data)
- **Wiki references Raw**: use relative paths `[source](../raw/earnings/{TICKER}-{Q}.txt)`
- **Schema rules everything**: this `SKILL.md` defines all rules

---

## 3. Mandatory Trigger Scenarios

### 🟢 MUST trigger (no user reminder needed)

The **first action MUST be `Read ${OPENORDER_HOME}/INDEX.md`** when any of the following appears:

#### 3.1 Ticker / company mentions
- Any equity ticker: US (4-letter), HK (4-digit), A-share (6-digit + .SZ/.SH), TW (.TW/.TWO), JP (.JP), KR, etc.
- Any company name (English or local language)
- Crypto: any token symbol (BTC, ETH, SOL, etc.) or protocol name

#### 3.2 Industry / theme keywords
Replace this list with your own domain. Defaults below cover common AI / hard-tech / energy themes:
- **Semiconductors**: foundry, fab, EUV, lithography, advanced packaging, CoWoS, chiplet
- **AI infra**: hyperscaler capex, data center, scale-out, scale-up, NVLink, InfiniBand
- **Photonics**: optical interconnect, CPO, CW laser, EML, DFB, VCSEL, InP, SiPh
- **Memory**: HBM, HBM3E, HBM4, DDR5
- **Energy / storage**: SOFC, fuel cell, BESS, sodium-ion, long-duration storage
- **Crypto**: L1/L2, DeFi, perp DEX, stablecoin, restaking
- *(extend with your own domain keywords in the customization layer below)*

#### 3.3 Framework / methodology keywords
- chokepoint, bottleneck, moat, value chain, supply chain
- super-cycle, supply-constrained, structural shortage
- target price, valuation, P/E, EV/EBITDA, DCF
- thesis, conviction, base/bull/bear case

#### 3.4 Earnings / financial keywords
- earnings, guidance, beat, miss, transcript, 8-K, 10-Q, 10-K, FY/CY quarters
- any concrete metric (revenue, gross margin, EPS, capex, backlog, inventory) tied to a company

#### 3.5 Trading / portfolio keywords
- "buy", "sell", "trim", "add", "short", "hedge"
- "position", "weight", "allocation", "portfolio", "basket"

#### 3.6 Explicit operation keywords
- **Ingest**: "read this article", "ingest", "archive", "save this source"
- **Lint**: "lint wiki", "health check", "find contradictions", "self-audit"
- **Query**: any normal question (default mode)

### 🟡 Suggested triggers
- "value chain", "upstream/downstream", "picks and shovels"
- "AI beneficiaries", "second derivative plays"
- Any "X vs Y" comparison

---

## 4. Operation 1: READ (mandatory every time)

```
Trigger → Read INDEX.md (mandatory, ~5s)
    ↓
Determine relevance, then read as needed:
    ├── Company question → companies/{TICKER}.md
    ├── Industry question → industries/{NAME}/README.md
    ├── Framework question → frameworks/{NAME}.md
    ├── Historical earnings → earnings/{TICKER}-{Q}.md
    ├── Portfolio → portfolios/{NAME}.md
    └── Timeline → log.md (newest first)
    ↓
When answering:
    1. Cite information timestamps ("based on YYYY-MM-DD data")
    2. Reference specific files ("see companies/{TICKER}.md")
    3. If data is stale → use WebSearch to confirm current state
```

---

## 5. Operation 2: INGEST (when user provides a new source)

**Triggered by**: user pastes a URL, sends a tweet/article, says "read this", "ingest", "archive".

**Standardized 5-step flow**:

```
Step 1. Fetch full content
   ├── URL: WebFetch / Browser
   ├── Tweet: browser MCP
   ├── Earnings: pull from filing / SEC direct link
   └── Write to raw/<subdir>/ (immutable; only add metadata header)

Step 2. Extract entities + key findings
   ├── Which companies are mentioned? (existing/new in wiki)
   ├── Which industries / concepts?
   ├── Key numbers, quotes, contradictions
   └── Confirm with user what to emphasize

Step 3. Update Wiki (may touch 10-15 files)
   ├── New company → use templates/company-template.md to create
   ├── Existing company → update "analysis log", revise bull/bear, adjust scores
   ├── Industry page → add "event tracking" entry
   ├── Framework → if validated/challenged, update framework file
   └── Each file: top "Last updated" date + bottom changelog entry

Step 4. Append log.md (mandatory)
   Add entry:
   ## [YYYY-MM-DD HH:MM] ingest | {title}
   - Source: raw/.../{file}
   - Key findings: ...
   - Files touched: companies/X.md, industries/Y.md, ...

Step 5. Update INDEX.md
   ├── Update top "Last updated"
   ├── Update "Wiki navigation" table (if new files)
   └── Update bottom "Update history"
```

**After ingest**, tell the user:
- Which files were modified (so they can review in Obsidian)
- Whether new findings need their decision

---

## 6. Operation 3: WRITE (when conversation produces new insights)

### 6.1 When to write

| Trigger event | Required write |
|---|---|
| User mentions an **uncatalogued company** | Immediately create `companies/{TICKER}.md` (use template) |
| **New earnings** released or discussed | Create `earnings/{TICKER}-{Q}.md` + update company profile |
| Conversation produces a **new insight/analysis** | Append to relevant file's "Analysis log" + log.md + INDEX.md |
| User makes a **trading decision** (buy/sell) | Create or update `portfolios/{NAME}.md` + log.md |
| **Industry change** (M&A, partnership, product launch) | Update `industries/{NAME}/README.md` "Event tracking" |
| **Framework validated or revised** | Update relevant `frameworks/` file + log.md |

### 6.2 Writing rules

#### Required metadata
- File top: `> **Last updated**: YYYY-MM-DD`
- File bottom: changelog (newest first)
- INDEX.md: update history + todos
- log.md: append one entry

#### Writing style
- **Concrete data**: not "revenue grew strongly" — say "revenue $1.81B (+27% YoY)"
- **Cite sources**: not "analysts think" — say "GS report 2026/3" or "CEO on Q3 FY26 transcript", with raw path
- **Flag assumptions**: model predictions must say "assuming X conditions"
- **Bull/bear balance**: every company profile MUST have both bull and bear arguments

#### Naming conventions
- Company: `companies/{TICKER}.md` (e.g. `AAPL.md`, `0700-HK.md`, `688012-SH.md`)
- Earnings: `earnings/{TICKER}-{QUARTER}.md` (e.g. `AAPL-Q1-FY26.md`)
- Industry: `industries/{NAME}/README.md`
- Framework: `frameworks/{NAME}.md` (kebab-case)
- Portfolio: `portfolios/{NAME}-{DATE}.md`
- Raw: see `raw/README.md`

### 6.3 Templates
See `templates/company-template.md` and `templates/earnings-template.md`.

---

## 7. Operation 4: LOG (append on every write)

**Location**: `${OPENORDER_HOME}/log.md`

**Format** (Karpathy convention — uniform prefix for grep):

```markdown
## [YYYY-MM-DD HH:MM] {action} | {one-line summary}
- Trigger: {user prompt or event}
- Files touched: {file1}, {file2}, ...
- Key findings/decisions: {1-3 lines}
- Raw source: {path if applicable}
```

`action` values:
- `ingest` — new source absorbed
- `query` — user Q&A (only log if it produced new insight)
- `lint` — health check
- `decision` — real trading decision
- `revise` — corrected old thesis
- `framework` — framework update

**How to append**: use StrReplace at the top of the `# Wiki Activity Log` heading (newest first).

**Benefit**: `grep "^## \[" log.md | tail -10` instantly shows recent activity.

---

## 8. Operation 5: LINT (periodic or explicit)

**Triggered by**: user says "lint wiki", "health check", "find contradictions"; or proactively offer monthly.

**Lint 5 checks**:

### 8.1 Contradictions
- Same company has conflicting target price / rating in `companies/X.md` vs `portfolios/Y.md`?
- Industry ranking in `industries/.../README.md` conflicts with `frameworks/.../*.md` scores?
- Same metric different across multiple `earnings/` files?

### 8.2 Staleness
- Company profile `Last updated` predates its latest earnings → flag for update
- Earnings file >90 days old but catalysts have passed → need a new earnings file?

### 8.3 Orphans
- Files in `companies/` not referenced by any portfolio / framework / industry?
- Raw sources without a corresponding wiki update?

### 8.4 Missing pages
- Companies/concepts mentioned **multiple times** across files but no profile (e.g. "Anritsu" cited 5 times but no `companies/Anritsu.md`)?
- Catalyst tables mention "watch X in YYYY/MM" — date passed without follow-up?

### 8.5 Data gaps
- Companies that haven't been refreshed in 30+ days
- Industries lacking a value-chain mermaid diagram

**Lint output**: a markdown report listing all issues + suggested next actions. **Does not auto-modify** — user decides.

---

## 9. Cross-Agent Compatibility

OpenOrder works with any AI agent that supports either `SKILL.md` or `AGENTS.md`:

| Agent | Skill mechanism | Install location |
|---|---|---|
| **Claude Code** (Anthropic) | `SKILL.md` (native) | `~/.claude/skills/openorder/` |
| **Cursor** (IDE + CLI) | `SKILL.md` (compatible) | `~/.cursor/skills-cursor/openorder/` |
| **Codex CLI** (OpenAI) | `AGENTS.md` or `SKILL.md` | `~/.codex/skills/openorder/` |
| **OpenCode** (sst) | `AGENTS.md` | `.opencode/agent/` or repo root |
| **Hermes Agent** (NousResearch) | `AGENTS.md` + `~/.hermes/skills/` | `~/.hermes/skills/openorder/` |
| **OpenClaw** | `AGENTS.md` | per project config |
| **Aider** | `CONVENTIONS.md` | repo root (symlink to SKILL.md) |
| **Cline / Roo Code** | `.clinerules` | repo root |

The repository ships **both** `SKILL.md` (this file) and `AGENTS.md` (mirror). The `install.sh` script auto-detects installed agents and creates the appropriate symlinks.

---

## 10. Special Scenarios

### 10.1 Uncatalogued company
1. WebSearch latest financials + industry position
2. Use `templates/company-template.md` to create `companies/{TICKER}.md`
3. Add to INDEX.md
4. Append `log.md` ingest entry
5. Answer the user

### 10.2 Stale data
1. WebSearch confirms latest data
2. Update file + INDEX.md timestamp
3. Note in changelog: "YYYY-MM-DD: data updated from X to Y"
4. Append `log.md` revise entry

### 10.3 Conflict with new data
1. **New data wins**
2. Note conflict reason in changelog
3. If thesis was wrong → revise bull/bear arguments
4. Append `log.md` revise entry

### 10.4 Real trading decision
1. Create or update `portfolios/{NAME}.md`
2. Record: entry/exit price, size, time, rationale
3. Append `log.md` decision entry
4. Add "review reminder" todo to INDEX.md

---

## 11. Self-check Checklist

Before ending any conversation that touched stocks / industries:

- [ ] Did I read INDEX.md?
- [ ] Did I read the relevant company profile(s)?
- [ ] Did I answer using wiki content?
- [ ] Are there new data / insights that need to be written back?
- [ ] Is there a raw source to ingest?
- [ ] Does log.md need a new entry?
- [ ] Does INDEX.md need updating?
- [ ] Are there new todos?

If **any answer is "no but should be yes"**, do it now.

---

## 12. Anti-patterns to avoid

### ❌ Anti-pattern 1: Answer without reading the wiki
**Wrong**: "AAPL is a consumer hardware company..." (from memory)
**Right**: Read INDEX.md → Read companies/AAPL.md → answer based on wiki

### ❌ Anti-pattern 2: Read but don't update
**Wrong**: Use stale data and stop
**Right**: If conversation produced new conclusion → append to file + log.md + INDEX.md

### ❌ Anti-pattern 3: Create file but don't update INDEX
**Wrong**: Create `companies/NEW.md` but INDEX.md unchanged
**Right**: Every new file → update INDEX navigation table + log.md

### ❌ Anti-pattern 4: Write data without timestamps
**Wrong**: "revenue +20% YoY" (which quarter?)
**Right**: "Q3 FY26 revenue $1.81B (+20.5% YoY), reported YYYY-MM-DD"

### ❌ Anti-pattern 5: Bull-only profiles
**Wrong**: List only positives
**Right**: Every profile must have a bear case section

### ❌ Anti-pattern 6: Skip Raw layer when ingesting
**Wrong**: Summarize an article straight into wiki without storing the original
**Right**: First save `raw/articles/{date}-{slug}.md`, then wiki references it

### ❌ Anti-pattern 7: Wiki changes without log.md entry
**Wrong**: Modify 5 files, log.md unchanged
**Right**: Every write operation must append log.md (even one line)

---

## 13. Customization (fork to your domain)

OpenOrder ships **investment research** as the default domain. To adapt:

1. **Edit Section 3 trigger keywords** to match your field (e.g. biotech, crypto, real estate)
2. **Edit `templates/`** to fit your entity type (instead of "company profile" → "drug pipeline" / "protocol" / "property")
3. **Edit `frameworks/`** to fit your scoring methodology
4. **Keep Sections 2/4/5/6/7/8 unchanged** — these are domain-agnostic operations

See [`docs/customize.md`](docs/customize.md) for examples adapting OpenOrder to:
- Crypto research wiki
- Academic literature review
- Personal journaling / quantified self
- Internal team knowledge base

---

## 14. External Tools Integration

| Tool | Role | How agent uses it |
|---|---|---|
| **Local markdown** (this wiki) | Primary store | Read / Grep / Glob |
| **git** | Version history + collaboration | `git log` + auto-commit hook |
| **Obsidian** | Visual browse + bidirectional links | Vault → `${OPENORDER_HOME}` |
| **WebSearch / Browser MCP** | Real-time data + ingest | Standard tools |

---

## 15. Version History

| Version | Date | Changes |
|---|---|---|
| v1.0.0 | First public release | Open-sourced as OpenOrder |

---

## 16. Credits

OpenOrder's three-layer architecture (Raw / Wiki / Schema), `log.md` timeline, Lint operation, and Ingest workflow are directly inspired by Andrej Karpathy's **LLM Wiki pattern**:
<https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f>

The investment-research domain framing, chokepoint scoring methodology, and cross-agent install scaffolding are original to OpenOrder.

License: MIT. See [`LICENSE`](LICENSE).
