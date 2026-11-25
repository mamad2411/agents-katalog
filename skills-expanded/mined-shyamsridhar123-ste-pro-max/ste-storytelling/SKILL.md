---
name: ste-storytelling
description: "Author evidence-linked explanations, decision briefs, research digests, and incident reviews with reader control. Uses native STE or host tools and standalone templates. Not for a short prose rewrite or automatic video export."
---

# STE storytelling

Use one reviewed story source with native STE tools or ordinary host tools. A story is a way
to organize evidence, not a reason to invent a dramatic arc or stronger conclusion.
See [native checks](../ste-promax/references/automatic-policy.md). This skill adds
no host-tool restrictions or manual STE approval steps.

## Author the source

Read [the example guide](../../examples/showcase/README.md) for starting points.
Apply [STE-ProMAX](../ste-promax/SKILL.md) writing priorities:
fidelity, requested scope/format, clarity, then style.

Choose the audience, one question, and a purpose:

| Purpose | Useful structure, not a mandatory plot |
| --- | --- |
| `explanation` | Concrete example, intermediate states, mechanism, understanding check |
| `decision-brief` | Decision question, evidence, options/proposal, unresolved conditions |
| `research-digest` | Research question, attributed findings, methods/limits, qualified implications |
| `incident-review` | Observed order, impact, hypotheses, proposed corrections; no invented closure |

Register sources with stable IDs and precise locators. Classify claims as
`observation`, `attribution`, `inference`, or `proposal`. Attribution names its
speaker; inference states its basis. Link claims to sources and beats to claims.
Source registration and reference validation do not establish truth, entailment,
causation, approval, or authenticity.

Keep material uncertainty in the claim and story, not only in a final chat note.
Review unlinked summary/beat prose and custom narration as carefully as linked
claims. A valid ledger cannot prevent an author from adding unsupported prose.
Unused claims remain reviewable; do not hide contrary evidence through beat
selection, ordering, captions, or emphasis.

Use optional native diagrams/charts only where they explain the beat. Read
[ste-visual-docs](../ste-visual-docs/SKILL.md) for visual-specific constraints.
Sequence order is not duration; categorical line spacing is not elapsed time.

Let readers choose guided progress or all content. Add a question when it tests
a specific likely misunderstanding. Supply a supported answer or leave it open;
do not invent feedback or call a click evidence of learning.

## Author from the installed plugin

Read the [showcase guide](../../examples/showcase/README.md) and use the
release-brief or retry-lab starter for the appropriate structure. Resolve the
plugin root from this skill's location, not the user's working directory.
Adapt the starter with `ste_write_artifact` or ordinary authoring tools into a new
workspace `artifacts/` directory. Native STE checks need the configured runtime;
ordinary authoring does not. No frontend build is required.
Never overwrite the installed plugin or execute untrusted source markup.

Use [the shared low-friction workflow](../ste-promax/references/low-friction-workflow.md).
Infer a reasonable purpose and audience from the request; briefly name a material
assumption rather than launching an intake form. Do not ask for an output folder,
theme, or choice among media the user did not request. Ask only when missing
evidence or a consequential choice would change the result.

Keep the original source, source/claim register, and material qualifications
with the output. Review the story in its actual HTML form and provide a readable
prose equivalent. Only generate additional companions when requested or useful.

For explicitly requested deterministic story compilation or batch workflows,
the [native engine](../../docs/AUTHORING.md) produces HTML, prose, storyboard,
narration, and evidence companions. Its validations are not implied for
host-authored output. A complete manifest is not a semantic review.

## Prepare narration only when requested

Narration requires a separately available media capability; native plugin
installation does not install voices or encoders. Review the script before
generating or pairing audio. If the native media capability is available, use
`ste_prepare_story_media` or run `narrate` with the
original story JSON in a different fresh output directory. Select one route:

```text
python "<bundle-root>" narrate "<absolute-story.json>" --output-dir "<absolute-new-media-dir>" --voice "<installed-voice-name>"
python "<bundle-root>" narrate "<absolute-story.json>" --output-dir "<absolute-new-media-dir>" --audio-dir "<absolute-audio-dir>"
```

The supplied-audio directory contains `<beat-id>.wav` for every beat. Inspect
actual non-silent PCM audio and measured duration; listen and compare the speech
with the reviewed script, visual order, and qualifications. Do not silently
install a voice or move private text to a service.

Split content that fails the media fit checks without removing qualifications.
Inspect long-caption warnings. Sequence-stage pacing is not measured event time
or verified speech-to-message alignment.

Preparation does **not** export an MP4. If an encoded video is requested, use a
separately available export workflow and verify the actual movie. Report missing
capabilities or unperformed checks instead of calling a preview an export.

## Delivery gate

Compare all formats with the same evidence ledger. Exercise Previous/Next,
outline links, all-content mode, answer disclosure, keyboard use, narrow layout,
no-JavaScript reading, and print output. Record any untested surface.

Return the requested artifact with material source/review gaps. Stop at the
requested medium; successful rendering does not demonstrate learning,
accessibility conformance, publication, or a completed decision.
