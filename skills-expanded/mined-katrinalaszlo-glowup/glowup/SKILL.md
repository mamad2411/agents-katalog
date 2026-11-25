---
name: glowup
description: Improve or review a CLI, developer tool, or agent skill using product-design principles. For terminal tools, improve Display, Flow, or Both with real Before, Proposed After, and verified Final After evidence while preserving machine contracts. For skills, improve discovery, instructions, safety, or validation. Use for "glowup my CLI", "improve this terminal interface", "improve this tool's UX", "glow up this skill", "audit this skill's interaction design", or a pre-launch design review.
---

# glowup — design the developer experience

Design for the person directing the work, the agent interpreting it, and any program
consuming the result. Inspect first, ask only consequential questions, preserve contracts.

## Route before loading depth

**Review-only:** an audit or review stays read-only. Run Capture and the relevant
checklist, then deliver ranked findings: file and line, observation, reader impact,
concrete proposed fix, and observable check. Do not create fixtures, edit files, preview
implementation, or enter a finish-action loop. If the user asks to apply findings,
their concrete proposed fixes become the Proposed After; retain that approval.

For changes, infer the target and focus, then load only the matching route:

| Target / focus | Read |
|---|---|
| CLI **Flow**: commands, prompts, options, feedback, recovery, next steps | [cli-flow.md](references/cli-flow.md) |
| CLI **Display**: hierarchy, spacing, alignment, scanability, emphasis | [cli-glowup.md](references/cli-glowup.md), [canon.md](references/canon.md), [display-preview.md](references/display-preview.md) |
| CLI **Both**: Display + Flow | Both routes above |
| Agent skill: discovery, instructions, safety, validation | [skill-design.md](references/skill-design.md) |

Reviews use the relevant checklist; display preview mechanics apply only when proposing
a visual change. Skill and Flow runs do not load visual or finish mechanics by default.
Open other references cited by the target only when needed to verify its instructions.
For program-only or CI-only paths, improve discoverability, schemas, structured errors,
noninteractive behavior, and safe retries; do not add human decoration. Do not rewrite
a well-performing skill for prose style. If no reader or task benefits, explain and stop.

## Keep the user oriented

Change runs follow `Capture → Choose → Preview → Implement & Verify → Compare & Finish`.
Show a compact marker at the start, stage changes, meaningful waits, and resumption:

```text
Glowup 2/5 · Choose
Now: Choose what to glow up.
Next: I’ll show the Proposed After before editing.
```

Use these names consistently; do not narrate every tool call or claim implementation
while previewing. A review uses `Capture → Findings`, without implying edits will follow.
If blocked, name the current stage and what allows progress.

## Capture

Identify the target, common task, readers, and affected layer: policy guides, contracts
make failure detectable, enforcement blocks invalid behavior. Infer from the request
and repository instead of opening with an intake interview.

Read enough docs, source, tests, and existing fixtures to execute safely. Keep opening
orientation read-only and single-agent: no project writes, new fixtures, reviewers, or
root-cause investigation before focus selection. For a CLI, capture one safe human path
with its command, data, terminal dimensions, output, and interaction; do not exercise
every subcommand yet. If setup is needed, use an existing fixture or user-supplied
screenshot or transcript. For a skill, read its whole `SKILL.md` and only task-relevant
references; capture how an ordinary fresh session discovers, interprets, executes, and
validates it, using the skill playbook's evidence rules.

If the target is ambiguous, ask one short question naming detected candidates. If none
exists, ask for a CLI, tool, or skill directory. Do not install or download a target
merely to preview it without explicit approval.

Authenticated, networked, destructive, production-affecting, privacy-sensitive, or costly
execution needs explicit authorization covering the resources and consequences. Reuse
that consent for baseline, implementation, and verification commands within its scope.
Ask again only when the resource, consequence, cost, or authority materially changes.

## Choose and bound the change

Infer focus from the request or accepted findings. If a CLI focus remains open, show
captured evidence and a recommendation, then ask **What should I glow up?** with exactly
**Display**, **Flow**, and **Both**, using the route descriptions above. Do not substitute
findings or visual directions for these options. Question options get a label and short
description, not a preview panel. Reproduce findings or mark them as hypotheses.

