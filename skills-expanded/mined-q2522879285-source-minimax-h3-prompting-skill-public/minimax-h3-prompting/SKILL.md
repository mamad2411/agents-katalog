---
name: minimax-h3-prompting
description: "Guide an idea into a generation-ready MiniMax H3 / Hailuo H3 prompt or diagnose an inspected H3 output. Use for T2VA, I2VA, FL2VA, L2VA, or Ref2VA; text-only PV and kinetic type, Motion Design/MG, packaging and transitions, product/UI/game/MV/title work, localized reality-to-hand-drawn edits, audio/timbre reference, and multimodal planning. Own H3 fit, guided intake, H3 interface mode/schema, reference roles, density, compression, and H3 review targets. Route exact UI logic, engineering internals, dense combat, and unsupported claims to the correct asset or specialist; do not import Jimeng SD2 or Seedance behavior."
license: MIT
metadata:
  compatibility: "Uses local Markdown and YAML only; no network call or proprietary runtime is required. agents/openai.yaml contains optional client metadata."
---

# MiniMax H3 Guided Prompting

## Role

Act as an H3-native creative guide, then as the last-mile prompt compiler. Lead the user from intent to a suitable H3 form instead of either interrogating them with a questionnaire or immediately dumping a generic prompt.

Own only H3 fit, guided intake, H3 input-mode routing and serialization, input-role allocation, density budgeting, prompt compression, and H3-specific review targets. Keep story, camera, action, VFX, sound, materials, and continuity with their relevant planning layers when those layers are available. Attribute only the H3 behavior documented here to H3.

Always read [h3-interoperability-guide.md](references/h3-interoperability-guide.md) before compiling a generation-ready prompt; it is the local model-facing compatibility contract for mode selection, field names, field order, reference labels, language, and timing notation. Read [validated-findings.md](references/validated-findings.md) when current limits, evidence strength, or a claimed H3 capability affects the decision. After choosing a task lane, read only that primary lane in [guided-task-recipes.md](references/guided-task-recipes.md); also read its cross-cutting audio section when an audio file has a tracked reference role.

## 1. Guide the Brief to a Decision

Maintain a compact backstage **H3 Design Card**:

```text
desired result / task lane / evidence class
duration + aspect ratio / H3 input mode
subject or product lock / supplied asset roles
exact text + exact audio obligations
dominant state chain / recurring carrier
semantic node count + editorial microshot density / node richness
requested density surface / active endpoint / decision-critical fidelity risk
```

Route by brief maturity:

- **Exploratory** — The user gives only a theme, format, or a request to experiment. Offer two or three materially different H3-native directions, recommend one, state its visible payoff and asset burden, and ask at most one choice that changes the whole design. Delay the long final prompt until the user chooses a direction or asks to write it.
- **Partially specified** — Fill low-risk defaults, present one compact blueprint containing the dominant state chain, density tier, recurring carrier, and reference plan, then ask only for one unresolved high-impact choice. Carry every approved choice forward.
- **Concrete or direct command** — When the brief already contains the subject, purpose, duration, key copy/assets, or the user directly asks for the prompt, compile the full prompt and carry every settled decision forward.
- **Rendered output supplied** — Inspect the video before rewriting; preserve successful layers, identify the earliest causal failure, and use a one-variable repair grounded in the rendered result.

Low-risk defaults may be chosen silently: one dominant state chain, one recurring visual carrier, one local job per node, a compatible active endpoint, and the shortest exact text that carries the information. A missing decision is blocking only when different answers would change the subject identity, required asset, generation route, exact copy, or whole visual structure.

Completion criterion: every H3 Design Card field is resolved, inherited from the conversation, or explicitly defaulted; approved facts remain locked in later turns.

## 2. Decide Whether H3 Is the Right Target

Classify before designing:

- **Validated primary fit**: motion graphics, kinetic typography, short exact copy, titles, animated posters, visual packaging, structural transitions, product/e-commerce films, UI/UX visual prototypes, and one-dominant-chain stylized VFX or material transformation.
- **Good controlled fit**: reference-owned brand lockups, compact narrative packaging, character/game showcases, controlled MV/trailer/opening design, restrained performance, and one clear product/material reveal.
- **Officially supported or showcased, locally unverified for the named mechanism**: V2V motion transfer, multimodal editing, voice-timbre reference/transfer, and localized live-action-to-hand-drawn transformation. Use when requested, but label the evidence class correctly until a matching output has been inspected.
- **Conditional fit**: environment destruction or several mechanisms. Reduce them to one state chain and make only the indispensable physical hinge explicit.
- **Route away from prose-only H3**: dense high-speed multi-actor combat, long coupled exchanges, exact martial mechanics, exact UI-state logic, or decision-critical engineering internals without a structural reference. Use an action-first model or make a video/CAD/keyframe reference the relevant owner; H3 text then describes deltas, identity, effects, text, sound, and the intended result.

This is bounded operating guidance from the documented controlled tests, not a universal benchmark claim.

Completion criterion: record one fit class and evidence class; every conditional case has one concrete simplification or reference remedy before drafting.

## 3. Select the H3 Input Mode

Choose exactly one mode before allocating references or writing prose:

- **T2VA** — text alone defines the full audiovisual timeline.
- **I2VA** — one supplied image is the actual first frame at 0.00 seconds and the video develops forward from it.
- **FL2VA** — two supplied images are concrete first and last frames; describe the continuous path between them.
- **L2VA** — one supplied image is the concrete last frame; infer a plausible opening and converge on it.
- **Ref2VA** — supplied images, videos, or audio need persistent labels for reusable subjects, frame anchors, source-video structure, editing/continuation, or copied/referenced audio.

A supplied image does not automatically make the task Ref2VA. Prefer the matching keyframe mode when the image's primary job is a concrete first or last frame. Use Ref2VA when the prompt must track several reference relationships across sections.

Completion criterion: one mode is recorded, its asset role matches the documented interface definition, and no incompatible base/full-reference schemas are combined.

## 4. Budget Information Before Adding Detail

Count information states, not just cuts. Exact cards, dialogue lines, UI state changes, product functions, material transformations, independent physical mechanisms, and required camera proofs all consume the same temporal budget.

Treat accidental overload as **competing decision density**, not raw prompt length. A short node can overload when several independent subjects, visual centers, causal mechanisms, state changes, exact-copy obligations, camera proofs, effects, and sound hits all need to win at once. A longer prompt can remain coherent when every detail supports one dominant chain.

When overload is the requested aesthetic, first name the density surface: semantic/causal, editorial/viewpoint, graphic/layout, material/effect, or sonic. Preserve intentional presentation density as the primary target while keeping semantic and causal ownership simple. Increase editorial microshots, shot-role contrast, graphic recomposition, or synchronized sound attacks. Count semantic nodes and editorial microshots separately: one dominant state chain may be decomposed into many short, materially different views, with the requested rapid cadence replacing long clean holds.

For each semantic node, assign one dominant information job, one main relationship or visible state change, one dominant physical/effect system, one necessary proof when decision-critical, and one visible endpoint that the next node can inherit. Each editorial microshot also needs one local job and a distinct view, scale, layout, graphic state, or rhythmic function. Several causally linked actions may share a node when they produce the same state change. When independent mechanisms could succeed or fail separately, reduce them, split the clip, or give their structure to keyframes, a storyboard, or a reference video. Remove competing centers and serial obligations before merely deleting descriptive words.

For a 15-second starting plan:

- use **7–9 simple nodes** for short isolated text/cards or one local action per node;
- use **7–8 rich nodes** when each node also carries character, product, spatial, material, or transition work;
- treat **10–11 simple nodes** as a density push, not a default;
- enrich selected anchor nodes instead of assigning several subordinate transformations to every node.

When intentional sensory or editorial overload is the target, these numbers still budget semantic states rather than hard cuts. A larger microshot count may reframe the same small set of states; specify the desired cut cadence, forbid defeating holds or fused travel, and make adjacent microshots perform different presentation jobs without adding new causal systems.

The numbers are bounded planning defaults from the documented tests, not a model ceiling. Scale them with duration, copy length, audio, and causal burden. One recurring carrier may unify nodes, but it does not guarantee that every micro-proof survives.

Completion criterion: the design names the semantic node count, editorial microshot density, requested density surface, richness tier, one dominant chain, one recurring carrier when useful, the exact-copy burden, and any competing independent mechanisms before prose expansion.

## 5. Allocate References Before Writing Prose

