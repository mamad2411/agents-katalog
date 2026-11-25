---
name: litig-customize
version: 1.0.0
description: Configure the litigation plugin to a specific firm, practice area, and jurisdiction with default rules, deadline calendars, templates, and escalation contacts.
author: matrixx0070
tags: [litigation, configuration, jurisdiction, deadlines, templates]
capabilities: []
---

## When to use
Use this once, at setup, and again whenever the firm adds a jurisdiction, practice area, or new supervising attorney. It sets the defaults every other litigation skill relies on: which rules set governs deadline math, which court calendars apply, which templates to emit, and who receives escalations. Reach for it when outputs are computing wrong dates or routing to the wrong reviewer.

**Not for:** day-to-day matter tracking (use litig-portfolio-status) or per-matter proof work (use litig-claim-chart).

## Method
1. Record firm identity: practice areas, primary courts, and default time zone.
2. Set the governing rules set per jurisdiction (federal and each state), including local rules and any standing orders in play.
3. Configure deadline-computation rules: calendar vs. court days, weekend/holiday rollover, and service-method adjustments.
4. Load court holiday calendars for each jurisdiction so date math skips closures.
5. Map templates (complaint, deficiency letter, meet-and-confer letter) to the correct jurisdiction's format and citation style.
6. **Decision point:** if a practice spans multiple jurisdictions, decide whether to set one default rules set with per-matter overrides or require explicit selection on every matter.
7. **Decision point:** if a court's local rules conflict with the state default, decide precedence and document the override.
8. Define escalation contacts: the supervising/responsible attorney per practice area and a backstop reviewer.
9. ATTORNEY-ESCALATION gate: have a supervising attorney confirm the rules set, deadline logic, and escalation map before the configuration goes live, since downstream advice-adjacent outputs depend on it.

## Example
> Firm: default TZ America/Los_Angeles. Jurisdictions: N.D. Cal. (FRCP + local rules), CA Superior (CCP). Deadline math: CCP §12/§12a — count court days, roll forward off holidays; +2 court days for electronic service (CCP §1010.6). Escalation: employment → J. Ruiz; commercial → D. Park (backstop: M. Ellison).

## Pitfalls
- **One-size deadline math.** Federal counts calendar days (FRCP 6); many states count court days — never share the rule engine blindly.
- **Missing local rules.** District and even individual-judge standing orders override defaults; capture them per court.
- **Stale holiday tables.** Court closures change yearly; refresh calendars annually.
- **Unassigned escalation.** Every practice area needs a named reviewer or the UPL/review gate silently fails.

## Output format
```
FIRM CONFIG
Time zone: <tz>
Jurisdictions: <court -> rules set -> local rules/standing orders>
Deadline math: <calendar/court days | rollover rule | service adjustments>
Holiday calendars: <jurisdiction -> source/year>
Templates: <type -> jurisdiction/citation style>
Escalation: <practice area -> supervising attorney | backstop>
```

## Reference
Deadline computation differs fundamentally by system. Under Fed. R. Civ. P. 6(a), you count every calendar day, exclude the trigger day, include the last day, and roll forward off weekends and legal holidays; Rule 6(d) adds 3 days when service is by mail. California CCP §12/§12a excludes the first day, includes the last, and rolls forward off holidays, and short "court day" periods (e.g., CCP §1005 motion notice) count only court days; electronic service adds time under CCP §1010.6. Local rules and judges' standing orders frequently modify these. Always compute from the operative rule and the current court holiday schedule; rules and holidays vary by jurisdiction and year. General guidance, not legal advice.
