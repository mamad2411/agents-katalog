---
name: radar
license: MIT
description: Track competitors, upstream tools and key dependencies of this repo — check versions, read changelogs, and produce recommendations grounded in THIS project's roadmap and code. Use for "/radar", "what's new in the ecosystem", "check competitors", or "did X release something".
---

# radar

Ecosystem tracking for the current repo. Deterministic work (version checks,
changelog fetching, state) is done by the bundled CLI; your job is the
**analysis layer**: read what changed, compare it against THIS project, and
say what matters.

All data lives in the consuming repo under `.radar/` (git-tracked JSON).
Run every command from the repo root.

```bash
node <skill-dir>/scripts/radar.js <command>  # or `bun` — needed if node is older than 22.18
```

## First use in a repo: `/radar init`

1. Run `radar.js init`.
2. Read the project's context (README, CLAUDE.md/AGENTS.md, package
   manifest, roadmap docs) and **propose seed entries** per category:
   - `official` — tools the project builds on (for an agent-adjacent
     project, `anthropics/claude-code` is almost always first)
   - `competitors` — same-space products
   - `deps` — libraries whose breaking changes hurt
   - `inspiration` — idea sources

   In the same turn, offer the weekly automatic check — say what they'd
   get, not the flag: a GitHub Actions workflow that runs the check every
   week, keeps a rolling "Radar digest" issue up to date, and comments on
   it when new updates land. The user won't know this exists unless you
   offer it.

   Also ask where findings should land later. 🔥/💡 is
   shorthand for you, not vocabulary for the user — they have not seen it
   defined. Ask with the meaning instead: changes that affect this repo,
   ideas worth adopting. Keep the plumbing invisible too: the user never
   hears "taskSink", "config" or "init". Look around FIRST (a task-board MCP tool, an issue tracker,
   a docs/specs dir, a TODO.md) and offer what you actually found as
   concrete choices in the user's own terms — "open tasks on your rigo
   board", "write a spec under docs/specs/" — plus the two always-valid
   defaults: "append to a markdown file in the repo" and "just report,
   file nothing". Never ask cold with abstract vocabulary.

   Then **stop and end your turn with that proposal.** Init is a two-turn
   flow: propose, wait, write. Ask everything you need in the first turn,
   so the user answers once. A tool the user has not named does not enter
   the registry — not via `radar.js add`, not via a hand-edit, not via a
   script. Listing what you already added is not proposing.
3. Once the user answers, add the approved entries via
   `radar.js add <type> <source> --category X` (types: github, npm, pypi,
   nuget, web). Use `web <url>` for anything with no repo and no package —
   a closed-source product that only publishes a release notes page. It
   tracks the first version-shaped string in that page's text; when that
   is the wrong number (a "2026" heading, a plan price) or the page's
   versions live only in markup, open `.radar/registry.json` and give the
   entry a pattern instead:
   `"source": { "url": "…", "pattern": "Conductor (\\d+\\.\\d+\\.\\d+)" }`.
   The pattern must sit **inside** `source`. Beside it nothing reads it,
   and radar refuses to check that tool rather than quietly falling back.
   A pattern is tried against the rendered text first and then against the
   page source, so it can also anchor on markup — a Mintlify changelog
   publishes versions only as `<Update label="v0.22.0">`, matched with
   `"pattern": "<Update label=\"v(\\d+\\.\\d+\\.\\d+)\""`.
   Verify against the live page before moving on — a wrong pattern reports
   phantom updates every week.
   If they said yes to the weekly check, run
   `radar.js init --workflow` — idempotent: existing `.radar/` data is
   untouched, it only installs the workflow. Then enrich each entry's `features` and `notes` fields in
   `.radar/registry.json` — these drive analysis quality. Close by
   relaying that knowledge, not just a version table: one or two lines
   per tool — what it is and what to watch for — so the user doesn't
   need a `deep` per tool just to know what they're now tracking.
4. Write `.radar/config.json`: `taskSink` = free text naming the sink the
   user picked (`"rigo board"`, `"GitHub issues"`, `"a spec file under
   docs/specs/"`). If they want findings reported and nothing more, write
   `null` — that is an answer, and recording it stops the main flow from
   asking again.

## Main flow: `/radar` (no args)

1. `radar.js check` — fetches latest versions, diffs against known state.
   No `.radar/` yet? The CLI says so and exits — don't improvise: run the
   `/radar init` flow above (propose, wait, write), then resume here.
   A tool's FIRST check records a baseline (`NEW — tracking from X`):
   tracking starts at the version first seen, past releases are not
   analyzed. Updates fire from the next release onward.
   `check` may end with a notice that the weekly workflow pins an older
   radar release. Relay it and offer `init --workflow --force` — but the
   old pin keeps working, so never run it unasked, and drop the subject
   if the user passes.
