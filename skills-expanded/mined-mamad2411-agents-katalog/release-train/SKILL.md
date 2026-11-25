---
name: release-train
description: "Drafts the release pull request that ships everything on dev to production — read-only, opens nothing without your say-so."
user_invocable: true
standards:
  input: [REFERENTIAL_INTEGRITY_STANDARD]
  processing: [CRITICAL_THINKING_STANDARD]
  output: [CRITICAL_THINKING_STANDARD]
register:
  founder_mode: default
  technical_mode:
    shape: json_envelope
    triggers: [intent, --raw, /sulis:jargon]
verification_spiral:
  tier: standard
  template_base: STANDARD_TIER_DEFAULT
related_skills:
  - relationship: related_to
    skill: ../change/SKILL.md
    notes: change ship lands work on dev and writes a changeset; this skill batches those changesets into the release PR
  - relationship: optional_input
    skill: ../../references/founder-facing-conventions.md
    notes: Audience=founder-facing; Rules 1-6 apply (echo-before-act, prompt-before-destroy, dual-register)
  - relationship: optional_input
    skill: ../../references/change-primitives.md
    notes: the 22-primitive vocabulary each changeset records; sets the release tier
---

# /sulis:release-train — cut the next release

## Conclusion (lead with the answer)

`/sulis:release-train` drafts the one pull request that ships everything
sitting on `dev` out to production. It reads the release notes each shipped
change left behind, works out the next version number, writes the pull-request
description and a changelog preview, and shows it all to you. By default it
opens **nothing** — it shows you the draft and the exact command, and you
decide.

| You type | What happens |
|---|---|
| `/sulis:release-train` | Shows the full draft — next version, changelog preview, the release pull request it *would* open — and stops. Opens nothing. (This is the default.) |
| `/sulis:release-train --dry-run` | Same as above, said explicitly. A preview, no side effects. |
| `/sulis:release-train --draft` | Opens the release pull request as a GitHub *draft* (not ready-to-merge) so you can keep editing it. |

Without `--dry-run`, once you confirm, it opens the release pull request from
`dev` into `main` and hands you the link. That pull request is the *only* thing
this skill ever creates — it never edits a file, never commits, and never
changes a version number itself. The version bump happens automatically, by the
robot, once you merge the pull request (that is deliberate — there is exactly
one thing in the whole system allowed to change versions, and it is not this
skill).

Founder-mode is the default: plain English, lead with the outcome. Ask for the
raw output any time ("show me the technical version" / `--raw`) and you get the
underlying numbers and commands.

## Resolving the tool path (MUST — first action)

The release-train computation reuses the changeset helper that lives inside the
sulis plugin (`_changeset.py`). When the plugin is installed in a downstream
project it sits under the plugin cache, not at a project-relative path. Resolve
the scripts directory ONCE at the start and capture it as `$SCRIPTS_DIR`:

```bash
# Resolve from the ACTIVE plugin version (its bin/ is on PATH) — avoids the
# lexical-sort cache pick that mis-ranks 0.98.0 above 0.126.0 (#49).
SCRIPTS_DIR=""
_sulis_bin=$(printf '%s\n' "$PATH" | tr ':' '\n' | grep -E 'sulis-ai-agents/sulis/[^/]+/bin$' | head -1)
if [ -n "$_sulis_bin" ] && [ -d "$(dirname "$_sulis_bin")/scripts" ]; then
  SCRIPTS_DIR="$(dirname "$_sulis_bin")/scripts"
fi
# Dev fallback: marketplace repo cwd.
if [ -z "$SCRIPTS_DIR" ] && [ -f "plugins/sulis/scripts/_changeset.py" ]; then
  SCRIPTS_DIR="$(pwd)/plugins/sulis/scripts"
fi
# Last-resort fallback ONLY if PATH anchor + dev both miss: a PORTABLE
# version-aware cache pick (numeric, NOT lexical, NOT `sort -V`).
if [ -z "$SCRIPTS_DIR" ]; then
  SCRIPTS_DIR=$(find ~/.claude/plugins/cache -name _changeset.py -type f -path '*/sulis/*/scripts/*' 2>/dev/null \
    | sed -E 's#(.*/sulis/)([^/]+)(/scripts/.*)#\2 &#' \
    | sort -t. -k1,1n -k2,2n -k3,3n \
    | tail -1 | cut -d' ' -f2- | xargs -I{} dirname {} 2>/dev/null)
fi
if [ -z "$SCRIPTS_DIR" ]; then
  echo "ERROR: cannot find the changeset helper. Run: claude plugin install sulis@sulis-ai-agents" >&2
  exit 1
fi
echo "SCRIPTS_DIR=$SCRIPTS_DIR"
```

