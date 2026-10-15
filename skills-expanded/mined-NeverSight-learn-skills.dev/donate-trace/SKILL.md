---
name: donate-trace
description: Donate a single coding-agent session to Trace Commons, an open public dataset of agent traces. Use this skill whenever the user wants to donate, contribute, share, or publish an agent session, trace, or conversation history to Trace Commons or an open dataset, or says things like "/donate-trace", "donate this session", "contribute my trace", "share this to the commons", or "publish my agent history". The skill locates the current session from the agent's own logs, strips paths, identity, secrets and PII locally, shows the user exactly what was removed, confirms the project is open-source, and opens a pull request to the dataset. Only ever donates from public, open-source repositories — never private or proprietary code.
---

# Donate a trace to Trace Commons

Trace Commons is one open, public dataset of coding-agent sessions that anyone can train on or study. This skill takes a single session from the current agent, removes anything sensitive on the user's own machine, and submits the cleaned result as a pull request to the dataset.

The whole point is that contributing is safe and the user stays in control: nothing leaves the machine until the user has seen what will be sent and confirmed it. Treat that promise as the core of the job.

## Hard rules (read first)

These are not negotiable. The dataset is public and permanent, so a mistake here is published immediately.

1. **The contributor certifies it's theirs to publish — you inform, they decide.** By choosing to donate, the contributor certifies that this session is not private or confidential and that they have the right to publish it publicly under CC-BY-4.0. Your job is to make that an *informed* certification, not to gatekeep: surface what you can actually see — a private-looking git remote, missing license, client/employer-looking code — so they decide with eyes open. Don't silently upload something that looks private; name what you see and let the contributor make the call. The responsibility for publishability and licensing rests with the contributor, not with you or the dataset. (Secret/PII scrubbing in the next steps is separate and still mandatory — see rule 2.)
2. **Local cleaning before upload.** All anonymization happens on this machine, before anything is sent. Never upload a raw session.
3. **User reviews before send.** Always show the user a summary of what was removed and ask for explicit confirmation. No silent uploads.
4. **One session only.** Donate the single session the user chose, not their whole history.
5. **When unsure about secrets, redact; when unsure about publishability, ask the contributor.** If you're unsure whether a field is a secret or personal data, redact it — dropping signal is acceptable, leaking is not. If you're unsure whether the project is public or theirs to share, surface it and let the contributor certify; that call is theirs, not yours.

## The flow

Follow these steps in order.

### Step 1 — Surface the source, let the contributor certify

Before touching any logs, look at where the session came from and surface anything that bears on whether it's the contributor's to publish — so their consent later is *informed*. You are not the gatekeeper; the contributor certifies. You just make sure they're not certifying blind.

- If you can see the working directory, check the remote and license: `git -C <dir> remote get-url origin` (and `git -C <dir> config --get remote.origin.url`), and look for a `LICENSE`/`LICENCE`/`COPYING` file or an SPDX/`license` field in the manifest.
- **Tell the contributor what you found, plainly**, e.g.: "This is a public repo licensed MIT" / "This repo is public but has no license (all-rights-reserved by default)" / "I can't find a public remote — this looks like a local or private project." Don't refuse on your own; surface it.
- **The one thing you don't do is silently upload something that looks private or like employer/client code.** Name it and let them decide. If they confirm it's theirs to publish, that's their certified call.
- Then move to cleaning. The explicit publishability certification happens at the confirmation step (Step 5).

### Step 2 — Find the session

Identify which agent (harness) this is and locate the session file. Each agent stores sessions differently. Read the matching reference file for exact paths and formats:

- **Claude Code** → `references/claude-code.md`
- **Codex** → `references/codex.md`
- **pi** → `references/pi.md`
- **opencode** → `references/opencode.md`
- **Cursor** → `references/cursor.md`

If you're not sure which agent you're running in, ask the user, or infer it from which session directory exists on disk. Default to the most recently modified session unless the user names a specific one.

Copy the session to a working location (e.g. `/tmp/donate-trace/`) so you never modify the user's real logs.

### Step 3 — Clean it (deterministic pass first)

Run the bundled scrubber on the copied file. It removes the highest-confidence leaks deterministically — home-directory paths and usernames, common secret formats (API keys, tokens, PEM blocks, JWTs, `KEY=value` env assignments in shell commands), and emails. Doing these in code rather than by eye is deliberate: these patterns have crisp signatures and a missed credential is the worst outcome.

```bash
python scripts/scrub.py --in /tmp/donate-trace/<session-file> --harness <harness> --out /tmp/donate-trace/cleaned.jsonl --report /tmp/donate-trace/report.json
```

