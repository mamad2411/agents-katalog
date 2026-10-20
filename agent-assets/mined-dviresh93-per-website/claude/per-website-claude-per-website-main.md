# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> Full job prep workflow rules are in `.claude/CLAUDE.md` (auto-loaded). This file covers technical commands and architecture.

---

## Running the Portfolio Website

```bash
npm run dev          # python3 -m http.server 8000
npm run docker:build # docker build -t viresh-portfolio .
npm run docker:run   # docker run -p 8080:8080 viresh-portfolio
```

Website content lives entirely in `data/*.json` — editing those files is the only way to update displayed content. No build step required.

---

## Resume Tool — MCP Setup (One-Time)

MCP servers register automatically when Claude Code opens this project (via `.mcp.json`). Both servers run inside Docker — no local Node or LaTeX installation needed.

```bash
./setup.sh    # Mac/Linux: build Docker image (first time, ~5-10 min)
setup.ps1     # Windows equivalent
```

After setup, `mcp__resume-generator__generate_resume` and `mcp__resume-memory__*` tools are available in Claude Code automatically.

---

## Resume Tool — Architecture

```
baseline-resume-data.json   ← source of truth for all resume content
        ↓
/apply command              ← enforces fit analysis + user approval gates
        ↓
resume-data.json (per job)  ← customized copy with job-specific changes
        ↓
MCP: generate_resume()      ← calls resumake-mcp via Docker
        ↓
resumake-mcp/lib/
  template-expander.js      ← resolves locked-template references
  latex-generator.js        ← converts JSON → LaTeX
  pdf-compiler.js           ← runs pdflatex inside Docker container
        ↓
viresh-duvvuri_YYMMDD-HHMM_role-title.pdf
```

**Fallback when MCP is unavailable:**
Edit the hardcoded path at the top of `generate-resume-standalone.mjs`, then:
```bash
node generate-resume-standalone.mjs
```

**Docker volume mounts (set in `docker-mcp.sh`):**
- `job-prep/applications/` → PDF output writes here on the host
- `resume-memory-mcp/data/` → SQLite DB (`memory.db`) persists between runs

---

## Resume Memory MCP — What It Does

`resume-memory-mcp/server.js` exposes these tools:

| Tool | Purpose |
|---|---|
| `get_profile_summary` | Compressed profile (~200 tokens) for fit analysis |
| `validate_resume` | Enforces locked content rules (`lib/resume-validator.js`) |
| `track_application` | Logs to SQLite for pattern learning |
| `check_resume_similarity` | Semantic search against past applications |

Locked-content rules are codified in `resume-memory-mcp/lib/resume-validator.js` — they mirror the rules in `.claude/CLAUDE.md`.

---

## Key File Locations

| What | Where |
|---|---|
| Resume source of truth | `job-prep/applications/_resources/baseline-resume-data.json` |
| Application workflow doc | `job-prep/RESUME_APPLICATION_WORKFLOW.md` |
| Validation rules | `job-prep/applications/_resources/VALIDATION_RULES.md` |
| Active applications | `job-prep/applications/{company-role}/` |
| Company interview prep | `interview-prep/companies/{company-name}/` |
| General coding practice | `practice-problems/python/` |
| Scratchpad (always .txt) | `scratchpad.txt` |
