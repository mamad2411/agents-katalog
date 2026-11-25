---
name: legibify
description: "Make agent output legible. Explains a pull request, a commit or a complex part of a codebase in layers a human can check: a 3-line verdict, a numbered walkthrough in plain controlled English with file:line anchors, a blast-radius diagram, and a single-file interactive explainer (graph with drill-down, node passport, guided walkthrough, comprehension checks that export to Anki or Obsidian). Optional video. Use when opening a PR, reviewing someone else's PR, handing work off for review, or when asked 'explain this PR', 'what does this change do' or 'how does X work in this repo'. Separates observation from hypothesis and lists what still needs verification. Not for the critical review of the diff itself, and not for changelogs. Inspired by Andrej Karpathy's post on making LLM output understandable."
---

# legibify

A reviewer's job is to understand, verify and decide, not to decode. legibify orders its output as a ladder: plain prose, then a diagram, then interactive HTML, then video. Climb only as far as the cheapest rung that makes the change verifiable.

## Modes

- **`explain`** (someone else's PR, or a past one): get the diff (`gh pr diff <n>`, `git diff main...HEAD`, or the commits) and produce the explainer for the reviewer.
- **`attach`** (a PR this agent opens): generate the explainer and put it in the PR body between `<!-- legibify -->` markers, so it can be regenerated without duplicating.
- **`topic`** (no diff): explain a system, flow or concept in the repo ("how does auth work", "what happens when a message hits the queue"). The model comes from reading the code, not from a diff, and L2 becomes a system diagram instead of a blast radius. Everything else stays the same.

## Input

The diff plus the minimum context: title, commits, touched files, and the surrounding code needed to follow the flow. Do not explain from the diff alone when the context changes its meaning, for example a caller outside the patch. In `topic` mode the input is the question plus the relevant area of the repo. Every node and claim still traces to `file:line`, and anything inferred is marked as inferred.

## Layers (L0 and L1 always, L2 when there is structure, L3 and L4 on request)

- **L0 · verdict**: 3 lines or fewer in chat: what it does, why, and the biggest risk. Chat gets nothing more; the details go to the artifact.
- **L1 · walkthrough**: the story of the change in numbered steps, in execution order (not alphabetical file order), each anchored to `file:line`. Plain controlled English, see [references/ste100.md](references/ste100.md).
- **L2 · blast radius**: the system with what the change touched drawn on top, in green, amber and red, with the new path numbered. See [references/blast-radius.md](references/blast-radius.md). Draw it when the PR changes topology, contracts or flow. A 20-line fix does not need it.
- **L3 · interactive explainer**: a graph with drill-down, a passport per node, a guided walkthrough, deep links and comprehension checks. Single-file, offline, dark by default (people read these at night) and usable on a phone. It is never drawn by hand: the agent writes a JSON model and `player/build.mjs` builds the HTML, see [references/player.md](references/player.md). On request, or when the PR is large (more than 15 files). The UX contract is in [references/format.md](references/format.md).
- **L4 · video (opt-in)**: delegated to the `showtime` skill if it is installed. The agent writes the spec (beats = L1 steps, narration in controlled English) and the machine renders it locally. For demos, onboarding or big changes. Never a substitute for the diff.

The full artifact structure and the PR body template are in [references/format.md](references/format.md).

## Fidelity contract

- **Observation is not hypothesis.** "The handler now retries 3 times" is an observation from the diff. "This fixes the prod timeouts" is a hypothesis and is labeled as one.
- **A view, not evidence.** The explainer summarizes. It ends with a "To verify" list: claims that need the source, such as tests actually run, runtime behavior, real config, or migrations over existing data.
- **Nothing without a trace.** Every claim points to a `file:line` in the diff or the code. What does not trace is dropped or marked as inferred.
- **Before and after.** If the change alters a flow, say how it worked before. The reviewer should not have to rebuild the previous state.
- **Never invent selectors, endpoints or names.** If a name is not literally in the diff or the code, it does not exist.

## Tone

Short sentences, active voice, one term per concept, no filler, no em dashes. Write in the language of the repo. The player UI ships in English and Spanish (`meta.lang`).

## Delegation

Extracting the diff and grouping files into concerns can go to a cheaper model: pass `git diff` and ask for the walkthrough in the format of references/format.md. The verdict, the observation/hypothesis split and the "To verify" list are reviewed by the strongest model available or by a human, because they are what the reader uses to decide.

## Sources

Where each layer comes from and what was taken from each project: [references/sources.md](references/sources.md).
