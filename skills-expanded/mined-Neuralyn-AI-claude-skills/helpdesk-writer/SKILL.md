---
name: helpdesk-writer
description: Use when the user asks to write, update, or draft a helpdesk article, tutorial, how-to, step-by-step guide, or documentation for a product feature, error message, format, limit, or workflow. Guides the full lifecycle: briefing → project selection → code recon → article writing → human approval → publication.
---

# Helpdesk Writer

Produces helpdesk articles backed by technically verified information: it
cross-checks the product's source code, the live UI in a sandbox account, and
a voice guide before writing a single line. Publishes only after explicit human
approval and only to a transport the user designates at that moment.

## When to activate

Requests to write, update, or draft:

- Tutorial / step-by-step / how-to
- Explanation of a product feature, flow, or concept
- Troubleshooting article / error message explainer
- Reference for a data format, limit, or requirement
- FAQ or conceptual article

## Expected environment prerequisites

- **Playwright MCP** installed: `claude mcp add playwright npx @playwright/mcp@latest`
- Product repositories cloned locally (backend, frontend, any other relevant repos).
- Python 3 with Pillow: `pip install Pillow`

The skill ships **no product-specific configuration**. Repo paths, sandbox
credentials, the chosen helpdesk transport, and the helpdesk portal structure
all come from the operator — either persisted in a project config file or
provided at runtime.

## Master workflow

Execute these steps in order. **Do not skip steps.**
Hard rule: **no technical claim enters the article without traceable evidence — from the code or from the UI.**
Hard rule: **never read, search, or use any file on the user's system that is outside the repositories declared in the project config.** This applies to every step of the workflow, without exception.

---

### Step 1 — Topic and language

Use `AskUserQuestion` (dialog) to collect:

- **What the article is about** — free text (e.g. "How to register products").
- **Article language** — offer choices based on any language already configured
  in the active project. If no project languages are configured yet, offer at
  least English and "Other" (the `AskUserQuestion` tool requires a minimum of
  2 options; never pass a single-item list).

Do not ask anything else in this round. Steps 2–3 decide the rest.

---

### Step 2 — Project selection or setup

Look for a project config file at `~/.helpdesk-writer/projects.json`. Each entry holds:

```json
{
  "name": "Project name",
  "dir": "~/.helpdesk-writer/projects/<slug>/",
  "repos": ["~/code/backend", "~/code/frontend"],
  "sandbox": { "url": "https://sandbox.example.com", "credentials_ref": "env:SANDBOX_CREDS" },
  "languages": ["pt-BR"],
  "last_used": "2026-05-10"
}
```

**If one or more projects exist** — ALWAYS use `AskUserQuestion` to display
them as options plus "Create new project". Never auto-select a project, even
if only one exists or one was used most recently.

**If no projects exist, or the user chooses "Create new project"** — run a
short setup dialog (one `AskUserQuestion` call per question where options help;
free-text otherwise):

A. Project name (free text).
B. Git repository paths — one or more local paths, comma-separated.
C. Sandbox URL + credentials. Before asking, explain: the sandbox is the
   live website or app we will navigate to capture screenshots and verify
   each step of the tutorial. Ask for the URL, login, and password. Always
   save all of these — including the password — directly to the project
   config on disk. Sandbox credentials are not production secrets; there is
   no need to redirect to env variables or warn about storage.

Save the new project to `~/.helpdesk-writer/projects.json` and create its
working directory at `~/.helpdesk-writer/projects/<slug>/`.

All draft output, screenshots, and cached recon for this project live inside
that directory. Cross-session Playwright storage state lives at
`~/.helpdesk-writer/projects/<slug>/state/<sandbox>.json`.

---

### Step 3 — Code recon  (read `references/code-recon.md`)

Now that we know the topic, scan only the relevant parts of the repositories.

- **Only read files inside the repositories the user declared in the project
  config.** Never read files outside those paths, regardless of what imports,
  paths, or symlinks are encountered.
