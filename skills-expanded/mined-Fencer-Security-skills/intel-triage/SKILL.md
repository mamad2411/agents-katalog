---
name: intel-triage
description: Triage a CVE, GHSA, or OSV id against the public Fencer Intel feed. Use when the user asks how severe a vulnerability is, whether it is in CISA KEV, what its EPSS score is, or which version fixes it. Pulls the record, KEV status, EPSS, severity, public exploits, and fixed versions, then gives a short priority. Cites https://intel.fencer.dev/<id> and says the feed has no entry instead of inventing one.
allowed-tools: Read
---

# Triage a vulnerability

Answer one question: given this id, what does Fencer Intel say, and how soon should someone patch?

## Before the lookup

Read the shared contract. From this skill's directory:

```bash
SKILL_DIR="${CLAUDE_SKILL_DIR:-${SKILL_DIR}}"
```

Read `$SKILL_DIR/../../shared/references/using-intel.md` in full. Follow it for the tool arguments,
the empty-result rule, distros that must not be displayed, and the Sources paragraph. If that file
is not on disk, use only the `fencer-intel` MCP tools (or the public GET endpoints named there) and
still end with the NVD sentence: "This product uses data from the NVD API but is not endorsed or
certified by the NVD."

## Steps

1. Take the id the user gave (CVE, GHSA, OSV, or an alias). If they gave several, triage each one.
   If they gave none, ask which id.
2. Call `get_vulnerability` with `{ "id": "<the id>" }`.
3. If the tool returns an error that Intel has no entry, call `search` once with `q` set to that
   exact id and `limit` 5. Use a returned row only when its id or aliases are the id the user
   asked about. If nothing matches, say Fencer Intel has no entry for that id and stop. Do not
   describe the vulnerability from memory.
4. Read the fields the tool returned. Do not add scores, dates, packages, or exploits that are
   absent.

## Priority

Apply the first matching row. Use only fields from this lookup.

| What the entry shows                                                         | Priority                                                                                          |
| ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| `withdrawn` is set                                                           | Withdrawn. Say the record is withdrawn or rejected. A patch recommendation does not apply.        |
| `kev` is set, or `ssvc.exploitation` is `active`, or `exploits` is non-empty | Patch now. It is in CISA KEV, CISA calls exploitation active, or the feed lists a public exploit. |
| `epss.score` >= 0.1, or `severity` is `critical`, or `critical` is true      | High. Patch in the current cycle.                                                                 |
| `severity` is `high`                                                         | Soon. Schedule the fixed version.                                                                 |
| Anything else                                                                | Track. Take the fix when convenient. The feed does not show active exploitation.                  |

Name the fixed versions from `fixes.versions`, `packages[].fixed`, and `fixes.distros`. If none of
those are present, say the feed does not list a fix. When Ubuntu, Alpine, or Azure Linux fixes are
shown, include the license line from the shared reference. The priority is a reading of these
fields, not a judgement of how exposed the user's own systems are.

## Answer

Lead with the priority and the canonical link. Then the evidence, then Sources.

```markdown
**<priority>** — [<id>](https://intel.fencer.dev/<id>)

- Severity: <severity>, CVSS <score> — omit the score when the entry has none
- CISA KEV: added <kev.added>, or "not in KEV". Quote `kev.action` when it is present.
- EPSS: <score> (percentile <percentile>), or "no EPSS returned"
- Public exploits: the links returned, or "none returned"
- Fix: the versions and links returned, or "the feed does not list a fix"
- Distro fixes, ATT&CK, ransomware groups, and vendor advisories only when the entry includes them, each with its license or credit object

Sources
<the Sources paragraph from using-intel.md>
```

Fill every angle-bracket from the entry. Leave a line out rather than writing a value the entry
does not have.

Keep the user's alias in the first line when it differs from the canonical id ("GHSA-… is
CVE-…"). Mention a maintainer advisory is unreviewed, and an inferred package is only probable,
when those flags are set.

Do not recommend a compensating control you did not read off the entry. The KEV `action` field is
the exception: quote it when it is present.
