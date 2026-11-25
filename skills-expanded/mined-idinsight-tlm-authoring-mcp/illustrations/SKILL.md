---
name: illustrations
description: Construire et vérifier le dossier d'illustration d'une leçon — prompt, vignette seule, bande assemblée, marqueur de réponse — en contrôlant l'image produite plutôt que le prompt, et sans rien régénérer sans accord explicite. À utiliser quand on parle d'illustrations, d'images, de vignettes, de dossiers d'illustration, ou de « refaire les images ».
---

# Illustration dossiers

## The pipeline, in order

1. **Prompt** — written from the section's own guidance and the document's image formatter, never
   from habit. Fetch them: `walk_document_section` returns both.
2. **One cell, at 1:1** — produce a single image first and look at it. If it is wrong, the prompt is
   wrong, and every image made from it will be wrong the same way.
3. **Assembled band** — compose the cells into the band the layout expects.
4. **The answer, recorded** — once the band is settled, read it enlarged and record which cell is
   correct (`answerCells` at `attach_image`, or `edit_nodes` on `metadata.answerMark` for a
   picture already attached). The server reads the band's cell count off the file itself and
   records it; a count you give that the picture contradicts is refused, so say the cell you SEE
   and let the count come from the picture. **Nobody draws the check mark**: the server draws the teacher's
   copy at render time from that record (a media entry with `mark:'answer'`), so a change upstream
   cannot orphan it, and the pupil's file stays plain. A band that admits two answers is reported,
   not decided.
5. **Attach** — once an image is settled, upload it (`create_media_upload_url` — all of a lesson's
   files in one call with `relPaths`, one confirmation — then the PUTs) and
   record it in the graph with `attach_image`: the lesson or activity it illustrates BY NAME, the
   name a page will place it by, and a one-sentence description of what it shows. The description is
   not decoration: it is what a reviewer reads beside the activity's text to catch a picture that
   contradicts its words. From then on every section covering that content lists the picture under
   `pictures` in `walk_document_section`, and a page places it as a `media` entry `{name, nodeId}`.
   A picture that is only briefed, not drawn, is attached with `commissioned:true`; its file is
   later uploaded to the path the node names, and the graph is not touched on delivery.

Each stage is checked before the next begins. Skipping to a full set and checking at the end means
discovering a prompt error twenty images later.

## Naming

**The document's image formatter states the convention — read it there.** What a file name is made
of differs between documents, so a name written down here would be one subject's rule wearing the
plugin's clothes.

What does not vary, and is procedure rather than subject: **a version increments and nothing is
overwritten**, so a regenerated image never silently replaces the one an expert already approved.
A new version is a new file, so it is attached again (a new node, a new name) and the old node is
retired with `delete_nodes`; approval is what publishing the draft means, as for any text. Both are
draft edits, audited and undoable.

## Check the produced image, never the specification

An illustration that satisfies its prompt exactly can still be wrong on the page: the wrong size,
cropped, unreadable at print scale, or showing something the text contradicts.

**Look at the image.** Dispatch the `illustrateur` subagent to build the dossier and verify it; it
returns a structure — which images exist, which are missing, which failed a check and why, which cell
each band's answer is — not a description of what it made. **Run it in the background** while the
page is composed: its audit is what its minutes buy, and nothing in the composition waits on it
until the review step, where its findings are read before anything is delivered.

There is one class of error no text-based check will ever catch: a **mismatch between text and
image**, where the words and the picture each make sense and disagree with each other. Two wrong
answer keys reached production that way. Catching it needs eyes on the rendered vignette beside its
text. That is this skill's job, and it cannot be delegated to a linter.

## A contact sheet per lesson

Assemble one sheet showing every image for the lesson together. Errors of consistency — a character
who changes appearance, an object family that drifts, a style that shifts halfway — are invisible
one image at a time and obvious on a contact sheet.

## Regenerate nothing without an explicit go-ahead

Regeneration is not free and it is not neutral: it can replace an image the expert has already
approved.

So: **present a list** of what you propose to regenerate and why, one line each, and wait for a yes.
Not "I'll refresh the images" — the actual list. A go-ahead covers the images on that list and no
others.
