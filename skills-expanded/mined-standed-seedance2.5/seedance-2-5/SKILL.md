---
name: seedance-2-5
description: Seedance2.5 skill for AI video production. Use whenever a user mentions Seedance2.5, Seedance 2.5, AI video, short videos, marketing videos, product demos, talking-head videos, video prompts, storyboards, scene cards, B-roll, video repair, or continuity QA. Turn supplied scripts, briefs, assets, footage notes, or approved storyboards into grounded Seedance-ready plans, prompts, and checks; do not invent product claims, fabricate people, or claim platform controls without checking the active Seedance interface.
---

# Seedance2.5

Plan and prompt video production from material the user can verify. This skill produces an editable production plan and prompt pack; the active Seedance interface determines the generation controls and renders the final media.

## Capabilities

| Route | Minimum input | Deliverable |
| --- | --- | --- |
| Narrative / short drama | Script or storyboard | Scene ledger, clip plan, continuity-safe prompts |
| AI short video | Topic, hook, or short script | Beat sheet, visual beats, video prompts |
| Marketing / product video | Product brief plus approved claims/assets | Claim-safe visual plan, shot list, prompts |
| Talking-head video | Speech script, transcript, or footage notes | B-roll and cutaway plan, prompts, edit notes |
| Product demo / explainer | Feature facts and product references | Demo sequence, proof beats, prompts |
| Repair / continuation | Failed clip plus the desired correction | Focused repair prompt and preserved state |

Read `references/video-routes.md` for the chosen route. Read `references/route-templates.md` to produce a route-specific brief and prompt preamble. Read `references/production-contract.md` before any multi-clip production task. Read `references/prompt-patterns.md` while writing or repairing prompts.

## Honest boundary

- Preserve supplied facts, dialogue, people, products, and reference assets. Ask rather than fill gaps with plausible fiction.
- Build prompts, plans, and QA; do not claim to render the final video, clone a person, create a voice, or use a platform feature unless the active interface supports it.
- Require authorization for reference images, videos, voices, performers, and brands. Do not imitate protected characters or living performers without permission.
- Treat the active Seedance UI/API as authoritative for duration, aspect ratio, audio, editing, and reference-asset controls.

## Workflow

### 1. Lock the production brief

Record only what changes the output: target audience and platform, source material, approved facts/assets, delivery format, sound policy, and whether the work is `draft` or `locked`.

For marketing work, use only claims supported by the user’s brief. For talking-head work, keep the supplied language intact and plan supporting visuals rather than rewriting the speaker’s voice.

### 2. Select the smallest route

Do not force every request through a screenplay workflow. A 15-second product demo needs proof beats; a talking-head edit needs B-roll timing; a short drama needs a scene ledger. Use the relevant route template and omit unrelated deliverables.

### 3. Plan before prompting

Make the visible story clear before adding style words. Each clip needs a purpose, an opening state, one playable change, and an ending state. Carry confirmed state forward; do not reset people, props, location, lighting, or product details between clips.

### 4. Write prompts in production order

Use the structure in `references/prompt-patterns.md`: references, start state, camera/action, dialogue/sound, end state, and only necessary constraints. Prefer observable direction over vague labels such as “premium” or “cinematic.”

### 5. QA the pack

Validate the route brief first:

```bash
python3 scripts/validate_video_plan.py --route short-video path/to/plan.md
```

For a multi-clip pack, run:

```bash
python3 scripts/validate_prompt_pack.py path/to/prompt-pack.md
```

Replace `short-video` with `marketing`, `talking-head`, `product-demo`, or `narrative` as appropriate. Resolve errors. Treat warnings as a prompt to manually check whether the next clip has enough inherited state.

## Delivery

Return only the route-relevant artifacts: brief, fact/asset list, beat or clip plan, prompt pack, and unresolved assumptions. For multi-clip work, include the validator result.
