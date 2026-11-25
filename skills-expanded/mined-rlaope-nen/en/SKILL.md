---
name: en
description: Aura-field auto-routing — read an incoming request's problem shape and engage the right nen abilities, stacked in dependency order when the work spans more than one discipline. Use when the user says "nen", "use nen", "nen mode", "run this through nen", "which skill applies", or "route this"; when a request plausibly spans more than one nen discipline; when you are about to pick a single skill and are not certain it is the right one; or when the user has asked for nen to be the standing baseline for the session.
---

## Stance

円 En is aura extended in a sphere: everything that enters the field is felt, and the feeling is itself the ability. Routing runs on the same law. Reading an incoming request properly — sensing which disciplines the work actually crosses — is not overhead before the real Nen starts; parsing the request and choosing abilities IS using Nen. En is the ability that makes the other abilities reachable.

The stakes are the librarian problem. A pack of disciplines without a sensing layer serves only the user who already knows the taxonomy — they must ask for enhancer by name to get profiling discipline, so the people who most need the routing receive none of it. And the cheap substitute is worse than nothing: keyword routing is a dead sensor. It fires on vocabulary while the actual work walks straight past it — "optimize" summons a profiler to a restructuring request, and the refactor ships unmeasured anyway. The law, stated once and binding always: sibling skill descriptions are scent, not the mechanism — classification happens on what the OUTPUT must be, never on which words appear in the request.

## Boundaries

En senses and engages abilities for ONE incoming request. The moment the work needs decomposing into units dispatched across agents with acceptance criteria, stop — that is manipulator, and en's job was complete the moment it engaged manipulator. The field does not run the operation; it detected that an operation was needed.

When the field senses a recurring need that no skill in the table covers, route to hatsu with the occurrence evidence. En never forges: sensing a gap and filling a gap are different abilities, and the second has its own discipline.

En never does the work itself. It is the field, not the fist: it engages enhancer to move the number, transmuter to reshape the code, emitter to land the words, specialist to name the mechanism, conjurer to close the failure modes — and those disciplines act. An en that starts optimizing has stopped sensing.

The engagement line is a routing decision, not a promise about the work. Binding the work is vow's ability: when vow is installed, the announcement is followed immediately by the engagement's vow block — pre-commitments distilled from the engaged skills' Done means, audited before any done claim. En senses; vow binds; the field never swears the oath itself.

## Method

1. **Restate the request as its problem shape in one line — what must be TRUE afterward.** Not what the request mentions; what the world must look like when the work is done. A number moved? A behavior-preserving change of shape? Words that land with a specific audience? An external mechanism named? Survival under failure proven? Distributed work verified? An ability that does not exist yet? That single line is the field's reading, and every later step leans on it.

2. **Map the shape to categories using those output-tests — explicitly not word overlap.** The request saying "fast" proves nothing; the output-test decides. Done means a measured number moved: enhancer, whatever the vocabulary. Done means the same behavior in a shape the next person can change: transmuter, even if the request said "optimize". Done means someone outside the room is persuaded: emitter, even if the topic is deeply technical.

3. **Select every skill the work genuinely spans.** One is common. Two or three is legitimate — real requests cross disciplines. All of them is a failed classification: return to step 1, because a shape that maps everywhere was never read.

4. **Order the stack by real dependency, not by prominence in the request.** Specialist names the mechanism before conjurer enumerates its failure modes; enhancer locks the number before transmuter reshapes what produced it; emitter speaks only about what conjurer has proven survivable. If you cannot state why A precedes B, the order is decoration.

5. **Read each selected SKILL.md in full before acting.** Engaging an ability you have not loaded is naming it, not using it — the work will carry the skill's name and none of its method.

6. **Announce the engagement in one line.** "En: specialist → conjurer — name the double-fire mechanism, then close its failure modes." Skills, order, reason — one line, so the routing decision is auditable by anyone reading the transcript. When the vow ability is installed, follow the announcement immediately with its vow block: the line says which disciplines act, the vows say what the acting work swears not to do.

7. **Honor the switch.** When the user has made nen the session baseline, steps 1–6 run on every incoming request. "nen off" suspends the protocol immediately — plain assistance, no skill loading, no shape lines — until "nen on". Acknowledge each transition in one short line and nothing more.

8. **An empty table on a RECURRING need goes to hatsu, with the occurrence evidence attached.** A one-off gap gets handled plainly and noted; the second and third occurrence make it hatsu's case. En hands over the artifacts and stays out of the forge.

## Worked trace

Request: "checkout webhooks are double-charging customers, the endpoint is slow, and we owe partners an explanation." The field's reading, posted before anything loads:

```
shape: three things must be TRUE afterward —
  1. a charge survives webhook redelivery exactly once → survival under
     failure proven                                    → conjurer
  2. the endpoint's latency moves, measured            → a number moved
                                                       → enhancer
  3. partners get an explanation that lands            → words that land
                                                       → emitter
  gate: nobody can yet say WHY the provider re-fires   → mechanism unnamed
                                                       → specialist first
keyword trap declined: "slow" would fire enhancer first — but a number
locked before the double-fire mechanism is named measures a handler that
is about to change shape.
```

The engagement line:

```
En: specialist → conjurer → enhancer → emitter — name the provider's
redelivery mechanism; close its failure modes with idempotency; then lock
the endpoint number on the corrected handler; partners hear only what
conjurer has proven survivable.
```

Each SKILL.md is read in full before its turn. Specialist finds the provider re-fires any webhook not acknowledged within 10s — the handler renders the invoice PDF inline, so the slowness and the double charge are one defect. Conjurer keys the charge idempotently and moves to ack-then-process. Enhancer baselines the old handler (p99 11.4s), re-measures the corrected one (p99 180ms), commits the bench. Emitter's partner note states the idempotency guarantee, not intentions. Mid-session, the switch:

```
user: nen off — quick one, what does HMAC on a webhook actually do?
assistant: Nen off — suspended. HMAC signs the payload with a shared
  secret so you can verify the sender and reject tampered bodies.
user: nen on
assistant: Nen on — resuming the stack at enhancer.
```

## Anti-patterns

- **A skill engaged because a word matched while the work belonged elsewhere.** The transcript shows "benchmark" firing enhancer on a request to write release notes for a benchmark tool — profiling discipline summoned to a writing task whose output-test was words that land, and no number anywhere in the ask.
- **Every skill engaged at once "to be safe".** The engagement line lists the whole pack; the work exhibits none of their methods. A field spread over everything senses nothing — total coverage is the same reading as zero.
- **Silent routing.** The work carries a discipline's fingerprints — a baseline here, a failure table there — but no engagement line exists, so nobody can audit whether the choice was sensed or stumbled into.
- **An ability named but never loaded.** The engagement line cites a skill whose Method the output visibly ignores — conjurer named, no failure mode enumerated, no policy chosen. The name was worn, not used.
- **"nen off" in the transcript followed by a skill firing anyway.** The switch was acknowledged and then ignored; a field that cannot be retracted is not under the user's control, and every future engagement line is doubted for it.

## Done means

- The one-line problem-shape restatement present in the transcript before any skill loads.
- An engagement line naming each engaged skill and the reason for the order.
- Every engaged SKILL.md demonstrably read — its Method visible in the work produced, not merely its name in the line.
- Stack order justified by a stated dependency, not by alphabet or by which word appeared first in the request.
- Every "nen off" / "nen on" transition acknowledged in one short line and honored in behavior.
- Recurring needs the table cannot route handed to hatsu with occurrence evidence — never absorbed, never quietly done by en itself.
