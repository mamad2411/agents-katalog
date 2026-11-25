---
name: ipl-infringement-triage
version: 1.0.0
description: Triage an IP infringement matter by direction and IP type, assess merits and urgency, and route it to monitoring, cease-desist, takedown, or an attorney.
author: matrixx0070
tags: [infringement, triage, trademark, copyright, patent, dmca, escalation]
capabilities: []
---

## When to use

Use this when infringement is in play in either direction: an inbound allegation that you infringe someone's IP, or a suspicion that a third party infringes yours. It classifies the matter fast, sizes the merits and the clock, and points to the right next move before anyone overreacts or lets a deadline slide.

**Not for:** drafting the demand once triage says send one (see ipl-cease-desist), filing an online takedown (see ipl-takedown), or a proactive brand clearance search with no dispute yet (see ipl-clearance). This triages and routes; it does not execute the remedy.

## Method

1. **Classify direction and type.** Inbound (you are accused) vs. outbound (you suspect a third party), and the IP type: trademark, copyright, patent, or trade-secret. These drive everything downstream.
2. **Gather evidence.** Priority dates/registrations, the accused use, side-by-side comparison, and any correspondence received.
3. **Assess merits** at a triage level. For trademark, apply the likelihood-of-confusion factors in Reference; for copyright, access + substantial similarity; for patent, note claims must be read by counsel.
4. **Assess urgency.** Statute-of-limitations exposure, a stated deadline in a demand letter, and ongoing/escalating harm. **Decision point:** a received demand letter with a response deadline is time-critical — do not let it lapse while triaging.
5. **Route:** monitor; cease-and-desist (ipl-cease-desist); online takedown (ipl-takedown); or attorney.
6. **ATTORNEY-ESCALATION GATE.** You assist; you do not give legal opinions and this is not legal advice. Any received demand letter, any patent claim (either direction), any trade-secret matter, and anything litigation-shaped stops here and routes to a licensed attorney.

## Example

Inbound: you receive an email claiming your app icon infringes a registered logo, demanding a response in 10 days. Direction: inbound, trademark. Marks share a stylized swoosh; goods overlap (mobile apps). Merits: plausible confusion. Urgency: hard 10-day deadline. Route: attorney immediately (received demand letter trips the gate); preserve evidence, send nothing substantive first.

## Pitfalls

- **Misreading direction.** Inbound and outbound need opposite postures; getting it backward wastes the first, best move.
- **Sitting on a demand letter.** A blown response deadline can forfeit options — the clock starts when it lands, not when you finish triage.
- **Self-assessing patent claims.** Claim construction is attorney work; a lay read invites a false clear.
- **DIY on trade secrets or litigation.** These escalate on sight; informal handling can destroy privilege or the secret itself.

## Output format

```
Direction: inbound (accused) | outbound (suspected)
IP type: trademark | copyright | patent | trade-secret
Evidence: <priority date/reg, accused use, comparison, correspondence>
Merits (triage): <analysis + factors>
Urgency: <SOL / demand deadline / ongoing harm>
Route: monitor | cease-desist | takedown | attorney
Attorney escalation: <yes/no + trigger>
```

## Reference

Trademark likelihood-of-confusion factors: similarity of the marks (sight, sound, meaning/commercial impression); relatedness of goods/services; strength/distinctiveness of the senior mark (fanciful > arbitrary > suggestive > descriptive > generic); channels of trade/marketing; purchaser sophistication; actual confusion; junior user's intent; likelihood of expansion ("bridging the gap"). Frameworks: DuPont, Sleekcraft, Polaroid. For online copyright, DMCA §512 notice-and-takedown is the usual fast path (route to ipl-takedown). Patent matters and any litigation-shaped dispute always escalate to a licensed attorney.
