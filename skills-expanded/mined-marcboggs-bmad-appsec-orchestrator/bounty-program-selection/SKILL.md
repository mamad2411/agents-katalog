---
name: bounty-program-selection
description: "Bug bounty program selection and portfolio strategy — the economics layer that sits BEFORE hunting. Evaluates programs across platforms (HackerOne, Bugcrowd, Intigriti, YesWeHack, Immunefi/web3, independent/self-hosted) on scope width, payout history, triage quality, competition density, and tech-stack fit. Builds a 5–6 program portfolio balanced for ROI. Use when choosing which program to hunt on, when deciding whether to stay or leave a program, when evaluating a new private invite, when building a hunting schedule, or when asking 'is this program worth my time?' Pairs with bb-methodology (session orchestration), recon-scope-triage (asset ownership), and feature-driven-testing (feature-first hunting). Also covers VDP economics, platform reputation mechanics, and the walk-away checklist."
---

# Bounty Program Selection

Your time is the scarce resource. This skill decides **where** to spend it —
before `bb-methodology` decides **how** and `feature-driven-testing` decides
**what to probe**.

---

## PART 0: The core economics

1. **Time-on-program compounds.** Months on one target beat weeks on ten.
   Deep familiarity — the codebase's patterns, the team's patch style, the
   deploy cadence — yields bugs that surface scanners can't reach. Resist the
   urge to hop after a dry week.

2. **Wide scope > high bounty.** A program with `*.target.com` in scope and
   moderate payouts will produce more findings than a single-domain program
   with a $50k top bounty. Scope width is the multiplier on your methodology.

3. **Risk vs. reward is per-hour, not per-bug.** A $500 XSS on a program
   that triages in 2 days and pays in 30 is worth more than a $2,000 XSS on
   a program that triages in 90 days and disputes half your reports.

4. **Portfolio, not lottery.** Maintain 5–6 active programs. Rotate attention
   based on deploy cycles and scope changes, not boredom.

---

## PART 1: Platform landscape

| Platform | Strength | Watch out for |
|---|---|---|
| **HackerOne** | Largest program count; reputation system unlocks private invites; structured scope/policy; Hacktivity for prior-art research | Reputation grind can incentivize volume over quality; some programs use managed triage (slower, less technical) |
| **Bugcrowd** | Curated programs; researcher-friendly triage on many programs; P1–P4 taxonomy standardized | Smaller public program pool; VRT sometimes disagrees with your severity assessment |
| **Intigriti** | Strong European program presence; researcher leaderboard; good triage SLAs on most programs | Smaller overall; fewer private invites if you're starting out |
| **YesWeHack** | European/APAC programs not on other platforms; some government programs | Smaller community; fewer disclosed reports for prior-art research |
| **Immunefi** | Web3/DeFi/smart-contract bounties; highest single-bounty payouts in the industry ($M range) | Requires smart-contract/blockchain expertise; findings are often all-or-nothing (Critical or nothing); protocol teams vary wildly in responsiveness |
| **Independent / self-hosted** | Google dorking (`"responsible disclosure" OR "vulnerability disclosure" OR "bug bounty" inurl:security`) finds programs not on platforms; less competition | No platform mediation if the team ghosts you; no reputation system; verify legal safe harbor before testing |

### Platform reputation mechanics

- **HackerOne:** Signal + Impact + Reputation. Signal is your valid:invalid
  ratio — protect it. A single N/A on a marginal report costs more reputation
  than the potential bounty is worth. Impact rewards chains and Criticals.
  Reputation unlocks private invites at thresholds (~100+ signal, varies).
- **Bugcrowd:** Accuracy + Priority. Similar economics — don't submit
  informational findings on paying programs.
- **Intigriti:** Leaderboard points. Monthly/quarterly competitions can boost
  visibility.
- **General rule:** On *every* platform, your signal/accuracy ratio is your
  most valuable long-term asset. Never submit a report you wouldn't bet money
  on. One N/A costs more than one missed bounty.

---

## PART 2: The program evaluation checklist

