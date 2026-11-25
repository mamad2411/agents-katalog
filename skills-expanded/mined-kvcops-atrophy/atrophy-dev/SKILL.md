---
name: atrophy-dev
description: Guides development of the atrophy CLI — a git history analyzer that tracks which coding skills a developer exercises versus outsources to AI. Use this skill when building, debugging, or extending any part of atrophy: git scanner, AI detector, skill mapper, challenge engine, Textual TUI, LLM providers (OpenAI, Anthropic, OpenRouter, Ollama local/cloud), multi-repo support, git hooks, VS Code extension, team mode, compare command, or publishing/leaderboard features.
---

# atrophy Development Skill v2.0

## The One-Line Mental Model

`atrophy` measures the DEVELOPER, not the codebase.
It tracks which engineering skills YOU personally exercise — not code quality, not linting, not dead code.
If a suggested feature is about analyzing the codebase itself, it is the wrong product.

---

## Architecture Decision Tree

When you get a task, identify the layer first:

```
Reading git commits?
  → atrophy/core/git_scanner.py (GitScanner)

Classifying human vs AI code?
  → atrophy/core/ai_detector.py (AIDetector)

Mapping code to skill categories?
  → atrophy/core/skill_mapper.py (SkillMapper, TreeSitterAnalyzer, LLMSkillClassifier)

Building LLM context for challenges?
  → atrophy/core/context_builder.py (ContextBuilder)

Generating personalized challenges?
  → atrophy/core/challenge_engine.py (ChallengeEngine)

Saving or reading any data?
  → atrophy/core/storage.py (Storage — SQLAlchemy 2.0 async)

Config, env vars, or API keys?
  → atrophy/config.py (Settings via pydantic-settings)

Any CLI command the user types?
  → atrophy/cli/app.py (Typer commands)

First-run setup or provider selection?
  → atrophy/cli/onboarding.py

Terminal formatting/panels?
  → atrophy/cli/output.py (show_error, show_success, show_info)

Interactive terminal dashboard?
  → atrophy/tui/dashboard.py (Textual App)

Any LLM API call?
  → atrophy/providers/ (get_provider() factory + specific provider files)

Git post-commit auto-scan?
  → atrophy/cli/app.py hook command + GitScanner --quick mode

Multi-repo management?
  → atrophy/cli/app.py repos command + Storage.list_all_projects()

Comparing time periods?
  → atrophy/cli/app.py compare/insights commands + SkillMapper on date ranges

Shareable profiles or leaderboard?
  → atrophy/cli/app.py publish/profile/leaderboard commands

Team features?
  → atrophy/cli/app.py team commands + ~/.atrophy/teams/ directory

VS Code status bar or commands?
  → vscode-extension/src/ (TypeScript, reads DB via better-sqlite3)
```

---

## Data Contracts (Exact Shapes)

These flow between modules. Match them precisely.

### Commit dict — produced by GitScanner
```python
{
    "commit_hash":          str,        # 40-char hex SHA
    "author_name":          str,
    "author_email":         str,
    "timestamp":            datetime,   # timezone-aware UTC
    "message":              str,
    "files_changed":        list[str],  # relative paths, basename only in outputs
    "additions":            int,
    "deletions":            int,
    "diff_text":            str,        # raw diff, added lines only (lines starting +)
    "minutes_since_prev":   float,      # minutes since previous commit by same author
    "session_additions":    int,        # total added lines in this coding session (<30min gap)
    "is_likely_squash":     bool,       # True if squash/merge detected
    "session_id":           str,        # UUID grouping consecutive commits into sessions
}
```

### Analyzed commit dict — AIDetector adds these fields
```python
{
    # ... all commit dict fields, plus:
    "ai_probability":       float,      # 0.0–1.0
    "classification":       str,        # "human" | "ai" | "uncertain"
    "velocity_score":       float,
    "burstiness_score":     float,
    "formatting_score":     float,
    "message_score":        float,
    "entropy_score":        float,
}
```

