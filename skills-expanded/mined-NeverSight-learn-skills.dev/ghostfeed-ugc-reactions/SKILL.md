---
name: ghostfeed-ugc-reactions
description: Create UGC reaction videos over MCP the way the dashboard does. Get a template, render an avatar into the source pose (the first frame), get the user to approve that frame, then animate it. Two families, clone the reference motion or a prompt. Refined from real founder dogfooding.
---

The tools enforce the hard rules server-side: every write is workspace-scoped,
credits are charged and reported for you, the duration limits are applied on
import, and the flow is fixed at two phases (frame, then video). This skill makes
you read the user's intent and run the flow well on top, and it makes the frame a
real checkpoint.

This is a thin remote control for the dashboard flow, not a new engine. You do
not reinvent anything. You quicken the click path over chat: pick a template,
render the frame, get a yes, animate it.

## Library-first casting

For every reaction request, prefer Ghostfeed's reusable clip libraries before
making a custom first frame. Follow this order unless the user explicitly names
or supplies an exact source:

1. Search `list_reaction_templates` for a suitable opening pose in the
   workspace's owned and stock templates. Judge candidates by `opensOn`, then
   use `motion` only to decide whether the source performance is also useful.
2. If no template is suitable, search `list_inspiration_reactions` the same way.
3. Only after both libraries have no reasonable opening-pose match, fall back to
   `referenceImageUrl` from an avatar photo, user reference, or external image.
   Tell the user briefly what the library lacked and why a custom frame is
   necessary.

A custom motion request does not imply a custom first frame. A template or
inspiration can supply only the opening composition while a prompt mode animates
the approved frame from the user's words. Do not paste the library clip's
`motion` into the video prompt unless the user asked to reproduce that motion.
Do not search the web or browse avatar photos for a source until the two
Ghostfeed libraries have been checked.

## The flow

1. Get a source, following the library-first order above. A template is a source
   motion clip. Four ways in:
   - Use one that exists: `list_reaction_templates` (stock plus the workspace's
     own). You cannot watch the motion, so if the user must choose, describe the
     options from name and category, do not pretend to have seen them.
   - Import from a link: `import_reaction_template` with `sourceUrl` (a TikTok or
     Instagram link).
   - Import a local file: `request_reaction_upload` returns a short-lived
     `uploadUrl`. PUT the raw file bytes to it with the given Content-Type (for
     example `curl -T clip.mp4 -H "Content-Type: video/mp4" "<uploadUrl>"`), then
     `import_reaction_template` with `uploadedFileUrl` set to the returned
     `fileUrl`.
   - Reuse an inspiration clip: `list_inspiration_reactions`, then pass its id to
     `generate_reaction_frames` or `import_reaction_template`. It is auto-saved to
     the workspace as a template first and the new template id is surfaced.
   Import is async and free. Poll `get_generation` until terminal. `succeeded`
   means ready. `needs_action` means the source is 30 to 120 seconds and must be
   cropped in the dashboard first, so open the `dashboardUrl` and hand that step
   to the user. Over 120 seconds is rejected.

2. Render the first frame. `generate_reaction_frames` with the source (a
   `templateId`, an `inspirationId`, or a `referenceImageUrl`) and one or more
   `avatars` (names or ids, up to 10). It makes ONE frame per avatar. Poll each
   returned generation until `succeeded`. The frame image is `output.url` and
   `output.id` is the `frameId` you carry into the video phase. It uses
   `gemini_flash` unless the user asks for another model (`list_image_models`).

3. Get the frame approved. This is the milestone, treat it as a hard stop. Show
   the user the rendered frame or frames and get an explicit yes that the avatar
   looks right BEFORE any video. The frame costs a fraction of a video, so this is
   where you catch a bad render cheaply. If a frame is off, `regenerate_reaction_frame`
   with that generation's id for a fresh take. Never start a video on a frame the
   user has not approved.

4. Animate the approved frame. `generate_reaction_video` with the approved
   `frameIds` and a `mode`. Poll each generation until its state is terminal:
   `succeeded`, `failed` or `canceled`. The clip is `output.url`. (The board in
   `list_reaction_videos` calls the same finished state `complete`; a generation
   never reports `complete`, so a client waiting for that word waits forever.)

5. Hand over. Report the spend and the dashboard link (see Money and link).

## Reading intent: clone or prompt

There are two families of video, and you pick by understanding what the user
wants, not by matching a keyword. Ask a short clarifying question when it is
ambiguous.

- Clone the reference motion. When the user wants the avatar to move like the
  reference video, use a clone mode. Name it explicitly: `one_to_one_standard` is
  the default WITHIN the clone family, but omitting `mode` altogether gives you
  `seedance_2_0_fast`, a prompt mode at 1.5 credits per second instead of 1. It
  runs Kling motion-control. No prompt, and the duration follows the source clip. Clone
  needs a frame that came from a template, because that template supplies the
  motion. A frame made from a reference image or a plain prompt has no motion to
  clone, so those go the prompt route.
- Animate from a prompt. When the user describes the motion they want, use a
  prompt mode (default `seedance_2_0_fast`) and pass a `prompt`. Duration is auto
  unless the user asks for a specific length.

`list_reaction_video_modes` has every mode with its per-second cost, so offer the
premium or higher-quality options with prices when the user wants better than the
default.

## Batches

Give `generate_reaction_frames` several avatars and you get one frame generation
each. Poll them together with `list_generations`. After the user approves the
frames they want, pass just those `frameIds` to `generate_reaction_video`. The
user can approve some and have you regenerate others, that is normal.

## What stays in the dashboard

You do bulk creation. Everything else is a human-in-the-loop step in the
dashboard: cropping a 30 to 120 second import, renaming or deleting templates and
videos, and editing a finished clip (speed, text overlays, download). Do not try
to do those over MCP. When an import lands `needs_action`, send the user to the
`dashboardUrl` to crop, then continue.

## Workspaces

Call `list_workspaces` first and keep the chosen slug or id. Reads may omit
`workspace` and use the credential's pinned read default. Every write requires
`workspace`; never infer it from whichever workspace the user last opened. A typo
fails with remediation listing the valid names, slugs, and ids.

## Money and link

Importing a template costs nothing. Frame generation reports an
`estimatedCreditCost` and charges as the frames render; video generation reports
the real `creditsSpent` and `creditsRemaining`. When a response carries
`creditsSpent` and `creditsRemaining`, state them on their own line, numbers from
the tool result:

```
💳 {creditsSpent} credits spent, {creditsRemaining} remaining
```

Reads and lists get no money line. `get_credits` has the balance if the user
asks.

When a response carries `dashboardUrl`, end your reply with the door on its own
line:

```
🔗 {dashboardUrl}
```
