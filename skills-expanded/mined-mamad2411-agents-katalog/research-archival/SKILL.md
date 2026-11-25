---
name: research-archival
description: Scrape AI research URLs, archive with frontmatter, create GitHub Issues with identity verification.
allowed-tools: Read, Bash, Grep, Glob, Edit, Write
---

# Research Archival

Scrape AI research conversations (ChatGPT, Gemini, Claude) and web pages, archive them as markdown files with YAML frontmatter, and create cross-referenced GitHub Issues — with mandatory identity verification at every step.

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

## FIRST - TodoWrite Task Templates

**MANDATORY**: Select and load the appropriate template before any archival work.

### Template A - Full Archival (scrape + save + issue)

```
1. Identity preflight — verify GH_ACCOUNT or resolve via curl /user
2. Scrape URL — route to Firecrawl or Jina per url-routing.md
3. Save the RAW scrape — docs/research/raw/…{source_type}.raw-scrape.txt, byte-exact, never edited
4. Record its sha256 — over the raw file's exact bytes
5. Write the EDITORIAL .md — frontmatter incl. raw_scrape_path + raw_scrape_sha256, and a POINTER.
   Do NOT paste the transcript in; see "File Saving — TWO artifacts, and never one"
6. Survey labels — gh label list, reuse existing, max 3-6
7. Create GitHub Issue — use --body with heredoc or --body-file
8. Update frontmatter — add github_issue_url and github_issue_number
9. Post canonical backlink comment on Issue
```

### Template B - Save Only (no issue)

```
1. Identity preflight (still required for consistency)
2. Scrape URL — route to Firecrawl or Jina per url-routing.md
3. Save the RAW scrape as .raw-scrape.txt + record its sha256
4. Write the EDITORIAL .md with the provenance pin and a pointer — never the transcript itself
```

### Template C - Issue Only (file already exists)

```
1. Identity preflight
2. Read existing file frontmatter
3. Survey labels — gh label list, reuse existing, max 3-6
4. Create GitHub Issue — use --body with heredoc or --body-file
5. Update file frontmatter with issue cross-reference
6. Post canonical backlink comment on Issue
```

---

## Identity Preflight (MANDATORY — Step 0)

**MUST execute before any `gh` write command. Non-negotiable.**

The `gh-repo-identity-guard.mjs` PreToolUse hook provides a safety net, but this skill performs its own check as defense-in-depth.

### Resolution Order

1. **Fast-path** — `GH_ACCOUNT` env var (set by mise per-directory)
2. **Token filename** — scan `~/.claude/.secrets/gh-token-*` for single base match
3. **API call** — `curl -sH "Authorization: token $GH_TOKEN" https://api.github.com/user`

### Verification

> 🔴 **`cd` into the repository INSIDE the heredoc, and export `GH_CONFIG_DIR` yourself.** A bare `/usr/bin/env bash` is a NEW process that does not inherit the interactive shell's functions, so on a machine using owner-per-path the `gh` you call from it is **not the `gh` you call from the prompt**. Measured 2026-09-06: `gh api user` returned the repository's own account from the interactive shell and a DIFFERENT, globally-active account from the heredoc, in the same directory — a false MISMATCH that blocks a correct archival, and one that looks exactly like a real credential problem. The mechanism is that `gh` is a shell function wrapping the binary with `GH_CONFIG_DIR` set from the per-repository `gh.configdir` git config key, so that key is what selects the identity. Resolve it in the script instead of depending on the caller's shell, and the check becomes shell-independent.