Capture the printed `SCRIPTS_DIR` into working memory and substitute the literal
path at every `python3 -c "import sys; sys.path.insert(0, '$SCRIPTS_DIR'); …"`
call below — environment variables do NOT persist between Bash tool invocations
in Claude Code.

**The version math is NOT re-implemented here.** Every tier and version
computation calls the proven functions in `_changeset.py`
(`read_changesets` / `cumulative_tier` / `next_version`). That module is the
single source of truth (it is the same code the release robot's bash mirrors and
the same code its unit tests pin). This skill is a thin, read-only orchestrator
over it — if you ever find yourself writing tier logic or SemVer arithmetic in
this skill, stop: call the helper instead.

---

## The workflow (five steps)

### 1. Pre-flight — is there anything to release, and is it safe?

Run these checks before computing anything. Any one of them can stop the run with
a plain-English explanation. The drift guard runs **first** — if production has
moved ahead of `dev`, nothing else this skill computes is trustworthy.

**a. (retired)** The old "refuse to operate against a stale `dev`" drift gate
(`drift_check.sh` + the GIT-12 back-merge invariant) was removed with the
two-branch model. On the trunk there is one line — `main` — so there is no
`dev`-vs-`main` drift to guard against. A release is a bump + tag on `main`,
computed from the changesets already on `main`.

**b. GitHub access.** Confirm `gh` is authenticated:

```bash
gh auth status
```

If it fails, stop and say so plainly with the fix (Rule 5):

> *"I can't reach GitHub right now — `gh` isn't signed in. Run `gh auth login`,
> then try `/sulis:release-train` again."*

**c. Get the latest.** Make sure the comparison is against the real remote
state:

```bash
git fetch origin --quiet
```

**d. Is there anything ahead of production?** Count what's on `dev` but not yet
on `main`:

```bash
COMMITS_AHEAD=$(git rev-list --count origin/main..origin/dev)
```

If `COMMITS_AHEAD` is `0`, there is **nothing to release** — stop cleanly:

> *"Nothing to release — `dev` is already level with production. Ship some work
> first (`/sulis:change ship …`), then come back."*

**e. Is a release already in flight?** Check for an open `dev → main` pull
request:

```bash
gh pr list --base main --head dev --state open \
  --json number,url,title --jq '.[]'
```

If one is already open, do **not** open a second. Surface it and ask how to
proceed (Rule 5 — explain + the choice):

> *"There's already a release pull request open from `dev` → `main`:
> {title} ({url}). I won't open a duplicate. Want to review and merge that one,
> or close it first and have me draft a fresh one?"*

Wait for the founder's answer; do not auto-decide.

**f. Version-drift guard.** The plugin version and the marketplace's copy of the
sulis version must match *before* a release — a mismatch means a previous
release only half-applied, and bumping on top would compound the error. Read
both and compare:

```bash
PLUGIN_V=$(python3 -c "import json; print(json.load(open('plugins/sulis/.claude-plugin/plugin.json'))['version'])")
ENTRY_V=$(python3 -c "import json; d=json.load(open('.claude-plugin/marketplace.json')); print([p['version'] for p in d['plugins'] if p['name']=='sulis'][0])")
```

If `PLUGIN_V` ≠ `ENTRY_V`, **abort** — this is not something to release over:

> *"I've stopped before drafting anything: the plugin's version
> (`{PLUGIN_V}`) and the marketplace's record of it (`{ENTRY_V}`) don't match.
> That usually means a previous release only half-finished. This needs a look
> before the next release — releasing on top would compound the mismatch.
> Nothing has changed."*

### 2. Discover — read what's accumulated

Read the three inputs the preview is built from. All read-only.

**a. The changesets** — the release notes each shipped change left behind. Read
them through the *same* helper the release robot uses, so the preview can't
diverge from what actually ships:

```bash
python3 -c "
import sys, json; sys.path.insert(0, '$SCRIPTS_DIR')
import _changeset
from pathlib import Path
cs = _changeset.read_changesets(Path('.changesets'))
print(json.dumps(cs, indent=2))
"
```

**b. The merged changes** — the human-readable list of what landed on `dev`
since production, for the pull-request body:

```bash
git log --oneline --no-merges origin/main..origin/dev
```

**c. The current three version values** (ADR-003 — the bump moves all three in
lockstep at one tier):

```bash
PLUGIN_V=$(python3 -c "import json; print(json.load(open('plugins/sulis/.claude-plugin/plugin.json'))['version'])")
ENTRY_V=$(python3 -c "import json; d=json.load(open('.claude-plugin/marketplace.json')); print([p['version'] for p in d['plugins'] if p['name']=='sulis'][0])")
META_V=$(python3 -c "import json; print(json.load(open('.claude-plugin/marketplace.json'))['metadata']['version'])")
```

