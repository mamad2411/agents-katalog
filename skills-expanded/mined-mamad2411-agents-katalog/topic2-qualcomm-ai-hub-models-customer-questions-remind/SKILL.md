# Customer Questions — Remind Czar + Draft from KB (Hybrid)

Read scraped customer questions, classify whether each thread has been
substantively answered, and emit `reminders.json`. For threads that still
need follow-up (`no-reply` / `ack-only`), also draft a starter answer from
the curated KB at `.claude/triage/customer-faq.md` — but **only when
drafting is enabled** (see `ENABLE_DRAFTS` under Context Variables).

The downstream `post-to-slack` job posts a single internal Slack message
listing the threads that still need a reply. When the JSON contains
drafts, they are attached as threaded replies under each reminder.

**You do NOT post to Slack. Your only outputs are the JSON file and a
base64 emit of it on stdout.**

**Budget: ~30 tool calls for ≤10 questions, ~50 for up to the cap. Batch
reads. Do NOT re-read the same file twice.**

## Context Variables

Injected via the workflow prompt:
- `QUESTIONS_PATH` — local file path to `questions.json` (input)
- `DRAFTS_PATH` — local file path where you must write the JSON output
  (the filename is `drafts.json` for compatibility with the post script)
- `MAX_QUESTIONS` — process at most this many questions
- `ENABLE_DRAFTS` — `"true"` or `"false"`. Gates draft emission in
  Step 2b. When `"false"` (default), classify every question but emit
  null draft fields with empty `flags` — the KB quality bar is not yet
  high enough for prod. When `"true"`, run Step 2b as documented.

Slack channel routing (`test_mode` workflow input) is handled by the
downstream post-to-slack job and is **not** exposed to you. Your
behavior does not depend on the target channel.

## Critical Rules

- **NEVER post to Slack or GitHub from this skill.** The downstream
  `post-to-slack` job handles posting.
- **NEVER address the customer or post on their original thread.** Drafts
  are for internal czar review only.
- **Liberal classification.** When in doubt whether a reply is substantive,
  err toward `no-reply` or `ack-only` — over-reminding is cheap; missing a
  real unanswered customer question is not.
- **Drafts ONLY when `ENABLE_DRAFTS == "true"` AND status is `no-reply` /
  `ack-only`.** Skip drafting entirely when `ENABLE_DRAFTS == "false"`
  and, when drafting is enabled, also skip for `answered` (already
  handled) and `internal-noise` (not a real question).
- **Drafts MUST be grounded in the KB.** If no FAQ entry matches, emit
  `draft_answer: null` rather than hallucinating. A null draft + `kb_miss`
  flag is more useful than a guess.
- **Drafts are short.** 2–4 sentences. No preamble ("Great question!"),
  no padding. Front-load the actionable fix.

## Step 1: Read input and the KB (~2 tool calls)

Read `$QUESTIONS_PATH`. The JSON shape is:

```json
{
  "questions": [
    {
      "id": "slack-CXXXXX-1731349200.000100",
      "medium": "slack" | "github",
      "channel_or_repo": "ai-hub-models",
      "thread_url": "https://qualcomm.slack.com/archives/...",
      "submitted_by": "Customer Name",
      "submitted_at": "2026-06-22T14:30:00Z",
      "title": "",
      "question": "full question text",
      "thread_replies": [
        {"user": "name", "is_internal": true, "text": "reply text"}
      ],
      "has_internal_reply": true
    }
  ]
}
```

Read `.claude/triage/customer-faq.md`. Each entry has the shape:

```
### faq-<id>

**Triggers:**
- "phrase 1"
- "phrase 2"
- mentions of `code_token`

**Question shape:** <one-line description>

**Answer:**
<canonical answer body>

**Citations:**
- `path/to/file.py:NN`
- https://...

**Confidence floor:** high | medium | low
**Last updated:** YYYY-MM-DD
```

Hold the KB in working memory for Step 2. Do not re-read it for each
question.

## Step 2: Per-question classification + drafting

For **each** question (up to `MAX_QUESTIONS`):

### 2a. Classify (always required)

Pick exactly one `status`:

| Status | Meaning | When to use |
|---|---|---|
| `no-reply` | Thread has zero Qualcomm replies. | `has_internal_reply == false` AND the question is a real customer ask. |
| `ack-only` | Qualcomm replied but only acknowledged ("got it, looking", "checking", "let me find the right person"). No substantive answer yet. | Internal replies present but none answer the question. **When uncertain, default to `ack-only`.** |
| `answered` | A Qualcomm engineer posted a substantive answer (named a fix, gave a number, pointed at a file/doc/release, redirected with concrete next step). | Reviewer would read this and say "no follow-up needed." |
| `internal-noise` | The "question" is internal chatter, a bump, a bot post, or otherwise not a real customer question. | Anything that slipped past the scraper filter. |

**Substantive vs ack — read every internal reply for intent, not keywords.**

Before applying any keyword shortcut, decide what each internal reply is
*doing*. Every reply falls into exactly one bucket:

1. **Handoff / routing** — an internal user pings another engineer to
   answer. Signature: contains a Slack `@mention` (`<@UXXX>`) AND a
   routing verb: "chime in", "any chance you can help", "take a look",
   "can you look at this", "please help", "assist", "point to the right
   person", "who can answer this". A handoff is **always** `ack-only`
   contribution — **even if the same message also contains a URL, a
   version number, or a channel name.** The URL is context for the
   pinged engineer, not an answer to the customer.
2. **Ack / info-gathering** — "got it, looking", "checking with X",
   "let me find someone", or a reply that asks the customer for more
   info ("what QAIRT version?", "which device?"). `ack-only`
   contribution.
3. **Redirect** — "please ask in <Discord / other Slack channel /
   forum>" without also answering the question. `ack-only` unless the
   customer's question was literally "where do I ask?" (in which case
   the redirect IS the answer).
4. **Substantive answer** — names a fix, gives a specific number,
   links a doc/PR/release that directly resolves the question, gives a
   specific command/flag, or definitively says "not supported on X".

**Per-thread rule:** the thread is `answered` **only if at least one
internal reply is bucket #4.** If every internal reply is #1, #2, or #3,
the thread is `ack-only`. `no-reply` is reserved for zero internal
replies.

**Common false-positive traps (all → `ack-only`, NOT `answered`):**
- Handoff that also cites a URL for the pinged engineer's reference
  (e.g. "<@Eng> any chance you can help — see this thread"). The URL
  isn't answering the customer.
- Redirect to Discord / Qualcomm Developer forum / another Slack
  channel when the customer's technical question is still open.
- A reply that only lists next-step questions to ask the customer —
  that's info-gathering, not an answer.
- Multiple handoffs stacked in one message (e.g. `<@A> <@B> can one of
  you chime in`). Still `ack-only` regardless of URL count.

**Common false-negative traps (all → `answered`, NOT `ack-only`):**
- A short internal reply that names a tool + quickstart URL (or a
  released app URL) as the answer, even when the customer's question
  was multi-part. The reply can be *higher-altitude* than the ask —
  "use tool X, or the shipped app" supersedes sub-questions about
  which flag / preprocessing step of tool Y.
- A one-line reply that redefines the recommended path ("this is now
  the supported way") + URL. If the URL directly resolves the
  question, it's bucket #4 regardless of reply length.

**Only after ruling out #1–#3 for every internal reply**, apply keyword
shortcuts to confirm bucket #4:
- "use v0.56.0", "set --target-runtime onnx", "fixed in #1234",
  "that model isn't supported on X chip" → substantive answer.
- A reply containing a specific number, file path, URL, or command
  **without** handoff / redirect signals → substantive answer.

**Age calculation:** compute `age_hours` as the integer hours between
`submitted_at` and the current UTC time. Treat any parse failure as `0`.

**Topic tag (1–2 words):** for every classified question — including
`answered` and `internal-noise` — emit a `topic` string of **1–2 words**
that captures what the thread is about. The czar uses this to scan the
reminder list at a glance without having to click each thread or read
the verbatim question.

Good topics (concrete, scannable):
- `qwen3 export`, `genie crash`, `sa8295 quant`, `tps regression`,
  `release assets`, `context length`, `qairt version`, `byom`, `melotts`,
  `npu dual`, `dlc adapter`, `windows arm`, `ubuntu setup`,
  `gemma roadmap`, `aimet config`

Avoid topics that are too generic to be useful:
- `bug`, `help`, `error`, `question`, `support` (these don't narrow
  anything)

If the question is `internal-noise` (a bump, channel chatter), use
`noise` or `bump` as the topic — the czar will skip those.

### 2b. Draft (drafting-enabled only; only for `no-reply` and `ack-only`)

**Gate:** if `ENABLE_DRAFTS == "false"` (the default), skip this section
entirely — for every question (regardless of status), emit
`draft_answer: null`, `kb_citation: null`, `confidence: null`,
`flags: []`. Do not read the KB. The reminder-only path is the default
behavior until the KB quality bar is met.

Otherwise (`ENABLE_DRAFTS == "true"`), for each question classified
`no-reply` or `ack-only`, attempt to draft a starter answer from the KB:

1. **Match against FAQ triggers.** Scan each FAQ entry's `Triggers` block
   for substring / keyword overlap with the customer's question (and the
   thread context). A match means the question is the same *shape* — not
   necessarily verbatim. If 2+ entries match, prefer the one with the
   most specific triggers.
