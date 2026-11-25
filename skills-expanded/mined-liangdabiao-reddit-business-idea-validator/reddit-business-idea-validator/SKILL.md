---
name: reddit-business-idea-validator
description: >
  Validate a business idea by scraping Reddit posts/comments and running a
  multi-agent LLM analysis pipeline that produces a scored HTML report.
  Use whenever the user says things like "验证创业想法", "调研 XX 在 Reddit
  上的反响", "这个产品有市场吗", "validate business idea", "is X a good
  business idea", "analyze market demand for X", "what pain points do
  people have around X", or provides a product/niche/idea and wants market
  signals, pain points, sentiment, competitive landscape, or a go/no-go
  recommendation. Also use when the user references this repo's pipeline
  ("跑一下 agent", "用 orchestrator 验证", "生成报告") and asks for a
  report. Produces an HTML report at reports/{idea}_{timestamp}.html with
  a 0-100 overall score, pain points, existing solutions, opportunities,
  recommendations, and a 4-category comment tag analysis.
---

# Reddit Business Idea Validator

**Self-contained skill** — the entire validation pipeline is vendored under
`pipeline/` inside this skill directory. No imports from the host repo.
DO NOT reimplement scraping, analysis, or report rendering. Your job is to:
(1) preflight the environment, (2) launch the pipeline with the right
parameter profile, (3) recover from common failures using checkpoints, and
(4) surface the score and report path to the user.

## Prerequisites

- The skill can run from any working directory — invoke scripts via absolute
  paths derived from `<skill_dir>`.
