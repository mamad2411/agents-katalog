---
name: secret-scan-method
description: Scan the repo including git history for leaked secrets — API keys, tokens, private keys, credentials. Run before any first push to a public remote, immediately after a committed-`.env` event, in CI on every PR, and as a quarterly full-history sweep. This skill is the detection primitive; `/secret-scan` is the remediation session that owns rotation playbooks, the history scrub and the persisted report.
kind: skill
pack: security
allowed-tools: [Read, Grep, Glob, Bash]
---

# secret-scan-method

Detect committed secrets in working tree, staged changes, and recent git history.

## Premise

Find real leaks, no hand-waves. Every finding cites the commit SHA + `<path:line>`, the matched rule (gitleaks rule id / trufflehog detector name), and a redacted excerpt of the match. The provider is identified by prefix when possible (`sk_live_`, `AKIA`, `ghp_`, `-----BEGIN ... PRIVATE KEY-----`). High-entropy hits are flagged separately from prefix-matched hits — entropy alone is suspicion, prefix is confirmation. Allow-listed test fixtures are documented in `.gitleaksignore`, not silently dropped. "Looks like a secret" without rule + redacted match is not a finding.

## Halt conditions

- Halt on any finding without `<commit>:<path:line>` + rule id + redacted excerpt.
- Halt on rotation/purge instructions that skip the rotate-first step (deleting the commit does not invalidate the credential).
- Halt on entropy-only findings that don't separate "high entropy near `token`/`secret`/`password` identifier" from "long config string".
- **Halt on a report written un-redacted.** A findings file that contains the live secret is a second copy of the leak, and CI keeps artifacts.

## Prerequisites

- One of: `gitleaks` (preferred), `trufflehog`, `detect-secrets`, already installed — the audit never installs one; none present → NOT-INSTALLED, to enable: `brew install gitleaks` / `pipx install detect-secrets`.
- Optional: a committed `.gitleaksignore` allow-list for known false positives.
- A second engine is a cross-check, not a requirement. A single-engine run is complete when every hit is either prefix-classified (§ What to look for) or read and classified by hand. Say which engine ran, and record a missing second engine on the report's scope line.

## Procedure

`detect` and `protect` were **deprecated in gitleaks v8.19.0** — still functional, hidden from `--help`. The current verbs are `git`, `dir` and `stdin`; use them, because copied-forward `detect`/`protect` lines are the first thing that breaks on a major bump.

1. Scan the working tree — fastest, catches what is on disk right now. `dir` reads files, not git, so **every hit has an empty `Commit`**. "Is it in history, has it shipped?" is answered only by step 3:
   ```bash
   gitleaks dir . --redact -v --report-format json --report-path /tmp/leaks-tree.json
   ```
2. Scan staged changes as a pre-commit gate:
   ```bash
   gitleaks git --staged --redact -v --report-format json --report-path /tmp/leaks-staged.json
   ```