2. **If a match is found:**
   - `draft_answer`: 2–4 sentences. Paraphrase the FAQ's `Answer` body,
     adapted to the customer's specific wording (their chipset, their
     model, their error). Front-load the fix. Drop preamble.
   - `kb_citation`: the FAQ `id` (e.g. `faq-qwen3-x2-elite-assets`).
   - `confidence`: copy from FAQ's `Confidence floor`.
   - `flags`: `[]`
3. **If no FAQ matches:**
   - `draft_answer`: `null`
   - `kb_citation`: `null`
   - `confidence`: `null`
   - `flags`: `["kb_miss"]`

**Drafts NEVER:**
- Address the customer ("Hi <name>")
- Mention internal-only details (memory, conversation context, agent name)
- Include code blocks longer than 3 lines (link to docs instead)
- Speculate beyond what the FAQ says

**Drafts SHOULD:**
- Lead with the actionable fix or the recommended command/version
- Cite the FAQ's `Citations` inline if relevant
- Stay under ~80 words

For `answered` and `internal-noise` questions: do not draft. Leave
`draft_answer`, `kb_citation`, `confidence` as `null` and `flags` as `[]`.

## Step 3: Output schema

Write to `$DRAFTS_PATH`:

```json
{
  "drafted_at": "<UTC ISO8601>",
  "drafts": [
    {
      "question_id": "<from input id>",
      "thread_url": "<from input>",
      "channel_or_repo": "<from input>",
      "submitted_by": "<from input>",
      "question_excerpt": "<first 200 chars of question text, single-line>",
      "topic": "<1-2 word category, e.g. 'qwen3 export'>",
      "age_hours": 27,
      "status": "no-reply" | "ack-only" | "answered" | "internal-noise",
      "draft_answer": "<2-4 sentence draft, or null>",
      "kb_citation": "<faq-id, or null>",
      "confidence": "high" | "medium" | "low" | null,
      "flags": []
    }
  ]
}
```

Field notes:
- Include **every** classified question, including `answered` and
  `internal-noise`. The post script filters to remind-worthy statuses;
  keeping the full list in the artifact makes review easier.
- `question_excerpt`: replace internal newlines with a single space, then
  take the first 200 chars. No mrkdwn formatting. **Retained in the JSON
  artifact for forensic review** even though the parent Slack message no
  longer prints it.
- `topic`: 1–2 words, see the topic tag guidance above. This is what the
  parent Slack bullet shows in lieu of the question excerpt.
- `flags` may include `kb_miss` (no FAQ matched) or `kb_partial` (matched
  but the FAQ only partially addresses the question). Leave `[]` otherwise.

After writing, print one summary line:
`Classified N questions: <a> no-reply (<d1> drafted, <m1> kb_miss), <b> ack-only (<d2> drafted, <m2> kb_miss), <c> answered, <d> internal-noise.`

## Step 4: Emit the JSON for the downstream post-to-slack job

The reusable agent workflow does NOT propagate `SLACK_NOTIFIER_TOKEN` to
your shell steps. The downstream `post-to-slack` job recovers the JSON
from this log via known markers.

Run this as ONE Bash call (the Breeze allowlist permits `python3` but
not `echo` / `base64` / compound shell — the helper wraps both):

```bash
python3 scripts/breeze_customer_questions/emit_drafts_b64.py "$DRAFTS_PATH"
```