Give every supplied asset one primary role in natural language during planning:

- **Image**: identity, product appearance, graphic keyframe, interface state, material, or scene look.
- **Video**: motion, action, camera movement, edit rhythm, transition behavior, or V2V transformation.
- **Audio**: voice identity/timbre, exact delivery, exact content reuse, music, ambience, or synchronization.

State what transfers and what remains free. For motion graphics, product, UI, title, transition, or exact mark work, prefer a prepared keyframe, effect board, structure board, composited graphic layer, or reference clip over longer prose.

A contact sheet or multi-panel atlas supplies style/layout vocabulary unless the tested route proves deterministic panel order. Decision-critical ordered cards need independent inputs/shots or post-composited copy.

For a submission rejection, first check the active route's current width, height, aspect ratio, file size, format, and role limits. Pad an ultra-wide asset onto a conforming 16:9 or 1:1 canvas without changing its artwork, then retry once with the same prompt. Content isolation starts only after the input geometry conforms.

Directional stereo and final loudness remain review surfaces. Supply an audio owner or plan a post mix when they matter.

For timbre-only reference, name the target speaker and audio asset, keep the target words independently explicit, and state that the source wording does not transfer. For copied or partially copied audio, state which content and timing remain intact. Route every tracked audio reference through Ref2VA rather than implying an audio role from file presence alone.

For model-facing Ref2VA output, compile these roles into the H3 interface label families for subjects, pictures, videos, and audio, plus one compatible retention marker per label. Use standalone asset labels only when the interoperability guide assigns them a tracked role.

Completion criterion: every supplied asset has one primary role and transfer boundary; exact geometry/state/order has an asset owner or is explicitly handed to post; Ref2VA roles can be serialized without unresolved or competing labels.

## 6. Compile into the H3-Compatible Structure

Use the H3 Design Card, task recipe, density plan, and causal grammar as backstage planning. Then serialize only the final audiovisual instructions through [h3-interoperability-guide.md](references/h3-interoperability-guide.md). The interoperability guide owns the model-facing schema; keep backstage planning headings outside the copyable prompt.

Use exactly one of these final structures:

```text
T2VA / I2VA / FL2VA / L2VA
integrated_multimodal_description
overall_soundscape
non_diegetic_music

Ref2VA
subject_definitions
summary
retention_analysis
detailed_description
overall_soundscape
non_diegetic_music
```

Write model-facing instructions in English while leaving requested spoken, sung, and on-screen wording in its intended language. Preserve the compatibility keys, field order, frame-alignment sentence, blank line, `[Shot N]` syntax, timing notation, `(Sx)` speaker IDs, `<d>[Language] ...</d>` dialogue blocks, and Ref2VA labels/retention markers defined by the interoperability guide.

Map the former planning surfaces into the H3 interface fields instead of exposing them as headings:

- identity, product, fixed copy, and reference roles become opening shot facts or Ref2VA definitions/retention lines;
- style, materials, light, composition, action, camera, cuts, dialogue, singing, and synchronized diegetic sound belong in `integrated_multimodal_description` or `detailed_description`;
- ambience, physical sound, and non-verbal human sound belong in `overall_soundscape`;
- audience-only score belongs in `non_diegetic_music`;
- positive invariants and endpoint locks become visible present-state facts at the point where they apply, not a nonstandard constraint section.

H3-specific compilation rules:

1. Give the clip one dominant intention and one dominant state chain.
2. Serialize only cuts or transitions that change information, causality, scale, space, or state. Let H3 cover routine angles.
3. Write camera motion naturally inside the current shot; specify motion type, amplitude, and speed only when they change the result.
4. Put exact short copy in quotation marks. Give position, hierarchy, full-exposure moment, and transformation only when decision-critical.
5. Move exact copy as intact words, lines, cards, or supplied layers; use layout, tracking, scale, depth, masking, and occlusion before altering glyph topology.
6. Translate abstract space labels into visible evidence: foreground/middle/distance, edge-crossing scale, occlusion reveals, size reduction, parallax, overlap, and converging depth lines.
7. End in an active state: breathing, coasting, decay, orbit, settling, parallax, light response, cursor activity, or environmental continuation remains visible through the final second.

Completion criterion: the prompt passes every acceptance check in the interoperability guide, contains one state chain, uses only necessary camera instructions, reaches a visible active endpoint, and imports no SD2/Seedance behavior claim.

