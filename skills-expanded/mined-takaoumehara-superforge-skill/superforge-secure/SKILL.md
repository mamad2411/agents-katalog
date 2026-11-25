---
name: superforge-secure
description: >
  Security review for products built by small teams — seven passes (secrets,
  authentication, authorization, input handling, data at rest and in transit,
  dependencies, exposed surface) producing a finding-by-finding ledger instead
  of a scanner dump. Ranks by what an attacker actually gets, not by a generic
  score. Covers the failure that dominates real incidents at this scale: a
  credential in a repository or a client bundle, and an endpoint that checks
  who you are but never whether this row is yours. Includes what to do once it
  has already happened — rotation order, blast radius, and the disclosure
  duties that follow. Use when the user says "security", "is this safe",
  "vulnerability", "API key", "leaked", "hacked", "penetration test", "auth",
  "permissions", "セキュリティ", "安全", "脆弱性", "APIキー", "漏れた",
  "不正アクセス", "認証", "権限", or runs /superforge-secure.
license: MIT
metadata:
  author: Takao Umehara
  version: "1.1"
compatibility: >
  Standalone.
  Reads docs/plan.md, docs/design.md, and docs/ship-readiness.md when present.
  Writes docs/security.md, which superforge-ship reads as a precondition.
  scripts/scan-secrets.sh needs bash and git (ripgrep optional).
  Every pass degrades to a documented reasoning check when no runtime is available.
---

# Superforge Secure — Security Review for Products Without a Security Team

Security is not a scanner score, and it is not a topic for later. A product can
pass every automated check, have no known CVE, and still let any logged-in user
read every other user's data by changing a number in a URL.

This skill runs the passes a machine cannot run, ranks findings by **what an
attacker gets**, and writes a ledger that `superforge-ship` reads before a
release.

---

## 0. The rule this skill exists to enforce

**Never report that something is secure. Report what was checked.**

"Secure" is not a state a review can establish — it is the absence of every
unknown flaw, which no process can demonstrate. A review can only say: these
seven passes were run against this surface on this date, and here is what they
found and what they did not cover.

This is the same discipline as `superforge-verify`, applied to a domain where
the false clearance is more expensive: a user who is told "we checked, it's
secure" stops looking.

**Two corollaries:**

- A clean dependency scan is the *start* of the review. It sees published
  vulnerabilities in third-party code and is blind to every flaw in yours,
  which is where the findings in §2's passes 1–3 actually live.
- **Report `SECURE-REVIEWED` / `FINDINGS-OPEN` / `NOT-ASSESSED`, never "secure".**

---

## 1. Scope before reviewing

Four things, written at the top of the report. Guess the defaults and confirm
rather than interrogating.

| | Default if unstated |
|---|---|
| **Surface** | every route or screen that touches data, plus every background job and third-party webhook |
| **Trust boundary** | anything the client sends is attacker-controlled — including headers, IDs, prices, and any value your own JavaScript put there |
| **Attacker model** | a logged-in ordinary user of your product. Not a nation state. This is the one that finds real bugs at this scale |
| **Blast radius** | what the worst single compromise reaches — one account, all accounts, the database, the payment provider |

**The default attacker model matters more than any other choice here.** Most
indie-product breaches are not sophisticated. They are an ordinary user who
changed an ID, or a public repository with a key in it.

---

## 2. The seven passes

Run all seven. A pass that could not be executed is recorded as reasoned or as
not assessed — never silently skipped.

| # | Pass | The question |
|---|---|---|
| **1** | **Secrets** | Is any credential reachable by someone who should not have it — in git history, in the client bundle, in a log, in an error message? |
| **2** | **Authentication** | Can someone become a user they are not? Session handling, password storage, reset flows, OAuth callbacks |
| **3** | **Authorization** | The route knows *who* you are — does it check whether *this row* is yours? Run this pass on every endpoint, not a sample |
| **4** | **Input** | Every value from a client is attacker-controlled. Where does it reach a query, a command, a template, a file path, or another user's screen? |
| **5** | **Data** | What is stored, encrypted how, transmitted how, retained how long, and deletable by whom? |
| **6** | **Dependencies** | Known vulnerabilities, unmaintained packages, and what a compromised build-time package could do |
| **7** | **Exposure** | What is reachable that should not be — debug routes, admin paths, open storage buckets, permissive CORS, verbose errors, unauthenticated APIs |

Each pass, what to actually look at per platform, and the specific checks that
find real bugs → **`references/attack-surface.md`**.

