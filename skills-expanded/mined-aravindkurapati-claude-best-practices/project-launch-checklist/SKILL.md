---
name: project-launch-checklist
description: |
  Audits a project for hiring visibility before going public. Verifies README clarity
  for impatient hiring managers, checks evaluation setup, tests, CI/CD, config file,
  and deployment link. Generates a pre-launch audit report with gaps and priorities.
  Use when you're ready to make a project visible to hiring managers or before submitting
  take-home assignments.
compatibility: claude-code
context: fork
version: 1.0.0
---

# Project Launch Checklist

A reproducible skill to audit any project before public visibility. Hiring managers spend 5-10 minutes on GitHub — this skill ensures every minute counts.

## How It Works

### Phase 1: README Audit
- Does the README explain what the project does in one sentence?
- Does it state the real problem it solves (not "demonstrates feature X")?
- Is there a live demo link or screenshot?
- Are key components linked (eval harness, config, prompts)?
- Is it written by a human, not AI? (overly polished READMEs are red flags)

### Phase 2: Engineering Signals
- Unit tests present? ✓/✗
- Integration tests? ✓/✗
- CI/CD pipeline configured (GitHub Actions)? ✓/✗
- Config file or `.env.example`? ✓/✗
- Live deployment or Streamlit/Gradio/HF Spaces link? ✓/✗

### Phase 3: Project-Specific Quality
**For ML/RAG projects:**
- Evaluation harness (golden datasets + metrics)? ✓/✗
- Before/after comparisons? ✓/✗
- Cost breakdown (tokens, API calls, monthly estimate)? ✓/✗

**For any project:**
- Architecture doc in `/documents/ARCHITECTURE.md`? ✓/✗
- Known limitations or future work? ✓/✗
- Code is clear and sparsely commented? ✓/✗

### Phase 4: Output Report
Generate a structured audit report showing:
- Green flags (what impresses)
- Gaps (what's missing)
- Quick wins (what to add in < 1 hour)
- Priority fixes (what moves the needle most)

## Execution

When ready to launch a project, use this in Claude Code:

```
Run project-launch-checklist:
- Path to project root: [path]
- Target audience: hiring managers / take-home assignment / both
- Priority: speed / depth / balanced
```

## The Checklist (Full)

### README (Hiring Manager Audience)
- [ ] One-sentence summary of what it does
- [ ] Problem statement (real, not abstract)
- [ ] Live demo link (Streamlit, Gradio, HF Spaces, Loom video, or screenshot)
- [ ] Production signals clearly visible (tests badge, CI/CD badge)
- [ ] Links to key files: `config.yaml`, eval metrics, architecture doc
- [ ] Human-written, not AI-generated (no obvious filler)
- [ ] < 500 words for "quick start" section
- [ ] Honest about limitations or future work

### Tests & CI/CD
- [ ] Unit tests in `tests/unit/` covering core logic
- [ ] Integration tests in `tests/integration/`
- [ ] GitHub Actions workflow in `.github/workflows/ci.yml`
- [ ] Tests run on every push
- [ ] Passing tests badge in README

### Configuration
- [ ] `config.yaml` or `.env.example` file
- [ ] Documented parameters (what each does, default values)
- [ ] People can experiment without code changes

### Evaluation (ML/RAG Projects)
- [ ] Golden dataset in `data/golden/` or similar
- [ ] Metrics defined (precision@k, MRR, cost per query, etc.)
- [ ] Before/after or baseline comparison
- [ ] Results displayed in README or `/documents/EVAL.md`

### Deployment
- [ ] Live demo link (not just local instructions)
- [ ] Or Loom video showing it in action (walking through design + execution)
- [ ] Deployment documented (Docker, environment setup)

### Architecture
- [ ] `/documents/ARCHITECTURE.md` explaining design choices
- [ ] Diagram (ASCII, Mermaid, or PNG)
- [ ] Why this approach (tradeoffs considered)

### Code Quality
- [ ] Variable names are clear (no single letters except loop counters)
- [ ] Functions under 20 lines where possible
- [ ] Error handling (not silently failing)
- [ ] Logging for debugging

---

## Quick Wins (1 Hour or Less)

If you're short on time, prioritize:

1. **README rewrite** (10 min) — explain what it does + why
2. **Add tests** (20 min) — unit tests for core logic using Claude Code
3. **GitHub Actions** (5 min) — run tests on push (copy template)
4. **Live demo** (10 min) — Streamlit or Gradio wrapper
5. **Config file** (10 min) — `.env.example` with documented params

These five alone move the needle significantly.

---

## Red Flags to Fix
- Broken links in README
- No way to actually run the code (missing setup steps)
- Claims not backed by eval (e.g., "state-of-the-art" with no numbers)
- Generic project (another cookie-cutter RAG tutorial)
- README that requires 10 minutes to understand what this is

---

## Rubric: Project Maturity Levels

**Level 1: Exists** (project is public, has a README)
- Signal: "I built something"

**Level 2: Runnable** (tests + CI/CD, clear setup instructions)
- Signal: "I follow engineering practices"

**Level 3: Evaluated** (tests + eval harness + metrics + config)
- Signal: "I think about impact, not just features"

**Level 4: Deployed** (live demo + architecture doc + cost breakdown)
- Signal: "I can ship"

**Level 5: Polished** (all above + domain expertise + multi-project breadth)
- Signal: "I'm ready to work"

Aim for Level 3–4 on 5–6 projects rather than Level 5 on one.

---

## Notes
- This skill works on any project (ML, full-stack, CLI tools, data pipelines)
- Use it as a checklist before making repos public
- Use it before take-home assignments (these get read more carefully)
- Takes ~30 min to audit, 1–3 hours to address gaps depending on what's missing
