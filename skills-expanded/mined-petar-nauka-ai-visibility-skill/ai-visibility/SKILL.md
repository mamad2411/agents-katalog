---
name: ai-visibility
description: Measure and improve whether AI assistants (ChatGPT, Claude, Gemini, Perplexity, Copilot) recommend a brand, and fix the reasons they do not. Use this skill whenever someone asks about AI visibility, AEO, GEO, answer engine optimization, generative engine optimization, "AI SEO", brand mentions or share of voice in AI answers, whether ChatGPT/Claude/Gemini recommends their site or product, why a competitor shows up in AI answers instead of them, llms.txt, robots.txt rules for GPTBot / ClaudeBot / PerplexityBot / Google-Extended, schema markup or JSON-LD for AI citation, tracking AI referral traffic in GA4, Bing indexing for ChatGPT, or auditing a page so assistants can quote it. Use it even when the request is vague ("are we showing up in ChatGPT?", "how do I get AI to mention my company?", "check if AI knows about my site") — it turns those into a measured audit with a fix list.
license: MIT
---

# AI visibility

## What this is for

Search used to rank pages; assistants recommend brands. When someone asks
ChatGPT "which is the best X for Y", they get three to five names and pick from
that list. There is no second page. If the brand is not in the list, it does not
exist for that buyer.

Three facts shape everything below:

- **Answers vary by model.** Overlap between the domains ChatGPT and Perplexity
  cite is roughly 11%. Checking one assistant tells you almost nothing.
- **The description matters as much as the mention.** When a model names a
  brand, it also characterises it in one sentence the brand did not write. That
  sentence is the positioning buyers act on.
- **Most of the signal is off-site.** Around 85% of brand mentions in AI answers
  trace back to third-party sources, not the brand's own pages. Rewriting the
  homepage alone rarely moves the number.

This skill measures the current state, then produces a ranked list of fixes.
It runs locally on plain files — no account, no database, no API key required.

## Workflow

Work through these in order. Steps 1-5 are the measurement; 6-8 are the fix.
Announce which step you are on so the user can follow along.

Everything lives in a **workspace directory** — create it inside the user's
project (or wherever they ask), never in a temp folder they will lose.

All scripts are `python3` with the standard library only. Invoke them as
`python <skill>/scripts/aeo.py -w <workspace> <command>`.

### 1. Set up the brand

```bash
python scripts/aeo.py -w ./ai-visibility init example.com --name "Example"
```

Then interview the user and fill in `brand.json`. Getting this right decides
whether the whole audit is accurate:

| Field | Why it matters |
|---|---|
| `domain` | The strongest mention signal. Bare domain, no `www`, no protocol. |
| `aliases` | Other names the brand goes by, including in other alphabets. A brand called in Cyrillic will be missed without this. |
| `keywords` | Distinctive product or service names that identify the brand even when its name is absent. |
| `competitors` | Named rivals. Unknown competitors are discovered automatically; listing the known ones makes share-of-voice comparable across runs. |
| `positioning` | One sentence: what it does, for whom, what makes it different. Used later to judge whether the model's description is right. |

If the user does not know their competitors, run step 4 first with a handful of
prompts — the answers will name them.

### 2. Build the prompt set

This is the step most people get wrong, and it determines whether the audit is
useful. Read `references/prompt-research.md` before writing prompts.

The short version: buyers write ~23 words describing their situation, not 3
keywords. Brand-name prompts are easy and nearly worthless. What you want are
the unbranded, situation-specific questions asked right before a decision.

Generate 15-25 prompts with the user, in **their buyers' language** (not
necessarily English), each tagged with `category` and `intent`. Write them to
`prompts.json`. Intent drives prioritisation later, so classify honestly:
`high` = close to buying, `low` = browsing.

### 3. Collect answers

Three routes; pick based on what the user has. **B is the most trustworthy**
because it captures what real assistants actually serve today.

**A — you answer them (no setup).** Create the files, then answer each prompt
yourself using web search, writing the answer into the file below the `====`
line.

```bash
python scripts/aeo.py -w ./ai-visibility run --models claude
```

Answer each prompt as you would for any user asking it cold: search, then give
your honest recommendation. Do this *before* reading `brand.json`, and do not
let the tracked brand influence the answer — otherwise the measurement is
worthless. Label this run `claude` and tell the user plainly that it is one
model's view, produced by the same assistant running the audit.

**B — the user pastes real answers (recommended).**

```bash
python scripts/aeo.py -w ./ai-visibility run --models chatgpt gemini perplexity claude
```

This creates one file per prompt × model. The user opens each assistant, asks
the prompt, and pastes the full answer under the `====` line, replacing
`(no response)`. Tell them to paste everything including links — citations are
data. Leaving a file untouched is fine; unfilled answers are excluded from the
percentages rather than counted as misses.

**C — automated via OpenRouter.** One API key covers every model.

```bash
export OPENROUTER_API_KEY=sk-or-...
python scripts/aeo.py -w ./ai-visibility collect --models chatgpt gemini perplexity
```

Roughly $0.02-0.10 per prompt × model with the default lightweight models. Warn
the user before spending their money, and quote the count: 20 prompts × 3
models = 60 calls.

### 4. Analyze and report

```bash
python scripts/aeo.py -w ./ai-visibility analyze
python scripts/aeo.py -w ./ai-visibility report
```