Run this checklist before committing significant time to a new program.
Score each dimension; a program that fails 3+ is a walk-away.

### Scope analysis
- [ ] **Scope width:** `*.target.com` (wide) vs. `www.target.com` only
  (narrow). Wide scope is strongly preferred — it multiplies recon and
  enables subdomain/shadow-API/mobile-API hunting.
- [ ] **Scope depth:** Are mobile apps in scope? APIs? Acquired properties?
  Internal tools behind VPN (with VPN access provided)?
- [ ] **Exclusions:** Read the out-of-scope list carefully. Programs that
  exclude "rate limiting", "missing headers", "self-XSS", "logout CSRF" are
  *normal* — these are non-bugs. Programs that exclude entire vuln classes
  you specialize in (`"no SSRF reports"`, `"no business logic"`) are a red
  flag for your ROI.
- [ ] **Tech stack fit:** Does the target run tech you're strong at? A
  Rails/React app when you specialize in PHP deserialization is a mismatch.
  Check Wappalyzer/BuiltWith/response headers before committing.

### Triage & payout signals
- [ ] **Triage speed:** Check disclosed reports or ask the community. < 7
  days first response = excellent. > 30 days = caution. > 90 days = walk
  away unless the payouts are exceptional.
- [ ] **Payout speed:** Bounty within 30 days of triage = good. 90+ days =
  factor the cash-flow cost into your ROI calculation.
- [ ] **Payout fairness:** Do they reward impact or pay a flat rate per vuln
  class? A program that pays $500 for every XSS regardless of impact
  undervalues your chains. Look for "we reward based on impact" language and
  evidence in disclosed reports.
- [ ] **Managed vs. direct triage:** Direct communication with the security
  team (visible in disclosed reports as team-member responses, not generic
  "Triager" responses) correlates with better outcomes. Managed triage adds
  a layer that can misunderstand technical findings.
- [ ] **Bounty table published?** Programs that publish their payout ranges
  (Low/Med/High/Crit) are more predictable. No table = higher variance.

### Competition & saturation signals
- [ ] **Disclosed report volume:** High Hacktivity volume on basic vulns
  (reflected XSS, open redirects) = the low-hanging fruit is picked. This
  is *good* if you hunt logic/chain bugs; *bad* if you rely on low-hanging
  fruit.
- [ ] **Program age:** New programs (< 6 months) are gold — less picked
  over, team is still learning what to expect. Old programs (5+ years) need
  deeper methodology but have more attack surface (legacy code, acquired
  properties, forgotten subdomains).
- [ ] **Researcher count / "hackers thanked":** Very high numbers on a narrow
  scope = saturated. High numbers on a wide scope = still plenty of surface.
- [ ] **Recent scope changes:** A scope expansion (new domain, new mobile
  app, new API) is the strongest signal to start or revisit a program. Set
  up monitoring (see `web2-recon`).

### Red flags (walk-away signals)
- Program disputes valid findings to avoid paying ("works as designed" on
  a clear IDOR; reclassifying Critical to Low without explanation).
- Triage goes silent for 90+ days on multiple reports.
- Scope shrinks after you start finding bugs in a specific area.
- "We don't consider [your specialty] in scope" added after your report.
- Program requires NDA but doesn't pay (all risk, no reward).

---

## PART 3: VDP economics

**Vulnerability Disclosure Programs** (no bounty) are not charity — they're
an investment with a different return:

| When a VDP is worth your time | When it isn't |
|---|---|
| You're building skills on a new vuln class or tech stack | You're already proficient and need income |
| The company is likely to upgrade to a paid program (check their hiring/security maturity signals) | The company has had a VDP for years with no sign of paying |
| You want to build a relationship with a specific security team | You're burning out giving free pentests |
| Cool swag, CVE credit, or hall-of-fame placement that matters to you | None of the above apply |
| Practice ground for new tooling or automation | You're spending > 1 day on it |

**Rule:** Cap VDP time at one afternoon session. If you find something
significant, report it and move on. Don't give a company a full pentest for
free.

---

## PART 4: Building your program portfolio

### The 5–6 program model

