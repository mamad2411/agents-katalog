---
name: intel-check-deps
description: Look up known vulnerabilities and fixed versions for a package list, lockfile excerpt, or SBOM on the public Fencer Intel feed. Use when the user pastes dependencies, a lockfile, or an SBOM and asks which vulns affect those versions or what to upgrade to. Sends that list to https://intel.fencer.dev. This is a feed lookup, not a full scanner. Cites https://intel.fencer.dev/<id> and reports an empty result when the feed returns no matches.
allowed-tools: Read
---

# Check dependencies against the public feed

This skill answers: for these exact versions, which entries does Fencer Intel already list, and
which versions does it say fix them?

It is a lookup. It does not build a call graph, check reachability, run a registry, or scan a host.
A package with no match is not certified safe.

## Before the lookup

```bash
SKILL_DIR="${CLAUDE_SKILL_DIR:-${SKILL_DIR}}"
```

Read `$SKILL_DIR/../../shared/references/using-intel.md` in full and follow it. In particular:
do not invent matches, do not display the distros the public feed excludes, do not POST the
lockfile to the stored-report endpoint unless the user asks for a public report, and end with the
Sources paragraph.

`check_stack` sends the lockfile, SBOM, or package list to https://intel.fencer.dev. The call
does not store a public report. Say that once, before the first call. A file read from the
workspace is sent only when the user asked for this lookup.

## Input

Accept whichever the user gave:

- A lockfile or SBOM pasted as text, with its filename (`package-lock.json`, `uv.lock`,
  `Cargo.lock`, a CycloneDX / SPDX / Syft JSON name, a GitHub Actions workflow, `action.yml`, …).
- A list of exact versions: ecosystem, name, and version (`npm` `lodash` `4.17.20`).

If they named a package without a version, say exact matching needs a version and offer
`intel-triage` or a `search` by `package` name instead. Do not guess the version from the
workspace unless they asked you to read a lockfile, and then pass that file's text through.

OS packages (deb, apk, rpm, Arch alpm) are checked only when they arrive inside an SBOM. Do not
invent a distro advisory for a bare package name.

## Steps

1. Call `check_stack`. Pass `lockfile` and `filename`, or pass `packages`. Do not pass both a
   file and a package list unless the user asked for both.
2. If the MCP tool is not connected, stop after the install hint in the shared reference. Do not
   upload the file.
3. Read `findings`, `os`, `unchecked`, `eol`, and `other` from the result. Ignore keys you were
   not given.
4. For a finding you are going to describe beyond id, severity, and the fixed version in the
   stack result, call `get_vulnerability` for that id. That is where KEV detail, EPSS, distro
   `license` objects, and `credit` objects live. Skip the extra call when the stack row is enough
   and the user only asked for a list.

## Answer

State up front that this is a Fencer Intel lookup of the versions they supplied, not a scan.

Sort language findings in this order, and keep the tool's order inside a group. A stack finding
carries `kev` as the date added when the entry is in CISA KEV, and `epss` as a number. It does not
carry the exploit list; do not claim a public exploit unless `get_vulnerability` returned one.

1. `kev` is set
2. `critical` is true, or `epss` >= 0.1, or `severity` is `critical`
3. `severity` is `high`
4. the rest

For each finding:

- Link the canonical id to `https://intel.fencer.dev/<id>`.
- Show the package name and version that matched, and the `fixed` versions returned.
- If `unreviewed` is true, say GitHub has not reviewed it.
- If `inferred` is true, say the package is only probable.

Then, when those arrays are non-empty:

- **OS packages** — distro, package, installed version, fixed version. Arch rows with
  `possible: true` are "may be affected". Ubuntu, Alpine, and Azure Linux rows get the license
  line from the shared reference.
- **Not checked** — the package, version, and `reason`. Do not turn these into findings.
- **Out of support** — the `eol` rows, with the endoflife.date link returned. Separate from vulns.
- **Other ids** — mostly malicious-package ids that are not Intel entries. List the ids returned
  and do not describe them further.

If `findings` and `os` are both empty, say the feed returned no matches for these versions. Repeat
that this is not a safety verdict. Still include unchecked, eol, and other rows when they exist.

Close with the `feed` URL from the result when the tool returned one, and the Sources paragraph.

An upgrade suggestion may name only a version the tool listed.