3. Scan history — the scan that matters, because a reverted commit is still a leak:
   ```bash
   gitleaks git . --log-opts="--since=90.days.ago" --redact -v \
     --report-format json --report-path /tmp/leaks-history.json
   # first audit on any repo: run it with no --log-opts (whole history, slow)
   ```
   **No-write variant, and the lineages `--all` misses.** `gitleaks git` runs git inside the target; under a read-only rule on the gitdir, feed the patch stream to `gitleaks stdin` instead. Two kinds of history sit outside `--all`: reflog-only commits, and the objects of a lineage that was rewritten or re-rooted, which were often pushed before the rewrite. `git fsck --unreachable --no-reflogs` lists those commits, and `--stdin` adds them to the walk. A stdin report has an empty `Commit` and `File`, and its `StartLine` is the line in the stream, so the mapper below turns each hit back into commit, path and added/removed, and marks the ones only an unreachable commit holds:
   ```bash
   T="${T:-.}"; SCAN="${SCAN:-$(mktemp -d "${TMPDIR:-/tmp}/secret-scan.XXXXXX")}"   # the repo; reports stay outside it
   G=(env GIT_OPTIONAL_LOCKS=0 git -C "$T")
   "${G[@]}" fsck --unreachable --no-reflogs --connectivity-only 2>/dev/null | awk '$2 == "commit" { print $3 }' > "$SCAN/unreachable-commits.txt"
   "${G[@]}" log --all --reflog --stdin -p --no-color --no-ext-diff --format='commit %H' < "$SCAN/unreachable-commits.txt" > "$SCAN/history.patch"
   gitleaks stdin --redact --no-banner --report-format json --report-path "$SCAN/leaks-history.json" < "$SCAN/history.patch"
   python3 -I - "$SCAN/history.patch" "$SCAN/leaks-history.json" "$SCAN/unreachable-commits.txt" <<'PY'
   import json, sys
   hits = json.load(open(sys.argv[2])); lost = set(open(sys.argv[3]).read().split()); want = {}
   for i, h in enumerate(hits): want.setdefault(h["StartLine"], []).append(i)
   commit = path = None; at = {}
   for n, line in enumerate(open(sys.argv[1], encoding="utf-8", errors="replace"), 1):
       if line.startswith("commit ") and len(line.split()) == 2: commit = line.split()[1]
       elif line.startswith("diff --git "): path = line.rstrip("\n").split(" b/", 1)[-1]
       for i in want.get(n, ()): at[i] = (commit, path, {"+": "added", "-": "removed"}.get(line[:1], "context"))
   for i, h in enumerate(hits):
       c, p, how = at.get(i, ("?", "?", "?"))
       print(f"{c[:12]} {p} {how} {h['RuleID']} entropy={h.get('Entropy', 0):.2f}" + (" UNREACHABLE" if c in lost else ""))
   PY
   ```
   Stdin hits carry no `File`, so neither `.gitleaksignore` nor a `paths` allow-list applies to them: filter the mapper's path column with the same patterns. An `added` line names the introducing commit. Measured 2026-10-15 on a real NestJS + React monorepo (read-only worktree, gitleaks 8.30.1, 5 minutes): 4,815 unreachable commits from a pre-re-root lineage that `--all` never walked, 13.2 M patch lines, 254 raw hits before any allow-list (196 only in the unreachable lineage, 249 `generic-api-key`, mostly test and audit paths), every one mapped back to a commit and a path.