```bash
/usr/bin/env bash << 'IDENTITY_EOF'
cd "$REPO_DIR" || { echo "BLOCKED — cannot cd to \$REPO_DIR"; exit 1; }

# Honour owner-per-path BEFORE calling gh. `gh.configdir` is a per-repository git config key, so it
# is invisible to a fresh shell unless read explicitly. Without this the next line asks the wrong
# account and the whole check is answered about a repo you are not writing to.
_cfgdir=$(git config --get gh.configdir 2>/dev/null)
if [ -n "$_cfgdir" ]; then
  export GH_CONFIG_DIR="${_cfgdir/#\~/$HOME}"
  unset GH_TOKEN GITHUB_TOKEN   # an ambient token silently outranks GH_CONFIG_DIR
fi

# Resolve authenticated user
if [ -n "${GH_ACCOUNT:-}" ]; then
  AUTH_USER="$GH_ACCOUNT"
  AUTH_SOURCE="GH_ACCOUNT"
elif [ -n "${GH_TOKEN:-}" ]; then
  AUTH_USER=$(curl -sf --max-time 5 -H "Authorization: token $GH_TOKEN" \
    https://api.github.com/user 2>/dev/null | grep -o '"login":"[^"]*"' | cut -d'"' -f4)
  AUTH_SOURCE="API /user"
else
  # `gh` keeps the credential in the OS keyring, so GH_TOKEN is frequently absent from the
  # environment on a correctly-configured machine. Asking gh is not a fallback, it is the
  # normal path -- and omitting it made the API branch return empty on every keyring setup.
  AUTH_USER=$(gh api user --jq .login 2>/dev/null)
  AUTH_SOURCE="gh api user (keyring, GH_CONFIG_DIR=${GH_CONFIG_DIR:-default})"
fi

# Resolve target repo owner.
# `github\.com` alone does NOT match an SSH host alias: this machine's own owner-per-path policy
# gives remotes like `git@github.com-terrylica:terrylica/repo.git`, where the character after
# `github.com` is `-`, not `:` or `/`. The optional `[^:/]*` consumes the alias suffix.
REPO_SLUG=$(git remote get-url origin 2>/dev/null | sed -n 's|.*github\.com[^:/]*[:/]\([^/]*/[^/.]*\).*|\1|p')
REPO_OWNER=${REPO_SLUG%%/*}

echo "Authenticated as: ${AUTH_USER:-<unresolved>} (via $AUTH_SOURCE)"
echo "Target repo owner: ${REPO_OWNER:-<unresolved>}"

# FAIL CLOSED. If either side is empty the comparison below is "" = "" and the guard reports
# SUCCESS while knowing nothing -- the exact green-signal-is-a-proxy failure this repo catalogues.
# Observed 2026-08-20: an SSH-alias remote produced an empty owner, an absent GH_TOKEN produced an
# empty user, and the check printed "Identity verified".
if [ -z "${AUTH_USER:-}" ] || [ -z "${REPO_SLUG:-}" ]; then
  echo ""
  echo "BLOCKED — identity could not be RESOLVED, which is not the same as verified."
  [ -z "${AUTH_USER:-}" ] && echo "  authenticated user : unresolved (set GH_ACCOUNT, or check \`gh auth status\`)"
  [ -z "${REPO_SLUG:-}" ] && echo "  repo slug          : unresolved from $(git remote get-url origin 2>/dev/null || echo '<no origin>')"
  exit 1
fi

if [ "$AUTH_USER" = "$REPO_OWNER" ]; then
  echo "Identity verified (personal repo, owner == authenticated user)"
  exit 0
fi

# NOT automatically a failure. On an ORGANISATION repo the owner is the org, never a user, so a
# string comparison can never match however correct the credential is. The real question is
# whether this identity may write here.
API_RC=0
REPO_JSON=$(gh api "repos/$REPO_SLUG" 2>/tmp/gh-identity-err) || API_RC=$?
OWNER_TYPE=$(printf '%s' "$REPO_JSON" | jq -r '.owner.type // empty')
CAN_PUSH=$(printf '%s' "$REPO_JSON" | jq -r '.permissions.push // empty')

if [ "$OWNER_TYPE" = "Organization" ] && [ "$CAN_PUSH" = "true" ]; then
  echo "Identity verified (organisation repo; $AUTH_USER holds push on $REPO_SLUG)"
  exit 0
fi

echo ""
echo "MISMATCH — do NOT proceed with gh write commands"
# Print what GitHub actually returned. A field that is absent prints as nothing, because absent is
# a state -- substituting a word like "unknown" would report a value GitHub never sent.
[ -n "$OWNER_TYPE" ] && echo "  owner.type       : $OWNER_TYPE"
[ -n "$CAN_PUSH" ] && echo "  permissions.push : $CAN_PUSH"
[ "$API_RC" -ne 0 ] && echo "  gh exit code     : $API_RC"
[ -s /tmp/gh-identity-err ] && echo "  gh stderr        : $(head -1 /tmp/gh-identity-err)"
echo "Fix: export GH_TOKEN=\$(~/.claude/tools/bin/gh-token-for-repo)"
exit 1
IDENTITY_EOF
```

**BLOCK if mismatch** — display diagnostic and do NOT continue to any `gh` write operation.