## Step 5: Done

Do **not** open a PR. Do **not** post on the customer's original thread.
Do **not** post drafts directly to the customer. Your output is:
`$DRAFTS_PATH` (the file) plus the base64 emit on stdout. The downstream
`post-to-slack` job posts the reminder message + thread replies and
uploads the JSON as a workflow artifact.

## Examples (mental model)

**Question:** "We can't load Qwen2-7B on Snapdragon X2 Elite — release-assets.yaml missing."
Thread replies: `[{user: "Eng A", is_internal: true, text: "Looking at this — will follow up."}]`
KB match: `faq-qwen3-x2-elite-assets`
→ `status: ack-only`, `topic: "qwen3 export"`, `draft_answer: "Qwen2-7B is old and we're not adding precompiled assets — recommend migrating to Qwen3-4B-Instruct-2507. Assets for X2 Elite are at https://qaihub-public-assets.s3.us-west-2.amazonaws.com/qai-hub-models/models/qwen3_4b_instruct_2507/releases/v0.56.0/qwen3_4b_instruct_2507-genie-w4a16-qualcomm_snapdragon_x2_elite.zip"`,
`kb_citation: "faq-qwen3-x2-elite-assets"`, `confidence: "high"`.

**Question:** "Where is the prebuilt UNet QNN bundle for v0.48.0?"
Thread replies: `[{user: "Eng B", is_internal: true, text: "https://qaihub-public-assets.s3... — that's the v0.48.0 UNet bundle."}]`
→ `status: answered` (specific URL given). `topic: "release assets"`,
`draft_answer: null`, `kb_citation: null`, `confidence: null`.

**Question:** "@here just bumping this — any update?"
Thread replies: any.
→ `status: internal-noise`. `topic: "bump"`. `draft_answer: null`.

**Question:** "When will you support Llama 4?"
Thread replies: `[]`, `has_internal_reply: false`.
KB match: none (roadmap question).
→ `status: no-reply`, `topic: "llama roadmap"`, `draft_answer: null`,
`kb_citation: null`, `confidence: null`, `flags: ["kb_miss"]`.

**Question:** "Why does my export fail with `BQ is not supported` on SA8295?"
Thread replies: `[]`.
KB match: `faq-sa8295-bq-not-supported`
→ `status: no-reply`, `topic: "sa8295 export"`, `draft_answer: "Upgrade to QAIRT 2.45 or later. The 'BQ is not supported' error on SA8295 (v68) was resolved in 2.45; not a model issue, a QAIRT version gap."`,
`kb_citation: "faq-sa8295-bq-not-supported"`, `confidence: "high"`.

**Question:** "How do I derive the 100 Dense INT8 TOPS spec for the IQ-9075 from profiler metrics?"
Thread replies: `[{user: "Czar", is_internal: true, text: "<@Eng> any chance you can help here? <@customer> since this is device-specific, you'll likely have better luck asking in Qualcomm Developers Discord (https://discord.com/invite/qualcommdevelopernetwork)."}]`
→ `status: ack-only` (handoff + redirect, no substantive answer). The
Discord URL is a redirect, not an answer to the TOPS math. `topic: "tops
derivation"`, `draft_answer: null`, `kb_citation: null`.

**Question:** "What's the right workflow for running a VLM on-device via GenieX (QAIRT)? I've tried genie-t2t-run.exe (text-only) and see genie-app-script.txt in the bundle. Is genie-app.exe the intended VLM path? What's the preprocessing pipeline for a custom image (.raw files)?"
Thread replies: `[{user: "Eng", is_internal: true, text: "Now you can run LLM/VLM directly via GenieX (https://github.com/qualcomm/GenieX#quickstart), or try the released app GenieX Chat Windows (https://aihub.qualcomm.com/apps/geniex_chat_windows)."}]`
→ `status: answered`. Bucket #4: fresh URLs, no `@mention` handoff, no
info-gathering, no forum redirect. The one-line reply is
higher-altitude than the multi-part ask — "use GenieX quickstart or
the shipped app" supersedes the sub-questions about which `.exe` and
which preprocessing step. A short URL-directed reply can answer a
long question. `topic: "geniex vlm"`, `draft_answer: null`,
`kb_citation: null`.
