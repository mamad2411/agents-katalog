---
name: pr-raycast
description: Prepare and open a pull request to raycast/extensions. Use when the user asks to open, submit, or get ready for a Raycast Store extension PR — not for general extension coding.
---

# Raycast Extension PR

## Scope

Use when the user wants to **prepare, validate, or open a PR** to
[raycast/extensions](https://github.com/raycast/extensions).

For extension code, lint rules, and store checklist details, use **`raycast`**. For
generic `gh pr create` mechanics, use **`pr`**.

## Related skills

| Skill        | Role                                              |
| ------------ | ------------------------------------------------- |
| `raycast`    | Lint order, store checklist, code patterns        |
| `lint`       | `uv run lintro fmt/chk` (first pass)              |
| `commit`     | Signed semantic commits, history restructuring    |
| `rebase`     | Sync onto `upstream/main`                         |
| `greptile`   | Pre-push Greptile CLI (max 2 runs)                |
| `coderabbit` | Pre-push CodeRabbit CLI (max 2–3 runs)            |

## Checklist

```text
- [ ] Rebase: 0 behind upstream/main
- [ ] Validate: lintro + npm run lint/build/validate (all pass)
- [ ] Commits: signed, logical groups (see commit skill)
- [ ] Store checklist: raycast skill (icon, screenshots, CHANGELOG, lockfile)
- [ ] Greptile CLI: ≤2 runs; fix or document skips
- [ ] CodeRabbit CLI: ≤3 runs per change set; fix or document skips
- [ ] Manual smoke test: bun run dev
- [ ] Push fork → open PR → post breakdown + how-to-test comments
```

## 1. Rebase & validate

```bash
git fetch upstream && git rebase upstream/main
git rev-list --left-right --count upstream/main...HEAD   # 0 N

uv run lintro fmt && uv run lintro chk                   # repo root

cd extensions/<name>
npm run lint && npm run build && npm run validate
```

Abort on failure. Do not push until green.

## 2. Commit history

Signed (`git commit -S`), semantic, imperative. New extensions: files should be `A`,
not `M`.

Suggested order for new extensions: scaffold → lib → UI → entry point → tests → docs.

Restructure after squash:

```bash
git reset --soft upstream/main && git reset HEAD
# commit in groups; verify: git diff <squash-sha> HEAD --stat is empty
```

## 3. Pre-PR audits

**Store checklist** — full list in `raycast` skill. Spot-check:

```bash
node -e "console.log(require('./package.json').keywords.length)"  # ≤12
head -3 CHANGELOG.md                                               # {PR_MERGE_DATE}
rg 'interface Preferences' src/                                    # none
git ls-files package-lock.json 'bun.lock*' yarn.lock pnpm-lock.yaml
```

**Common Greptile findings:** manual Preferences types, shell/`AppleScript` file ops,
`unlink()` on user files, ungated debug logs, inaccurate CHANGELOG, icon invisible on
dark UI.

**Greptile CLI:** `greptile review -b main --agent` (max 2 runs).

**CodeRabbit CLI:** `coderabbit review --agent --type committed --base main` (max
2–3 runs per change set). Run parallel with Greptile when possible.

## 4. Open PR

```bash
git push -u origin HEAD

gh pr create \
  --repo raycast/extensions \
  --head <fork>:<branch> \
  --base main \
  --title "Extension Name: Brief description" \
  --body "$(cat <<'EOF'
### 🤖 Disclosure

[AI assistance disclosure + human review statement]

## Description

[One paragraph]

### Features

[User-facing bullets]

### Technical Highlights

[Architecture, test count]

## Screencast

Screenshots in `metadata/`.

## Checklist

- [x] [Prepare for Store](https://developers.raycast.com/basics/prepare-an-extension-for-store)
- [x] [Publish docs](https://developers.raycast.com/basics/publish-an-extension)
- [x] `npm run build` tested in Raycast
- [x] Assets in `assets/` are used; README media outside `metadata/`
- [x] `npm run lint` and `npm run validate` pass
EOF
)"
```

Do **not** use `gh pr create --fill`. Title: `Extension Name: Brief description`.

## 5. Post-PR comments

Add separately after opening:

1. **File breakdown** — table by category (impl, tests, images, config, docs) with counts
2. **How to test** — prerequisites, `bun run dev`, **sample data URL**, smoke-test steps

Reviewers need sample data or credentials to test — always provide one.

## Review feedback

1. `npm run validate` → signed commit → push
2. Reply on threads; re-request review if needed

Stale: 14 days idle → stale; 21 days → auto-close.
