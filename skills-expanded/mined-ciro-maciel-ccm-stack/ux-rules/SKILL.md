---
name: ux-rules
description: Screens that never wait on slow jobs, never call a failure empty, use one loader then skeletons, keep the record in the URL. Use for any screen or list.
---

# Screens that respect people

Each rule below exists because a real screen broke it and a person noticed.

## Never wait on a slow job

No click waits on AI, an import, an export or anything slow. Create the record first, do the work in the background, and take the person straight to the screen of the thing being made: its skeleton, a visible "working" state, each part appearing as soon as it is ready. A spinner inside a modal that waits for a model call reads as broken.

## One loader per navigation, skeletons after it

The session check may show one loading indicator. After that, every wait is a skeleton: the shape of what is coming, where it will appear. Two loaders in a row read as two loads, and changing the second one's size or color does not fix the sequence. The "loading" flag starts as `true` and turns off on both success and failure; starting it as `false` creates a frame where the list is empty and nobody has read it.

## Empty, failed and loading are three different states

"No items yet" while loading is false. "No items yet" after a failed request is also false. Every list distinguishes:

- **loading:** skeleton;
- **failed:** what went wrong in plain words, and "Try again";
- **truly empty:** what to create first.

If old data is already on screen when a refresh fails, keep showing it and report the failure beside it; do not replace what the person is reading with an error.

## Lists load as you scroll

Load a small page and keep loading as the person scrolls. No "Show more" button, no fetching a thousand rows up front.

## The chosen resource lives in the URL

The selected project, site or record is part of the route (`/projects/{id}/settings`), never only in component state or local storage. Reload, share and back all keep working. Route by stable id, not by a position or a per-account counter.

## Forms

Errors appear under the field that caused them, focus moves to the first one, each field is checked when the person leaves it, and an error clears as soon as the value is right. What the person typed survives any error.

## Do not cut to fix

A request to fix order, spacing or background never authorizes removing content. Solve the layout and keep everything.

## The simplest thing for the person

When two designs both work, pick the one with fewer steps and fewer choices for the person, apply it, and say why in one line. Do not hand them a menu of options.