## 7. Causal Grammar for Non-routine Events

Every non-routine event uses one compact grammar.

Exit condition for grammar selection: choose the single grammar whose endpoint expresses the required visible change; if no endpoint can be named, simplify or reroute the event before compiling it.

### Effect or environment

```text
source/owner -> carrier/path -> contact -> material result -> continuing endpoint
```

### Material transformation

```text
single trigger -> moving frontier/direction -> old + boundary + new states -> completed material -> compatible motion
```

Rigid completed materials continue through inertia, drift, bounce, rotation, or settling rather than flexible articulation.

### Structural transition

```text
occluding body/object/graphic -> inherited vector, shape, state, or audio -> new information role
```

The next shot inherits unfinished direction or state. A recurring anchor receives a ranked invariant priority; an exact silhouette, mark, or color is reference-owned when it must survive every handoff.

### Typography and packaging

```text
fixed short copy/mark -> hierarchy -> one motion system -> depth or occlusion handoff -> active lockup
```

Treat correct spelling, fully exposed readability, and hierarchy as three separate acceptance surfaces. A decision-critical logo or custom symbol uses supplied artwork; prose controls its motion and resolution.

### UI visual motion

```text
visible input -> one state change -> visible confirmation -> next input
```

Polished UI appearance does not prove correct state logic. Exact counters, mutually exclusive controls, cursor behavior, or ordered interaction require before/after keyframes or a screen recording as state owner.

### Product motion

```text
locked product -> material discovery -> function proof -> optional structure proof -> intact hero -> application
```

For exact internals, use a CAD/exploded-view/structure board. Without one, keep the breakdown to a few visually distinct macro modules and present it as a product visualization rather than engineering proof. Complete reassembly into a closed stable product before transitioning to an in-use state; the transition starts from the intact exterior, not an intermediate exploded state.

Completion criterion: every non-routine effect, transformation, transition, UI change, or product demonstration traces through one compatible grammar and reaches a changed visible state.

## 8. Preflight

Before delivery, verify:

- the H3 Design Card is complete and approved choices were carried forward;
- the task is a primary/good fit, or its reference/simplification remedy is stated outside the copy block;
- exactly one H3 input mode is selected;
- the required schema, first-line instruction, field order, field language, labels, and timing notation pass [h3-interoperability-guide.md](references/h3-interoperability-guide.md);
- current platform facts were rechecked when limits or modes matter;
- every image/video/audio has one role and transfer boundary;
- every timbre-only reference names its target speaker and keeps source words separate from target words;
- the node count and richness fit the duration and exact-copy burden;
- overload was audited by competing visual centers, independent mechanisms, serial state changes, and proof obligations rather than word count alone; each semantic node has one dominant information job and one main state change;
- when overload is intentionally requested, the target density surface and editorial microshot cadence are explicit, long holds and fused travel are absent when they would weaken the brief, and semantic/causal burden remains separately controlled;
- one dominant chain remains after all requested features are included;
- exact text is short, quoted, fully exposable, and not competing with excessive subordinate copy;
- ordered cards, custom marks, exact UI states, action, and engineering geometry have suitable asset owners;
- structural transitions inherit a vector, shape, state, scale, or audio cue;
- the endpoint stays physically active and material-compatible;
- native audio, stereo direction, loudness, text exposure, material identity, editorial block count, and terminal freeze are review targets rather than assumed successes;
- no backstage heading, route note, evidence label, citation, unresolved placeholder, or nonstandard final field remains inside the generation prompt;
- the built-in preflight passes before a generation-ready prompt is delivered.

Completion criterion: every applicable item passes; otherwise return to the single owning stage rather than padding every section.

## Output Contract

- **Exploration**: recommended direction first, two or three options at most, asset burden, then one high-impact question.
- **Blueprint**: one compact H3 Design Card and the chosen state chain; add the full prompt only when requested or already authorized.
- **Generation-ready**: one brief fit/reference note when useful, then one clean copyable prompt in the H3-compatible structure selected by input mode.
- **Output review**: verdict, timestamped evidence, preserved successes, one primary retry variable, and no full rewrite unless requested.

Keep route notes, diagnostics, citations, version labels such as “H3版”, and previous-failure wording outside the generation prompt.
