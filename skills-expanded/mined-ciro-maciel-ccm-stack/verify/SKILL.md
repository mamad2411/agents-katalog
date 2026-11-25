---
name: verify
description: Prove a feature the way a user reaches it, with a feature map (one file per feature) and a verification guide. Use after UI changes or to prove behavior.
---

# Map every feature, prove it like a user

An agent arriving cold does not know what "working" means in this product. The feature map writes it down once, from the user's side, so any agent can prove behavior instead of trusting a green API.

## The verification guide

Create `docs/verify/README.md` in the project, written for the next agent:

- **Launch:** the exact command that starts the app for verification, and how to tell it is usable (not just that a process answers). Include seed data and teardown.
- **Health check:** one read-only check that answers "is this instance worth driving?": right version, our port, valid session.
- **Drive:** how to operate it the way a person does: browser automation, a terminal session, plain HTTP for services. Use stable handles (accessible names, roles, routes), never CSS classes or positions.
- **Evidence:** what to capture (screenshot of the action and of the result, the row written, the message sent) and where it is kept.
- **Cleanup:** stop only what you started; never delete the evidence.

## The feature map

`docs/verify/features/README.md` lists the features; each has its own file with four sections:

```markdown
# Publish a post

## Parts
Publish now, schedule, unpublish.

## How a person gets there
Dashboard > Posts > the post > "Publish". Also through the API: POST /posts/{id}/publish.

## Driving it
Open /posts/{id}, press the button named "Publish", wait for the "Published" badge.
Proof: the public page shows the post with a stamp unique to this run.

## Gotchas
The test account only. The CDN may serve the old page for a few seconds: retry the read.
```

Start with the three to five features people use most. When a feature has several entry points (screen, API, link), proving one of them is an incomplete proof.

## Prove, never weaken

Run one mapped journey end to end before calling the guide done. If seed data is missing for a journey, the journey fails and the reason goes into Gotchas. Never loosen a journey to make it pass.

## Keep it honest

When the app changes, update the map in the same change. Periodically compare the map with the routes and screens in the code, and fix what drifted.