**Pass 1 is scriptable, and should be scripted.** Six places is exactly the
count people stop checking under time pressure:

```bash
scripts/scan-secrets.sh                 # tree, git history, bundle, env, CI, tracked files
scripts/scan-secrets.sh --bundle dist   # point it at a real build
scripts/scan-secrets.sh --no-history    # faster, skips the check people skip
```

It reads only, never prints a usable secret (matches truncate to four
characters), and exits 1 on findings so it can gate CI. **A clean run is not
"no secrets"** — it means these patterns did not match here, and it says so.

**Passes 1 and 3 are where the findings are.** If time is short, run those two
properly rather than all seven shallowly, and say in the report that you did.

---

## 3. Severity — rank by what the attacker gets

Generic scores are calibrated for enterprise software and misrank small
products badly. Rank by outcome:

| Level | The attacker can | Response |
|---|---|---|
| **Critical** | Read or change data belonging to users who are not them; act as another user; reach the database or the payment provider | Stop. Fix before anything else ships |
| **High** | Reach data of one specific other user; escalate their own privileges; take an irreversible action | Fix before this release |
| **Medium** | Learn something they should not (enumerate users, read internal errors, map the system) | Fix soon; record the decision if deferred |
| **Low** | Nothing directly — a weakness that needs another flaw to matter | Log it; do not let it crowd out the above |

**Write the exploitation path, not the category name.** "IDOR on /api/orders"
is a label. "Any logged-in user can change `?id=` and read another customer's
address and order history" is a finding someone will act on today.

---

## 4. What this skill does not do

- **It does not replace a penetration test** for a product handling payments at
  volume, health data, or children's data. It tells you when you have reached
  that line — see `superforge-ship/references/legal-triggers.md` §4.
- **It does not write the fix silently.** A security fix applied without being
  understood is how a vulnerability moves rather than closes.
- **It is not a compliance certification.** SOC 2, ISO 27001, and PCI DSS have
  their own auditors, and this ledger is an input to them at most.

---

## 5. When it has already happened

A leaked key or a suspected breach is a different procedure from a review, and
the ordering matters — rotating in the wrong order locks you out or leaves the
attacker in. Containment, rotation order, working out the blast radius from
logs you may not have kept, and the disclosure duties that follow →
**`references/when-it-happens.md`**.

**Do this before the post-mortem.** The instinct to work out *how* first is the
one that leaves the attacker inside for another day.

---

## Deeper reference

**`references/attack-surface.md`** — the seven passes in detail: where secrets
actually leak (git history and the client bundle, not config files), the
authorization pass run endpoint by endpoint, what "attacker-controlled" covers,
storage and transit decisions, dependency and build-time risk, and the exposure
sweep. Web, iOS, and Android.

**`references/when-it-happens.md`** — containment before diagnosis, the
rotation order, reconstructing blast radius, what to preserve, the honest
notification, and when the law requires one.

---

## Artifact

Write `docs/security.md`.

```markdown
# Security review — <target> @ <commit>

> Written by: superforge-secure · Last updated: <YYYY-MM-DD>
> Surface: <what was reviewed> · Attacker model: <default: logged-in ordinary user>
> Passes run: <1-7, and which were reasoned rather than executed>

## Verdict
SECURE-REVIEWED / FINDINGS-OPEN / NOT-ASSESSED — and the one sentence why

## Findings
| # | 深刻度 | 攻撃者ができること | どこ | 直し方 | 状態 |

## Pass ledger
| # | パス | 実行 / 推論 / 未評価 | 見たもの |

## 確認していないこと
<正直に。空欄は、たいてい不完全ではなく不誠実>
```

**`superforge-ship` reads this file as a precondition.** A missing
`docs/security.md`, or one carrying an unresolved Critical, is a `BLOCK` there.
`superforge-handoff` carries the verdict forward.

Findings that are really implementation defects go to `superforge-dev`; ones
that are really data-handling obligations go to `superforge-ship`; ones that
need a regression test go to `superforge-test`. **A finding that stays in this
file is a finding nobody fixed.**

## Delegate when a sharper skill is installed

`security`, `harden`, `security-review` (deeper review) · `threat-model` ·
`secrets-management`, `dependency-audit` (specific passes) ·
`auth-flow` (implementing the fix) · **`superforge-ship`** (the legal duties a
finding triggers) · **`superforge-test`** (locking a fix so it cannot regress).
