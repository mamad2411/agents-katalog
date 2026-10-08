---
name: triaging-github-issues-and-prs
description: Use when the user asks you to look at, check, review, triage, or reply to a GitHub issue or PR, especially submissions that add content to a curated directory (new library entries, listings, catalog items). Covers verifying claims in the submission, drafting a reply, and posting it (optionally as an alt identity).
---

# Triaging GitHub Issues and PRs

## Overview

Three phases: **investigate**, **adversarial check**, **reply**. Don't collapse them. Don't post until the user has approved the exact body.

## When to use

- "What do you think of PR #N?"
- "Check issue #N"
- "Reply to that PR"
- "Is this submission legit?"

Especially valuable when the PR adds content to a curated list/directory, where the project's value depends on the maintainer not accepting junk.

## Phase 1: Investigate

Pull the PR/issue and the diff up front:

```bash
gh pr view <N> --json title,body,files,additions,deletions,author,state
gh pr diff <N>
# or
gh issue view <N> --json title,body,author,state,comments
```

Note things in the PR body that look promotional or evasive: UTM tracking parameters, marketing taglines, vague "trust us" claims, brand-new domains.

### For library-directory submissions, verify claims independently

Don't take the YAML/JSON at face value. Check each external reference:

| Claim | How to verify |
|---|---|
| `homeUrl` | `curl -sS -o /dev/null -w "HTTP %{http_code}\n" --max-time 10 <url>` and `host <domain>` — a domain that resolves to `0.0.0.0` or fails to connect is dead, even if WHOIS says registered |
| Domain age | `whois <domain> \| grep -iE "creation date"` — a domain registered days/weeks before the PR is a flag |
| `githubRepo` | `gh api repos/<owner>/<repo> --jq '.full_name, .stargazers_count, .pushed_at'` |
| `npmPackage` | `npm view <name> version time.modified` |
| Author | `gh api users/<login> --jq '{login, name, created_at, public_repos, followers}'` — fresh sockpuppet vs long-standing user |
| Schema validity | Read the project's schema/validator before assuming a field is required. `null` may already be allowed — find precedents (`grep -l "field: null" data/`) before flagging it |
| Feature/capability flags | If the value is a prose excuse like *"Adding X is up to you in your shipped source"*, that means the library does **not** ship the feature — it should be `false`, not a string. String values are for "yes, with caveats" (compare against accepted entries). |

Run the cheap independent checks in parallel (one Bash tool message, multiple calls).

### Sandbox gotcha

If a network check fails, confirm it's not the sandbox before drawing conclusions:

```bash
nono why --host <domain>
```

If `nono` says ALLOWED and the connection still fails, the failure is real.

## Phase 2: Adversarial pass (REQUIRED)

Before drafting a reply, dispatch a subagent to challenge your conclusion. This is non-negotiable — you are about to recommend public action on someone's contribution, and confirmation bias is the failure mode.

Use the `general-purpose` (or `Explore`) agent. Prompt template:

> I just reviewed PR #<N> on <repo> and concluded: <one-sentence verdict>.
>
> My evidence: <bulleted list of the specific facts you used — domain status, repo lookup, whois date, schema precedents, etc.>
>
> Try to break this. Specifically:
> 1. Re-run the verification commands and confirm or contradict each fact (don't trust my summary — check directly).
> 2. Is there a charitable interpretation I'm missing? (e.g. domain not yet pointed at the live host, repo private but legitimate, etc.)
> 3. Are there accepted entries in this repo that already have the property I'm flagging as disqualifying?
> 4. Anything in the PR body, author history, or related issues I overlooked?
>
> Report under 250 words: confirmed facts, contradicted facts, charitable reads worth raising with the maintainer.

If the adversarial pass contradicts a fact, fix the draft. If it surfaces a charitable read, decide whether to soften the reply or ask the user.

## Phase 3: Reply

### Draft structure that works

```
[Greeting / acknowledgement — one short sentence]

[Verdict in one sentence — "I can't merge this as-is" / "Looks good, merging" / etc.]

**Bold blocker headline.** One paragraph: what's wrong, the specific evidence, what the contributor needs to do.

**Bold blocker headline.** ...

[Closing line — "Happy to revisit once X" or similar, leaving the door open if appropriate]
```

Cite specific evidence (DNS result, whois date, file path of a precedent). Vague reviews invite argument; specific ones don't.

### Show the draft, get approval

Always show the user the draft and wait for explicit approval before posting. Don't post on the first turn even if asked to "review and post" — the body is going public under a real identity. One confirmation round is cheap.

### Post

Use a HEREDOC so quoting/markdown survives:

```bash
gh pr review <N> --repo <owner>/<repo> --request-changes --body "$(cat <<'EOF'
[approved body]
EOF
)"
```

- `--request-changes` formally blocks merge.
- `--comment` is non-blocking commentary.
- `--approve` approves.

For issues use `gh issue comment <N> --repo <owner>/<repo> --body "$(cat <<'EOF' ... EOF\n)"`.

### Posting as an alt identity

Only when the user explicitly asks. Confirm available identities, switch, post, switch back, verify:

```bash
gh auth status                              # show what's available
gh auth switch --user <alt-login>
gh api user --jq .login                     # confirm the switch took
gh pr review <N> --repo <r> --request-changes --body "$(cat <<'EOF' ... EOF\n)"
gh auth switch --user <primary-login>
gh api user --jq .login                     # confirm restored
gh pr view <N> --repo <r> --json reviews --jq '.reviews[-1] | {author: .author.login, state}'
```

If the user wants the alt to read like a bot, an opening line like "Hey, I'm @<primary>'s bug bot." sets expectations. Get the exact wording approved — typos in identity-establishing lines look bad ("Hell" vs "Hello").

## Authorization gates

Posting on GitHub is a visible, hard-to-reverse action. Always confirm the user wants it before running `gh pr review`, `gh pr comment`, `gh issue comment`, etc. Approval of the draft text counts; "review the PR" does not authorize posting.

Never run `--approve` or merge actions without an unambiguous instruction.

## Common mistakes

- **Posting on the first ask.** "What do you think of PR #N" is a request for analysis, not a request to post. Default to drafting and showing the user.
- **Skipping the adversarial pass.** Easy to skip; it's where confirmation-bias errors get caught.
- **Treating the schema as authoritative without checking precedents.** A field being `null` may already be common. Grep before flagging.
- **Flagging string-valued feature flags as schema violations.** They're a deliberate "yes, with caveats" mechanism. The actual misuse is using a string to disguise a `false`.
- **Forgetting to switch back.** After `gh auth switch --user <alt>`, leaving the alt active means the next unrelated `gh` command runs as the wrong user. Switch back and verify with `gh api user --jq .login`.
- **Drawing conclusions from sandboxed network failures.** Run `nono why --host <domain>` before claiming a site is dead.