The scrubber writes the cleaned session and a JSON report listing every redaction it made.

### Step 3.5 — Deep secret scan (if available)

Run the optional deep scan over the cleaned file:

```bash
python scripts/scan.py --in /tmp/donate-trace/cleaned.jsonl --report /tmp/donate-trace/scan.json
```

This wraps TruffleHog (hundreds of maintained detectors) for breadth beyond the scrubber's pattern list. Read the `STATUS:` line:

- **`trufflehog_not_installed`** — don't block and don't auto-install. Note it for the Step 5 summary so the user knows the deep scan didn't run locally. (The anonymous donation path runs it server-side; the attributed path does **not**, so for attributed donations either suggest installing TruffleHog with the one-liner the script prints, or proceed knowing only the pattern pass ran.)
- **`findings`** — treat each as a **must-confirm item** in the review pass below: it may be a real secret the scrubber missed, or a false positive on a high-entropy string (hash, ID, base64). Resolve each with the user before uploading. These do not auto-block — TruffleHog runs without verification, so judgment is required.
- **`clean`** / **`scan_error`** — proceed; mention a scan error in the summary if it occurred.

### Step 4 — Review pass (your judgment)

The scrubber catches patterns; you catch meaning. Read the cleaned session and look for things a regex can't recognize:

- Personal names, company names, or client names in prose (prompts, commit messages, comments).
- Internal hostnames, project codenames, ticket IDs, or URLs that identify a person or org.
- Anything in free text that a stranger could use to identify who wrote this or where they work.

Redact anything you find by replacing it with a neutral placeholder (e.g. `[NAME]`, `[COMPANY]`, `[INTERNAL_URL]`). Note what you changed so it can go in the summary. When unsure, redact.

See `references/anonymization.md` for the full field-by-field guide to where sensitive data hides in each harness.

### Step 5 — Show the user, get confirmation

Summarize plainly what will be donated and what was removed. Keep it human:

```
Ready to donate this session to Trace Commons.

Removed:
- 4 home-directory paths (your username)
- 1 API key in a shell command
- 2 email addresses
- 1 company name in a commit message ("Acme")

Deep scan: TruffleHog clean.   (or: "not installed — pattern pass only";
or: "flagged 1 'Box' match, you confirmed it's a hash, not a secret")

The cleaned session has 35 messages and 12 tool calls. Nothing has been
uploaded yet.

By saying yes, you're certifying this session isn't private or confidential
and that you have the right to publish it publicly under CC-BY-4.0. Open the
pull request?
```

Always include the **Deep scan** line so the user knows whether the deep scan
actually ran — never let its absence be silent, especially for attributed
donations, which get no server-side backstop.

The confirmation **is the contributor's certification** that the content is
theirs to publish — make that explicit (as above) and wait for an explicit yes.
The responsibility for publishability rests with them; your job was to make the
decision informed and to scrub secrets/PII, not to withhold the donation. If the user wants to see the full cleaned file, show it. If they want to pull something else out, do it and re-summarize.

### Step 6 — Submit

Only after confirmation. There are two ways to submit, and the skill picks one automatically but lets the user choose.

First, detect whether this machine has a Hugging Face login. The current CLI is
`hf`; older machines have the deprecated `huggingface-cli`. Use whichever exists:

```bash
HF_CLI=$(command -v hf || command -v huggingface-cli)
"$HF_CLI" auth whoami 2>/dev/null || "$HF_CLI" whoami 2>/dev/null
```

(`hf auth whoami` is the current form; the legacy CLI uses `huggingface-cli whoami`.)

- **If it succeeds** (prints a username): default to the **attributed** path. The donation becomes a pull request opened by the user's own account. Tell them: "You're logged in to Hugging Face as `<name>`, so I'll open the pull request under your account. Prefer to donate anonymously instead?"
- **If it fails** (not logged in): default to the **anonymous** path. The donation is sent through the Trace Commons server, which opens the pull request on your behalf under a project account. No Hugging Face account needed. Tell them: "You're not logged in to Hugging Face, so I'll donate anonymously through the Trace Commons server. Prefer to attribute it to your own account? You'd need to run `hf auth login` (or `huggingface-cli login` on older installs) first."

Always state which path you're taking and let the user switch. Some people want attribution; some specifically want anonymity even when logged in. Respect the override.

Then submit via the chosen path. Both paths open a pull request (never a direct push) so a maintainer reviews before anything goes public. See `references/publishing.md` for the exact commands for each path.

Then tell the user where to track it and thank them once, briefly.

## If the user just wants to understand the skill

If they're asking what this does rather than asking to donate right now, explain it plainly and point them at the open-source-only rule. Don't start reading their logs unless they want to donate.
