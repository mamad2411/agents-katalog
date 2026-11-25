---
name: loremaster-setup
description: >
  Guided, interactive onboarding that takes a Hermes Agent user from "tap added"
  to "first project live" — run it on first install of the Loremaster pack, when
  adding a new project (new channel + new lore vault), or when reconfiguring an
  existing setup (scripts, Jira, timezone, Obsidian).
version: 0.2.0
author: Loremaster
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [setup, onboarding, install, vault, config, scrum, PM]
    related_skills: [refine-wiki, wiki-qa]
---

# Loremaster setup — from "tap added" to "first project live"

Interactive onboarding. You (the agent) drive it; the human decides.

## Conduct (invariant)

- **One step at a time.** Run a step, show the result, confirm it passed, then move on.
  Never batch steps, never skip a verification.
- **Detect, don't decide.** Detect current state and report it; every choice (vault path,
  channel, timezone, skip/do) belongs to the human.
- **Every write is proposed first.** Show the exact file/diff/command, get an explicit
  approval in chat (or via the `request_approval` tool if installed), then apply. This is
  the pack's approval-gate philosophy — the setup skill is not exempt.
- **Never echo secrets.** No tokens, no `.env` contents, no key files in chat — check
  existence with `grep -q`/`test -f` only.
- **Re-runnable.** Every step starts by detecting what is already done and skips it.
  Steps 6 (Jira), 8 (Obsidian), and 10 (developer-side skills) are optional; offer to skip.

## Step 1 — Preflight

Run each check, report a pass/fail table, and fix failures before continuing.

```bash
hermes --version          # expect: Hermes Agent v0.17.0 or later
hermes gateway status     # expect: active (running) — or the user runs it in foreground
git --version             # expect: any modern git
graphify --version        # expect: graphify 0.8.44
```

- **hermes < v0.17** → stop; ask the user to upgrade (`hermes update`) first.
- **Gateway not running** → `hermes gateway start` (installed service) or `hermes gateway run`
  (foreground). If neither is set up, point to `hermes gateway setup`.
- **Chat platform:** ask which platform the gateway is connected to. Slack is recommended —
  the channel = project binding (Step 5) is Slack-first in this pack version. Confirm the
  wiring without touching any secrets: `hermes gateway status` reports the connected
  platform (expect a connected Slack line). If nothing is connected, walk the user through
  `hermes gateway setup`.
- **GitHub push auth** (the vault pushes need it):
  ```bash
  gh auth status            # expect: Logged in to github.com
  # or, for SSH remotes:
  ssh -T git@github.com     # expect: "successfully authenticated"
  ```
  On failure: `gh auth login`, or add an SSH key / deploy key. Re-verify before Step 4.
- **graphify missing or wrong version** → propose (then run after approval):
  ```bash
  uv tool install 'graphifyy==0.8.44'
  ```
  The version pin matters — the helper scripts (Step 3) are tested against this exact
  release; do not install an unpinned latest. If `uv` is missing, install it first per the
  official guide at https://docs.astral.sh/uv/getting-started/installation/ (download the
  installer, let the user review it, then run) — with approval.

## Step 2 — Install the remaining skills

Check what is already there, then install only what is missing:

```bash
hermes skills tap list                       # expect: loremaster-ai/loremaster listed
hermes skills tap add loremaster-ai/loremaster   # only if missing
hermes skills list --source hub              # note which loremaster skills are installed
```

Install the missing ones (all pack skills except this one):

```bash
for s in backlog-proposal backlog-update conflict-detection daily-scrum impact-analysis \
         meeting-agenda refine-wiki resolve-conflicts sprint-planning sprint-retro wiki-qa; do
  hermes skills install "loremaster-ai/loremaster/skills/$s" --yes
done
```

- Expected per skill: quarantine → security scan → install at trust level **community**.
  The third-party risk prompt is normal — tell the user to expect it.
- **GitHub API rate limit** errors → set `GITHUB_TOKEN` or `gh auth login`, retry.
- The **first** search/browse after `tap add` can come back empty while the hub index
  warms up — just run it again.