### Skill profile dict — produced by SkillMapper
```python
{
    "sql_databases": {
        "score":            float,      # 0–100
        "last_seen":        datetime | None,
        "total_hits":       int,
        "recent_hits":      int,        # last 30 days
        "trend":            str,        # "up" | "down" | "stable" | "new"
        "description":      str,
        "emoji":            str,
    },
    # ... same for all 10 skill keys:
    # async_concurrency, data_structures, sql_databases, regex_parsing,
    # error_handling, api_design, testing, algorithms, system_io, security
}
```

### Challenge dict — produced by ChallengeEngine
```python
{
    "skill_name":           str,
    "difficulty":           str,        # "easy" | "medium" | "hard"
    "title":                str,        # max 8 words
    "description":          str,        # 3-4 sentences
    "estimated_minutes":    int,        # 5–120
    "hints":                list[str],  # exactly 2 items
    "success_criteria":     str,        # one sentence
    "fallback":             bool,       # True if LLM response was generic
}
```

### Personal Baseline dict — produced by AIDetector.build_baseline()
```python
{
    "avg_velocity":                 float,  # lines/min, median of first 30 commits
    "avg_commit_size":              float,  # median additions per commit
    "uses_conventional_commits":    bool,   # >50% of first 30 use feat:/fix: pattern
    "uses_autoformatter":           bool,   # .ruff.toml / .prettierrc / .black present
    "typical_session_hours":        float,
    "computed_at":                  datetime,
}
```

### Team Profile dict — published by atrophy team --checkin
```python
{
    "username":             str,        # git config user.name (user can override)
    "week":                 str,        # "2026-11" format
    "skill_scores":         dict[str, float],   # all 10 skills, 0-100
    "human_ratio":          float,
    "streak_weeks":         int,
    "primary_language":     str,
    "top_skills":           list[str],  # top 3
    "skills_to_revisit":    list[str],  # dead zones
    # NO repo names, NO file paths, NO commit messages, NO code snippets
}
```

---

## AI Detection — Signal Details

When working on `ai_detector.py`, always use these exact weights and thresholds:

### Signal Weights
```python
SIGNAL_WEIGHTS = {
    "velocity":    0.30,
    "burstiness":  0.25,
    "formatting":  0.20,
    "message":     0.15,
    "entropy":     0.10,
}
```

### Velocity Signal
- Lines per minute = `additions / max(minutes_since_prev, 0.5)`
- Use SESSION-level velocity, not per-commit: group commits <45min apart
- ≥80 lines/min → 0.95 | ≥40 → 0.75 | ≥10 → 0.50 | <10 → scales to 0.05
- If `is_likely_squash=True`: floor this signal at 0.45, ceiling at 0.55

### Burstiness Signal
- CV = std(line_lengths) / (mean(line_lengths) + 1e-9) on added lines only
- CV < 0.20 → 0.85 | CV 0.20-0.40 → 0.85-0.50 | CV 0.40-0.70 → 0.50-0.15 | CV > 0.70 → 0.10
- Fewer than 5 added lines → 0.50 (not enough data)

### Formatting Signal
- Ratio of "clean" lines: consistent indent, no trailing whitespace, 1-120 chars
- Clamp to [0.1, 0.9]
- If `uses_autoformatter=True` from baseline: reduce weight from 0.20 to 0.05

### Message Signal
- Conventional commit pattern match → 0.75
- If `uses_conventional_commits=True` from baseline: INVERT — conventional = 0.25 (human)
- Message < 4 chars or contains "fix", "wip", "ok", "why", "finally" → 0.05
- If `uses_conventional_commits=True` from baseline: reduce weight from 0.15 to 0.05

### Entropy Signal
- Shannon entropy H of character frequency on added lines combined
- H > 4.8 → skip (minified), return 0.50
- H < 3.2 → 0.80 | H 3.2-3.8 → 0.50-0.30 | H 3.8-4.8 → linear 0.30-0.70

### Classification Thresholds
```python
if ai_probability >= 0.62:  classification = "ai"
elif ai_probability <= 0.38: classification = "human"
else:                        classification = "uncertain"
# squash commits: always "uncertain" regardless of score
```