For a skill, infer **discovery**, **instructions**, **safety**, or **validation**; ask
one consequential question only when needed. Before any proposal or approval, state:

- **Boundary:** Display is presentation only; Flow changes human interaction; Both
  combines them. A skill pass preserves purpose and tool contracts. Broader authority
  or product scope requires approval.
- **Success:** the observable task improvement and affected-reader checks that would
  falsify it. For each recommendation, name the reader, protected constraint, adaptation
  to this medium, and test. Port the reason behind a heuristic, not its surface rule.

Preserve established voice and user taste. Use the selected playbook for proposal detail.

## Preview and approval

Show the captured **Before** beside or immediately before the complete **Proposed After**
in normal conversation. CLI comparisons use the same command, data, and dimensions;
Flow uses transcripts, Display uses the rendering gates in its playbook. Skill previews
use instruction excerpts plus expected behavior on a representative request.

Focus selection does not authorize edits. Ask **Apply**, **Revise the preview**, or
**Change focus** when approval is still missing. Explicit prior approval of concrete
changes, including accepted audit fixes, already satisfies this gate: identify those
changes as the proposal and proceed. Ask again only for consequential scope changes or
unresolved design choices. Revising is repeatable; keep previewing until the user
applies or stops, never implement to escape an iteration.

## Implement & Verify

Restate the approved target, pass, boundary, preserved contracts, and next stopping point.
Capture relevant baselines before editing; skip unrelated paths. For CLI changes these
may include first run, help, an error, empty/success state, piped and structured output,
and exit paths. Use existing fixtures, temporary configuration, sandboxes, and dry runs.
Apply the smallest coherent change. Keep routine single-command work single-agent;
separate reviewers are useful only when complexity or risk justifies them.

Rerun the real human path with the same command, data, and dimensions. Iterate if the
result misses the approved direction. A non-TTY, simulation, or fallback run does not
verify an interactive path; report the gap and obtain a real terminal capture when it
matters. Remove disproved findings from the change count and say they were not bugs.
Skill structure and fresh-session behavior checks follow
[skill-design.md](references/skill-design.md); self-review alone is not independent
validation. If a primary fresh session cannot run, report
**implemented; behavior validation pending** with the fixture and exact resume step.

### Never break the machine path

- Keep logic and machine behavior intact in a Display pass. Return from every
  structured format before human rendering; `--json` and other machine formats remain
  byte-identical. Flow preserves documented inputs, structured outputs, exit meanings,
  and noninteractive paths; test intentionally changed human behavior for compatibility.
- Enable ANSI only on a TTY unless a documented force-color flag explicitly requests
  it. Piped output stays plain by default; respect `--no-color` and `NO_COLOR`.
- Compare piped stdout and structured output byte for byte, exit codes by value, and
  stderr on its original channel with equivalent meaning. Approved Flow changes may
  improve human error wording while preserving structured errors and error meaning.
- Test interactive, noninteractive, piped, and structured paths independently. TTY is
  a transport hint, not proof the caller is human.

## Compare & Finish

Deliver **Before**, **Final After**, and **Changes and checks**, in that order. The CLI
Final After is a fresh implemented capture using the original task, data, and dimensions,
never the preview. For a skill, show the before fixture, changed instructions, and
fresh-session behavior comparison, or the explicit pending-validation handoff. Include
confirmed changes, preserved contracts, unverified paths, and disproved hypotheses.
Do not finish with raw After output and an implementation summary alone.

Reuse this evidence for a concise PR summary when requested. If the user already asked
to finish, commit, share, or publish, complete authorized actions and stop; do not add
another mandatory choice. Otherwise briefly offer relevant additive next actions:
**Export visual**, **Share Before/After**, **Commit changes**, **Another glowup pass**.
Visual actions apply only when there is a visual to export. Saying done or choosing
nothing ends the run. Read [finish.md](references/finish.md) only for requested finish
actions; load [export-share.md](references/export-share.md) only for Export or Share.