- Verify: `hermes skills list --source hub` now shows every pack skill enabled (the 11
  above plus this one).

**Optional (Slack only, recommended):** the approval-buttons plugin that provides the
`request_approval` tool the skills call before every external write:

```bash
hermes plugins install loremaster-ai/loremaster/plugins/loremaster-approval --enable
hermes gateway restart
```

Note: tested against Hermes Agent v0.17.0 (it imports private internals); if it breaks
after a Hermes upgrade, pin the hermes version. Update later with `install --force`.

## Step 3 — Fetch the helper scripts

The four deterministic helpers are **not delivered by skill install** (they live at the
repo root `scripts/`). Fetch them to `~/.hermes/scripts/`:

```bash
mkdir -p ~/.hermes/scripts
for f in loremaster-graphify-plan.py loremaster-graphify-build.py \
         loremaster-derive-wikilinks.py loremaster-poker.py; do
  if [ -e ~/.hermes/scripts/"$f" ]; then
    echo "exists, skipping: $f"          # re-run safe — never overwrite silently
    continue
  fi
  curl -fsSL "https://raw.githubusercontent.com/loremaster-ai/loremaster/main/scripts/$f" \
       -o ~/.hermes/scripts/"$f"
done
```

Verify they are runnable (a usage error is the expected output):

```bash
python3 ~/.hermes/scripts/loremaster-graphify-plan.py
# expect: "usage: loremaster-graphify-plan.py <concepts_dir> [--force]"
```

On curl failure (DNS/proxy/404): report the exact error; do not substitute guessed
alternatives. The loop skips files that already exist; to refresh one, show `ls -l`,
ask, and delete it before re-running the loop.

## Step 4 — Create or wire the lore vault

Ask: **new vault, or wire an existing repo?** Either way the vault is a git repo shaped:

```
raw/        # truth — humans write here (PRD.md, decisions/, gtm/, planning/)
wiki/       # derived — machine-written (concepts/*.md + index.md); never hand-edited
conflicts/  # open conflict / underspecified-decision reports
graphify-out/  # graph build products (appear after the first refine)
```

**raw is truth, wiki is derived** — one-way: `raw/` → `wiki/` → knowledge graph →
`[[wikilinks]]`. Humans never edit the derived layers.

**New vault** — propose the full file set from
[references/vault-skeleton.md](references/vault-skeleton.md), get approval, then:

```bash
VAULT=~/vaults/<project-name>    # basename = project name (Jira mapping in Step 6 keys on it)
mkdir -p "$VAULT"/{raw/decisions,raw/gtm,raw/planning,wiki/concepts,conflicts}
cd "$VAULT" && git init -b main
# write README.md, .gitignore, raw/PRD.md, wiki/index.md per the skeleton, then:
touch "$VAULT"/{raw/decisions,raw/gtm,raw/planning,wiki/concepts,conflicts}/.gitkeep
git add -A && git commit -m "Initialize lore vault skeleton"
```

**Existing repo** — verify it has `raw/` (or propose moving source docs under `raw/`),
add the missing skeleton pieces (`wiki/`, `conflicts/`, `.gitignore` entries) with approval.

**Remote + push check** (auth from Step 1 must hold):

```bash
gh repo create <owner>/<project-name>-lore-vault --private --source "$VAULT" --push
# or wire an existing remote:
git remote add origin <url> && git push -u origin main
git push --dry-run origin main && echo push-auth-ok    # dry-run proves WRITE access
```

On auth failure, report it as-is (no workarounds) — fix auth, re-verify, then continue.

## Step 5 — Bind channel = project (channel prompt, human-approved)

Slack only; on other platforms skip and note that the vault path must then be given per
conversation. This is the pack's isolation invariant: **channel = project = vault**.

1. Ask for the project's Slack channel ID (channel name → right-click → copy link → the
   trailing `C0…` segment). The agent must already be invited to that channel.