### IMPORTANT Disclaimer
The `ai_detector.py` module docstring MUST always contain:
"This is a probabilistic mirror for self-reflection only. NOT accurate enough
to evaluate others. Do not use to judge teammates, grade students, or make
employment decisions."

---

## Skill Detection — 3-Layer Priority Order

Always apply layers in this order for each commit:

```
1. tree-sitter AST (if language supported AND diff >= 10 added lines)
   → TreeSitterAnalyzer.analyze_diff()
   → Most accurate — understands actual code structure

2. LLM semantic classification (if no AST support AND provider != "none" AND recent 90d)
   → LLMSkillClassifier.classify_diff()
   → Handles unknown languages and ambiguous patterns
   → Cache results by diff hash (avoid re-calling for same code)

3. Keyword fallback (always available, zero cost)
   → Only scan inside string literals and identifiers
   → Never scan inside comments or docstrings
   → Use language-specific comment strippers first
```

### The 10 Canonical Skills (keys must match exactly)
```
async_concurrency   data_structures    sql_databases    regex_parsing
error_handling      api_design         testing          algorithms
system_io           security
```

### Recency Weights (always apply)
```python
if days_ago <= 30:   weight = 3.0
elif days_ago <= 90: weight = 2.0
else:                weight = 1.0
```

### Score Formula
```python
score = min(100, weighted_hits * 2.5)
```

### Dead Zone Rules
A skill is a dead zone if EITHER:
- `last_seen` is None OR more than 45 days ago
- score < 8 (barely exercised)

---

## LLM Provider Pattern

All providers implement `BaseLLMProvider` from `providers/base.py`:

```python
class BaseLLMProvider(ABC):
    @abstractmethod
    async def complete(self, system: str, user: str, max_tokens: int = 800) -> str:
        """Returns completion text. Raises ProviderError on failure."""
```

### Provider-Specific Rules

**OpenRouter:** Uses `AsyncOpenAI(base_url="https://openrouter.ai/api/v1")`.
Model list: `GET https://openrouter.ai/api/v1/models` → `data[].{id, name, pricing.prompt}`.
Free models: `pricing.prompt == "0"`. Sort free first.
Model picker: interactive search loop — number, search term, or direct `provider/model-id`.

**Ollama Local:** Uses `ollama.AsyncClient(host=base_url)`.
SSRF guard: base_url must start with `http://localhost` or `http://127.0.0.1`.
List models: `GET {base_url}/api/tags` → `models[].{name, size, details}`.
Returns `[]` silently if not running — never crash.

**Ollama Cloud:** Uses `ollama.AsyncClient(host="https://ollama.com", headers={"Authorization": f"Bearer {key}"})`.
List cloud models: `GET https://ollama.com/api/tags` with auth header.
Same API as local — just different host + auth.

**Factory pattern:**
```python
from atrophy.providers import get_provider
provider = get_provider(settings)  # Returns correct provider or raises ProviderError
```

---

## Storage Patterns (SQLAlchemy 2.0 Only)

### Correct Pattern (always use this)
```python
async with AsyncSession(self.engine) as session:
    async with session.begin():
        result = await session.execute(
            select(Project).where(Project.path == path)
        )
        project = result.scalar_one_or_none()
```

### Wrong Pattern (never use — SQLAlchemy 1.x)
```python
session.query(Project).filter_by(path=path).first()  # WRONG
```

### All 8 Tables
```
projects, commits, skill_snapshots, challenges,
settings, baselines, wins, comparisons
```

### Key Methods to Know
```python
# Core
storage.save_project(path, name, author_email)
storage.get_project(path) → Project | None
storage.list_all_projects() → list[Project]
storage.upsert_commits(project_id, commits)
storage.save_skill_snapshots(project_id, skill_profile)
storage.get_skill_history(project_id, skill, months)
storage.get_combined_skill_profile(project_ids) → merged profile

# Challenges
storage.save_challenges(project_id, challenges)
storage.get_pending_challenges(project_id)
storage.mark_challenge_complete(challenge_id)
storage.get_streak(project_id) → int (weeks)

# Engagement
storage.detect_and_save_wins(project_id, old_profile, new_profile) → list[Win]
storage.save_comparison(project_id, period1_label, period2_label, result)
storage.get_last_comparison(project_id) → dict | None

# Baseline
storage.save_baseline(project_id, baseline_dict)
storage.get_baseline(project_id) → PersonalBaseline | None

# Settings
storage.get_setting(key, default) → str | None
storage.set_setting(key, value)
storage.update_last_scanned(project_id)
```

