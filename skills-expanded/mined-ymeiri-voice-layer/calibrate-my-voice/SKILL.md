---
name: calibrate-my-voice
description: "Build or refresh the local voice-layer profile used by write-in-my-voice from user-approved evidence. Use only when the user explicitly asks to calibrate, train, set up, refresh, rebuild, or update their voice-layer profile from sources like git commits, PRs, code reviews, Slack, chat exports, sent email, Google Docs, Confluence, design docs, RFCs, ADRs, issue comments, agent session transcripts, or pasted samples. Do not invoke for ordinary rewrites or drafts."
---

# Calibrate My Voice

Create or update a local voice-layer profile for the `write-in-my-voice` skill. Calibration is a consented setup workflow, not a hidden preprocessing step.

## Defaults

- Profile path: `~/.config/voice-layer/voice-profile.md`.
- Template: `assets/voice-profile.template.md`.
- Raw samples: do not retain them after analysis unless the user explicitly asks.
- Exact examples in the profile: keep short and only when the user approves.
- Assistant-generated text: do not treat it as the user's voice unless the user explicitly accepted or edited it.
- Retention promises apply to the generated profile and files this skill creates. The active agent, connector, or host application may still persist session transcripts or tool-result artifacts outside the profile. Before reading connector/private sources, disclose this limitation and, where possible, prefer metadata-only inventory, scoped reads, temporary files outside the repo, and cleanup after analysis.

## Consent gates

Before reading private sources, state the source, scope, and what will be retained. Ask for confirmation if the user has not already been explicit.

Start every calibration with source negotiation unless the user already gave a complete, explicit source plan and explicitly excluded all other sources.

The negotiation must let the user choose between pasted samples and agent-collected samples. If tools or connectors are available, offer them as options without using them yet.

If using connectors, MCP tools, hosted agents, or agent session exports, explain that raw source content may be visible to the active agent and may be persisted by the agent host as session or tool logs even when the voice profile itself keeps only derived patterns. Do not imply that `derived-patterns` retention erases all external session artifacts.

Do not use a hard-coded product menu as the final menu. First inventory what the current agent can plausibly collect from, then build the source menu from that local capability set.

Never:

- scrape broad workspaces without scope,
- treat other people's writing as the user's voice,
- treat assistant output, generated docs, or rejected drafts as the user's voice by default,
- include private messages as raw profile examples by default,
- write samples into the repo,
- continue when the user declines a source.

If the user asks to mimic, clone, or calibrate from another private person's
voice, refuse briefly. Offer to calibrate from the user's own messages or from
an explicitly authorized shared style guide instead. Include both alternatives
in the refusal using those terms. Keep the refusal short and do not use em
dashes.

## Wizard workflow

1. Establish scope.
   - Inventory available collection capabilities without reading private content: connected apps/tools, visible MCP connectors, obvious local CLIs, local git repos, and user-provided export paths.
   - Present a source menu before collecting anything.
   - Ask which sources the user approves, what scope/date range applies, and whether exact short examples may be retained.
   - Include "pasted samples only" as a first-class option.
   - Include agent-collected options only when the current agent has plausible tools/connectors/CLIs for them. Name the actual available tool when known.
   - Prefer recent, user-authored samples from 2 or more channels.
   - If only one channel is available, label the profile as channel-skewed.
   - If the user approves only one source, continue with that source and record the limitation.
2. Gather samples.
   - Prefer PR/MR descriptions and review comments over local git commits for technical communication style when those sources are available or connectable.
   - Use local git commit messages only when the user explicitly approves commit-message samples, or when PR/MR sources are unavailable or declined and the user accepts commits as a fallback. `scripts/collect_git_samples.py` can collect commit-message samples.
   - Never treat local git commits as PR descriptions, PR review comments, or issue comments.
   - Use available connectors or CLIs only inside the scope the user approved.
   - If an approved source returns only metadata, zero usable user-authored samples, or a tool/auth failure, do not count it as collected. Tell the user what happened and ask whether to retry, connect/authenticate, provide an export or paste, skip that source, or proceed without it.
   - Store any temporary raw files outside the repo, delete them after analysis, and tell the user if the agent host persisted separate session/tool artifacts that this skill cannot automatically remove.
   - For exports or pasted samples, ask the user to identify channel and approximate date range.
   - For agent sessions, use only user-authored turns, user corrections, explicit style preferences, and final drafts the user accepted or edited.
3. Filter.
   - Keep only user-authored text.
   - Remove signatures, quoted replies, bot output, generated text, boilerplate, logs, code blocks, and copied docs.
   - For agent sessions, treat rejected assistant drafts as negative preference signals, not as style samples.
   - For docs, keep user-authored structure and prose. Exclude generated docs unless the user accepted or substantially edited them.
4. Analyze.
   - Extract sentence rhythm, vocabulary, openings, closings, punctuation texture, hedging, pushback style, formatting, channel deltas, recurring phrases, repeated model-shaped scaffolding, and aversions.
   - Extract voice-layer facets: stable voice, requested or observed vibes, audience adaptation, documentation style, cultural/language baseline, and agent-session signals.
   - For documentation, capture TL;DR habits, section order, depth, context level, alternatives, risks, open questions, validation, citations/links, tables, diagrams, and decision records.
   - For agent sessions, capture how the user asks, corrects, rejects, accepts, and defines quality.
   - Distinguish observed habits from aspirational preferences the user states.
5. Write the profile.
   - Use the template structure and the profile contract.
   - Summarize patterns. Avoid storing raw corpora.
   - Mark source coverage, date range, limitations, and confidence.
   - Mark agent-session signals separately from final-message voice samples.
   - Keep the profile validator-compatible: if exact examples were not approved, the Examples section must contain only `No approved examples.`.
   - With derived-pattern retention, do not put exact user-authored phrases in other sections either. Paraphrase recurring phrases, openings, closings, typos, emoji habits, idioms, and relationship-specific jokes as tendencies unless the user approved exact examples.
   - Wrap long prose lines in the profile body. Do not write large unbroken paragraphs or raw pasted text into the profile.
6. Confirm.
   - Show the profile summary and ask what is wrong or missing.
   - Apply corrections. The user is the ground truth.
   - Before saying calibration is complete, look for `scripts/validate_profile.py` in the current working directory, the nearest parent repo root, and the skill package root. If found, run it against `~/.config/voice-layer/voice-profile.md`.
   - If validation fails, treat it as blocking. Repair the profile and rerun the validator until it passes, or ask the user how to proceed.
   - If no validator can be found, say exactly where you looked and ask the user to run the validator if they have the repo checkout. Do not call the profile finalized.

## Source adapters

Read `references/source-adapters.md` before using a source you have not used in this session.

Read `references/source-menu.md` before the first user-facing calibration question.

Read `references/profile-contract.md` before writing or editing the profile.

## Done criteria

Calibration is complete when:

- the profile exists at the target path,
- it records source coverage and limitations,
- it contains no unapproved raw private excerpts,
- the user had a chance to correct the profile,
- the profile passes `scripts/validate_profile.py` when that validator is available,
- validator failures are repaired before completion is claimed,
- `write-in-my-voice` can read it on future turns.
