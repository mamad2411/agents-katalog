---
name: security-test-engagement
description: "Commission or run an authorised penetration test, red-team exercise or bug-bounty engagement from the asset owner's side: a signed authorisation naming the exact scope, systems, IP ranges and dates before any testing starts; rules of engagement with explicit stop conditions and a named emergency contact who can halt the test; rules for what counts as safe test data and test accounts so a tester never touches real customer records; and a path from each finding through triage, an owned remediation ticket, and a retest that closes it. Use when someone is scoping a pentest, writing rules of engagement, deciding what a red team may and may not touch, or turning pentest findings into fixed and verified work. Not for a design-time threat model (threat-model), one code diff (security-review), or a chaos or failover drill (game-day)."
allowed-tools: "Read, Write, Edit, Grep, Glob"
---

# Security Test Engagement

An engagement is finished when every finding is either closed on a confirmed retest or open with an owner and a date, and when the authorisation, the rules of engagement and the emergency contact were all in writing before the first test action — not reconstructed afterwards from memory of what everyone agreed to.

This is a paperwork discipline, not a technique one, and the two failures it exists to prevent are both paperwork failures. The first is starting on a verbal go-ahead: testing begins because "legal said it's fine" or "we've done this before," and when something breaks mid-engagement there is nothing to point to that says what was actually authorised. The second is a permission list with no stop conditions: a document that says what a tester may do but never says when they must stop gives them every reason to keep going and no signal for the moment a discovery — an unrelated active compromise, a risk to customer data, an effect on production beyond what was agreed — should end the test immediately. Everything below is either the authorisation that prevents the first failure or the stop condition that prevents the second.

## Scope

Use for: scoping an external pentest or bug-bounty engagement, writing rules of engagement for an internal or external red team, deciding what a tester may and may not touch, setting the rules for test data and test accounts, and routing pentest or red-team findings through triage, remediation and a confirmed retest.

Do not use for: a design-time threat model with no engagement to authorise (`threat-model`), reviewing one code diff (`security-review`), a chaos experiment or failover drill (`game-day`), triaging a dependency-scanner alert queue (`dependency-triage`), or fixing the Terraform or workflow issue a finding turned up (`iac-review`, `pipeline-hardening`). This skill's own text carries no attack technique, tool invocation against a target, or payload — that is the domain of specialised offensive tooling and training this repository does not carry, and describing one here would be the same defect as shipping one.

## Hard gates

Skipping one of these does not make the engagement faster — it makes it unauthorised.

1. No testing action of any kind before a signed, dated authorisation naming the exact scope — systems, IP ranges, domains, applications, and explicitly what is out of scope — exists and is attached to the engagement record.
2. No engagement without a named, confirmed-reachable emergency contact for its entire window. A contact who has not been reached before testing starts is a name, not a contact.
3. No tester-created account or test data touches a real customer record without the asset owner naming that exception explicitly, in writing, in advance.
4. No finding closes without a retest result attached. A shipped fix is a claim; a retest that no longer reproduces the finding is the verification.

## Workflow

### 1. Get the authorisation signed before anything else happens

Name the signing authority — the asset owner, not the tester and not whoever requested the test — the exact scope, and the start and end dates. An engagement that starts on a verbal go-ahead has no way to prove later that it was authorised at all, which is the difference between a security test and unauthorised access in the eyes of the law and of your own incident process. Attach the signed document to the engagement record before the first test action, because an authorisation attached afterwards is indistinguishable, to anyone reading the record later, from one that never existed until someone needed it to.

### 2. Write rules of engagement with stop conditions, not just permissions

State what the tester may do — the techniques and systems in scope, at the level of "network penetration test against the systems in scope" rather than any specific method — what they may never do (destructive actions, social engineering against specific named individuals unless separately authorised, actions against production data), and the conditions under which the test stops immediately: discovery of an active, unrelated compromise; any action that risks customer data exposure; any effect on production availability beyond what was explicitly authorised. A permission list with no stop condition gives the tester no way to know which findings are stop-worthy in the moment they find them.

### 3. Name a reachable emergency contact for the whole engagement window

A named person, a phone number that is actually staffed during the test hours, and a fallback if that person is unreachable. Confirm the contact is reachable before testing starts, not merely listed — an unstaffed emergency line discovered mid-engagement is the same failure as no line at all, at the worst possible moment to learn it.

### 4. Set test-data and test-account rules before the tester needs an account

Decide in advance, in writing, whether the engagement runs against production with synthetic accounts, a staging environment with realistic but non-real data, or production read-only. This is not something to improvise when the tester asks for credentials. The default, absent an explicit exception, is that a tester never sees a real customer record — leaving this undecided is how it gets decided by accident, in production.

### 5. Route every finding through triage to an owned ticket

Each finding gets a severity, an owner and a due date, the same discipline any other vulnerability process uses. Hand the severity call and remediation planning to whichever skill owns the affected surface once the finding is triaged — `dependency-triage` for a vulnerable package the test turned up, `iac-review` for a misconfigured resource, `security-review` for an application-layer finding worth a follow-up code review. This skill's job stops at getting the finding into that process; it does not re-derive how to fix a Terraform misconfiguration or a dependency finding.

### 6. Retest, and close only on confirmed remediation

A finding is not closed because a fix shipped; it is closed because the same test that found it was rerun and it no longer reproduces. A fix that was not retested is a claim, and the gap between a claim and a verified remediation is exactly where a "fixed" vulnerability reappears in the next audit.

## Anti-patterns

**Starting on a verbal go-ahead.** It almost always arrives wrapped in urgency — an audit deadline next week, a customer demanding proof before a renewal — and that urgency is exactly the condition under which skipping the signature feels reasonable and costs the most if anything goes wrong during the window.

**Rules of engagement that only say what is allowed.** A tester who finds something interesting just outside scope has every incentive to keep going, because stopping to ask feels like giving up progress on a live lead. The stop conditions exist to take that call away from the person with the least reason to make it conservatively.

**An emergency contact who is a name with no confirmed phone line.** Contacts named months before a test rotate teams, go on leave or change numbers, and a document nobody has reopened since it was written does not know that happened.

**Testing against real customer data because nobody set the rule.** Once a real record shows up in a tester's report or a proof-of-concept screenshot, the engagement has produced its own data-handling incident on top of whatever it was scoped to find — a problem for `data-privacy`, not this skill.

**Closing a finding because the fix shipped.** An unretested "fix" that resurfaces at the next audit usually comes back as a new ticket rather than a reopened one, which hides the fact that it is a repeat rather than a fresh finding.

## Output format

```markdown
## Engagement
[Asset owner, tester or firm, dates, and what triggered this engagement.]

## Authorisation
Signed by:  [name, role]
Scope:      [systems, IP ranges, domains — and explicitly, what is out of scope]
Dated:      [start / end]

## Rules of engagement
Permitted:       [techniques and systems]
Prohibited:      [destructive actions, named exclusions]
Stop conditions: [each one, and who decides]

## Emergency contact
[Name, number, confirmed reachable, fallback.]

## Test data and accounts
[Environment, synthetic vs real data, any explicit exception and who approved it.]

## Findings
| Finding | Severity | Owner | Ticket | Retest result |

## Closed out
[Findings retested and confirmed fixed; anything still open and why.]
```