---

## Context Builder — For LLM Challenges

`ContextBuilder.build_challenge_context()` assembles a max-1200-char context package:

1. **Project file structure** (top 15 most-committed files by name, not content) — max 300 chars
2. **Skill-relevant code snippet** (added lines from a human commit matching this skill) — max 500 chars
3. **Tech stack** (detected from pyproject.toml/package.json/go.mod) — max 200 chars
4. **Language + framework hint** — remaining chars

If LLM response has `"fallback": true` OR description shares no words with context:
→ use `FALLBACK_CHALLENGES[skill][difficulty]` hardcoded challenge instead
→ show dim note: "(Generic challenge — add more commits for personalized ones)"

---

## Multi-Repo Rules

- `cwd` matching: commands with no flags always target the repo matching `Path.cwd()`
- `--all` flag: combines data across ALL initialized projects
- Combined skill profile: weighted average by commit count per repo
- `atrophy repos --scan-all`: runs `scan --quick` on each project sequentially with progress

---

## Git Hook Details

Hook file path: `{repo}/.git/hooks/post-commit`

Fixed content (never interpolate user input):
```bash
#!/bin/sh
# atrophy auto-scan hook
# Installed by: atrophy hook --install
# Remove with: atrophy hook --uninstall
(atrophy scan --silent --quick &) 2>/dev/null
exit 0
```

`--quick` behavior: only process commits newer than `last_scanned_at` from DB.
`--silent` behavior: zero Rich output, log to `~/.atrophy/scan.log` only.

---

## Textual TUI Rules

```python
# Always run Textual commands inline (doesn't take over full terminal)
AtrophyDashboard().run(inline=True)
ChallengeViewer().run(inline=True)
ConfigEditor().run(inline=True)

# Background data loading — never block the event loop
class AtrophyDashboard(App):
    async def on_mount(self) -> None:
        self.run_worker(self._load_data)

    async def _load_data(self) -> None:
        data = await storage.get_all_skills_latest(project_id)
        self.query_one(SkillPanel).update(data)
```

Dashboard keyboard bindings: `q` → quit, `r` → refresh, `c` → challenges.

---

## Team Mode Constraints (Immovable)

1. No central server — EVER
2. Team data travels via an existing git repo the team owns
3. Published profiles: skill scores + ratios ONLY — zero raw data
4. Show exact data to be shared BEFORE any push operation
5. Require explicit `[y/N]` confirmation before every `git push`
6. File naming: `members/{username}_{YYYY-WW}.json`
7. Team repo detection: presence of `.atrophy-team` marker file

---

## Publish / Profile Rules

### atrophy publish — shareable profile
Safe fields to include: aggregated skill scores, ratios, streak, language, coding_style, top skills, dead zones, commit count, months tracked, username.

NEVER include: repo names, file paths, commit messages, code snippets, employer info.

### atrophy profile — local HTML card
Self-contained single HTML file — no external dependencies.
SVG polygon radar chart generated in Python using:
```python
import math
def skill_polygon(scores: dict, cx=200, cy=200, max_r=150) -> str:
    n = len(scores)
    points = []
    for i, (_, score) in enumerate(scores.items()):
        angle = (2 * math.pi * i / n) - (math.pi / 2)
        r = (score / 100) * max_r
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        points.append(f"{x:.1f},{y:.1f}")
    return "M " + " L ".join(points) + " Z"
```

### GitHub Gist upload (atrophy publish → option d)
- Only read `GITHUB_TOKEN` from environment — never ask interactively
- Validate token format: starts with `ghp_` or `github_pat_`
- Show warning + require `[y/N]` before creating public Gist

---

## Compare Command Logic

