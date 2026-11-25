---
name: ipl-cease-desist
version: 1.0.0
description: Assess and draft a cease-and-desist demand letter for IP infringement while avoiding overclaiming, declaratory-judgment exposure, and misrepresentation risk.
author: matrixx0070
tags: [ip, cease-and-desist, trademark, copyright, infringement, demand-letter, escalation]
capabilities: []
---

## When to use

Use this when you hold IP rights (trademark, copyright, patent, or trade secret), someone appears to be infringing, and you want a measured demand letter rather than an immediate lawsuit. It structures the assessment and drafts a defensible letter that does not overreach.

**Not for:** online copyright better handled by a platform notice (use `ipl-takedown` for DMCA §512); assessing whether *you* might infringe before launch (use `ipl-fto-triage`); or answering an accusation against you (use `ipl-infringement-triage`).

## Method

1. **Confirm you own valid, enforceable rights.** Registration status, chain of title, and that the right is live (not lapsed/abandoned).
2. **Confirm the infringement has merit.** For trademark, run the likelihood-of-confusion factors (below); for copyright, confirm ownership + access + substantial similarity.
3. **Choose the escalation rung:** informal notice → formal C&D → litigation. Start no higher than the facts justify.
4. **Decision point:** send a **C&D** versus a **platform takedown** (online copyright → `ipl-takedown`) versus going **straight to counsel** (patent assertions, high-value or repeat infringers).
5. **Draft with the required elements:** identify your right and registration, the infringing use, the legal basis, a specific demand, and a reasonable response deadline.
6. **Avoid overclaiming.** Claim only rights you hold and can prove.

**ATTORNEY-ESCALATION GATE:** Patent assertions, any litigation threat, and any letter that could trigger a declaratory-judgment action, a trademark-bullying claim, or DMCA §512(f) misrepresentation exposure MUST be reviewed by a licensed attorney before sending. You draft and assess; you do not opine or authorize sending. This is not legal advice.

## Example

A competitor uses your registered SaaS word mark on a near-identical logo in the same channels. Confusion factors line up (similar marks, related services, overlapping channels). You draft a formal C&D citing the registration, identifying the infringing use, demanding they cease within 14 days. Because it threatens litigation and could invite a declaratory-judgment suit, you route it to counsel before sending.

## Pitfalls

- **Overclaiming your rights.** Asserting rights you don't hold invites unclean-hands and reverse-domain-name-hijacking findings.
- **Threatening litigation you can't file.** A hollow threat can hand the recipient declaratory-judgment jurisdiction.
- **Firing a §512(f) takedown loosely.** Misrepresenting copyright ownership creates liability to the target.
- **Skipping the ownership check.** A lapsed or unregistered right guts the demand.

## Output format

```
C&D ASSESSMENT — <matter> | right type: <TM|©|patent|trade secret>
Rights owned & enforceable: <registration #, chain of title, status>
Merit: <TM confusion factors / © access+similarity / other> -> <weak|solid>
Channel: informal notice | formal C&D | takedown (ipl-takedown) | straight to counsel
Draft letter:
  - Identify right & registration
  - Identify infringing use
  - Legal basis
  - Specific demand + deadline
Escalation: <patent? litigation threat? DJ / §512(f) exposure? -> attorney review before sending>
```

## Reference

**Trademark likelihood-of-confusion factors:** similarity of marks; relatedness of goods/services; strength of the senior mark; trade channels; purchaser sophistication; actual confusion; the junior user's intent; and bridging the gap.

**DMCA §512** is the online-copyright alternative to a C&D: notice-and-takedown to the hosting platform. §512(f) penalizes knowing material misrepresentation, so send only on rights you actually own.

**Overclaiming risks:** unclean hands, reverse-domain-name-hijacking, and handing the recipient declaratory-judgment jurisdiction by threatening a suit. This is not legal advice.
