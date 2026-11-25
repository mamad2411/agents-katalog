---
name: rnd-cli
description: Use the `rnd` CLI to query the React Native Directory (~2400 packages) for package facts — maintenance status, new-arch support, TypeScript types, GitHub activity, alternatives, and project audits. Invoke whenever the user mentions React Native or Expo packages, asks whether a library is maintained, wants a replacement / alternative for an RN library, audits their React Native project's deps, compares two RN packages, or discusses New Architecture / Fabric / Turbo Modules / Expo Modules compatibility. Also trigger when reviewing React Native code and you need to verify a package's health or find something better — even if the user doesn't explicitly say "check the directory." This CLI emits facts only, never opinions; reason about them yourself.
---

# rnd — React Native Directory CLI

`rnd` is a Rust CLI that queries [reactnative.directory](https://reactnative.directory) and scans React Native codebases. It's designed for AI agents: it auto-emits JSON inside `CLAUDECODE` / `CODEX` / `CODEX_CI` environments and emits only **facts** (never curated opinions) so the agent can reason about what to do.

## When to reach for this skill

- User asks: "is X maintained?", "what's better than X?", "should I use A or B?"
- User mentions a React Native library by name and you need to verify its health
- User is auditing, upgrading, or migrating an RN project
- User talks about New Architecture / Fabric / Turbo Modules / Expo Modules
- You're reviewing RN code and spot a dep you want to check before recommending changes
- User has a `package.json` with React Native deps and asks for feedback

Do NOT use for: pure web projects, non-RN npm packages (unless the user is asking about them in an RN context), or general JavaScript ecosystem questions.

## Check installation first

The binary is usually on `$PATH` as `rnd`. Before invoking, check:

```bash
command -v rnd
```

If missing, tell the user:

> The `rnd` CLI isn't installed. Install it with:
> ```
> cargo install --path /Users/galhavkin/Desktop/react-native-directory-cli
> ```
> Or use the release binary at `/Users/galhavkin/Desktop/react-native-directory-cli/target/release/rnd`.

Do not attempt `cargo install` yourself — that's a user decision.

## Core commands

| Command | Purpose |
|---|---|
| `rnd search <query>` | Find packages by name/description/topic |
| `rnd info <pkg>` | Detailed facts on one package |
| `rnd alternatives <pkg>` | Candidate replacements (tagged by how they matched) |
| `rnd trending` | Top packages by weekly downloads — **native-only by default** |
| `rnd discover` | Actively-maintained, highly-rated native packages (score ≥70, pushed in last 90 days) |
| `rnd list --category X --platform Y --new-arch` | Filter packages |
| `rnd compare <a> <b>` | Side-by-side comparison of two packages |
| `rnd analyze [path]` | Scan a project's `package.json` + source for facts |
| `rnd cache info` / `rnd cache clear` | Manage the 24h-TTL directory cache |

### `trending` vs `discover` — which to use

- **`rnd trending`** — raw download leaders. Use when you want to know "what's everyone installing?" Defaults to native-only; pass `--include-js` if the user explicitly wants pure-JS libs (semver, lodash, zod) in the results.
- **`rnd discover`** — quality-curated. Use when the user wants to find **quietly great** libraries they might not have heard of. Filters by directory score + recent push + native code. Tunable via `--min-score <0-100>` (default 70) and `--days <N>` (default 90).

## Global flags worth knowing

- `--json` — force JSON (auto-on inside `CLAUDECODE`/`CODEX`, so usually not needed)
- `--pretty` — force pretty output (for humans, or when capturing readable text)
- `--refresh` — bypass the 24h cache and hit the API fresh
- `--quiet` — suppress non-essential output (useful in CI)

## Interpreting `analyze` output

`rnd analyze .` scans the project root and emits per-flagged-dep facts. Each `PackageFinding` JSON has:

- `flags` — one or more of: `archived`, `unmaintained`, `no new-arch support`, `no TypeScript types`
- `in_directory` — whether the dep is indexed by reactnative.directory
- `github_url` — go read the repo if you need context
- `license`, `latest_release`, `latest_release_date`, `last_pushed_at` — activity signals
- `stars`, `weekly_downloads`, `directory_score`, `topics` — raw metadata
- `has_native_code`, `has_types`, `new_architecture` — authoritative booleans
- `used_in` — every `file:line` in the project that imports this package
- **`alternatives_in_project`** — packages **already present in the user's `package.json`** that the algorithm identified as plausible alternatives for the flagged dep. **This is the highest-value field.** If populated, it means the user can likely drop the flagged dep and reuse something they already have (e.g. `react-native-easing-gradient` → `alternatives_in_project: ["expo-linear-gradient"]`).

**Severity heuristic the agent should use** (not enforced by the CLI):

| Flags contain | Treat as | Action |
|---|---|---|
| `archived` or `unmaintained` | Red — usually worth replacing | Run `rnd alternatives <pkg>` |
| `no new-arch support` + `has_native_code` | Yellow — relevant only if the project is migrating to New Arch | Check if user cares about New Arch |
| `no TypeScript types` + native code | Minor — types via `@types/*` often exist | Usually fine |
| flag appears but package is pure-JS (zod, tailwindcss, etc.) | The CLI already skips flagging JS libs for new-arch/types. If you see these flags, trust the CLI — they're real. |

## Interpreting `alternatives` output

Each candidate has a `_match` tag (JSON) or visible `[tag]` (pretty):

| Tag | Meaning | Signal strength |
|---|---|---|
| `[directory]` | The directory API's own curated `alternatives[]` field — maintainer-curated | Strongest — treat as authoritative pointer |
| `[topic]` | GitHub topic Jaccard overlap after stopword filter | Strong for well-tagged libs |
| `[name]` | Package name token overlap (e.g. `masked-view` → other `*-view` libs) | Medium — useful for niche libs with poor topics |
| `[desc]` | Description keyword overlap with stemming | Weakest — can include loosely-related libs |

Hard filters always apply: candidates must match the target on `hasNativeCode`, must not be archived/unmaintained. This means `[desc]` matches for an animation library won't surface random state-management libs.

## Canonical workflows

### 1. User asks "is X maintained?" or "what's X like?"

```bash
rnd info X
```

Then check `flags`, `last_pushed_at`, `latest_release_date`, `directory_score`. Decide and explain to the user.

### 2. User asks "what's a better X?" / "alternative to X?"

```bash
rnd info X              # first understand what X is
rnd alternatives X      # then surface candidates
```

Read candidates in order. `[directory]` matches are the strongest signal. If only `[desc]` results appear, be cautious — they may be loosely related. **Never parrot a suggestion without explaining the trade-offs.** The CLI gave you facts; you weigh them.

### 3. User wants to audit a React Native project

```bash
rnd analyze <project-path>
```

For each flagged package:

1. **Check `alternatives_in_project` first.** If populated, the user already has a package that can cover this use case — recommend reusing it and dropping the flagged dep (e.g., `easing-gradient` → they already have `expo-linear-gradient`). This is the fastest win and avoids adding new deps.
2. If `alternatives_in_project` is empty and the flag is `archived`/`unmaintained`, run `rnd alternatives <pkg>` to find candidates.
3. If the flag is only `no new-arch support` and the user isn't actively migrating to New Arch, note it but don't push a replacement.
4. Always show file:line locations from `used_in` so the user can find the code.

### 6. User asks "what are the best RN packages for X?" / discovery

```bash
rnd discover --limit 20
# or filtered
rnd list --category camera --new-arch
rnd search "<topic>" --limit 10
```

Use `discover` when the user wants "what's actually good right now?" — it surfaces well-rated, active native packages. Use `list`/`search` when they have a specific category in mind.

### 4. User is picking between two known packages

```bash
rnd compare A B
```

Tells you stars, downloads, platforms, new-arch status — factually. Interpretation ("A has 5x the downloads so it's more established") is yours.

### 5. User wants to find something new for a category

```bash
rnd search "navigation" --limit 10
rnd list --category storage --new-arch
rnd trending --limit 20
```

## Design principle — why this matters

`rnd` intentionally emits **no opinions**. No "you should use MMKV." No "expo-image is better than fast-image." No scores or rankings beyond what the directory itself publishes.

This is because **you, the agent, are better at reasoning about current library trade-offs than any hardcoded registry.** Popularity numbers lag quality (a newer, better lib always has fewer downloads at first). Hardcoded swaps rot. You have fresher training and can weigh the user's specific project context.

So: the CLI gives you ground truth about the codebase and the directory. You decide what to do.

## When facts conflict with your prior belief

If the CLI says a package is `unmaintained` but you're sure it's fine, **trust the CLI over your training data**. The directory's maintenance flag comes from live metadata (last push date, archived status, maintainer declarations). Your training data may be 6-12 months stale.

Conversely, if the CLI surfaces a `[desc]`-tagged alternative that you know is wrong or irrelevant, you can confidently skip it. `[desc]` matches are acknowledged to be weaker.

## Common pitfalls to avoid

- **Don't re-run `--refresh` repeatedly.** The 24h cache exists so you don't hammer the API. Only use `--refresh` if the user is actively debugging data freshness.
- **Don't use `--json` in a CLAUDECODE session** — JSON is already the default there. Adding it is redundant.
- **Don't propose swaps for packages flagged only with `no TypeScript types`** unless the user cares. It's a minor flag.
- **Don't invent facts the CLI didn't give you.** If you need specific info (changelog, bundle size), say so — don't fabricate.
- **Don't call `rnd` for non-RN packages unless the user clearly asks.** Our directory is RN/Expo-specific.

## Output to the user

When relaying CLI results:

1. **Lead with the verdict**, not the data dump. "Yes, it's maintained" → then supporting facts.
2. **Cite the file:line** when a dep is flagged and you want the user to take action.
3. **Name the match tier** when recommending an alternative — "the directory itself points to X" (`[directory]`) carries more weight than "description mentions animation" (`[desc]`).
4. **Say what you'd do** if the user asks, but explain the trade-off so they can override you.