### atrophy compare (default)
- Period 1: commits from 180 days ago to 90 days ago
- Period 2: commits from last 90 days
- Re-run SkillMapper on each period's commits independently
- Output: side-by-side table with delta column and trend arrows

### Change indicators
```python
if delta >= 15:   indicator = "↑↑"  # green
elif delta >= 5:  indicator = "↑"   # green
elif delta >= -4: indicator = "→"   # dim
elif delta >= -14:indicator = "↓"   # yellow
else:             indicator = "↓↓"  # red
```

### Overall trend
```python
if improvements > declines and human_ratio_improved:  "IMPROVING"  # green
elif improvements > declines:                          "MIXED"      # yellow
else:                                                  "DECLINING"  # red
```

---

## Security Checklist (Run Before Finishing Any File)

```
[ ] No shell=True anywhere — all subprocess use list args
[ ] API keys only in SecretStr — never in logs or error messages
[ ] Keys read from ~/.atrophy/.env — never from config.json
[ ] All user file paths resolved with Path.resolve() and bounds-checked
[ ] No raw SQL string concatenation — SQLAlchemy ORM only
[ ] No pickle anywhere in codebase
[ ] All network servers bind to 127.0.0.1 only
[ ] LLM responses sanitized: strip fences, validate keys, type-check, truncate >2000
[ ] Email inputs validated with regex
[ ] Git hook content is fixed template — no user input interpolation
[ ] Team publishes show exact data + require confirmation before push
[ ] GitHub token validated (ghp_ or github_pat_) before use
[ ] Path traversal check on all user-supplied file paths
```

---

## Common Mistakes — Never Repeat These

| Mistake | Fix |
|---|---|
| Using `shell=True` for git commands | Use GitPython API or `subprocess.run([...], shell=False)` |
| Writing API keys to `~/.atrophy/config.json` | Keys go to `~/.atrophy/.env` via `python-dotenv` only |
| Using `typer.prompt()` for API keys | Use `getpass.getpass()` — never echo keys |
| Using SQLAlchemy 1.x `session.query()` | Always use `select()` + `AsyncSession` |
| Blocking Textual event loop with `time.sleep()` | Use `await asyncio.sleep()` or Textual workers |
| Letting library exceptions reach the user | Catch and re-raise as AtrophyError subclass |
| Sending full file contents to LLM | Max 400 chars of diff, basenames only |
| Including repo names in team profiles | Aggregated scores only — no identifiable data |
| Using raw httpx for Ollama chat calls | Use official `ollama` Python library |
| Binding badge server to `0.0.0.0` | Always `127.0.0.1` |
| Scanning comments/docstrings for skill keywords | Strip comments first, scan identifiers only |
| Forgetting `is_likely_squash` check in velocity | Squash commits → always "uncertain" |
| Forgetting `uses_autoformatter` baseline check | Adjust formatting/message weights if true |

---

## Definition of Done

A task is complete when ALL of these pass:

1. Code follows all rules in the workspace rules file (`atrophy-rules.md`)
2. All 14 security checklist items pass
3. The data contract shapes are preserved (if touching scanner/detector/mapper)
4. A test exists in `tests/` for the new functionality
5. `uv run ruff check atrophy/` passes with zero warnings
6. The feature works end-to-end via `uv run atrophy [command]`
7. Custom exceptions are used — no raw library exceptions bubble to user
8. All terminal output goes through `atrophy/cli/output.py` or Rich directly

---

## Key Development Commands

```bash
uv sync                              # Install all dependencies
uv run atrophy --help                # Run the CLI
uv run atrophy init                  # Test init flow
uv run pytest tests/ -v              # Run all tests
uv run pytest tests/ -k "test_name"  # Run specific test
uv run ruff check atrophy/           # Lint
uv run ruff format atrophy/          # Format
uv run bandit -r atrophy/ -ll        # Security scan
uv run pip-audit                     # CVE scan
uv run pre-commit install            # Install hooks
uv run pre-commit run --all-files    # Run all pre-commit checks

# VS Code extension (from vscode-extension/ dir)
npm install
npm run compile
npm run watch
```