This scores every answer — mentioned or not, the sentence describing the brand,
position in any ranked list, sentiment, competitors, cited URLs — and writes
`report.html` (self-contained, openable in a browser) plus `summary.md`.

### 5. Read the results with the user

Do not just hand over the percentage. Walk through, in this order:

1. **Lost high-intent prompts.** Each one is a buyer being sent to a competitor.
   This is the whole point of the exercise.
2. **The descriptions.** Open `runs/<date>/results.json` and read the
   `description` field for answers where the brand appears. Compare each to
   `positioning`. A brand that sells premium but gets described as "a budget
   option" has a perception problem no amount of technical work will fix.
3. **Position.** Being 5th of 5 is closer to invisible than to 1st.
4. **Where competitors are cited.** `Most-cited pages` in the report lists pages
   already inside the answers. Getting mentioned on one of those is usually
   cheaper than ranking a new page.

### 6. Diagnose why

For each lost high-intent prompt, work out the cause. Read
`references/diagnosis.md` — it gives the three root causes (coverage,
consistency, specificity), how to tell them apart from the evidence in the run,
and what each one implies. Produce a short diagnosis per prompt, not a generic
lecture.

### 7. Fix the technical layer

```bash
python scripts/aeo.py -w ./ai-visibility tech
```

Checks whether AI crawlers are allowed, whether `llms.txt` and `sitemap.xml`
exist, and what schema the homepage exposes. A blocked crawler makes every
other effort pointless, so this is the first thing to repair.

Generators for the fixes:

```bash
python scripts/aeo.py schema spec.json          # JSON-LD, ready to paste
python scripts/aeo.py -w ./ai-visibility llmstxt --limit 40
```

`references/technical-fixes.md` covers robots.txt recipes per crawler, which
schema types matter, the `llms.txt` format, Bing Webmaster setup (ChatGPT
searches through Bing), and the GA4 channel-group regex for measuring AI
referral traffic.

### 8. Fix the content

For each page that should be winning a lost prompt:

```bash
python scripts/aeo.py -w ./ai-visibility page https://example.com/some-page
```

This extracts the signals that decide whether an assistant can lift a quotable
answer out of the page. Score them against the seven criteria in
`references/content-rubric.md` and give the user concrete rewrites — actual
sentences and markup they can paste, not advice to "improve clarity".

`references/playbook.md` holds the five levers behind all of this: clarity,
positioning, third-party presence, structure, and measurement. Consult it when
the user asks *what to do* rather than *what is broken*.

## Re-running

Visibility is a trend, not a snapshot. Suggest a monthly re-run: same prompts,
same models, new run directory (`--run 2026-09-01`). The report shows the delta
automatically, and withholds it when the two runs used different models — a
comparison across different model sets is not a trend.

## Command reference

| Command | Purpose |
|---|---|
| `init <domain>` | Create workspace, `brand.json`, `prompts.json` |
| `run [--models ...] [--run ID]` | Create empty answer files to fill in |
| `collect [--models ...]` | Fetch answers via OpenRouter (needs `OPENROUTER_API_KEY`) |
| `analyze [--run ID]` | Score answers into `results.json` |
| `report` | Build `report.html` + `summary.md` |
| `tech [domain]` | Crawler access, llms.txt, sitemap, homepage schema, AEO score |
| `page <url>` | Extract AEO signals from one page |
| `schema <spec.json>` | Generate JSON-LD |
| `llmstxt [--limit N]` | Generate `llms.txt` from the sitemap |
| `selftest` | Verify the detection logic (49 checks) |

Every command takes `-w/--workspace` and `-h`.

## Working notes

- **Answer in the user's language.** The tooling is language-neutral; prompts,
  descriptions, and your analysis should be in whatever language the user and
  their buyers use. Bulgarian and English sentiment terms ship by default;
  for other languages, extend `POSITIVE_WORDS` / `NEGATIVE_WORDS` in
  `scripts/aeolib.py` and add `context_words` to `brand.json`.
- **Sentiment is triage, not truth.** It is a keyword tally. Treat every
  `negative` as a signal to read the raw answer, not as a finding.
- **Never invent numbers.** Every figure in your summary must come from
  `results.json` or `metrics.json`. If a run is thin, say so.
- **Empty answers are not misses.** They are excluded from the denominator and
  reported separately. Do not let a half-filled run become "visibility dropped".
- **One model is not a measurement.** If the user only checked ChatGPT, say
  what that does and does not tell them before drawing conclusions.
- **If outbound network access is unavailable** (common in a sandboxed
  environment), `tech`, `page`, `collect`, and `llmstxt --limit` cannot fetch.
  Everything else — the whole measurement and diagnosis path — still works,
  because it reads pasted answers from disk. For the fetching commands, ask the
  user to paste the content instead: `robots.txt`, `llms.txt`, the page HTML, or
  the sitemap. Then analyze it directly rather than reporting a failure. Do not
  present a blocked fetch as a finding about their site.

## File layout

```
<workspace>/
├── brand.json              domain, aliases, keywords, competitors, positioning
├── prompts.json            id, text, category, intent
├── runs/
│   └── 2026-08-01/
│       ├── responses/      p01__chatgpt.txt … one file per prompt × model
│       ├── results.json    per-answer analysis
│       └── metrics.json    aggregated metrics
├── report.html             self-contained dashboard
├── summary.md              same findings as markdown
└── technical-audit.json    crawler / schema / llms.txt state
```

`references/workspace.md` documents every field and the answer-file format,
including how to import answers exported from another tool.
