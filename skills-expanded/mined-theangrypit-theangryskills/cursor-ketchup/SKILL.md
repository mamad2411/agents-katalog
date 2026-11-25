---
name: cursor-ketchup
description: "Use when the user explicitly requests $cursor-ketchup to catch up on verified changes in this chat since their last message, with every pending decision made clear and actionable."
disable-model-invocation: true
---

## Runtime selection

Before runtime-dependent work, read [execution selection](references/runtime/selection.md). In a verified T3 host follow [the T3 contract](references/runtime/t3.md) and its method reference; the inline section below is the native Codex branch, not literal T3 dispatch. Outside T3, native Codex follows that inline branch unchanged. If the host is ambiguous or a required capability is unavailable, report the gap; a permission refusal never authorizes switching branches.

## Native Codex branch

# Ketchup

Catch the user up on what changed in this chat since the last message they wrote before `$cursor-ketchup`. Notifications and subagent results are not their messages. Assume the user remembers their last message and nothing after it.

Use `cursor-bro`'s voice, not its task (read that installed skill if available): plain words, short sentences, no jargon. Say what changed for the user, not how you did it. Leave out hashes, file paths, commands, build numbers, and test counts unless the user needs one to act. Call each PR, branch, or agent by a name the user would know. Give context for facts that need it.

## Gather what changed

Keep project state read-only. Make visuals only from evidence already available. Do not change code, start a service or job, or post anything. Collect your own work since that message, subagent reports, and messages from others in this chat. Check current state for each PR, CI run, or agent this chat touched. Check every number against its source and say when you correct one.

An action item is a decision or step only the user can take, including product choices, approvals, irreversible actions, or missing access. Include every item still waiting, even if raised before the user's last message. Work you can do yourself is not an action item. Do not invent calls. An unasked irreversible step gets one action line and no visual.

For each item awaiting a decision, gather its link, user impact, evidence, risk, and your recommendation. Write "unknown" when a needed fact is unavailable. Leave out links you do not have.

## Write the reply

Open with one short sentence naming what waits on the user, or that nothing does. If nothing happened and nothing waits, say so and stop.

Spend words on decisions, not the story. Keep the account of what happened under 100 words, not counting visuals. Give each pending item about 30 words, and let the reply grow with the item count. Never drop items or make them too small to stay under a total word limit.

Show what happened with screenshots or videos first, then any diagram that explains a change. Follow the workspace's selected presentation surface. Use a visual when it makes the change easier to understand. Then give one short bullet per requested item with its result and whether it is done, running, failed, or unchecked. Each bullet must stand alone. Name bugs found and fixed. Do not repeat action-item details. Add at most three short lines that change what the user knows, then one line for work you can still do.

List every action item. For one item, use one bullet with the call, your recommendation, user impact, evidence, and risk. When one call covers several items, give the call and recommendation once, then a separate bullet for each item, riskiest first, with its link, name, impact, evidence, and risk. State an item's recommendation only when it differs. Say what waiting costs only when it is more than delay.

For a choice between options, name every option the work considered, its benefit, cost, and current state. If screenshots already show options, put benefits and costs beneath them. A link can add depth, but the reply alone must let the user decide.

## Visuals

A visual is a screenshot, video, Mermaid diagram, chart or diagram from an available native visualization tool, or a generated image. A Markdown table is not a visual.

Draw how systems connect, a PR stack or dependency chain, a before and after, or options side by side when a picture is clearer. Never draw a status list, an action-item list, or disconnected boxes. Do not repeat facts in text and visuals.

Keep visuals easy to scan, with at most six boxes and eight words per box. Use plain labels. Embed screenshots and videos inline when the change is visible. If none exists, say "No screenshot yet" in that item's summary bullet and state what changed on screen. Draw only from observed facts. Link only artifacts that exist.