> **Why the organisation branch exists.** The original check was `AUTH_USER != REPO_OWNER → block`.
> On an organisation repository the owner is the **org**, so that comparison can never match no
> matter how correct the credential is — it blocked every legitimate archival into a shared repo.
> Measured 2026-08-20 on `Eon-Labs/alpha-forge`: authenticated `terrylica`, owner `Eon-Labs`,
> `owner.type = Organization`, `permissions.push = true`. That is the correct identity, and the
> check called it a mismatch.
>
> The guard's purpose is to stop writes going to the **wrong account**, and "may this identity write
> here" is answered by `permissions.push`, not by string equality with the owner. The personal-repo
> equality path is kept as the fast, offline case; the org path costs one API call and is only
> reached when equality fails.

---

## Scraping Workflow

Route scrape requests based on URL pattern. See [url-routing.md](./references/url-routing.md) for full details.

### Decision Tree

```
Any JS-rendered share link (chatgpt.com/share/, gemini.google.com/share/, claude.ai/artifacts/)
  → Firecrawl public API (POST https://api.firecrawl.dev/v2/scrape)
  → Use curl (not WebFetch — it summarizes instead of returning raw)

Simple static page
  → Either works. Jina Reader (https://r.jina.ai/{URL}) is one GET and fine here.
```

**Default to Firecrawl.** Measured 2026-08-13 on two `chatgpt.com/share/*` links, Jina returned
**17% and 12%** of Firecrawl's content and truncated mid-sentence; Firecrawl reached the true page
footer both times. Jina also needs `-H "x-timeout: 30"` or it returns ~321 bytes of login chrome.

### Firecrawl Scrape

No health check, no preflight, no revival. The public API needs no key and has no host to be down —
handle a failed request per request rather than gating the run on a liveness probe.

```bash
/usr/bin/env bash << 'SCRAPE_EOF'
set -euo pipefail

# waitFor gives the SPA time to render; without it a share link returns the shell.
RESPONSE=$(curl -sS --max-time 180 -X POST https://api.firecrawl.dev/v2/scrape \
  -H "Content-Type: application/json" \
  -d "$(jq -n --arg u "$URL" \
        '{url: $u, formats: ["markdown"], waitFor: 8000, timeout: 60000}')")

CONTENT=$(printf '%s' "$RESPONSE" | jq -r '.data.markdown // empty')

if [ -z "$CONTENT" ]; then
  echo "ERROR: Firecrawl returned no markdown:" >&2
  printf '%s\n' "$RESPONSE" | head -c 400 >&2
  echo "Retry once, then fall back to: curl -H 'x-timeout: 30' https://r.jina.ai/${URL}" >&2
  exit 1
fi

printf '%s\n' "$CONTENT"
SCRAPE_EOF
```

> **Do not reintroduce a self-hosted Firecrawl.** The gpu-host-2 deployment (ports 3002/3003, five
> containers) was retired 2026-08-13 and reclaimed ~18 GB. It required health checks, container
> restarts, and WORKER-STALLED triage that the public API makes unnecessary at this volume.

---

## File Saving — TWO artifacts, and never one

An archival produces **two** files. This is the single most important thing on this page, because
getting it wrong is expensive and the cost is invisible until someone tries to verify the archive.

```
docs/research/raw/YYYY-MM-DD-{slug}-{source_type}.raw-scrape.txt   the scrape, byte-exact, NEVER edited
docs/research/YYYY-MM-DD-{slug}-{source_type}.md                   editorial + a POINTER to it
```

- `slug` — kebab-case summary (max 50 chars)
- `source_type` — from enum: `chatgpt`, `gemini`, `claude`, `web`

### 🔴 Do NOT paste the transcript into the `.md`