- `.env` with at minimum (searched in this order: cwd, then skill root):
  - `OPENAI_API_KEY`, `OPENAI_BASE_URL` (must end with `/v1`), `OPENAI_MODEL`
  - `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, `REDDIT_USER_AGENT`
- Python 3.10+, `pip install -r <skill_dir>/requirements.txt` already run.
- Reddit app type must be **"script"** at https://www.reddit.com/prefs/apps
  (otherwise 401 on auth).

## File Layout

```
.claude/skills/reddit-business-idea-validator/
├── SKILL.md                         # this file
├── requirements.txt                 # Python deps for the vendored pipeline
├── scripts/
│   ├── preflight.py                 # Phase 1: env/deps/API checks
│   ├── run_pipeline.py              # Phase 3: non-interactive runner
│   ├── recover.py                   # Phase 4: list/inspect/resume runs
│   └── extract_report.py            # Phase 5: read run_id → report/score
├── pipeline/                        # vendored, self-contained pipeline
│   ├── paths.py                     # central output-path definitions
│   ├── agents/                      # orchestrator + 4 subagents + skills
│   ├── mcp_servers/                 # reddit / llm / storage MCP servers
│   └── models/                      # pydantic data models
├── references/
│   ├── failure-recovery.md          # error → fix map
│   ├── param-matrix.md              # fast / standard / deep profiles
│   └── report-anatomy.md            # report sections explained
├── reports/                         # OUTPUT: generated HTML reports
├── agent_context/checkpoints/       # OUTPUT: per-run checkpoint JSONs
└── logs/                            # OUTPUT: pipeline logs
```

All scripts accept `-h` / `--help`. Most emit JSON or JSONL so you can parse
them programmatically. All outputs (reports, checkpoints, logs) are managed
by the skill and land under the skill directory — see `pipeline/paths.py`.

## Workflow

### Phase 0 — Decide if this skill applies

Apply when the user provides an idea/product/niche AND wants one of:
market validation, pain-point discovery, demand estimation, sentiment,
competitive landscape, go/no-go recommendation, or a Reddit-based report.

Do NOT apply for: pure keyword research, SEO tasks, generic LLM brainstorming,
or when the user clearly wants a different data source (App Store, Amazon,
Xiaohongshu, etc.) — this pipeline only covers Reddit.

If the user does not state a data source but mentions "Reddit", " subreddit",
"post", or English-language markets, default to this skill.

### Phase 1 — Preflight (always run first)

```bash
python "<skill_dir>/scripts/preflight.py"
```

Outputs a single JSON object. Read it and react:

| Field | On false |
|---|---|
| `env_ok` | List the missing keys from `missing[]`, tell user to create `.env` in cwd or at `<skill_dir>/.env`, **STOP** |
| `deps_ok` | Offer `pip install -r <skill_dir>/requirements.txt`, then re-run preflight |
| `reddit_ok` | Likely wrong app type — tell user to verify Reddit app is "script" type at https://www.reddit.com/prefs/apps |
| `llm_ok` | Check `OPENAI_BASE_URL` ends with `/v1`; check API quota/billing |

Only proceed to Phase 3 when `env_ok && deps_ok && reddit_ok && llm_ok` are
all true. Preflight is fast (<5 s) — re-run freely.

### Phase 2 — Pick a parameter profile

Default to **standard**. Offer the choice via `AskUserQuestion` if the user
hasn't specified; otherwise pick based on signals:

- "fast" / "快速" / "试试" / "smoke test" / dev iteration → **fast**
- default / "完整" / "正式" / "深度调研" / no signal → **standard**
- "尽可能多" / "最深" / "thorough" / one-shot for a real decision → **deep**

See `references/param-matrix.md` for exact numbers per profile.

### Phase 3 — Run the pipeline

Launch in **background**, then poll output. The runner emits JSONL on stdout
(one event per line) and a final summary event you can parse.

```bash
python "<skill_dir>/scripts/run_pipeline.py" "<idea>" --profile standard
```

Use the Bash tool with `run_in_background: true`. Read incremental output
with `TaskOutput`. Each line is JSON; key events:

```
{"event":"run_started","run_id":"...","profile":"standard","idea":"..."}
{"event":"stage","step":"scrape_data","progress":0.0,"message":"执行: 抓取..."}
{"event":"stage","step":"scrape_data","progress":1.0,"message":"完成: 抓取..."}
...
{"event":"done","success":true,"report_path":"D:\\...\\reports\\<idea>_<ts>.html","score":72,"run_id":"...","execution_time":187.4}
```

On `event:"done"` with `success:true`, you have the report path and score —
go to Phase 5.

On `event:"done"` with `success:false`, read `error` and `failed_step`, then
jump to Phase 4 / `references/failure-recovery.md`.

### Phase 4 — Recover from failure

Two recovery modes:

**4a. Resume from checkpoint** — useful when scrape or analysis succeeded
but a later step crashed (timeout, network blip):

```bash
python "<skill_dir>/scripts/recover.py" --resume-last --idea "<idea>" --profile standard
```

This finds the latest run_id for that idea, inspects which checkpoints
exist, and re-invokes the pipeline using existing partial results where
possible.

**4b. Just list & inspect** — for understanding state:

```bash
python "<skill_dir>/scripts/recover.py" --list                       # all runs
python "<skill_dir>/scripts/recover.py" --list --idea "<idea>"       # filtered
python "<skill_dir>/scripts/recover.py" --show <run_id>              # checkpoint detail
```

For known errors (401, quota, malformed JSON), follow `references/failure-recovery.md`
instead of blind retry — some failures are deterministic and need a human
fix.

### Phase 5 — Surface results to the user

After `event:"done"`:

1. **Extract full result** (cheap, idempotent):
   ```bash
   python "<skill_dir>/scripts/extract_report.py" --run-id "<run_id>"
   ```
   Returns JSON with `report_path`, `score`, `summary`, top pain points,
   opportunities, and recommendations.

2. **Tell the user** in chat, concisely:
   - Overall score (0-100) and one-line gut interpretation
     (≥75 strong, 50-74 promising, 30-49 weak, <30 likely no-go)
   - Top 3 pain points
   - Top 3 opportunities
   - Report absolute path — offer to open in browser
   - Run id (so they can resume later or compare)

3. **Do not paste the full HTML.** It's large. Summarize; the user can open
   the file.

4. Offer follow-ups: re-run with `deep` profile, compare with another run,
   adjust the idea wording and re-validate.

## Operating Principles

- **Never reimplement pipeline stages.** Call `run_pipeline.py`.
- **Always run preflight before the pipeline** on a fresh session — costs
  5 seconds, saves a 10-minute failure.
- **Background the pipeline.** It can take 3-30 min depending on profile.
  Use `run_in_background: true` and poll `TaskOutput`; don't block the turn.
- **Parse JSONL, don't regex human text.** Stderr still has human logs for
  debugging — only stdout is structured.
- **Be honest about scores.** A 35/100 is a useful negative result. Don't
  sugarcoat; the user wants signal.
- **Resume > restart.** If a stage crashed after a successful scrape,
  reuse the scrape via `recover.py --resume-last` instead of re-scraping
  (Reddit rate limits are real).

## Common Mistakes to Avoid

- Don't pass `--profile fast` to "be helpful" without asking — fast misses
  signal. Default is `standard`.
- Don't read `.env` keys yourself to "verify" — preflight already does it
  authoritatively.
- Don't try to `pip install` new packages mid-run; if preflight says deps
  missing, ask the user.
- Don't shorten the business idea when passing it through — the pipeline
  uses it as the search keyword verbatim.
- Don't run two pipelines in parallel — they share `reports/` and checkpoint
  dirs and will race on filenames.

## References (read on demand)

- `references/failure-recovery.md` — error → fix table, opened when phase 3/4 fails
- `references/param-matrix.md` — exact knobs per profile
- `references/report-anatomy.md` — what each section of the HTML report means
