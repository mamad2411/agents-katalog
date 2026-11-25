---
name: cve
description: >
  Research a published weakness and work out what it actually means for this system: from a
  product and version to a list of weaknesses, whether attackers are using it, whether a
  working exploit is public, whether the affected code is even reachable here, and what the
  fix is. Use when someone mentions a CVE number, asks "are we affected by", "is this
  exploitable", "what is the risk of this advisory", "our scanner flagged version X",
  "dependency alert", "patch or not", or /redteam:cve.
---

# Researching a published weakness

A version number and a weakness number are not a finding. The finding is what that weakness
allows in this system, and whether anything needs to be done this week. This skill gets you
from one to the other.

Two mistakes to avoid. Reporting a scanner's list of numbers as findings, which wastes the
client's time on components their code never calls. And dismissing something as unreachable
without checking, which leaves a real hole open.

## The order to answer the questions

**1. What exactly is affected.** Pin down the product, the version, and the way it is
deployed. Get the version from the running system where you can, and from the dependency
file where you cannot, because the two often disagree. Note whether the version is the
package version or a distribution's repackaged version, since those are numbered
differently and patched at different times.

**2. Which weaknesses are published against it.** Work through the sources in this order:

- The vendor's own security advisories, which are usually the most accurate about which
  versions are affected
- The national vulnerability database entry, for the description, the classification and the
  standard score
- The ecosystem's own advisory database for the language or package manager, which is
  usually more precise about affected version ranges than the national database
- The distribution's tracker, if the software came from an operating system repository,
  because a distribution often backports a fix without changing the version number

Where two sources disagree about affected versions, believe the vendor and the ecosystem
database over a generic entry.

**3. Is it being used by attackers right now.** Check the catalogue of weaknesses known to
be exploited in the wild, and the published likelihood-of-exploitation scoring. Something on
the exploited list moves to the top of the fix queue regardless of its score, because
somebody is already doing it.

**4. Is there a public working exploit.** Look for the original write-up, the proof
published with the advisory, and public exploit collections. Read the write-up rather than
just noting that one exists, because it tells you what conditions the exploit needs. Many
public exploits only work with a setting the client does not use.

**5. Is the affected code reachable here.** The question that changes the answer most, and
the one scanners cannot answer.

- Does the application actually call the affected function or feature? With source access,
  search for the calls. Without it, work from what the application does.
- Is the vulnerable feature switched on in this configuration?
- Can untrusted input get to it, and from where? A weakness reachable only by an
  administrator is a different problem from one reachable by a stranger.
- Is there something in front that already blocks the route?

Write down which of these you checked and how. This is the reasoning the client will
question, and it is what makes the finding defensible.

**6. What the fix is.** One of: upgrade to a version, apply a vendor patch, change a
setting, remove the component, or rebuild an image so it picks up a patched base. Say which,
and give the specific version or setting. If upgrading is not realistic this quarter, go to
`../backport/SKILL.md`.

**7. Confirm it, if the rules of the test allow.** A safe check that the weakness is
genuinely present beats a version number every time. `../poc/SKILL.md` covers doing that
without breaking anything.

## Writing it up

One finding per weakness that actually matters here, not one per scanner row.

Each one needs: the number, the affected component and version, what it allows in plain
words, whether it is reachable here and how you established that, whether it is known to be
exploited, the standard score alongside your own rating with reasoning, and the specific
fix. Use `../triage/SKILL.md` for the rating and
`../../templates/finding.md` for the shape.

Group the ones that do not matter here into a single short section that says they were
reviewed and why they were set aside. Naming them stops the client's own scanner starting an
argument later.

## What changes with your access level

Outside only: you are guessing at versions from what the server volunteers, and you cannot
answer the reachability question properly. Say the version is unconfirmed and rate it as
suspected rather than confirmed.

Part access: you can often confirm versions through the application's own behaviour, and you
can test whether the feature is exposed.

Full access: you get the real dependency tree and you can answer reachability by searching
for the calls. Do that before rating anything, because it frequently turns a severe-looking
number into a low-priority item, and occasionally the other way round.

## Helper

`../../scripts/cve-lookup.py` takes a product and version and returns published weaknesses
from the public databases. It is a starting point for step 2, not a substitute for steps 3
to 6.