2. For each tool WITH an update: `radar.js changelog <id>`. For `web`
   tools it hands back the page URL and the range instead of the notes —
   radar machine-checks only the version string there. WebFetch the page
   yourself and analyze that range; if the page shows nothing about those
   versions, say so rather than reporting on whatever it does show.
3. Analyze. For every meaningful change, ground it in this project:
   - Read the relevant part of THIS repo (roadmap, the subsystem the
     change touches) before claiming impact.
   - Classify: 🔥 affects us directly / 💡 feature worth adopting /
     ✅ irrelevant (say so in one line, don't pad).
   - For 💡 items: state what the competitor did, how it maps to this
     project's architecture, and a concrete next step. Exploring to get
     there is fine — download a package to read its source, prototype to
     verify a claim — but do it in a temp dir OUTSIDE the repo, never in
     the working tree. Needs this repo's own code? Use a temp git
     worktree (`git worktree add /tmp/radar-exp && …` , remove after) —
     full repo, zero footprint in the user's checkout. Cleanup-later on
     the working tree is not a plan (interrupted turns leave junk, and
     undo can eat the user's uncommitted changes); the repo only ever
     receives the report, and implementation starts when the user asks.
4. Read `taskSink` from `.radar/config.json` and offer to file the 🔥/💡
   items there — it names the sink in the user's own words, so honor it
   (`"rigo board"` → the board's MCP tools, `"GitHub issues"` → `gh`).
   `null` means the user already said report-only: skip this step. Field
   absent means the question was never answered (an init that didn't
   finish, or a config from before `taskSink`) — don't guess a sink, and
   don't surface the plumbing: no "taskSink", no config paths, no "init
   didn't finish", and no 🔥/💡 in the question itself — say what they
   mean. Do what init does: look around the repo, then ask in
   plain words with the concrete options you found ("open tasks on your
   board", "append to a markdown file", "just report — I won't ask
   again"). Record the answer silently so this is the last time.

   Offer, never act: no task, issue or file gets created until the user
   says yes. A `taskSink` records WHERE findings go if the user wants
   them filed, not standing permission to file them.
5. `radar.js mark-analyzed <id>` for each tool you covered, so the next
   run only surfaces new material.

Report format: lead with the one-line verdict per tool, details after.
No boilerplate — a tool with nothing relevant gets one ✅ line.

## Other commands

| Ask | Do |
|-----|----|
| `/radar help` | Explain how radar works in your own words: the init → check (NEW baseline) → changelog → analyze → mark-analyzed cycle, the optional weekly CI issue flow, and what `.radar/` holds. Use examples from THIS repo's registry. `radar.js help` prints the CLI reference |
| `/radar add <url or name>` | Infer type/source, `radar.js add`, then fetch the README and fill `features`/`notes` in the registry. No repo and no package — a product site — is the `web` type: find its changelog/release notes page (not the marketing page) and add that URL |
| `/radar discover` | Web-search for new tools in the registry's categories; propose candidates with stars + one-liner; add only what the user approves. `discover` scans a category broadly; `deep` drills into one named tool |
| `/radar deep <id or name/url>` | Read the tool's README, docs, recent releases, and its most-reacted open issues (top pain points and requested features — not the full list); report how it compares to this project. **Tracked** (id matches the registry): also update its `features`/`notes` and refresh `stars` (they're recorded at add time and go stale otherwise). **Untracked** (a name or URL): the research is identical — it runs off the web, not the registry — so do it anyway, then close with a reasoned add/skip recommendation and a category. Add only via `radar.js add`, only if the user says yes |
| `/radar list` / `show <id>` / `history <id>` | Run the CLI command, relay output |

## Notes

- `.github/workflows/radar.yml` exists only because `init --workflow` was
  run — it belongs to the optional weekly CI check, not to the skill
  install channel; deleting it removes the check cleanly, local `/radar`
  use is unaffected. It runs the `mralabs/radar` composite action pinned
  to a commit SHA. A `.github/radar/` dir is the pre-0.5 vendored CLI —
  but check radar.yml first: the pre-0.5 workflow RUNS that dir. If
  radar.yml references `.github/radar/`, delete both together and re-run
  `init --workflow`; only then is the dir safe to remove.
- GitHub API is rate-limited (60/h anonymous). Radar authenticates from
  `GITHUB_TOKEN`/`GH_TOKEN`, or falls back to `gh auth token` when neither
  is set. If checks error, run `radar.js rate-limit` — it shows the current
  quota and whether the run is authenticated at all.
- Registry `notes`/`features` are curated knowledge, not cache — improve
  them whenever a deep-dive teaches you something.
- Never auto-add tools or auto-create tasks; the registry stays curated
  by the user.
