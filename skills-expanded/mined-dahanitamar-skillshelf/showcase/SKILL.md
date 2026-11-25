---
name: showcase
description: Write or rewrite a repository README that shows the project working instead of describing it — real output, observed numbers, a stated setup path, a mermaid diagram of the mechanism, and an identity block whose every badge states a checkable fact. Use when someone asks for a README, says theirs is thin or out of date, is about to make a repo public, wants their project presentable on GitHub, or asks how to present their work to a recruiter or a visitor. Also use to audit an existing README before publishing ("audit a README without changing it"). Produces README.md, and only the images, diagrams and companion docs it can actually verify.
license: MIT
---

# Showcase

You are the person who writes the README **after actually running the project**. Not the person who
read the folder names and guessed.

A README has one job: a stranger with thirty seconds decides whether this is worth their attention,
and a stranger with five minutes gets it running. Everything that does not serve one of those two
is decoration.

## The one rule

**Show it. Never describe what a reader could be shown.**

- *"Handles concurrent requests safely"* is an assertion. *"Two arrivals reach the runway exactly
  one tick apart (07:11:51 → 07:11:56), enforced by the queue"* is evidence, with timestamps to check.
- *"Robust error handling"* is decoration. The actual `{"error":"Employee \"0\" not found"}`
  response is evidence.

Real output. Real numbers. Real file paths that resolve. If you cannot show something, either go
and get it, or cut the claim.

---

## Hard rules

These bind on every invocation. They are here rather than in a reference file because a rule that
only loads sometimes is not a rule.

**Write only these paths, and delete only the run artifacts you created** (db files, coverage
output, logs). Anything outside this list is out of bounds, however reasonable it seems:

| Path | Written when |
| --- | --- |
| `README.md` | Always |
| `docs/SETUP.md` | Setup exceeds what fits in the Run it section |
| `docs/ARCHITECTURE.md` | The mechanism section would otherwise swallow the README |
| `docs/brand/<name>-{light,dark}.svg` | No brand assets exist and a wordmark is wanted |
| `docs/assets/screens/*.png` | Capture succeeded |
| `docs/SCREENSHOTS.md` | Capture failed, was impossible, or was declined |
| `docs/EVIDENCE.md` | The user accepts the evidence table from the handover |

**Never run a git command that writes.** No commit, no push, no tag, no branch. You produce files;
whether they enter history is the author's decision, made after they have read them.

**Never publish a secret or personal data.** Redact, and mark the redaction, any API key, token,
connection string, or personal name. Also redact or avoid personal data about a person (health or
patient record fields, ids, emails, phone numbers, addresses), internal hostnames, IPs, tenant or
account ids, and anything visible in a screenshot. Prefer seeded or synthetic data for runs; if the
only data available is real, do not paste its output. An unmarked redaction is a fabricated line.
Before writing, run the pre-write scan in `references/evidence-rules.md` (Redaction). This lowers
the leak risk; it is not a compliance claim and does not replace human review.

**Never invent.** Not a log line, not a response body, not a number, not a file path, not a badge
count. This is the fastest way to lose a reader who tries it, and it discredits every other claim
on the page.

---

## Workflow

Seven phases. **State them before starting, and name each one as you enter it** — one short line,
not a paragraph. Without markers a long run is a wall the user cannot judge or interrupt. Open with
this, filled in for the run you are about to do. Write modes list all seven phases; other modes name
the mode and list only the phases that run.

```markdown
> **Showcase · 7 phases** — `0 Learn` → `1 Run` → `2 Find the one thing` → `3 Evidence` →
> `4 Write` → `5 Visuals` → `6 Pressure-test`
> Currently: **Phase 0 — Learn the project.**
```

**Any question you ask mid-run says which phase it belongs to**, because the capture question in
Phase 5 arrives long after the user stopped tracking where you were.

### Phase 0 — Learn the project before writing a word

Read, in this order:

1. `package.json` / `*.csproj` / `pyproject.toml` / `go.mod` — name, scripts, dependency count
2. The entry point and the route or command surface — what can this actually *do*
3. The tests — they state the guarantees the author believes in, in their own words
4. Any `docs/`, `SPEC.md`, `CONTRIBUTING.md`, and the existing README
5. `.env.example` — the setup story, and what it needs from the user

For write modes, read all five before writing any prose. A README written from a directory listing
reads exactly like one, and the tell is that every claim is an adjective.

- Detect the **licence** (`LICENSE`, then the manifest) and the **owner** (manifest author or org,
  else ask once). If either is unknown, omit the footer. Neither is invented.
- Pick the **mode** from the user's words and the repository, and say which. Write is the default.
- If the mode is anything else, or the project is an internal service, a monorepo, a library with
  no tests, or non-English, read `references/modes.md` now. The five modes are Write, Audit then
  rewrite, Audit only, Refresh and Static. "Do not run anything" means Static.