2. Build the prompt block from
   [references/channel-prompt-template.md](references/channel-prompt-template.md), filling
   in the channel ID, project name, and the vault's **absolute** path.
3. **Propose it:** show the full block plus the exact insertion plan (append under
   `slack.channel_prompts`; if `slack.allowed_channels` exists, append the channel ID
   comma-separated). **Do not touch any other key. Do not quote other channels' prompts
   back into chat.** Wait for explicit approval — this edits the live agent config.
4. After approval — backup first, then edit surgically:
   ```bash
   CFG="$(hermes config path)"
   cp "$CFG" "$CFG.bak.$(date +%Y%m%d-%H%M%S)"
   ```
   Apply the approved block, then validate:
   ```bash
   if python3 -c 'import yaml' 2>/dev/null; then
     python3 -c "import yaml; yaml.safe_load(open('$CFG'))" && echo YAML-OK || echo YAML-BROKEN
   else
     echo NO-PYYAML    # no validator on this host — the gateway restart below is the check
   fi
   ```
   `YAML-BROKEN` → restore the backup, report, stop. `NO-PYYAML` → proceed, but if the
   gateway restart in the next step fails to come back up, restore the backup and report.
5. Tell the user to run `hermes gateway restart`, then verify by mentioning the agent in
   the channel — it should answer as that project's SM/PM and name the vault path.

If DENIED: keep the backup unused, change nothing, and continue to the next step.

## Step 6 — Jira (optional — offer to skip)

Ask whether the team uses Jira. If yes:

```bash
mkdir -p ~/.hermes/keys
curl -fsSL https://raw.githubusercontent.com/loremaster-ai/loremaster/main/examples/jira.env.example \
     -o ~/.hermes/keys/jira.env
curl -fsSL https://raw.githubusercontent.com/loremaster-ai/loremaster/main/examples/jira-projects.tsv.example \
     -o ~/.hermes/keys/jira-projects.tsv
chmod 600 ~/.hermes/keys/jira.env ~/.hermes/keys/jira-projects.tsv
```

- Ask in chat for `JIRA_BASE_URL` and `JIRA_EMAIL` and fill them in.
- **The API token must never pass through chat.** Ask the user to edit
  `~/.hermes/keys/jira.env` themselves on the host and set `JIRA_API_TOKEN=`
  (least-scope token — ideally an account that sees only the managed projects), then say
  "done". Never read the token back, never echo it.
- Replace the example rows in `jira-projects.tsv` with one line per vault:
  `<vault-basename><TAB><JIRA_KEY>` (propose the exact line, then write).
- Verify without exposing anything: load the credentials
  (`set -a; . ~/.hermes/keys/jira.env; set +a`), then call
  `GET {JIRA_BASE_URL}/rest/api/3/myself` with HTTP Basic auth (Jira email + API token)
  via Python urllib, written at run time. Report **only the HTTP status code** — expect
  `200`. The token never goes on a command line, and the response body is never printed.
  `401/403` → token or scope wrong; ask the user to re-issue and retry. Never print the
  response body.

## Step 7 — TEAM_TZ (team timezone)

Skills date-stamp every artifact with `TZ="$TEAM_TZ"` so filenames and dates match the
team's wall clock, not the host's (often UTC).

```bash
timedatectl show -p Timezone --value    # linux;  macOS: readlink /etc/localtime
```

Show the detected host timezone and **ask the user to confirm the team's IANA timezone**
(they may differ — e.g. a cloud host on UTC, a team on `America/New_York` or
`Asia/Tokyo`). Then tell the user where to set it (propose the exact lines; append only
with approval):

- **Current session** (interactive/CLI runs): `export TEAM_TZ="Area/City"`. If the user
  wants it permanent, they add that line to their own shell profile themselves — propose
  the line, don't edit their profile.
- **Gateway service environment** (gateway-spawned sessions): systemd —
  `systemctl edit hermes-gateway`, add `[Service]` / `Environment=TEAM_TZ=Area/City`,
  then `systemctl daemon-reload` and `hermes gateway restart`; launchd — add it to
  `EnvironmentVariables` in the service plist.