- Use the topic from step 1 as a search scope: grep for relevant identifiers,
  routes, schemas, validators, and constants.
- For each target repo, read its `CLAUDE.md` / `AGENTS.md` if present — these
  often describe the module layout and pinpoint the feature's location.
- Extract: accepted formats, numeric limits, exhaustive error list, defaults,
  conditional flows.
- Summarise findings in `~/.helpdesk-writer/projects/<slug>/drafts/<article-slug>/recon.md`
  with `path:line` for every piece of evidence.

If the feature has no corresponding code, **warn the user and do not invent**.

Do not re-read the whole repository in later steps — the recon summary is the
single source of truth for subsequent steps. If a question arises, go back to
the summary first; only re-query the repo if the summary is insufficient.

---

### Step 4 — UI walkthrough  (read `references/ui-walkthrough.md`, `references/runtime-state.md`, `references/screenshot-conventions.md`)

Load cached Playwright storage state if it exists. Navigate to the sandbox and
check the URL: if it matches the login pattern, replay the login flow and save
the refreshed state.

**The full walkthrough is mandatory.** Even when code recon already provides
enough information to write the article, every step of the flow must be
executed in Playwright from start to finish — no skipping. If any step cannot
be completed, stop immediately and inform the user before proceeding.

For each step of the article outline:

- Navigate to the screen.
- Capture raw screenshot; save to `drafts/<article-slug>/raw/step-NN-<short>.png`.
- Generate a thumb for analysis:
  `python scripts/annotate.py thumbnail --in raw/step-NN-<short>.png --out thumbs/step-NN-<short>.webp`
  Read the thumb, not the raw — ~10× cheaper in tokens.
- Append the step to `drafts/<article-slug>/trace.json` (schema in `references/runtime-state.md`).

If the UI contradicts the code (e.g. code allows 100 items but UI shows "max 50"),
**stop and report**. Do not silently pick a side.

---

### Step 5 — Output format

Use `AskUserQuestion` (dialog) to ask what format the article should be saved / published in:

- Markdown (`.md`)
- HTML
- Plain text (`.txt`)
- Word (`.docx`)
- PDF

This determines how the final file is written in step 6.

---

### Step 6 — Image post-processing  (read `references/screenshot-conventions.md`)

Run `scripts/annotate.py` over raw captures:

- Red outline: screen overview with highlighted element.
- Numbered markers + arrows: multiple sub-elements in sequence.
- Cropped zoom-in: small details (toggles, icons, badges).
- Blur: any time test data looks real (email, tax ID, name).

Save processed images as WebP to `drafts/<article-slug>/assets/step-NN-<short>.webp`.

---

### Step 6b — Screenshots decision

Before writing, use `AskUserQuestion` to ask whether the user wants screenshots
included in the article. Options: "Yes — capture and annotate screenshots" /
"No — text only".

If yes, proceed with steps 4 and 6 (UI walkthrough + image post-processing).
If no, skip steps 4 and 6 entirely and go straight to article writing.

---

### Step 7 — Article writing  (read `references/style-guide.md`)

Compose the article in the format selected in step 5, following the standard
structure for the article type.

Non-negotiable rules:

- Write in the language selected in step 1, addressing the reader as "you".
- Every technical claim carries an HTML comment with its source:
  `<!-- src: backend/api/products.ts:42 — limit 100 -->`.
- Every screenshot has text before (introduces what the reader will see) and
  text after (what to do next).
- Errors are explained as **what happened → why it happened → what to do**.

---

### Step 8 — Human review

Save the article to `drafts/<article-slug>/article.<ext>` (extension matches
the format chosen in step 5). Then tell the user where the file is — show only
the file path, nothing else. **Do not render or print the article content in
chat.**

Example message:

> Draft saved: `~/.helpdesk-writer/projects/<slug>/drafts/<article-slug>/article.md`

**Never publish.** Wait for explicit approval.

If the user requests changes, redo the relevant steps and show again.

---

### Step 9 — Publication target  (read `references/publishing-rules.md`, `references/helpdesk-platforms.md`)

