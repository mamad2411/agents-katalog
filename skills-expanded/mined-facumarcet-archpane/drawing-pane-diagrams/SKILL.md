---
name: drawing-pane-diagrams
description: Use when drawing, redrawing or editing a diagram with the archpane `diagram` tool, or when a user asks to diagram, visualize, map or draw a system, flow, architecture or build plan in the side pane.
---

# Drawing pane diagrams

## Overview

The pane is a narrow terminal column (~60–110 columns) that someone reads while they keep talking to you. A diagram is readable there when it answers **one question** with **few boxes and one direction of flow**. A system bigger than that becomes several named diagrams, never one big one.

## What a pane diagram is

- **One question.** Either an overview ("how does sync work end to end") or one stage in detail ("what does the bulk path do").
- **5–10 boxes, at most 4 on any level.** The widest level sets the width: four boxes is already ~90 columns.
- **One direction.** Edges run from trigger to outcome, mostly one level down. An edge that skips levels draws a long line beside everything in between.
- **Boxes are the steps of this flow.** A store, external API or piece of infrastructure gets a box only when it is the subject or the endpoint of the flow. Otherwise it goes in the `note` of the box that uses it ("writes DynamoDB; calls Shopify Admin API").
- **Groups: none, or 2–3 stages.** A group is a stage of the flow holding 2+ boxes on consecutive levels (`realtime`, `bulk`). Don't group by kind (`storage`, `external`): `kind` already says that, and such groups scatter into single-box borders.
- **Few edge labels.** Label an edge only when the arrow alone is ambiguous (`slow`, `v2`, `legacy`), and keep it to 8 characters or fewer. Leave plain calls and enqueues unlabeled.
- **Short box text.** `label` is 18 characters or fewer, `kind` is one word, and the details (flags, stores, retries) go in `note`.

## A system bigger than that

1. **Overview:** a diagram named `<topic>` with one box per stage, 8 boxes or fewer. Set each stage box's `detail` to `"<topic>/<stage>"`: the box is marked ▸, and clicking it opens that diagram.
2. **Detail diagrams:** one per stage, named `<topic>/<stage>`, each following the shape above. Show what the stage connects to as the first or last box.
3. **Draw every diagram you link.** The tool lists linked diagrams that aren't drawn yet.
4. **What to tell the user:** the overview is open. Clicking a ▸ box opens its detail, and the breadcrumb at the top leads back.

## Plans and builds

- Every box you'll build gets `status`: `done` if merged, `planned` otherwise.
- Existing components the plan touches get **no** status.
- Leave uncommitted or stretch items out of the diagram and mention them in your reply.
- Move statuses with `patch` as the work lands.

## After every `set` or `patch`

The tool answers with the laid-out size and, when it won't read well, warnings with fixes. **If there's a warning, fix it before you reply:** split, drop a box, or move a dependency into a note. Then `set` again. Done means the tool says it fits the pane.

## Common mistakes

| Mistake | Fix |
|---|---|
| Every component of the system in one diagram | An overview plus detail diagrams |
| Storage and external groups | Name the stores and externals in notes; group by stage |
| An edge for every data dependency | Keep the control flow; describe the rest in notes |
| A label on every edge | Labels only where the arrow is ambiguous |
| Replying while the tool still warns | Fix it and `set` again first |