Verify: `TZ="$TEAM_TZ" date +%F` prints today's date in the team's timezone.

## Step 8 — Obsidian (recommended — offer to skip)

The vault is plain markdown, so each teammate can browse it as an
[Obsidian](https://obsidian.md) vault — on their own machine, not the agent host:

1. Clone the vault repo, then Obsidian → **Open folder as vault**.
2. Install the community **Obsidian Git** plugin. Configure **pull-only**: auto pull on a
   short interval (e.g. 2 minutes), auto commit-and-push **off** — the agent host is the
   single writer of the derived layers, and auto-push from teammate machines races it and
   leaks half-finished state. Humans edit `raw/` only and commit-and-sync **manually**
   when they do.
3. The graph view is the payoff: `wiki/concepts/*.md` carry frontmatter `related`
   `[[wikilinks]]` **derived from the graphify graph** — Obsidian visualizes the team's
   lore (clusters, hubs, how a decision ripples). Never hand-edit `related` or `[[ ]]`;
   the next derivation overwrites them. To change a link, change `raw/` and re-refine.
4. `.obsidian/` must stay gitignored in the vault (editor state is per-person) — the
   skeleton's `.gitignore` already covers it; verify on existing repos.

## Step 9 — Smoke test

Run the whole pipeline once, end to end, in the vault.

1. If the user already has a real PRD, use it as `raw/PRD.md`. Otherwise propose writing
   the tiny sample from [references/sample-prd.md](references/sample-prd.md) to
   `raw/PRD.md` (two related features, so the graph gets an edge) and commit it.
2. Run one refinement pass **by following the `refine-wiki` skill exactly** (plan →
   inline semantic extraction → build → wikilink derivation → commit → push approval).
3. Verify the artifacts:
   ```bash
   ls wiki/index.md graphify-out/graph.json && ls wiki/concepts/
   # expect: index + graph.json exist, and one concept page per PRD concept
   ```
   `graphify-out/graph.json` should contain nodes for each concept and at least one edge.
   Missing graph → re-check Step 1 (graphify 0.8.44) and Step 3 (scripts); empty wiki →
   re-read refine-wiki's preconditions (e.g. an open conflict holds refinement).
4. Ask-and-answer one question **by following the `wiki-qa` skill** (graphify query →
   read only the pointed-to pages → answer with `sources` cited), e.g. "what does the
   PRD say about sharing?" A cited, evidence-only answer = the project is live.
5. If the sample PRD was used: remind the user to replace it with the real one and
   re-run refine-wiki — deleted concepts drop out of the graph automatically.

## Step 10 — Developer-side skills (optional — offer to skip)

The last mile of an issue happens in each developer's local coding agent (Claude Code,
Cursor, or any agentskills.io client). This repo ships those skills in `client-template/`
— they install by being **committed into the product repo**, not per developer.

1. Ask for the product repo path (the code repo, not the vault). Skip if the team does
   not use local coding agents.
2. Fetch `client-template/.claude/` from this repo (same raw.githubusercontent.com base
   as Step 3, files under `client-template/.claude/skills/<name>/SKILL.md` for
   backlog-kickoff, backlog-complete, backlog-recall, project-onboard) into
   `<product-repo>/.claude/skills/`. If `.claude/skills/` already exists there, show
   what would be added and never overwrite existing skills without approval.
3. Propose the commit (show `git status`), get approval, commit with message
   "Add Loremaster developer-side skills" and push.
4. Tell the team: everyone gets the skills on their next `git pull` — `backlog-kickoff
   <issue>` to start an issue, `backlog-complete <issue>` to finish (pre-push conflict
   check → commit/push → Jira transition).

## Wrap-up

Report a final checklist: hermes/graphify versions, skills installed, scripts fetched,
vault path + remote, channel bound (or skipped), Jira (or skipped), TEAM_TZ, Obsidian
notes, developer-side skills (or skipped), smoke test result. List anything skipped so
the user can re-run this skill later — it detects done steps and picks up where it left
off.