It is the obvious thing to do and it is wrong. **Alpha-forge PR #540 removed a duplicated transcript
after five successive review rounds**, each of which found a class of meaning-changing edit that the
equivalence checker certified as identical: structural markers erased (a quotation demoted to the
author's own assertion), inline delimiters erased (`` `not` `` reading as the English word),
identifiers and URL paths retargeted through `_` and again through `__`, table cell boundaries moved
so an outcome attached to the wrong reference, and literal asterisks consumed inside escapes, fenced
and indented code blocks, and raw HTML attributes.

The last class is a **category error, not a bug**. [CommonMark 0.31.2](https://spec.commonmark.org/0.31.2/)
specifies parsing in two phases — _"In the first phase, lines of input are consumed and the block
structure of the document … is constructed. Text is assigned to these blocks but not parsed. … In the
second phase, the raw text contents of paragraphs and headings are parsed into sequences of Markdown
inline elements"_ — so a line-oriented normaliser has **no block phase** and cannot tell a paragraph
from a fenced code block. No amount of further patching converges.

Why the question arises at all: any repository whose tooling reformats markdown (here, the `itp-hooks`
Stop hook running `prettier --write` and `markdownlint-cli2 --fix`) makes a pasted copy **impossible
to keep byte-identical**, so "is the copy still saying what the original said?" becomes a question you
must answer on every commit. **With one copy there is no question.**

### Enforcing one-copy: MEASURE the duplicate, never pattern-match a marker

The first gate refused re-embedding by looking for the legacy `<!-- RAW-SCRAPE-BODY-BEGINS -->`
comment. Review defeated it in one move: **append the whole transcript after a plain `---`, omit the
marker, and the gate returns success** — while the test named `test_re_embedding_the_transcript_is_refused`
stayed green, because that test built its fixture _using_ the marker. A pattern match presented as a
structural guarantee, verified on the one input where the bug could not appear.

Re-embedding is a **near-duplicate detection** problem, so use the standard measure for one:
_containment_ over w-shingles, from Andrei Z. Broder, "On the resemblance and containment of
documents", SEQUENCES 1997, `doi:10.1109/SEQUEN.1997.666900` — _"the containment c(A,B) of A in B is
a number between 0 and 1 that, when close to 1, indicates that A is roughly contained within B"_, over
_"the bag (multiset) of all shingles of size w contained in D"_.

Four things make it work in practice:

- **Containment, not resemblance.** The question is directional — how much of the _transcript_
  reappears — and resemblance is symmetric, so a long editorial section would dilute it and mask a
  full paste.
- **Calibrate the threshold; do not choose it.** Measure the real archive and a ladder of partial
  pastes. Ours: `0.0097` legitimate quoting → `0.1172` a tenth → `1.0000` the whole thing, so a `0.10`
  limit sits ~10× above quoting and below every meaningful paste. Publish the ladder next to the
  constant, or the number reads as a guess.
- **Tokenise lowercased alphanumerics**, so the measure survives the very reformatting that made
  byte-comparison impossible. A re-embedded transcript must still be caught after `prettier` runs.
- **Sets, not multisets.** Broder defines a bag; a set answers "how much _distinct_ material was
  reproduced", so pasting one fragment twenty times counts once — which is the right semantics here.

**Scope the invariant to the repository, not to one file.** The second bypass was simply moving the
copy: a sweep of only the archive that _pins_ the transcript reported success while a sibling `.md`
held 100% of it. Sweep every markdown file, **and** measure their concatenation — twelve fragments
each under the limit still reconstruct the transcript.

State the two limits rather than claiming them away: **a single quoted line must still pass** (the
archive itself legitimately quotes at ~1%, so any threshold that refuses one pasted line forbids
quotation entirely), and **a heavily paraphrased re-embed defeats the measure** — at that point the
documents genuinely differ and no automatic check can rule on whether meaning survived. That is the
same undecidability that killed the normaliser; reviewer judgement is the only control.

### The `.txt` extension is load-bearing

Store the raw scrape as `.txt`, not `.md`. Markdown tooling globs `*.md`; a raw scrape kept as `.md`
gets rewritten and its hash invalidated **without anyone touching it**. The extension makes the
artifact immune by construction rather than by configuration — `.prettierignore` and
`.gitattributes -text` are worth adding as defence in depth, but they are not the mechanism.

### YAML Frontmatter

See [frontmatter-schema.md](./references/frontmatter-schema.md) for the full field contract.

```yaml
---
source_url: https://chatgpt.com/share/...
source_type: chatgpt-share
scraped_at: "2026-02-09T18:30:00Z" # a REAL timestamp; never a rounded guess
scraped_at_source: "how you obtained it, e.g. mtime of the scraper's output file"
raw_scrape_path: docs/research/raw/YYYY-MM-DD-{slug}-{source_type}.raw-scrape.txt
raw_scrape_sha256: "sha256 of the raw file's exact bytes"
transcript_location: "not reproduced in this file; the sole copy is raw_scrape_path"
model_name: gpt-4o
claude_code_uuid: SESSION_UUID
github_issue_url: ""
github_issue_number: ""
---
```

`raw_scrape_path` and `raw_scrape_sha256` are a **pair**. Declaring one without the other is worse
than declaring neither: a hash with no file proves nothing, and a file with no hash is unverified
while looking pinned. Gates should discover on **either** key so a half-declaration is refused rather
than silently skipped.

Leave `github_issue_url` and `github_issue_number` empty — update after Issue creation.

### What goes in the `.md`

Editorial only, and it is worth writing properly because it is the part a human reads:

1. A **provenance warning** stating the transcript is not reproduced here and is untrusted AI output.
2. An **audit note** — which citations were checked, by what method, and what was found. Distinguish
   _identity_ checks (the DOI resolves to this title/author/venue) from _content_ checks (the source
   actually says what the summary claims). They are different, and conflating them is the usual error.
3. Any **known errors** in the source, stated where a reader will see them rather than only in the PR.
4. A **pointer** to the `.txt` with its size and sha256.

Verify citations by **content** via the Crossref API, never by HTTP status — a 403 bot-wall and a 404
are indistinguishable from the status line. When Crossref carries no abstract, say so and mark the
claim unverified rather than implying it was checked.

**Match every verbatim quotation back against the retrieved document programmatically**, and check the
extraction before trusting the match. `textutil -convert txt -stdout` on a PDF returned exactly the
file's byte count — the raw bytes passed straight through, reported as success — against which any
quote would have "verified" into binary noise. Sanity-check extracted length against page count, then
compare whitespace-insensitive and ligature-folded, since extraction mangles inter-word spacing.

When the match fails, **find out which kind of failure it is before editing anything**. Ours failed
twice: once because the extractor interpolated a page number mid-sentence (the quotation was
faithful), and once because a `'` had been substituted for the source's `"` _inside_ quotation marks.
The second is a modification of quoted text however small it looks, and it is the same defect as
substituting spoken names for glyphs that would not extract.

---

## GitHub Issue Creation

### Label Survey

Survey existing labels first — reuse preferred, create only when concept is genuinely novel.

```bash
gh label list --repo owner/repo --limit 100
```

**Policy**: Max 3-6 labels per issue. Common labels: `research`, `ai-output`, `chatgpt`, `gemini`, `archival`.

### Create Issue

Use `--body` with heredoc for inline composition, or `--body-file` for very large content.

```bash
/usr/bin/env bash << 'ISSUE_EOF'
# Write body to temp file
cat > "/tmp/issue-body-${SLUG}.md" << 'BODY_EOF'
## Summary

Brief description of the archived research content.

## Source

- **URL**: SOURCE_URL
- **Type**: source_type
- **Model**: model_name
- **Scraped**: scraped_at

## Key Findings

- Finding 1
- Finding 2

## Archived File

`docs/research/FILENAME.md`
BODY_EOF

# Create issue
gh issue create \
  --repo owner/repo \
  --title "Research: descriptive title here" \
  --body-file "/tmp/issue-body-${SLUG}.md" \
  --label "research,ai-output"

# Clean up
rm -f "/tmp/issue-body-${SLUG}.md"
ISSUE_EOF
```

### Update Frontmatter

After issue creation, update the archived file's frontmatter with the issue URL and number.

---

## Canonical Backlink Comment

Post a comment on the Issue linking back to the archived file. **Metadata goes in a markdown list,
not as consecutive prose lines:**

```
**Archived**: `docs/research/YYYY-MM-DD-slug-source_type.md`

- **Scraped**: 2026-02-09T18:30:00Z — scraper, byte count, whether it reached the page footer
- **Source**: [chatgpt-share](https://chatgpt.com/share/...)
- **Session**: `SESSION_UUID`
- **PR**: #NNN — commit `abcdef12`
```

> **Do not restore the bare consecutive-line version.** GitHub renders every newline in a comment as
> `<br>`, so four stacked `Key: value` lines are indistinguishable from hard-wrapped prose and the
> `GH-HARD-WRAP-GUARD` PreToolUse hook **rejects the command** (measured 2026-08-20 — the previous
> template in this file was itself the thing that tripped it). A list expresses "these are separate
> items" structurally, which is both what is meant and what the guard accepts. Reaching for the
> `GH-HARD-WRAP-OK` override here would suppress a correct complaint.

### Every issue/PR body must be authored as unbroken paragraphs

This applies to the Issue body and the PR body too, not just the backlink. Author each **paragraph**
as ONE long line and let GitHub reflow it; keep breaks only for list items, headings, code blocks and
blank lines. Editors that soft-wrap make this invisible — check with:

```bash
awk '{ if (length($0) > 100 && $0 !~ /^[-*|#> ]/) printf "L%d: %d cols\n", NR, length($0) }' body.md
```

Long lines are **expected and correct** for prose paragraphs; the failure mode is many lines of
~80–100 columns in a row.

---

## Post-Change Checklist

After modifying THIS skill:

1. [ ] YAML frontmatter valid (no colons in description)
2. [ ] Trigger keywords current in description
3. [ ] All `./references/` links resolve
4. [ ] Identity preflight section remains FIRST in workflow
5. [ ] Append changes to [evolution-log.md](./references/evolution-log.md)
6. [ ] Validate: `uv run plugins/plugin-dev/scripts/skill-creator/quick_validate.py plugins/gh-tools/skills/research-archival`
7. [ ] Validate links: `bun run plugins/plugin-dev/scripts/validate-links.ts plugins/gh-tools/skills/research-archival`

---

## Troubleshooting

| Issue                                                                                                 | Cause                                                                                                                                 | Fix                                                                                                                                                                                                                                                |
| ----------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `GH-HARD-WRAP-GUARD` rejects the command                                                              | Body authored as hard-wrapped prose                                                                                                   | Reflow each paragraph to ONE line; use a list for stacked `Key: value` metadata. Do **not** reach for `GH-HARD-WRAP-OK` — the guard is right                                                                                                       |
| Identity preflight blocks on an org repo                                                              | Owner is the org, so `AUTH_USER != REPO_OWNER` always                                                                                 | Expected — the check now falls through to `owner.type == Organization` + `permissions.push == true`. If it still blocks, you genuinely lack push                                                                                                   |
| Preflight reports a MISMATCH naming an account you are not using, and `gh` works fine from the prompt | The heredoc is a fresh process with no shell functions, so it called the raw `gh` binary and missed the per-repository `gh.configdir` | `cd` inside the heredoc AND export `GH_CONFIG_DIR` from `git config --get gh.configdir` before the first `gh` call. Confirm with `gh api user --jq .login` run inside vs outside the heredoc — differing answers is this bug, not a bad credential |
| `gh pr create` says "you must first push the current branch" **after** a successful push              | Run from a linked worktree; `gh` cannot resolve the upstream                                                                          | Pass `--head <branch> --base main` explicitly. Confirm the branch is really remote with `git ls-remote --heads origin <branch>`                                                                                                                    |
| Wrong account posting                                                                                 | GH_TOKEN mismatch                                                                                                                     | Check `mise env \| grep GH_TOKEN`, verify `GH_ACCOUNT`                                                                                                                                                                                             |
| Body exceeds 65536 chars                                                                              | GitHub API limit                                                                                                                      | Split across issue body + first comment                                                                                                                                                                                                            |
| Firecrawl returns no markdown                                                                         | Transient API failure                                                                                                                 | Retry once, then fall back to Jina with `-H "x-timeout: 30"`                                                                                                                                                                                       |
| Scrape returns the page shell                                                                         | SPA had not rendered yet                                                                                                              | Raise `waitFor` (8000 → 15000) and `timeout` in the request body                                                                                                                                                                                   |
| Jina returns ~321 bytes                                                                               | Missing timeout header                                                                                                                | Add `-H "x-timeout: 30"` — without it Jina returns login chrome                                                                                                                                                                                    |
| Jina output truncated                                                                                 | Jina under-covers JS-heavy pages                                                                                                      | Expected — use Firecrawl; Jina got 17%/12% coverage in the 2026-08-13 test                                                                                                                                                                         |
| mise parse error                                                                                      | Stale .mise.toml syntax                                                                                                               | Run `mise doctor`, check `[hooks.enter]` syntax                                                                                                                                                                                                    |
| Identity guard blocks                                                                                 | Non-owner account                                                                                                                     | `export GH_TOKEN=$(~/.claude/tools/bin/gh-token-for-repo)`                                                                                                                                                                                         |

## References

- [Frontmatter Schema](./references/frontmatter-schema.md) — YAML field contract
- [URL Routing](./references/url-routing.md) — Scraper routing table
- [Evolution Log](./references/evolution-log.md) — Change history

## Post-Execution Reflection

After this skill completes, check before closing:

1. **Did the command succeed?** — If not, fix the instruction or error table that caused the failure.
2. **Did parameters or output change?** — If the underlying tool's interface drifted, update Usage examples and Parameters table to match.
3. **Was a workaround needed?** — If you had to improvise (different flags, extra steps), update this SKILL.md so the next invocation doesn't need the same workaround.

Only update if the issue is real and reproducible — not speculative.