| # | Value | Where it lives | Series today |
|---|---|---|---|
| 1 | plugin version | `plugins/sulis/.claude-plugin/plugin.json` → `.version` | `0.77.x` |
| 2 | marketplace's sulis entry | `.claude-plugin/marketplace.json` → the sulis plugin's `.version` | `0.77.x` (same as #1) |
| 3 | marketplace umbrella | `.claude-plugin/marketplace.json` → `.metadata.version` | `1.122.x` |

### 3. Compute the manifest — what the release *will* be

Hand the changesets to the helper for the tier, then bump all three values at
that one tier (`next_version` is series-agnostic — it bumps `0.x.y` and `1.x.y`
identically):

```bash
python3 -c "
import sys, json; sys.path.insert(0, '$SCRIPTS_DIR')
import _changeset
from pathlib import Path
cs = _changeset.read_changesets(Path('.changesets'))
tier = _changeset.cumulative_tier(cs)              # 'patch' | 'minor' | 'major' | None
manifest = {
    'changeset_count': len(cs),
    'cumulative_tier': tier,
    'version_bump_will_happen': tier is not None,
    'expected_plugin_version': _changeset.next_version('$PLUGIN_V', tier),
    'expected_entry_version':  _changeset.next_version('$ENTRY_V',  tier),
    'expected_meta_version':   _changeset.next_version('$META_V',   tier),
}
manifest['expected_tag'] = 'v' + manifest['expected_meta_version']
print(json.dumps(manifest, indent=2))
"
```

The three rules to hold to (ADR-003):

- The **expected tag** is `v<expected_meta_version>` — the umbrella version, not
  the plugin version. (Every existing tag is `v1.xxx.0`; there is no `v0.xx.0`
  tag.)
- The **changelog header** uses the **plugin** version: `## v<expected_plugin_version> — <date>`.
- All three values move by the **same** tier.

**No changesets is valid** (`cumulative_tier` is `None`,
`version_bump_will_happen` is `false`). This is an admin-only / docs-only
release — there's nothing for consumers to install differently, but the pull
request still opens. Note it in the draft; do not treat it as an error:

> *"No release notes have accumulated on `dev`, so the version won't change.
> The release pull request still opens to promote what's there; the robot will
> see there's nothing to bump and skip the version change."*

### 4. Draft the pull-request body + changelog preview

Build the draft from the manifest and the changeset summaries. Title by tier:

| Tier | Title |
|---|---|
| `major` | `release: sulis v<expected_plugin_version> (major)` |
| `minor` | `release: sulis v<expected_plugin_version> (minor)` |
| `patch` | `release: sulis v<expected_plugin_version> (patch)` |
| none | `release: sulis (no version change — admin/docs-only)` |

**Body** (plain English; lead with the outcome):

- **What this release does** — one line: the cumulative tier, the version move
  (`0.77.0 → 0.78.0` for plugin + sulis entry; `1.122.0 → 1.123.0` for the
  umbrella), and the expected tag (`v1.123.0`).
- **Changes in this release** — one bullet per changeset, taken from each
  changeset's `summary` (founder-readable). Group the changelog preview under a
  `## v<expected_plugin_version> — <date>` header, mirroring the existing
  `plugins/sulis/CHANGELOG.md` shape (a bolded one-line tier+summary, then the
  detail bullets).
- **What happens on merge** — "When you merge this, the release robot bumps all
  three version values to {expected}, assembles the changelog, deletes the
  consumed changesets, tags `{expected_tag}`, and publishes the GitHub Release."
- **How you'll know it worked** — "the bot's `release: sulis v…` commit lands on
  `main`; `/plugin update` pulls the new version."

**Breaking / major callout (MUST).** If the cumulative tier is `major`, lead the
body with a prominent callout and require an explicit confirmation before
opening anything (even without `--dry-run`):

> *"⚠️ This is a **major** release — it carries a breaking change. Anyone on the
> current version may need to adjust when they update. The changes that make it
> breaking: {list}. Open the release pull request? (yes / no)"*

### 5. Surface + confirm

**`--dry-run` (the default).** Print the full draft — the title, the body, the
changelog preview, the expected three-value bump, and the expected tag — then
show the exact command that *would* open it, and stop. Open **nothing**:

> *"Here's the release I'd cut (preview only — I've opened nothing):*
>
> *Version: {plugin} `0.77.0 → 0.78.0` · umbrella `1.122.0 → 1.123.0` · tag
> `v1.123.0`*
>
> *{changelog preview}*
>
> *To open it for real, run `/sulis:release-train` and confirm — or run this
> yourself:*
> ```
> gh pr create --base main --head dev \
>   --title "release: sulis v0.78.0 (minor)" \
>   --body-file <the drafted body>
> ```
> *"*

**Pin the dev SHA into the pull-request body (do this immediately before
opening).** The release robot needs to know which `dev` commit this release was
cut against, so that after the merge it can tell a clean release (advance `dev`
to match production) from a raced one (open a catch-up pull request instead). It
reads that commit from a single machine-readable line at the bottom of the
pull-request body. Capture `dev`'s current commit and append it to the body file
that's about to be opened — append-only, always last, so it's the line the robot
reads (ADR-005):

```bash
DEV_SHA=$(git rev-parse origin/dev)
printf '\n\n<!-- dev-sha-at-open: %s -->\n' "$DEV_SHA" >> /tmp/release-train-body-<timestamp>.md
```

`git rev-parse origin/dev` returns a 40-character commit hash; the line written
is exactly `<!-- dev-sha-at-open: <hash> -->`, an HTML comment that stays
invisible in the GitHub pull-request view but is recovered verbatim by the
robot. Use `origin/dev` (not `HEAD` — after any release-prep step `HEAD` may not
be on `dev`); the earlier drift check (Step 1a) already ran `git fetch origin`,
so `origin/dev` is current. Capture it here, in the same breath as opening the
pull request — not earlier — so the pinned commit is the one true at open time
even if the founder spent a while reviewing the preview (ADR-005). Writing the
pin *before* `gh pr create` means the pull request is never visible without it,
so the robot can never see a release pull request that's missing its pin.

**Without `--dry-run` (open it).** After the founder confirms (and after the
mandatory major-callout confirmation if it's a major release), open the pull
request and hand back the link:

```bash
gh pr create --base main --head dev \
  --title "release: sulis v<expected_plugin_version> (<tier>)" \
  --body-file /tmp/release-train-body-<timestamp>.md \
  $DRAFT_FLAG
```

`$DRAFT_FLAG` is `--draft` when `--draft` was passed, empty otherwise. Capture
the URL from stdout and report:

> *"Opened the release pull request: {url}. Review it, then merge when you're
> ready — the robot takes it from there (version bump, changelog, tag, GitHub
> Release). Nothing has changed yet; merging is the moment of release."*

If it was opened `--draft`, say so: "…opened as a draft so you can keep editing
— mark it ready when it's good."

---

## Dry-run mode — walk the canonical (when the canonical is authored)

When the release-train canonical lives at
`plugins/sulis/instances/release-train/` (Workflow + Steps + Triggers +
FailureModes + Tools authored as JSON-LD instances), the `--dry-run`
preview can walk the canonical itself instead of describing the
release purely from imperative YAML inspection. The founder gets a
Step-by-Step narrative derived from the spec — what each Step would
do, which FailureModes guard it, what the human-gate Step (open the
PR + merge) requires — rather than re-reading bash.

Per **ADR-001** (Path A — canonical-as-spec, imperative CI continues),
the canonical walk runs at *dry-run time only*. The actual release
machinery in `release-on-merge.yml` stays imperative and zero-token;
the LLM-driven runner pays its token cost once per release decision,
not per CI run. The drift detector (FR-015) is what keeps the
imperative path faithful to the canonical between dry-runs.

To invoke the canonical walk, dispatch the brain's `execute-workflow`
agent against the canonical directory:

```bash
# Probe for the canonical directory first; fall back if absent.
CANONICAL=plugins/sulis/instances/release-train
if [ -d "$CANONICAL" ]; then
  # Resolve the founder-Project (the marketplace plugin being released)
  # and dispatch the brain agent. for_project binds the Project's
  # state_contract variables so each Step's prose renders correctly.
  /sulis-brain:execute-workflow "$CANONICAL"
else
  # Canonical absent (older marketplace fork, or canonical not yet
  # authored). Skip the canonical walk and use the imperative-only
  # preview above. No regression — the existing dry-run still works.
  echo "Canonical absent — using imperative-only preview."
fi
```

The agent reads `workflow.jsonld`, `steps.jsonld`, `triggers.jsonld`,
`failuremodes.jsonld`, and `tools.jsonld`, walks the Steps in order,
and produces a per-Step preview rendered from each Step's
`agent_instructions` field. The non-dry-run (open-the-PR) path is
unchanged — it continues to use the imperative flow described in
section 5.

**Token-cost envelope (NFR-001).** The canonical walk is the only
token-consuming part of the release train; the imperative path
remains zero-token. NFR-001 in the SRD sets the per-dry-run budget;
exceeding the budget surfaces a warning to the founder so the cost
shape is visible at invoke time. Step 5 (`draft-pr-body-and-changelog`)
also declares its own per-Step token budget (NFR-010) and falls back
to a deterministic CHANGELOG-from-template if it overruns.

**Fallback.** If `plugins/sulis/instances/release-train/` doesn't
exist (e.g. a marketplace fork that hasn't authored the canonical),
the skill falls back to the imperative-only preview from section 5.
No regression — every fork keeps a working dry-run.

---

## Composition — where this sits in the release train

The release train has three moving parts; this skill is the middle one, and it
is the only one a founder runs by hand:

1. **`/sulis:change ship`** lands a finished change on `dev` and writes a
   **changeset** — a tiny note recording *what* changed and its release tier,
   but no version number. Changesets accumulate on `dev`, one per shipped
   change.
2. **`/sulis:release-train`** (this skill) batches those accumulated changesets
   into one release: it previews the version bump and the changelog, and opens
   the `dev → main` pull request. It is **read-only** — it never bumps, never
   commits, never edits a file. Its only side effect is opening that one pull
   request.
3. **The release robot** (`release-on-merge.yml`, a GitHub Action) is the single
   authority that actually bumps. When the release pull request merges to
   `main`, the robot applies the cumulative tier to all three version values,
   assembles the changelog, deletes the consumed changesets, tags
   `v<umbrella-version>`, and publishes the GitHub Release.

Keeping this skill read-only is the load-bearing constraint: there is exactly
**one** thing allowed to change versions (the robot), so a release can never
half-bump or race itself.

## When to invoke this skill

- The founder wants to release everything on `dev` to production.
- The founder asks "what would the next release look like?" / "what's the next
  version?" (run it `--dry-run` — the default — for a no-side-effect preview).
- The founder wants to open the release pull request for review before merging.

## When NOT to invoke this skill

- The founder wants to land one piece of work on `dev` — that is
  `/sulis:change ship`, not a release.
- The founder wants to actually *bump the version* by hand — they don't, and
  this skill won't either; the robot owns the bump on merge.
- The founder wants to merge the release pull request — that is a deliberate
  click in GitHub (or `gh pr merge`), the moment of release; this skill only
  drafts and opens it.

## Gotchas

- **Read-only on the remote, bar the one pull request.** This skill never
  commits, never edits the working tree, and never changes a version number.
  Its only side effect is `gh pr create` — and only without `--dry-run`, only
  after the founder confirms. If you catch yourself about to write a file or run
  `git commit` / `jq` over a manifest, stop — that is the robot's job, not this
  skill's.
- **Never re-implement the version math.** The tier and the three bumped values
  come from `_changeset.cumulative_tier` / `next_version` via `python3 -c` — the
  same code the robot mirrors and the unit tests pin. Hand-rolling SemVer
  arithmetic here is exactly the drift this design exists to prevent (EP-03).
- **The tag is the umbrella version, not the plugin version.** `v<metadata.version>`
  (e.g. `v1.123.0`), never `v0.78.0`. The changelog *header*, by contrast, uses
  the plugin version (`## v0.78.0 — …`). Don't swap them.
- **No changesets is a valid release, not an error.** `cumulative_tier` of
  `None` means admin/docs-only — the version won't move, but the pull request
  still opens. The robot detects nothing-to-bump and skips the version change.
  Say so; don't bail out.
- **`--dry-run` is the default.** A bare `/sulis:release-train` opens nothing —
  it previews. Opening the pull request takes an explicit confirmation (and,
  for a major release, a second explicit confirmation behind the breaking-change
  callout).
- **One release at a time.** If a `dev → main` pull request is already open,
  surface it and ask — never open a duplicate.
- **Abort on version drift.** If the plugin version and the marketplace's sulis
  entry disagree, stop before drafting anything — a prior half-applied release
  must be sorted out first.
- **Don't narrate the machinery.** The founder doesn't need to hear about
  `_changeset.py`, `sys.path`, `cumulative_tier`, or the bash the robot mirrors.
  Surface what's now true — the next version, the changelog, the link — and what
  they should do next (FE-09 / no mechanism narration).

## Vocabulary

- **Release train** — the batched-release model: changes accumulate on `dev`
  (each leaving a changeset), then a release batches them all into one version
  bump on merge to `main`. Decouples *landing work* from *cutting a release*.
- **Changeset** — the small note a shipped change leaves behind
  (`.changesets/*.yaml`): what changed and its release tier, but no version
  number. The release reads these to work out the bump and the changelog.
- **Tier** — the size of the release (`patch` / `minor` / `major`), derived from
  the change kind (the 22-primitive vocabulary). The release tier is the biggest
  tier across all accumulated changesets.
- **The bump** — moving all three version values up by one tier, plus the tag.
  Done once per release, by the robot, on merge. Never by this skill.
- **The release robot** — `release-on-merge.yml`, the GitHub Action that is the
  single authority for the bump. It runs on merge to `main`.
- **Dry-run** — a preview with no side effects (the default). Shows the draft and
  the exact command; opens nothing.

## See also

- `../../scripts/_changeset.py` — the changeset helper this skill reads through
  (`read_changesets`, `cumulative_tier`, `next_version`); the single source of
  truth for the version math.
- `../../../../.changesets/README.md` — the changeset YAML contract (the shape
  each shipped change writes and this skill reads).
- `../change/SKILL.md` — `/sulis:change ship`, which writes the changesets this
  skill batches.
- `../../references/founder-facing-conventions.md` — Rules 1-6.
- `../../references/change-primitives.md` — the 22-primitive vocabulary the tier
  derives from.