Only after the user approves the draft, ask where to publish.

Use `AskUserQuestion` to ask how to publish:

- **MCP server** already configured in Claude Code (user provides the server name).
- **HTTP API** (user provides base URL + auth token — store credential ref, not the value).
- **Save to file only** (no publishing; article is saved locally in the chosen format).

**Do not pre-fill Chatwoot or any specific platform.** The user designates the
transport at this point.

---

### Step 10 — Platform capability discovery

Once the transport is available, probe it for publishing-related capabilities:

- List available categories, folders, sections, or collections.
- List available tags or labels.
- Check for multi-locale / multi-language support.

Summarise what you found. Do not ask the user to fill in a YAML schema — ask
only about what the platform actually exposes and what the article needs.

---

### Step 11 — Metadata and placement

Use `AskUserQuestion` dialogs (one question at a time, offering discovered
options as choices) to collect:

- Target category / section / folder — offer the list discovered in step 10.
- Tags / labels — offer suggestions derived from the article topic + discovered taxonomy.
- Publication status: draft or live.
- Any other fields the platform requires (cover image, description, slug).

---

### Step 12 — Multi-language (optional)

If the platform supports multiple locales, ask:

> "Would you like to publish translations of this article?"

If yes, use `AskUserQuestion` to let the user pick target languages (offer the
locales the platform supports). Generate each translation (re-use the same
recon and screenshots; rewrite the prose) and publish each locale.

---

### Step 13 — Publish

Strip all evidence HTML comments from the final content. Upload via the
configured transport using the canonical payload defined in
`references/helpdesk-platforms.md`.

---

### Step 14 — Save preferences

After a successful publication, offer to save:

- The transport choice (MCP server name or HTTP API base URL) as the default
  for this project.
- The target category / section.
- The publication language(s).

Saved preferences are shown as pre-selected options the next time the user
runs the skill for the same project.

---

## Reference files

| File | When to read |
|---|---|
| `references/code-recon.md` | Before step 3 |
| `references/ui-walkthrough.md` | Before step 4 |
| `references/runtime-state.md` | Before step 4 — storage state, reusable flows, per-article trace |
| `references/screenshot-conventions.md` | Steps 4 and 6 |
| `references/style-guide.md` | Step 7 |
| `references/helpdesk-platforms.md` | Steps 9 and 13 — platform adapters + publishing conventions |
| `references/publishing-rules.md` | Steps 9 and 13 |
| `playbooks/*.md` | When the user's topic matches an existing playbook |
| `examples/*.md` | For reference of the final article format |

## Scripts

- `scripts/annotate.py` — image annotations (number, arrow, box, crop, blur,
  composite) and `thumbnail` (downscale + WebP for cheap agent reads). Run
  `python scripts/annotate.py --help`.

## Draft structure

```
~/.helpdesk-writer/projects/<project-slug>/
├── drafts/<article-slug>/
│   ├── recon.md              # code evidence (step 3)
│   ├── outline.md            # article outline
│   ├── trace.json            # replayable Playwright record (step 4)
│   ├── raw/                  # raw screenshots (PNG)
│   ├── thumbs/               # downscaled WebP — what the agent reads
│   ├── assets/               # annotated screenshots for article (WebP q90)
│   └── article.<ext>         # final article in the chosen format
└── state/<sandbox>.json      # shared Playwright storage state
```

Keep `drafts/<article-slug>/` even after publishing — it serves as history and
as the source for future updates or translations.

## Principles

1. **Code truth > UI truth > impression.** In that order.
2. **Every technical claim has a trace** (`path:line`) in the draft.
3. **Never publish without human review.** Prior approval does not carry over
   to a new article.
4. **If code and UI disagree, stop and report.** Do not pick a side.
5. **Never invent.** If a feature has no corresponding code, warn the user
   instead of speculating.
6. **Speak the user's language, not the developer's.** The final article
   must not read like a GitHub issue.
7. **Ask only what is needed, only when it is needed.** Collect topic and
   language first; platform details only after approval.
