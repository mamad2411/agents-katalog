---
name: pushing-taubyte-projects
description: Pushes Taubyte project changes via `tau push` — `tau push project [--config-only|--code-only]`, `tau push website <name>`, and `tau push library <name>` — with the rule that `--message` is required when `--defaults` is set, and the push-config-before-code ordering for resource-dependent changes. Also explains the `tau pull` "already up-to-date" non-zero-exit quirk. Use when pushing local changes to GitHub through `tau` (instead of raw `git push`), or when triggering remote-cloud webhooks / Dream injects after edits.
---

# Pushing Taubyte Projects

## When to use

- "Push my project / website / library to the cloud"
- After editing config (resources) or code (function source)
- Before a `dream inject` cycle on Dream local
- `tau push` fails with `Commit Message: is required ... required value missing`

## Mental model

`tau push` wraps `git add -A && git commit -m <msg> && git push` for the relevant repo, then optionally signals the cloud. **GitHub remains the source of truth**; `tau push` is a convenience over raw git, plus it knows about the `--config-only` / `--code-only` split for the project's two repos.

## The `--message` rule

When invoked with `--defaults`, `tau push` will **not** prompt for a commit message. You **must** pass `--message <msg>` (or `-m <msg>`) explicitly, or you'll see:

```
Commit Message: is required ... required value missing
```

Always include `-m`. Example template:

```bash
tau --defaults --yes push <subcommand> -m "<commit message>"
```

## Project pushes

### Both config + code

```bash
tau --defaults --yes push project -m "<message>"
```

### Config only (recommended after resource changes)

```bash
tau --defaults --yes push project --config-only -m "<message>"
```

### Code only (recommended after function source changes)

```bash
tau --defaults --yes push project --code-only -m "<message>"
```

## Website / library pushes

Each website and library lives in its own repo, so each gets its own push:

```bash
tau --defaults --yes push website <site_name>   -m "<message>"
tau --defaults --yes push library <lib_name>    -m "<message>"
```

### Remote-cloud note (registration + hooks)

On remote clouds, a website/library repo may need to be **imported/registered** on that cloud before pushes reliably trigger builds:

```bash
tau --defaults --yes import website <site_name>
tau --defaults --yes import library <lib_name>
```

If builds are "silent" after pushes, check GitHub webhooks. Repeated imports can create **duplicate webhooks**; if needed, delete all hooks on the repo and re-import once to recreate a single clean hook.

## Push ordering rule

When you've added or edited resources, **push config first** and wait for the cloud's config build to succeed before pushing website/library code that depends on those resources. Otherwise the website/library build can fail with "resource not found" or build into a stale config.

```
Ordered push progress:
- [ ] tau push project --config-only -m "add <resources>"
- [ ] Wait for the config build to complete (success or fail)
- [ ] If failed, fix config and re-push before continuing
- [ ] tau push project --code-only -m "..."   (if code changed)
- [ ] tau push website <site> -m "..."        (if site changed)
- [ ] tau push library <lib> -m "..."         (if lib changed)
```

For Dream local, follow each push with the appropriate `dream inject` — see [triggering-dream-builds](../triggering-dream-builds/SKILL.md).

## Pulling (sibling command)

```bash
tau --defaults --yes pull project
tau --defaults --yes pull project --config-only
tau --defaults --yes pull project --code-only
tau --defaults --yes pull website <site_name>
tau --defaults --yes pull library  <lib_name>
```

**Quirk**: `tau pull project` (and friends) can print `already up-to-date` and **exit non-zero**. In git terms this is success; treat it as a CLI-output quirk, not an error. Don't gate retries on the exit code alone — read the message **and** confirm with **`git fetch` + `git status`** in **`config/`** / **`code/`** (or the website repo) that you really are aligned with **`origin`**.

### Remote: “site down” but APIs work

If **`GET https://<fqdn>/`** fails with **no HTTP match for `GET` / 500** but **`GET https://<fqdn>/api/...`** returns **200**, the **HTTPS functions** deployed from the **code** repo — the **website** repo did not publish a static **`AssetCid`**. Fix with **`tau push website <site_resource_name>`** and verify **`tau query builds`** includes a job for the **`tb_code_…_<site>`** repository with **`AssetCid`** populated (see [deploying-to-remote-clouds](../deploying-to-remote-clouds/SKILL.md)).

## Common failure → recovery

| Symptom | Recovery |
| --- | --- |
| `GET /` fails on remote but `/api/...` works | **`tau push website <site>`**; confirm website-repo job + **`AssetCid`** in **`tau query builds --json`** (functions can work while static `/` has no artifact yet) |
| `Commit Message: is required ...` | Add `-m "<msg>"` |
| `unknown cloud` on push | Re-select cloud, retry: `tau --defaults --yes select cloud --universe <u>` (or `--fqdn <fqdn>`) → push again |
| Push reports success but cloud doesn't see changes (Dream) | Run the appropriate `dream inject push-all` (bootstrap) or `push-specific` |
| `project ids not equal <patrick> != <yaml>` | Update `config/config.yaml` `id:` to the cloud canonical project id, then re-push |
| `tau push website` not available / errors out | Fall back to plain `git push` from the website repo (only for website/library, never for project config/code) |

## Don't bypass with raw git

For the **project config and code repos**, never bypass a failing `tau push project` with raw `git push` — `tau` may need to write metadata or sync with the cloud. Fix the underlying error.

For **website and library repos**, raw `git push` is an acceptable fallback when `tau push website|library` is unavailable in your CLI version.

## Gotchas

- **`--defaults` removes prompts but adds the `-m` requirement** — they go together.
- **Don't trust `tau pull`'s exit code alone** for the "already up-to-date" case.
- **Push order matters** for resource-dependent code; otherwise a website build can fail because the new domain/database isn't yet in cloud config.
- **For non-interactive automation** every `tau push` invocation must include both `--defaults --yes` and `-m`.
- **Dream inject requires a real `HEAD`.** If the project `code/` repo branch exists but has **no commits**, Dream inject can fail with `getting HEAD ... reference not found`. Create a minimal initial commit and `tau push project --code-only -m "init"` before bootstrapping Dream.

## Related skills

- `bootstrapping-taubyte-projects`
- `selecting-taubyte-context`
- `creating-taubyte-resources`
- `triggering-dream-builds`
- `diagnosing-dream-builds`