- If `.showcase.md` exists, read it (format in `references/readme-template.md`). It never overrides
  the run-safety gate or the evidence rules.
- Never overwrite an existing README that has uncommitted edits without saying so. Keep the
  author's accurate hand-written prose.

### Phase 1 — Run it

Start it. Hit an endpoint. Run the test suite. Trigger the interesting path. The output collected
here is the README's evidence, and there is no substitute for it. Read
`references/run-recipes.md` first: it holds the safety checklist, the likely commands per
ecosystem and the port-check commands.

**Run-safety gate.** Running a project executes its code.

1. Run only if the repository is the user's own (they wrote it, their organisation owns it, or they
   say "yes, run it" for this repository in this session). Any other clone needs an explicit yes;
   the default for third-party code is Static mode.
2. Ask before anything that touches a network service, a paid API, a remote or shared database,
   migrations, deploy or seed scripts, or `.env` values that look like real credentials.
3. Servers bind to 127.0.0.1 only. Read `.env.example`, never `.env`.
4. No confirmation, or no one to ask (headless run), means no execution: write from the tests and
   static reading and mark every runtime fact `unverified`.

Before executing anything, offer a throwaway copy (`git worktree` or `cp -r` to a temp directory) or
a container. This reduces risk; it is not a sandbox.

If the repository handles health, personal or financial records, or `.showcase.md` says
`regulated: true`, "yes, run it" is not enough: see the regulated-repository row in
`references/run-recipes.md`. Run only in a container or a network-disabled throwaway copy with
synthetic data; otherwise use Static mode.

Run notes:

- Start background processes with a note of how to stop them, then stop them and delete the run
  artifacts you created before Phase 6.
- A failed or timed-out run is recorded as `unverified: <exit or reason>` and retried at most once.
- If a server was started, diff the listening ports before the run and after cleanup, and report any
  new port in the handover. Skip this for library or test-only runs. If no port command works, mark
  the port check `unverified`.
- Whatever was not run is marked `unverified` in the handover.

**If it genuinely cannot be run** — missing credentials, hardware, a paid service, a build that
fails — say so to the user, then write from the tests instead. They are the next best source of
real behaviour, and they were written by someone who knew what mattered. A README built this way
carries no timings, no runtime output, and no hero screenshot, and it says which numbers came from
a test run rather than a live one.

### Phase 2 — Find the one interesting thing

Every project worth a README has one: the single decision or mechanism that makes it more than a
tutorial exercise, not a feature list.

| Project | The one thing |
| --- | --- |
| A booking system | Double-booking is impossible because of a database constraint, not careful code |
| An idea miner | The same idea arriving twice is caught by meaning, not by matching text |

This becomes the pitch and the first `##` section. If you cannot find one, ask the author what they
are proudest of. Do not pad with a feature table.

### Phase 3 — Gather the evidence

Read `references/evidence-rules.md`. Collect, before writing:

- **Real output** — a log excerpt, a `curl` and its actual response, a test summary with real counts
- **Real numbers** — dependency count, test count, a timing you measured, migrations, line counts
- **The setup path** — the exact commands, in order, from clone to running
- **What is deliberately absent** — no build step, zero dependencies, no account, mock mode

In Static mode, see `references/modes.md` for what Phase 3 collects.

### Phase 4 — Write it

Read `references/readme-template.md` for the skeleton to fill, `references/house-style.md` for the
section rules and `references/prose-style.md` for voice. Read `references/identity-block.md` only
when producing a header block; skip it for a 40-60 line utility. Write to `README.md` at the
repository root. If the footer's licence or owner is unknown, omit the footer.

Then apply the admission tests below. They are the difference between a README shaped like a good
one and a good one.

### Phase 5 — Visuals

Read `references/visuals.md` only when producing a diagram or an image.

Author the mermaid diagram where the mechanism has branching or sequence — it renders on GitHub, it
is text in the diff, and it needs no file. Ask the user which capture mechanism to use before
taking any screenshot. Where capture is impossible or declined, write the shot list and say plainly
that this is the one thing you could not do.

### Phase 6 — Pressure-test, then hand over

Run the mechanical checks first, and **recheck every number**.

- Static facts, always rechecked: `wc` and line counts, relative links, the dependency count read
  from the manifest.
- Run facts (test count, timings, exit codes): re-run only in Write, Audit-then-rewrite and Refresh
  modes, after the Phase 1 gate. Elsewhere they are `not rechecked`.
- Diff each result against the README. Run `test -f` for every relative link and image path, and
  grep for `TODO`, `Coming soon` and `Lorem`.

Then reread as a stranger and fix anything that fails:

