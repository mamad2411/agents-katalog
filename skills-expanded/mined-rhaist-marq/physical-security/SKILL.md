---
name: physical-security
description: "Covers layered physical controls for facilities and data centers: concentric zones, tailgating defense, badge and visitor management, CPTED, environmental resilience, and where physical access becomes cyber compromise. Use when the user asks how to secure an office, plant or data center, prevent tailgating, design visitor or badge processes, or assess physical-to-cyber risk."
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# Physical security (defense-in-depth)

Physical access defeats most cyber controls: a person at the keyboard, the
console port, or the disk wins. Design in concentric layers so bypassing one
control still leaves the attacker outside the next: **deter → detect → delay →
respond → recover**. No single fence, lock, or guard is the control; the
overlap is. This is the defensive counterpart to physical/social-eng offense
(`load_skill social-engineering-defense` for the human layer).

## Concentric zones (outer → inner)

- **Perimeter**: lighting, fencing, bollards/barriers, signage. CPTED's three
  levers: natural surveillance (sightlines, no blind corners), natural access
  control (one obvious funneled entry), territorial reinforcement (clear public
  vs private boundary). Goal: deter and channel, not just wall off.
- **Building shell**: badge-controlled entry, reception as a real checkpoint,
  no propped doors (door-held-open alarms), CCTV with retention ≥ 90 days.
- **Interior zones**: escalating credentials per sensitivity. Floors/wings
  segmented; a building badge ≠ a data-hall badge.
- **Secure room / cage / rack**: MFA at the door (badge + PIN or badge +
  biometric), and the rack itself locked. Smallest blast radius gets strongest control.

## Data-center / high-value facility controls

- **Mantrap / interlocking vestibule** at the data hall: two doors, only one
  opens at a time, one person per cycle; the structural anti-tailgating control.
- **Anti-passback**: a badge that entered can't enter again without an exit
  swipe; this kills badge-sharing and pass-back. Enforce in + out sequencing.
- **MFA on sensitive zones**: badge + PIN / biometric / mobile credential.
- **CCTV + alarm fusion**: cameras on every door, alarms on forced/held doors,
  recorded and tied to badge events for after-the-fact reconstruction.
- **Asset control**: media/equipment in-out logging; no personal devices in the
  hall; sanitize or shred decommissioned drives (NIST SP 800-88).
- verify (controls checklist): https://www.cisa.gov/topics/physical-security

## Tailgating / piggybacking defense

- The hardest human-layer problem: people hold doors out of politeness.
- Structural fixes beat policy: mantraps, full-height turnstiles, optical
  speed-lanes; one credential, one person.
- Detective: door-ajar alarms, anti-passback violations, video analytics for
  two-bodies-one-swipe, periodic badge-vs-presence audits.
- Cultural: "badge every person, every time," challenge-and-escort norm, no
  shame for asking a stranger to badge in. Reinforce via `load_skill security-awareness`.

## Visitor & badge management

- Pre-registration tied to a named internal sponsor + a time window.
- Photo ID check at sign-in; time-limited, visually distinct visitor badge;
  escort required in non-public zones; sign-out enforced.
- Employee badges: provisioned via joiners/movers/leavers workflow synced to HR.
  **Same-day revoke on termination** is the control that actually matters.
  Periodic access recertification; deprovision orphaned/loaner badges.
- Contractors/vendors get scoped, expiring access: never permanent.

## Environmental & availability controls

- **Power**: dual feeds, UPS for ride-through, generator + fuel contract; test
  failover on a schedule (an untested generator is decoration).
- **HVAC/cooling**: redundant units, temp/humidity monitoring with alerting:
  thermal shutdown is an outage.
- **Fire**: VESDA early smoke detection + clean-agent (inert gas) suppression in
  data halls; never water over live equipment. Annual inspection.
- **Water/flood**: leak detection under raised floor; no equipment below grade
  in flood zones.

## Where physical meets cyber (the crossover risks)

- **Console / OOB access**: a serial/iLO/iDRAC/IPMI port is unauthenticated
  god-mode. Lock the rack, disable unused ports, credential the BMC, segment its mgmt network.
- **USB / removable media**: drop-key and BadUSB attacks bypass the perimeter.
  Disable/whitelist USB, epoxy or port-block where feasible, enforce DLP.
- **Evil-maid**: unattended/unencrypted device = full compromise via boot. Full-disk
  encryption with TPM + pre-boot PIN, Secure Boot, tamper-evident seals on travel laptops.
- **Shoulder-surf / clean-desk**: privacy screens, auto-lock, locked drawers,
  shred bins. Whiteboards and sticky notes are recon gold for an on-site attacker.
- **Network jacks / rogue devices**: 802.1X / MAC-auth on physical ports; disable
  unused jacks in lobbies/conference rooms; rogue-AP and unknown-device detection.

## Measure it

- Tailgating-test pass rate (red-team physical entry attempts caught).
- Mean time to revoke badge on termination (target: same business day).
- % doors with working alarm + camera coverage; % access reviews completed on time.
- Failover test cadence met (power/cooling/fire): pass/fail, not "documented."
