# mushanghai-track-leader/AGENTS.md

> Five modes for TL ops: Scope Brief, Tech Stack, BioBloom Pitch Triage, Daily Traffic-Light, Synthesis. See `../AGENTS.md` for family-level conventions.

## Modes

| Letter | Name | Trigger | Primary Output Path |
|---|---|---|---|
| A | Track Scope Brief | define track scope plus core questions | `assets/track-scope-brief.md` filled in |
| B | Tech Stack Decision | tech stack decision, wearables, logging tools | `assets/track-scope-brief.md` Tech Stack section |
| C | BioBloom Pitch Triage | Recruitment Night, pitch triage | in-scope, out-of-scope, or reshape verdict |
| D | Daily Traffic-Light Check-in | traffic light check, 🟢🟡🔴, mid-experiment status | one-line status per experiment |
| E | End-of-Track Synthesis | track synthesis, end-of-cycle | filled synthesis report |

## Local Layout

- `SKILL.md` - five-mode TL router.
- `references/biobloom-pitch-triage.md` - Mode C context and triage flow.
- `references/good-night-hackers-tl.md` - dual-enrollment language for TLs.
- `assets/track-scope-brief.md` - Mode A output, Mode B Tech Stack section.
- `assets/pitch-triage-rubric.md` - Mode C 5-question rubric.
- `assets/traffic-light-check.md` - Mode D daily status template.
- `assets/track-synthesis.md` - Mode E aggregation template.

## Where to Look

| Task | Location | Notes |
|---|---|---|
| Define track scope | `assets/track-scope-brief.md` | Mode A fills it. |
| Lock accepted tools | `assets/track-scope-brief.md` | Mode B uses Tech Stack section. |
| Triage pitches fast | `assets/pitch-triage-rubric.md` | Pair with `references/biobloom-pitch-triage.md`. |
| Run daily status | `assets/traffic-light-check.md` | One line per experiment. |
| Synthesize the track | `assets/track-synthesis.md` | Aggregate final reports. |

## Local Conventions

- Traffic-light markers must be exactly 🟢, 🟡, 🔴.
- `track-leader/ROLE.md` is a service catalog, not recruitment.
- Mode C verdicts stay scoped to in-scope, out-of-scope, or reshape.

## Anti-Patterns (this skill)

- Rubber-stamping proposals without applying the review checklist.
- Using `[green/yellow/red]` text instead of emoji markers.
- Recruiting new Track Leaders through this skill.
- Letting BioBloom pitch triage exceed the two-minute target.

## Hand-Offs

- Mode C hands to `mushanghai-experiment-leader` Mode B after Recruitment Night.
- Mode D receives status material from `mushanghai-experiment-leader` Mode E.
