# Daily Standup Coach (Skill classifier fixture)

A pure-prose AI skill that helps teams prepare for and run daily standup
meetings. This SKILL.md fixture is used by `bin/tests/test_classify_project.py`
as a known-Skill target for the v1.5.3 project-type classifier: SKILL.md at
fixture root, no substantial code, prose word count substantially exceeds
code line count.

The fixture is a synthetic skill, not a real one in production use; its
content is realistic enough to exercise the classifier but should not be
mistaken for a deployable skill.

## When to use this skill

The skill activates when an operator asks for help running a daily standup
meeting. Triggers include phrases like "help me run standup," "review my
standup notes," "draft talking points for tomorrow's standup," or "summarize
this week's standups." It can also be invoked as part of a larger sprint
ceremony orchestration where standup is one of several meetings the operator
needs to facilitate.

The skill does not activate for retrospectives, sprint planning, refinement
sessions, or other agile ceremonies. Those meetings have different shapes
and different anti-patterns and would need their own skills. If an operator
asks the skill to handle a non-standup meeting, the skill politely declines
and points at the appropriate alternative tool, if one exists, or suggests
the operator use a general-purpose meeting facilitator.

## What this skill produces

For each invocation the skill produces three artifacts. The first is a
concise meeting agenda: who is presenting, in what order, with how much
time each. The agenda follows the round-robin pattern that most teams
default to, but the skill will reorder if the operator has flagged that a
specific blocker should be discussed first. The second artifact is a set of
prompts the operator can use to keep the meeting on track: when to redirect
a tangent, when to move someone to "parking lot," when to escalate a
recurring blocker. The third artifact is a brief written summary of the
meeting that can be posted to a shared channel after the meeting concludes.

The artifacts are written incrementally as the skill processes the
operator's input. The agenda lands first because most operators want to
review it before the meeting; the prompts land second because they're
needed during the meeting; the summary template lands last because it's
populated post-meeting from the operator's notes.

## Phase 1 — Pre-meeting preparation

Phase 1 runs in the time window between the operator deciding to use the
skill and the standup meeting starting. The skill reads any context the
operator provides — last week's notes, the team's current sprint goals,
known blockers — and produces a draft agenda.

Phase 1's output is `agenda.md` in the operator's working directory. The
file has three sections: roster (who is expected to attend, in presentation
order), focus areas (sprint goals being discussed this week), and parking
lot (topics that came up but should be deferred). Each section is brief —
the agenda is meant to fit on one screen so the operator can keep it open
during the meeting.

The operator can edit the agenda before the meeting. The skill respects
operator edits and uses the edited agenda as the basis for the next phase
rather than regenerating from scratch.

If the operator hasn't provided any context, Phase 1 produces a skeleton
agenda with placeholders the operator fills in. This is the most common
case for first-time use of the skill — the operator hasn't yet trained the
skill on the team's specific dynamics.

## Phase 2 — In-meeting facilitation

Phase 2 runs during the standup meeting itself. The operator is presumably
busy facilitating, so the skill operates in low-touch mode: it watches a
shared notes document the operator updates as the meeting progresses, and
emits short prompts when it detects patterns that need redirection.

Patterns the skill watches for include: someone has been talking longer
than their allotted time; the same blocker has come up across multiple
recent standups; a topic is drifting into deep-dive territory and should be
moved to a follow-up meeting; the team is reporting all-green on a goal
that other signals suggest is at risk.

When the skill detects one of these patterns, it emits a prompt as a
comment in the shared notes. The prompt is brief and actionable: not "this
discussion seems to be drifting," but rather "consider parking this for a
follow-up; @alice and @bob can sync after standup." The operator can ignore
the prompt, apply it, or modify it.

Phase 2's output is the cumulative set of prompts emitted during the
meeting. They live in `meeting_prompts.md` and are timestamped so the
operator can correlate them with the meeting recording if one exists.

## Phase 3 — Post-meeting summary

Phase 3 runs after the standup meeting concludes. The operator typically
hands the skill the raw notes from the meeting plus any audio transcript
the team's recording tool produced. The skill produces a written summary
suitable for posting to the team's shared channel.

The summary has a fixed structure: what the team accomplished since last
standup, what the team is working on now, what blockers exist and who
owns each. The structure is fixed because variability in summary structure
makes it hard for downstream consumers (the team's tooling, the manager's
weekly digest) to extract structured data.

Each section of the summary is a bulleted list. Each bullet is a single
sentence. Each blocker bullet names an owner and an expected resolution
window — the skill prompts the operator if those fields aren't clear from
the notes.

Phase 3's output is `summary.md`, which the operator reviews before posting.

## Phase 4 — Pattern recognition across meetings

Phase 4 runs periodically — typically weekly — and looks across the recent
history of summaries to identify patterns. A blocker that has appeared in
three consecutive standups without resolution. A team member whose updates
have been getting shorter and more vague over time. A sprint goal that the
team has been reporting progress on but never closing out.

The skill flags these patterns to the operator without prescribing action.
The operator typically knows the team better than the skill does and is in
a better position to decide whether a flagged pattern warrants intervention.
The skill's job is to surface the pattern, not to act on it.

Phase 4's output is `patterns.md`, an append-only log of patterns the skill
has identified. Each entry has the pattern, the evidence (which standups
contributed), and a suggested escalation path the operator can take if
they want to address the pattern.

## Phase 5 — Retrospective input preparation

Phase 5 is invoked at the end of a sprint, typically during the operator's
preparation for the team retrospective. The skill bundles the patterns
from Phase 4 plus a summary of the sprint's standups into a retrospective
input document.

This is not the retrospective itself — the skill explicitly does not run
retrospectives, only standups. The output is meant to be one input among
many for the operator (or a separate retrospective skill) to consume.

The output is `retro_input.md` and is structured around the standard
retrospective categories: what went well, what didn't, what to try next.
The skill populates each category from standup data; the operator and the
team add categories the standup data can't speak to.

## Anti-patterns the skill avoids

The skill explicitly does not do the following, even when asked: rate
individual contributors against each other; produce performance review
input; act as a surveillance tool for tracking who is "really working";
generate disciplinary documentation. These uses misread the standup as a
status-reporting meeting rather than a coordination ritual, and the skill
declines them with a brief explanation pointing at appropriate alternative
practices.

The skill also avoids over-instrumenting standups: it does not push for
more meetings, longer meetings, or more detailed reporting unless the
operator has explicitly requested those changes. The default bias is
toward shorter, lower-touch meetings with clear outcomes.

## How the skill calibrates

The skill maintains a small per-team calibration state that captures the
team's preferences: how strict to be about time-boxing, how aggressive to
be in flagging patterns, how much to summarize versus quote raw notes.
The calibration is updated when the operator overrides a skill suggestion
("don't flag this kind of thing again") or when the operator explicitly
tunes ("be more aggressive about parking-lot suggestions").

Calibration is persistent across invocations. It lives in `calibration.json`
in the operator's working directory and is portable between machines if
the operator copies the file.

## Extending the skill

Operators can extend the skill by adding domain-specific reference files
under `references/`. Each reference file describes a class of pattern or
intervention specific to the operator's context — for instance, a file
describing the team's specific definition of "blocked" or a file listing
the senior contributors whose updates should always be parked rather than
deep-dived during standup.

The skill reads `references/` at the start of each invocation and incorp-
orates the reference content into its decision-making. Reference files
must be markdown; other formats are not supported.

When SKILL.md and a reference file disagree, SKILL.md wins. Reference
files are supplementary, not authoritative.
