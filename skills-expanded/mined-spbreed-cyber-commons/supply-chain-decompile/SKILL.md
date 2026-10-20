---
name: supply-chain-decompile
description: >-
  Scan an SBOM for known vulnerabilities, reconcile it against what is actually
  on disk, and decompile the dependency that no manifest declares. Use when a
  dependency scan comes back clean, when a third party ships a binary bundle,
  or when asked what a closed-source library in the build actually does.
allowed-tools: Read, Glob, Grep, Bash
---

# What is in the build that the manifest never mentioned?

Dependency scanning answers one question well: *are any of the components I
declared known to be vulnerable?* Both halves of that sentence are limits. It
sees only what was **declared**, and only what is **already published** as an
advisory.

A vendor's integration bundle drops a jar into `lib/`. It is in no manifest,
so it is in no SBOM, so no scanner has an identifier to look up and the report
comes back clean. The clean report is accurate and it is about the manifest,
not about the build.

The step past that is unglamorous and mechanical: **reconcile the SBOM against
the filesystem**, and for anything on disk with no manifest entry, read the
artefact itself. Compiled code carries its strings, its class references and
its method references in a structured table, and recovering them needs no
vendor cooperation and no source.

## When to use this

When any third party ships compiled artefacts into your build — SDKs,
integration bundles, agent plugins, MCP server distributions. Also whenever a
dependency scan is clean on a system that has never had a clean anything, which
usually means the scanner is reading a manifest that stopped describing the
build some time ago.

## Procedure

**1 — Scan what was declared.** Parse the SBOM, match every component against
an advisory feed on `(package, version)` with a real range comparison, and
report each hit with the fixed version. This is the part existing tools do, and
it is worth doing first so the gap that follows is visible against it.

**2 — Reconcile against the filesystem.** List what is actually present in the
built image and diff it against the SBOM's components. Two directions, and both
are findings: **on disk, not in the SBOM** is undeclared code, and **in the
SBOM, not on disk** means the SBOM describes a different build.

**3 — For undeclared artefacts, read the artefact.** No source, no manifest, no
identifier to look up. A compiled class file carries a constant pool: every
string literal, every class it references, every method it calls, in a
documented table before any bytecode. Parse it — the format is stable and the
parser is about forty lines.

**4 — Read the recovered strings and calls as a capability claim.** A URL and
an HTTP client class in the same artefact is an egress capability. A crypto
class beside them tells you what the traffic will look like on the wire. Report
the capability, which is provable from the constant pool, rather than the
intent, which is not.

**5 — Say plainly what the scan could and could not have found.** An
undeclared artefact has no CVE because it has no identifier, not because it is
safe. Those two produce identical output on a dependency report, and only one
of them is a reason to relax.

## Example

**Input** — the fixture committed at the top of [`scripts/supply_chain_decompile.py`](scripts/supply_chain_decompile.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
SBOM: cybertravels-booking 4.7.1 · 5 declared components

   CRITICAL org.apache.commons/commons-text 1.9     GHSA-599f-7c49-w659
             Variable interpolation permits script execution (Text4Shell)  -> fixed in 1.10.0
   HIGH     pyyaml 5.3.1   GHSA-8q59-q68h-6hv4
             Arbitrary code execution via full_load / FullLoader  -> fixed in 5.4
   MEDIUM   requests 2.31.0  GHSA-h5c8-rqwp-cp95
             Proxy-Authorization header leaked on redirect  -> fixed in 2.32.0
```

The run continues past this. `test_skills.py` executes the script on every
build, **with no model configured** — so what CI proves is that it runs and
refuses legibly, not that it prints these lines. The output above is a recorded
run against a real model, and nothing re-diffs it: a model's answer is not
reproducible, and this repository does not claim otherwise anywhere it can be
checked.

## Output contract

```json
{
  "sbom": {"components": 0, "vulnerable": 0},
  "advisories": [{"package": "str", "version": "str", "id": "str",
                  "severity": "str", "fixed": "str"}],
  "reconciliation": {"undeclared_on_disk": ["str"], "declared_not_present": ["str"]},
  "decompiled": [{"artefact": "str", "strings": ["str"], "classes": ["str"],
                  "capabilities": ["str"]}],
  "unassessable_by_sbom": 0
}
```

`unassessable_by_sbom` is the number this whole procedure exists to produce. A
report where it is absent has quietly claimed that undeclared code is
vulnerability-free.

## Failure modes

- **Comparing versions as strings.** `1.9 < 1.10` is false lexically and true
  in every version scheme in use. It silently drops the finding.
- **Treating "no advisory" as "no vulnerability".** It means nobody has
  published one against that identifier, and an undeclared artefact has no
  identifier at all.
- **Reconciling in one direction.** Components in the SBOM that are not on disk
  are the same defect seen from the other side: the manifest and the build have
  diverged.
- **Reporting intent from strings.** The constant pool proves an endpoint and a
  client class are present. It does not prove what is sent, and a report that
  says "exfiltrates PII" on that evidence will be dismissed along with the real
  finding next to it.