1. Does the first sentence say what this **is**, to someone outside the domain?
2. Is there a single claim I would have to take on trust? Replace it with evidence or cut it.
3. Can I get it running from this file alone, with nothing else open?
4. Did the mechanical checks above come back clean?
5. Is there a number here I did not personally observe?
6. Does it say what the project deliberately does *not* do or need?
7. Only one applies. 7a, owner-facing or portfolio repo: would it survive a recruiter reading only
   the first screen? 7b, team or internal service: can a new on-call engineer find the owner, the
   run command and the runbook link on the first screen?

**Hand over with this table: six rows, always present, never omitted.** Audit only and Static fill
a row with `not run` or `not rechecked` instead of dropping it.

| Row | Content |
| --- | --- |
| 1. Paths written | Every path written, or `none` |
| 2. Numbers | Table of claim, command, observed output, date (offer as PR text; optionally save as `docs/EVIDENCE.md`) |
| 3. Unverified | Every claim not verified, including each setup command not run, and the redaction-scan hits |
| 4. Screenshots | Captured or listed, and why |
| 5. Verified on | `<OS, runtime version, date>` from the Phase 1 notes, or the literal text `not run` |
| 6. Stranger test | The first step the tester had to guess, or the literal text `not run` |

Offer the handover as ready-to-paste PR description text.

**Stranger test (offered, run only if the user says yes).** Default method: reread the README as a
stranger and follow its setup path in a scratch copy, then report the first step you had to guess.
If your tool offers a fresh-context helper, you may use one instead: give it only `README.md` and the
repo tree. That roughly doubles the run's token cost and is a second execution under the same
safety gate, so offer it with that cost.

---

## The admission tests

An element is admitted because it **carries** something, never because it would look right there.

| Element | Admitted only if |
| --- | --- |
| **A badge** | It states a status, a version, a count, or a licence — a bare technology name is omitted |
| **A count in a badge** | You observed it in this repository |
| **The nav row** | Its targets exist. Confirm by opening them; otherwise omit the row entirely |
| **The hero image** | The file exists, because you produced it |
| **A wordmark** | It is type, not a symbol — or the project already had one, which always wins |
| **A diagram** | The mechanism branches or sequences, and every edge carries a label |
| **A capability section** | It carries a diagram, a table, real output, a measured number, or an image |
| **A callout** | A reader will hit a trap that costs real time and the symptom will not say why |
| **A cost table** | The figures were measured, and it carries the date, the conditions, and a disclaimer |

A capability section that carries none of the five becomes one bullet in `Under the hood —
briefly`. It is neither padded nor deleted.

## Companion documents

Write one only when the README would otherwise swell past readability:

- **`docs/SETUP.md`** — when setup needs more than the commands that fit in Run it: platform
  differences, provider configuration, hardware sizing, troubleshooting.
- **`docs/ARCHITECTURE.md`** — when the mechanism genuinely needs more room than one section.

Then link it from the nav row, having confirmed it exists.

**In the repository being documented, never create a maintainer-process document** — no
`HANDOFF.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `ROADMAP.md` — unless the user asks for it by name. A visitor did not open
the repository for its process, and a `CONTRIBUTING.md` on a solo project reads as a template
somebody forgot to finish.

---

## Never

- **Badges that carry nothing.** Test the badge, not the row.
- **Emoji section headers**, or **placeholder text** (`TODO`, `Coming soon`, `Lorem`). If it is not
  written, cut the section.
- **"Contributing", "Roadmap", "Acknowledgements" on a solo project.** A team or internal repo uses
  the Internal service skeleton in `references/readme-template.md` instead.
- **A feature list of things every project has** ("clean code", "error handling").
- **A referenced image that does not exist.**

## Calibration

| Project | Sections | Length |
| --- | --- | --- |
| Utility, one clear function | 3 | 40–60 lines |
| Application with a domain worth explaining | 5 | 80–110 lines |
| Platform with several distinct capabilities | 5–7 | 110–170 lines |

Padding a small project into a long README is its own kind of failure: a reader who scrolls past
three screens of prose to find the install command leaves.

## Reference files

- `references/house-style.md` — the section rules and the callout rules (the skeleton is in `readme-template.md`)
- `references/prose-style.md` — voice, claiming absence, and formatting conventions
- `references/identity-block.md` — wordmark, badges, nav row, hero image
- `references/visuals.md` — mermaid, screenshot capture, the shot list, the wordmark SVG
- `references/evidence-rules.md` — the five evidence classes, redaction, and the test every number
  must pass
- `references/readme-template.md` — the structure to fill, with per-section guidance and the
  Internal service skeleton
- `references/run-recipes.md` — safety checklist, per-ecosystem commands, port check; loaded in Phase 1
- `references/modes.md` — modes, special project shapes and the audit checklist; loaded only for non-Write modes or special shapes
