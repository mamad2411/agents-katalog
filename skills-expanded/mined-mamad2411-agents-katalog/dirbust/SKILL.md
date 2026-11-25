---
name: dirbust
description: Recursive web directory and file brute-forcing (content discovery) for authorized pentesting and CTF. Use after finding an http/https service to discover hidden paths, admin panels, backups, and API routes. Triggers on "dirbust", "directory brute", "content discovery", "find hidden directories/files", "gobuster dir", "fuzz paths/endpoints".
---

# Directory & content discovery

Recursive content discovery against an authorized web service, driven by
`./roo dirbust` (gobuster + baked SecLists wordlists). gobuster has no
native recursion — `roo` drives it breadth-first, re-running `dir` on each
directory it finds, and streams every hit to the CLI as it lands.

## Scope guardrail

Authorized targets only — CTF boxes, lab ranges, or signed-scope hosts. Confirm
scope before brute-forcing. This is active, noisy traffic.

## When to use

After a buckaroo identifies an http/https port (see the **recon** skill). Resolve
any hostname the box reveals into `./hosts` first and dirbust the *name*, not the
bare IP — vhosts serve different content.

## Run it

```bash
./roo dirbust http://box.htb/                 # VPN: prefix ROO_NET=container:roorecon-vpn
./roo dirbust http://box.htb/app/ --depth 2   # start under a subpath
```

Output: `recon-results/<host>/dirbust.txt` (`status<TAB>url`) and `dirbust.log`
(full gobuster output per level). Hits also stream live — act on them as they
appear; don't wait for completion.

Options:
- `--wordlist <name>` — baked: `common.txt` (default, ~4700, recursion-friendly),
  `raft-medium-directories.txt`, `DirBuster-2007_directory-list-2.3-medium.txt`,
  `DirBuster-2007_directory-list-2.3-big.txt` (thorough, slow). Or a `/wordlists`
  path / host file. **Recursion multiplies requests** — keep the default for deep
  runs; reserve big lists for `--depth 0` (single level).
- `--depth N` — recursion depth (default 2; `0` = no recursion).
- `--ext php,txt,html` — also try these file extensions per word.
- `--threads N` (default 40), `--max-dirs N` (default 60, hard recursion cap;
  roo logs when it's hit so truncation is never silent).
- `--skip a,b,c` — extra directory names to record but not descend into (added
  to the built-in asset/noise list).

## Recurse intelligently — probe where it pays, skip the noise

`roo` only descends into hits that look like real directories, and skips the dead
ends, so requests go where findings live:

- **Descend on a real-directory signal.** A trailing-slash redirect
  (`[--> .../path/]`) is the reliable one; absent that, an extensionless
  `2xx`/`403` is a directory candidate. Files (anything with an extension) and
  plain redirects elsewhere (e.g. `/dashboard → /login` auth gates) are recorded
  but never followed.
- **Don't recurse into asset trees.** `css/`, `js/`, `images/`, `fonts/`,
  `static/`, `assets/`, `vendor/`, `node_modules/` and friends are skipped by
  default — busting them burns thousands of requests for nothing. Add app-specific
  noise with `--skip` (e.g. `--skip docs,thumbnails`).
- **Steer by what you learn, not brute depth.** Recursion is multiplicative, so a
  big list at `--depth 2` explodes. Prefer a shallow first pass (`--depth 1`,
  `common.txt`), then *manually* deepen the dirs that matter — `admin`, `api`,
  `backup`, `dev`, `uploads`, `.git`, anything `403` — by re-running on that
  subpath with `--depth 0 --wordlist DirBuster-2007_directory-list-2.3-big.txt`.
  A 200 listing or a `403` is worth a deep dig; a static dir is not.

## Interpreting hits

- `200` → live content; fetch it (`./roo shell curl …`) and read it.
- `403` → exists but forbidden; try bypasses, or dirbust *into* it for children.
- `301/302` → follow the target; trailing-slash redirects are real dirs.
- `401` → auth-protected; note for credential reuse.

## Notes for the operator

- Enumeration, not exploitation — produces a map of reachable paths; the operator
  approves what to attack.
- Tools run only in containers (no host fallback). First run builds the gobuster
  image (downloads the wordlists). Surface build/Docker errors; don't fall back
  to a host binary.
