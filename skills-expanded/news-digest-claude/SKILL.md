# News Digest

Automated news digest emails produced by scheduled remote Claude Code agents. Each agent researches news, writes a JSON data file, then renders and sends an HTML email via `render.py`.

## Architecture

```
Scheduled trigger (Anthropic cloud)
  → Agent researches news (WebFetch + WebSearch)
  → Writes /tmp/stories.json
  → Runs: python3 render.py --template <name> --data /tmp/stories.json --send
  → Email sent via Resend API
```

## Digests

| Digest | Template | Schedule | Sections |
|--------|----------|----------|----------|
| Iran Conflict Daily | `iran-daily` | Daily 12:00 UTC (8am ET) | Military, Diplomatic, Humanitarian, Economic |
| Global Weekly | `global-weekly` | Sundays 12:00 UTC (8am ET) | Americas, Europe, Asia-Pacific, Middle East & Africa, Economy & Markets, Science & Technology |
| NYC Weekly | `nyc-weekly` | Sundays 12:00 UTC (8am ET) | City Hall & Politics, Transit & Infrastructure, Housing & Real Estate, Public Safety, Culture/Food/Events, Business & Economy, Education |
| Agentic Engineering Weekly | `agentic-weekly` | Sundays 12:00 UTC (8am ET) | Setups, Patterns, Releases |
| Indie SaaS Weekly | `indie-saas-weekly` | Sundays 12:00 UTC (8am ET) | Factory Flows, Launches, Stacks |

## Remote Triggers (3-slot limit)

| Trigger | ID | Sends |
|---------|-----|-------|
| Daily Iran War Update | `trig_016FofHKZEw7RrU7Trh5CQdY` | Iran daily |
| Weekly Global + NYC | `trig_018ygtozXBKo5TANpFuZLSxG` | Global weekly + NYC weekly |
| Weekly Agentic + Indie SaaS | `trig_01VWaVE6Ab2tNTb6hUtCTKty` | Agentic weekly + Indie SaaS weekly |

## Key Files

- `render.py` — CLI that loads a template, renders JSON data into HTML, and optionally sends via Resend. Flags: `--template`, `--data`, `--send`, `--output`.
- `templates/*.html` — HTML email templates using Python `string.Template` (`$variable` substitution). All currently extend the same base structure.
- `examples/*.json` — Sample JSON data files showing the expected schema.

## JSON Data Schema

```json
{
  "title": "string",
  "date_range": "string",
  "subject": "string (used as email subject)",
  "summary": ["bullet strings"],
  "stories": [
    {
      "section": "string",
      "headline": "string",
      "bullets": ["strings"],
      "framing_watch": "optional string"
    }
  ],
  "this_week": ["optional, NYC only"],
  "what_to_watch": ["optional developing stories"],
  "sources_consulted": [{"name": "string", "url": "string"}]
}
```

**Sources rule:** there is a single `sources_consulted` list at the footer — per-story source lists were removed because they were incomplete in practice (outlets named in `framing_watch` for coverage comparison were often missing from a story's own `sources`). Include *every* outlet that influenced the digest in any way, including ones referenced for framing/comparison.

**`render_sources_consulted` is defensive on purpose.** The research agent (Sonnet 4.6) sometimes serializes `sources_consulted` as a JSON-stringified array instead of a real list — that would previously leak literal `[{"name":...}]` text into the email footer. `render.py` now (a) `json.loads` any string input and retries, and (b) renders any list item that isn't a `{name,url}` dict as a plain-text `<span>` instead of skipping or crashing. Keep this recovery path — the agents are non-deterministic and this is the only guardrail between bad JSON and a visibly broken email.

**Tests.** `python3 -m unittest tests.test_render -v` from the repo root. Add regression cases to `tests/test_render.py` — do not write one-off scripts in `/tmp/`.

## Environment

- `RESEND_API_KEY` — Required for `--send`. Already configured in the Anthropic cloud default environment.
- `DIGEST_TO_EMAIL` — Recipient(s). `render.py` supports a comma-separated list.
- `DIGEST_FROM_EMAIL` — Sender (default: `digest@morningtide.news`)

## Email Accounts & DNS

| Service | Auth | Purpose & Notes |
|---------|------|-----------------|
| Resend | `crotto100@hotmail.com` | Outbound digest sends from `digest@morningtide.news`. Domain `morningtide.news` verified. **Separate Resend account** from PageAudit/MailScore — Resend free tier allows only 1 domain per account. API key embedded in trigger prompts (`re_3BPhVaDS_*`). |
| ImprovMX | Magic-link login as `cotto3@icloud.com` | Inbound: catch-all `*@morningtide.news` → `cotto3@icloud.com`. Free tier. MX records (`mx1/mx2.improvmx.com`) added to Squarespace DNS 2026-05-02. Replies to digest emails land in the iCloud inbox. |

## Remote Execution

Triggers are managed via `RemoteTrigger` API (or https://claude.ai/code/scheduled). The agents run in Anthropic's cloud with a git checkout of this repo. Allowed tools: `Bash`, `Write`, `WebSearch`, `WebFetch`.

### Recipient management (important)

**Recipient lists and the Resend API key currently live inside each trigger's prompt blob**, not in the repo or the trigger's environment variables. Each trigger's Phase "Render and send" step inlines `export DIGEST_TO_EMAIL="a@x,b@y,..."` and `export RESEND_API_KEY=...` into a bash block. To add/remove a recipient you must `RemoteTrigger get` the trigger, edit the `DIGEST_TO_EMAIL` line inside `job_config.ccr.events[0].data.message.content`, and `RemoteTrigger update` with the full job_config. The "Weekly Global + NYC" trigger contains **two** `DIGEST_TO_EMAIL` exports — one per digest — so scope changes carefully.

Cleaner pattern (not yet implemented): move `RESEND_API_KEY` and per-digest `DIGEST_TO_EMAIL` into trigger env vars so recipient edits don't require rewriting the prompt and the API key stops living in trigger history.

### Editing trigger prompts (pattern that actually works)

Each trigger's prompt blob is 3-7KB and contains JSON examples with escaped quotes and embedded code fences. Do **not** hand-escape this inside a `RemoteTrigger update` call — one missed `\"` corrupts the trigger. Instead:

1. Write a small Python helper (`/tmp/build_trigger_updates.py`) that defines each new content string as a raw triple-quoted literal and serializes the full `job_config` body to `/tmp/update_*.json`. Preserve `environment_id`, `session_context`, event `uuid`, and the API key line from the current `RemoteTrigger get`.
2. For each trigger, run `python3 -c "import json; print(json.dumps(json.load(open('/tmp/update_X.json')), ensure_ascii=False))"` in Bash. The Bash tool output gives you the compact, correctly-escaped JSON.
3. Paste that compact JSON directly into the `body` parameter of a `RemoteTrigger update` call. Verify via `RemoteTrigger list` or `get` afterwards.

This was the only reliable way to do schema migrations on the triggers; inline hand-escaping kept breaking.