| Slot | Program type | Why |
|---|---|---|
| 1–2 | **Deep targets** — wide scope, months of investment, you know the codebase | These are your bread and butter. Most of your high-impact findings come from here. |
| 1 | **Fresh target** — new program or recent scope expansion | Low competition, high discovery rate. Rotate when it matures. |
| 1 | **Skill-builder** — different tech stack or vuln class than your comfort zone | Deliberate practice. Lower immediate ROI, higher long-term ceiling. |
| 1 | **Quick-hit** — narrow scope but fast triage and reliable payouts | Cash flow stabilizer. When your deep targets are in a dry spell. |
| 0–1 | **VDP / CTF / research** — no bounty, pure learning | Only when you have capacity. First to drop when busy. |

### Rotation triggers

- **Stay** when: scope expands, new features ship regularly, team communicates
  well, you're still finding bugs after months.
- **Rotate out** when: 3+ reports sitting in triage with no response, you've
  exhausted the feature surface and recon reveals no new assets, the program
  cuts scope or payouts, or the team's response pattern signals they're
  winding down.
- **Revisit** when: scope change notification, major acquisition, platform
  announces increased bounties, you develop a new skill that applies to their
  stack.

### Monitoring for scope changes

Don't manually check program pages. Automate:

- **Platform notifications:** Enable scope-change alerts on HackerOne /
  Bugcrowd / Intigriti for your active programs.
- **Web monitoring:** `web2-recon` JS-diff monitoring, CertSpotter/crt.sh
  certificate transparency monitoring for new subdomains, Google Alerts for
  `site:target.com` new indexed pages.
- **Social signals:** Follow the target's engineering blog, Twitter/X, and
  GitHub org for product launches (new feature = new attack surface).

---

## PART 5: Prior-art research (before you start hunting)

Before investing time, check what's already been found:

1. **Hacktivity / disclosed reports** — read the last 20–50 disclosed reports.
   They tell you: what the team considers valid, what vuln classes they've
   seen, what they reward well, and (crucially) what areas have already been
   picked over.
2. **OpenBugBounty** — check for historical XSS/injection disclosures.
3. **Google dorking the target + "bug bounty"** — blog posts by other
   researchers describing their approach. Tells you which areas are saturated
   and which angles haven't been tried.
4. **CVE databases** — historical CVEs on the target's tech stack. A CVE in
   their framework version → check if they patched.
5. **GitHub / public code** — search for the target's domain in public repos
   (leaked API keys, internal docs, employee side projects referencing
   internal endpoints). Feed findings into `hunt-source-leak`.

---

## PART 6: The decision flowchart

```
New program or invite arrives
        │
        ▼
   Scope wide enough? ──No──► Pass (unless payout is exceptional)
        │Yes
        ▼
   Tech stack match? ──No──► Skill-builder slot only (slot 4)
        │Yes
        ▼
   Triage < 30 days? ──No──► Check disclosed reports for pattern
        │Yes                       │
        ▼                    Still slow? ──► Pass
   Bounty table fair? ──No──► Proceed with caution, test with 1 report
        │Yes
        ▼
   Check prior-art (PART 5)
        │
        ▼
   Competition level?
   ├─ Low (new/expanded) ──► Fresh target slot (slot 3) — priority
   ├─ Medium ──► Deep target slot (slots 1–2) if stack fits
   └─ High (saturated basics) ──► Only if you hunt logic/chains
        │
        ▼
   Commit: run feature-driven-testing first pass,
   then bb-methodology Phase 0–1
```

---

## Cross-references

- **What to do once you've chosen:** `bb-methodology` (session orchestration)
- **First pass on the target:** `feature-driven-testing` (feature → probe →
  dispatch)
- **Asset ownership triage:** `recon-scope-triage` (before testing anything)
- **Surface expansion:** `web2-recon`, `hunt-subdomain`, `hunt-shadow-api`
- **Reporting quality:** `report-writing`, `triage-validation`,
  `evidence-hygiene`
- **Toolkit setup:** `bb-local-toolkit`, `security-arsenal`
