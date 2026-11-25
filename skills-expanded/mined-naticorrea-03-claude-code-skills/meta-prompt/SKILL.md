---
name: meta-prompt
description: Builds ready-to-paste Meta AI (Muse Spark) prompts for reading Instagram, Facebook, and Threads directly. Describe a research goal (find micro-influencers or ambassadors, find videos to react to, monitor brand mentions, scan niche trends, check saturation, mine comments, tear down a competitor, verify handles, study a creator's voice before a pitch) and this skill asks a few clarifying questions, fills the variables (niche, follower range, brand, time window, etc.), and outputs a copy-paste prompt for the meta.ai app. It also hands out the Hook Machine, a full multi-turn workflow that analyzes a creator's top reels, extracts why the winners win, builds a grading rubric, then generates, grades, and rewrites hooks. It never calls Meta AI itself and never invents capabilities. Trigger on "/meta-prompt", "build a meta ai prompt", "meta prompt for <goal>", "find microinfluencers on instagram", "find videos to react to", "monitor mentions of <brand>", "what's trending on instagram for <niche>", "hook machine", "analyze a creator's hooks", "build a hook rubric", or any request to research Instagram creators, content, or brands that would be run inside Meta AI.
---

# Meta AI Prompt Builder

## What this is

Muse Spark (Meta AI, used at meta.ai) can read public Instagram, Threads, and Facebook content directly, which Claude cannot. But it is a closed chat app with no API or MCP, so Claude cannot run it. This skill does the next best thing: it interviews the user about their research goal, picks the right prompt from the library, fills in the specifics, and hands back a strong, paste-ready prompt to run inside meta.ai.

**Output is always a prompt for the user to paste into meta.ai. This skill never fetches Instagram data itself and never pretends to.**

## Grounded capabilities (do not exceed these)

Only build prompts around capabilities Muse Spark actually has:
- Reading and semantic search over public Instagram, Threads, and Facebook posts (content since Jan 2025)
- Finding creators by niche, topic, location, and follower count
- Reading captions, comments, and engagement to surface trends
- Studying a creator's feed and voice
- Finding brand mentions across the three platforms

If a user's goal needs something outside this list (TikTok or YouTube, guaranteed exact view/engagement numbers, scheduling, posting, anything on private accounts), say so plainly and offer the closest grounded prompt instead. Do not invent a capability to satisfy the request. Every generated prompt already forces meta.ai to self-report what it cannot do, which is the honest backstop.

## The library

The prompt templates live in `prompts/library.md`. Read it when this skill runs. Current entries:

| ID | Use case |
|----|----------|
| A1 | Micro-influencer / ambassador finder |
| A2 | Existing-fan creator finder (already posted about the brand) |
| A3 | Handle verification + profile snapshot |
| B1 | Reaction / stitch target finder (videos to react to) |
| B2 | Niche trend scan |
| B3 | Saturation & gap check |
| B4 | Comment mining (audience questions and pain) |
| C1 | Brand mention monitor |
| C2 | Competitor account teardown |
| D1 | Creator voice study before a pitch |
| E1 | Hook Machine (full multi-turn workflow, delivered whole, not variable-filled) |

**E1 is different from the rest.** It lives in `prompts/hook-machine.md`, not in `library.md`, and it is not a single-shot template. It is a complete multi-turn workflow the user works through inside meta.ai. When the goal is hook analysis or hook writing off a real creator's reels, hand out the entire `hook-machine.md` code block unchanged (do not fill variables, do not trim steps, do not strip the STEP 0 capability check). Say the honest caveat noted in that file: the workflow depends on Muse Spark returning transcripts and view counts, which is unverified, and STEP 0 forces meta.ai to admit what it cannot pull before anything else runs.

## Flow

1. **Take the goal.** The user describes what they want to learn or find on Instagram, in their own words.

2. **Match to the library.** Map the goal to one or more template IDs.
   - If it clearly matches one, name it and proceed.
   - If it could match two or three, use a multiple-choice question to let the user pick (they prefer concrete options over open questions). Offer the closest 2 to 4 IDs plus a short description of each.
   - If it matches nothing grounded, say so and suggest the nearest fit.
   - Some goals are naturally a **sequence** (e.g. "help me start an ambassador program for a client" = A2 then A3 then D1; "do Phase 0 research for a new client" = A1/A2 + A3 + B2 + B3). When so, say which prompts you'll build and in what order, then build each.

3. **Interview to fill the variables.** Read the chosen template's `Fills:` line and ask only for the variables it needs. Prefer multiple-choice questions with sensible defaults where the option set is knowable (time window, follower range bands, count). Ask open questions only for genuinely free-text fields (niche, brand name, handles). Batch the questions so it is one quick round, not a drip.
   - Sensible defaults to offer: window = last 30 days, count = 5 to 10, follower range for micro-influencers = 5k to 50k. Always let the user override.

4. **Fill and output.** Substitute every `{{variable}}`. If a variable changes the shape of the output, update the template's `<example>` row to match. Output the finished prompt in a single code block, with a one-line instruction above it: "Paste this into meta.ai (logged in with the relevant Instagram account)." If you built a sequence, output each prompt in its own labeled code block, in run order.

5. **Preserve the template standard.** Every template is engineered to the standard in `prompts/library.md` (directive first line, numbered steps, self-test as step 1, inputs in a named tag, explicit output format, a one-shot example, honesty rules, no em dashes). Do not flatten it when filling. Never strip the step-1 self-test; it is the honesty mechanism.

6. **Offer the loop-back.** After output, remind the user: run the first prompt, and if meta.ai reports it cannot pull a field (view counts, comments, transcripts), paste that back and the prompt can be adjusted or the goal re-routed to a grounded template.

## Rules

- Output prompts only. Do not attempt to fetch Instagram data or claim you did.
- Do not fabricate Muse Spark capabilities. Stay inside the grounded list.
- Keep the user's variables exactly as given. Do not silently change a niche or follower range.
- No em dashes in anything you write or generate (user rule). The templates already follow this.
- If the user wants a use case that recurs, note that it could be added to `prompts/library.md` as a new template, but do not edit the library without being asked. Any new template must follow the template standard (see `prompts/library.md`).