4. List what gitleaks cannot judge by content: secret-bearing **files** (a committed `.env.production` whose value is a low-entropy word passes every rule), and secrets **plumbed into an image** (`ARG`/`ENV NPM_TOKEN=${NPM_TOKEN}` has no literal to match, yet bakes the value into the image config and history). `--hidden` is required because these files are dot-files; `.gitignore` still applies, so an ignored local `.env` is not listed:
   ```bash
   N='(^|/)(\.env(\.[\w-]+)*|\.npmrc|\.pypirc|\.netrc|\.htpasswd|\.git-credentials|credentials(\.\w+)?|kubeconfig|id_(rsa|dsa|ecdsa|ed25519)|[\w.-]*\.(pem|key|p12|pfx|jks|keystore|ppk|tfstate|tfvars))$'
   rg --files --hidden -g '!**/.git/**' -g '!**/node_modules/**' . | rg -i "$N" | rg -v '\.(example|sample|template|dist|defaults?)$'
   git log --all --diff-filter=A --name-only --format= | sort -u | rg -i "$N" | rg -v '\.(example|sample|template|dist|defaults?)$'
   rg -n --pcre2 '^\s*(ARG|ENV)\s+\w*(TOKEN|SECRET|PASSWORD|PASSWD|API_?KEY|PRIVATE_?KEY|ACCESS_?KEY|CREDENTIALS?|AUTH)\w*' -g '*Dockerfile*' -g '*.dockerfile' -g '*Containerfile*' -g '!**/node_modules/**' .
   ```
   Read each listed file: a value is a finding, while a `${VAR}` reference or a template is not. An `ARG` consumed by `RUN --mount=type=secret` is the safe form; an `ENV` of it in the final stage is the leak.

   **AI context files** (the learning pack's KN-34 handover): a secret in a file an agent loads every session is pasted into every model context and transcript, so it is critical even when the repo is private. A tree scan misses a gitignored `CLAUDE.local.md`, so scan the list by path:
   ```bash
   i=0; rg --files --hidden --no-ignore -g '**/{CLAUDE,CLAUDE.local,AGENTS,GEMINI}.md' -g '**/.cursor/rules/**' -g '**/.cursorrules' \
     -g '**/.github/copilot-instructions.md' -g '**/.github/instructions/**' -g '**/ai/**/*.md' -g '**/.claude/**/*.md' -g '!**/node_modules/**' . |
   while IFS= read -r f; do i=$((i + 1)); gitleaks dir "$f" --redact --no-banner --report-format json --report-path "$SCAN/ctx-$i.json" >/dev/null 2>&1; done
   ```
   The host memory directory (`~/.claude/projects/<encoded>/memory/`) is outside the repo: scan it only when the user passes it (learning decision O-3). Measured 2026-10-19 on `benchmarks/fixtures/stale-knowledge` (gitleaks 8.30.1): 45 context files, 1 hit, the seeded `generic-api-key` at `ai/runbooks/local-dev.md:8`.
5. Cross-check entropy on suspect files with a second engine. In trufflehog v3 the path is positional, `--directory` is deprecated, and `--results=verified` replaces the hidden `--only-verified`:
   ```bash
   trufflehog filesystem . --results=verified --json | jq '.'
   ```
6. For each finding: identify the provider from the prefix (§ What to look for), find the introducing commit (`git log --all --source -- <file>`), and treat the credential as live until the provider says otherwise.

## Reading the output

**The exit code is not the answer.** `gitleaks` exits `0` for no leaks, `1` for **"leaks or errors encountered"**, and `126` for an unknown flag — so a `1` in CI may be a finding or a broken invocation, and only the report file distinguishes them. Wire CI on the report's contents, and treat an empty report plus a non-zero exit as a failed run, not a clean one.

Each JSON finding carries `RuleID`, `Description`, `File`, `StartLine`, `Commit`, `Author`, `Email`, `Date`, `Match`, `Secret`, `Entropy`, `Tags`. Read them in this order, because the first two decide everything downstream:

1. **`RuleID` → confirmation or suspicion.** A provider rule (`stripe-access-token`, `aws-access-key-id`, …) is a *format match*: the string is shaped like a real credential. A generic/entropy rule is *suspicion only*. Never escalate an entropy hit to CRITICAL without classifying it first.
2. **`Commit` → is it only in history?** In a `git` scan, an empty commit means staged or working tree only, so the secret has not shipped anywhere yet: fix it before it does. A `dir` scan never fills `Commit`, so its empty field says nothing; match the hit against the `git .` report before reading it as unshipped. A populated commit means it is in every clone, every fork, and the platform's event API. **That is still a leak.** Reachability from HEAD is irrelevant.
3. **`Author` / `Date` → who to tell and what window to audit.** These are the inputs to the provider-side log review ("was this key used between `Date` and now?"), which is the step that turns a leak into an incident or closes it.
4. **`Match` / `Secret` → only ever read redacted.** With `--redact` these are masked; without it, your report *is* the secret. This is why step 1-3 above all pass `--redact`.

**What to do, per class — in this order, always:**

| Finding class | First action | Then |
|---|---|---|
| Provider-prefix match, live credential | **Rotate at the provider.** Nothing else first. | Verify the old value is rejected, review the provider's access log for the leak window, then scrub history |
| Provider-prefix match, already-rotated key | Confirm rejection with a real call | Scrub or accept-with-note; record why it is inert |
| Entropy-only, near a `token`/`secret`/`password` identifier | Classify it — ask the author what it is | Rotate if real; `.gitleaksignore` with a reason if not |
| Entropy-only, a long config value / hash / generated fixture | Nothing | `.gitleaksignore` entry **with a reason comment** |
| Private key block | Rotate the key pair and remove the public half from every `authorized_keys` | Scrub, then re-issue |

**Rotation precedes removal, always.** Scrubbing history without rotating produces a repo that looks clean and a credential that still works — the worst of both states, because the evidence is gone and the exposure is not. `/secret-scan` owns the per-provider rotation playbook and the scrub procedure; hand off there once this skill has classified.

## What to look for

- Anthropic / OpenAI / Gemini: `sk-ant-`, `sk-`, `AIza` (a Gemini Developer API key; most `AIza…` keys are Firebase project identifiers — § False positives)
- Stripe: `sk_live_`, `pk_live_`, `whsec_`
- AWS: `AKIA[0-9A-Z]{16}`, `aws_secret_access_key`
- GitHub: `ghp_` (classic PAT), `github_pat_` (fine-grained PAT), `gho_` / `ghs_` / `ghu_` (OAuth/app tokens)
- Slack: `xox[baprs]-` (bot / app / refresh / user / legacy tokens)
- HuggingFace: `hf_`
- SendGrid: `SG.`
- Twilio: `AC[0-9a-f]{32}` (account SID), `SK…` (API key SID)
- npm: `npm_` (automation / publish token)
- GCP service-account JSON (`"type":"service_account"`)
- Private keys: `-----BEGIN (RSA|OPENSSH|EC) PRIVATE KEY-----`
- DB URLs with passwords: `postgres://user:pass@host`, `mysql://...`, `mongodb+srv://...`
- JWT signing secrets, generic high-entropy strings near identifiers like `token`, `secret`, `password`

## Output

```
Secret scan — last 90 days

BLOCKERS (2):
  commit abc1234   src/config/stripe.ts:8
    rule:stripe-live-secret  match:sk_live_redacted   author:<who>  date:<when>
    Action: rotate at the provider FIRST, then review their API log for the window, then purge.

  commit def5678   .env.staging:12
    rule:postgres-url-with-password  match:postgres://app:redacted@host
    Action: rotate the DB user credential, redeploy, then purge.

WARNINGS (1):
  src/seed.ts:42  (working tree only — no commit)
    rule:high-entropy-string  match:9f3a7b...redacted (40 chars)
    Unclassified — confirm with the author before escalating or allow-listing.

Next: hand BLOCKERS to `/secret-scan` for the rotation playbook + history scrub.
```

## False positives / gotchas

- Test fixtures intentionally use fake-looking keys (`sk_test_...`, `dummy-token-1234`) — allow-list them in `.gitleaksignore`, **with a reason**; an unexplained allow-list entry is how a real leak gets muted.
- **A `.gitleaksignore` fingerprint is commit-scoped** (`<commit>:<file>:<rule>:<line>`). A `gitleaks dir` run has no commit, and a moved line has a new number, so both re-report every fixture the file meant to mute: on a real monorepo, about 48 lines. Prefer the path-scoped allow-list below.
- **Your own prefix sweep needs guards.** A bare `EAA` (Meta token) prefix matched base64 PNG bodies in e2e specs 25 times out of 78 on a real tree: require its length and charset. A `postgres://user:pass@` count excludes `localhost`, `127.0.0.1` and `<placeholder>` hosts.
- **Per-fingerprint `.gitleaksignore` entries do not scale on a mock-heavy tree.** Every new mock file re-fires in CI, and a scanner that is red on every PR teaches people to merge past it. There, allow-list by **path**, scoped to the generic rule only, so that a provider-prefixed key pasted into a mock still fires. Add it to `.gitleaks.toml`; the `[[allowlists]]` table with `targetRules` is gitleaks ≥ 8.25:
  ```toml
  [extend]
  useDefault = true            # keep the default rules; this file only adds

  [[allowlists]]
  description = "Synthetic credentials in tests and mocks. Generic rule only."
  targetRules = ["generic-api-key"]
  paths = ['''(^|/)(test|tests|__tests__|e2e|__mocks__|mocks|fixtures)/''', '''\.(spec|test|e2e-spec|mock)\.[cm]?[jt]sx?$''']
  ```
  **Measured on a real repo** (a NestJS + React monorepo; gitleaks 8.30.1): together with the repo's own image-tag allow-list, this cut the tree scan from 46 hits to 7 and full history from 50 to 12. The one provider-prefixed key in a test file was still reported. Keep the allow-list narrow, as that repo's own is: one rule, a pattern, a reason in the comment. Never disable a rule to quiet a path.
- **Firebase `AIza…` keys are not secrets.** In `google-services.json`, `GoogleService-Info.plist` (`API_KEY`), a Firebase web config or a Flutter `firebase_options.dart`, the `AIza…` value identifies the project and ships in every client by design; gitleaks' `gcp-api-key` rule still matches it. Classify it as an identifier ([`precedents/mobile.md`](../../../../snippets/precedents/mobile.md) § 44): the controls are the key's API restrictions and App Check, not rotation. The exception is a **Gemini Developer API key** — an `AIza…` passed to `GenerativeModel(apiKey:)` or a Generative Language API client — which bills to the project and is critical. Allow-list a Firebase config file by path for that one rule, with the reason in the comment.
- Generated JWTs in tests look like real tokens; the body is base64 — entropy scanners flag them.
- Long config values (a 200-char URL, a lockfile integrity hash) trip entropy detection — review context.
- `git filter-repo` rewrites history — every collaborator must re-clone or hard-reset to the new history.
- "Just deleting the commit" does NOT remove the secret — it stays in the reflog, the platform's event API, forks, and others' clones until rotated. Rotation is non-negotiable.
- A secret that reached a **published build artifact** (image layer, source map, bundled config) is not fixed by scrubbing the repo — the artifact needs its own recall.

## Related

- `/secret-scan` — the remediation session: per-provider rotation playbook, four-axis classification halt, history-scrub procedure, persisted `ai/audits/` report. This skill finds and classifies; that command closes.
- `@security-auditor` — names this skill as its secrets sweep; that agent treats a `GO` emitted without it as a halt.
- `rules/security-principles.md` — the secret-management + never-log-secrets MUSTs.
