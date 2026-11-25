---
name: mage-character-consistency
description: |
  Keep one character the same across a series of images and video shots with
  Mage, including profiles, back views, and full turns. Locks the details that
  must not change (sides included), makes a full-body master and a
  front-side-back sheet on Mango 4, and for video a 360° turntable on Lemon
  that rides along as a reference video; then shoots each scene on the right
  route, checks every result against the references, and fixes drift by its
  cause. Use when: "same character in every shot", "my character keeps
  changing", "character drift", "the face changes in my videos", "the back of
  her head is different every time", "the tattoo switches sides", "360
  turntable of my character", "turnaround video", "a series with the same
  character". NOT for: saving a portrait as an @handle (use mage-characters),
  a sheet image alone (mage-character-sheet), scripted dramas
  (mage-short-drama), product UGC ads (mage-ugc-video), or real people
  without their consent.
license: MIT
compatibility: Requires the Mage connector (https://mcp.mage.space/mcp) and a Mage account with Gems. Face crops, frame checks, and frame-rate work need a shell with ffmpeg; without one, the skill saves whole images and asks the user to review video.
metadata:
  author: mage-space
  version: "0.0.0" # x-release-please-version
---

# Mage Character Consistency

Image and video models remember nothing between generations. A prompt alone reinvents the person every time, and one front-facing reference pins only the front: whatever it doesn't show (the back of the head, the far arm, a logo on a backpack) is invented again in each shot, and left and right details swap. This skill shows the model every angle once, gives each reference one job, and checks each result before the next one builds on it.

Three rules run through it:

1. **Lock it.** 3 to 5 details that never change, written once and pasted word for word into every prompt.
2. **Turn it.** A full-body master, a front-side-back sheet, and, for video where the character turns, a 360° turntable. Fix mistakes in these first: every later shot copies them.
3. **Tell it.** Every prompt says what each reference is for and what to ignore (the grey studio, the sheet's panels).

## Before you start

1. **Mage tools:** `list_models`, `get_model`, `estimate_cost`, `generate`, `get_request`, `list_characters`, `create_character`, `list_references`, `create_reference`, and `create_upload` for local files. If they are missing, ask the user to connect Mage (Claude: Customize → Connectors → Add custom connector, `https://mcp.mage.space/mcp`; Claude Code: `/mcp` to sign in if the Mage plugin is installed, otherwise `claude mcp add --transport http mage https://mcp.mage.space/mcp`; others: https://www.mage.space/mcp), then wait.
2. **Inputs are links:** https URLs of the files themselves, data URLs under about 3 MB, uploads from disk (`create_upload`, when you can run commands; pass the `url` it returns, never the signed upload URL), or earlier Mage results. Files attached to the chat never reach Mage: ask for a direct link. A cloud session needs `cdn3.mage.space` and `storage.googleapis.com` reachable to download results or upload files.
3. **Consent.** Only build a real person's likeness with that person's consent, and never to impersonate anyone.

## UX rules

1. **Reuse first.** Check `list_characters` and `list_references` (every page) and compare the images, not only the names. Use a master, sheet, or turntable the user already has; make only what is missing.
2. **One plan, one price.** List the stages the route needs, price each paid step with `estimate_cost` using the exact config you will send, show the total, and wait for a yes. Video is the expensive part: every second of Lemon reference video bills like a second of output, again in every scene that uses it. Before the turntable exists, `estimate_cost` can't see it, so add its seconds to each scene at the scene's per-second rate (720p: 168 Gems; a 3 s scene with a 6 s turntable is 1,512, not 504). Once it exists, price each scene again with its URL in `videos`, and ask before any scene that costs more than you quoted.
3. **Say the route and its trade-off** before generating, and report the route you actually ran.
4. **Pilot before a batch:** one scene, checked, before the rest. A pilot that passes doesn't pass the others: check each one.
5. **Only claim what you checked.** A completed request is not a pass. Say what you compared and where; if you can't view a result, say it needs the user's review and what to look for.
6. Be concise: links with one-line labels (model, length, Gems), no ids or JSON, in the user's language. Results expire after 30 days.

## Run each step

`get_model` once per model before its first call; `estimate_cost`; `generate` with a new UUID as `idempotency_key`; then `get_request` with `wait_seconds: 120` until `completed`, `failed`, or `cancelled`. If a `generate` response is lost, send the same arguments with the same key to recover the request without a second charge; a deliberate retry gets a new key. Start steps that don't depend on each other together.

## Choose the route

| The job | Route | Trade-off |
|---|---|---|
| Stills only: a set, a campaign, a comic | Stages 1–4, then image scenes on Mango 4 | Cheap; no motion |
| Video where the character turns: back views, profiles, orbits, big head turns | **Turntable**: stages 1–5, then Lemon in reference mode | The strongest hold across angles; the turntable bills again in every scene |
| A fixed shot whose framing and wardrobe must hold | An approved scene still as Lemon's first frame | Locks the opening exactly; holds less once the character turns |
| Final-quality video with simple motion | Cherry 2 Pro with the master and sheet as reference images | Mage's best video; no first frame, no reference video |
| The user's footage, keeping its performance | Magejutsu recast with the master and sheet | Follows the source's motion, camera, and sound; not for new shots |

When the user asks for the strongest consistency in video, use the turntable route, or say why another route fits their shot better.

## 1. Lock the details

Pick 3 to 5 traits the character really has: face shape, eye colour, hair colour and style, a scar, a tattoo, an accessory. Write LEFT or RIGHT in capitals only for a feature that has a side, from the character's own point of view (her RIGHT cheek is on the viewer's left in a front view). Never give a central trait a side.

```text
the same oval face, dark brown eyes, shoulder-length center-parted black hair, a thin scar on her RIGHT cheek, a silver ring on her LEFT hand
```

Paste it word for word into every prompt. The prompt must agree with the references: "long hair" against a buzz-cut master makes the model split the difference.

## 2. The master

One full-body image that everything else copies. Mango 4 (`mango`, `model_id: "mango-v4"`), `aspect_ratio: "2:3"`, `resolution: "2K"`; Guava 2 Pro (`guava`, `model_id: "guava-2-pro"`) when the user wants the most photoreal skin and hair. Template: Master in `references/prompts.md`. From a user's design or photo, pass it as `image` and keep its look.

With no design yet, make 2 candidates, show them, and keep one. Before going on, check every locked detail at full size, on its side. A side wrong here is wrong in everything that follows.

## 3. The sheet

Mango 4 with the master as `image`, `16:9`, 2K. Template: Sheet in `references/prompts.md`: a top row of front, right-profile, and back views, full body at one scale; a bottom row of front, three-quarter, and profile close-ups. Check every panel against the master and against each other; regenerate a swapped side now.

## 4. Save them

- **The face as a character.** `create_character` with `name` and the face: when you can run commands, crop the sheet's front close-up tight around the face and upload it (`create_upload`); otherwise save the master itself. Use the handle it returns (`@kai`), never an assumed one. A character holds the face; the sheet carries the body, the clothes, and the back.
- **The sheet as an outfit.** `create_reference` with the sheet and `kind: "outfit"` (`@kai-look`). Mage gives a reference to the model as "<kind> from image N", and "outfit from image N" is the sheet's main job; one line in the prompt adds the rest: "it also shows his hair and build from the side and back; ignore its panels and grey background".
- **Never save a sheet as a `pose`:** "pose from image N" tells the model to copy the sheet's standing pose.

## 5. The turntable (video where the character turns)

1. **Split frame.** Mango 4 with the master as `image`, `16:9`: the full body in the left third, a large head-and-shoulders close-up in the right two-thirds, a thin vertical gap, the same grey studio. Template: Split frame. Check both figures are the same person.
2. **Turntable.** Lemon (`lemon`) in reference mode: the split frame as `image`, `@kai` and `@kai-look` in the prompt, `aspect_ratio: "16:9"`, `resolution: "720p"`, `audio: false`, `duration: "10"`; `"6"` when two characters share a scene or more than two scenes will use it, since it bills again in each. Template: Turntable. Not frame mode: a first frame shows only the front, and Lemon takes no reference beside one, so it would invent a back that contradicts the sheet in every scene.
3. **Check it** from start to end: the split layout held (reference mode doesn't pin the first frame), one complete rotation at an even speed, both figures in sync, every sided detail on its side all the way round, the back of the head and the outfit matching the sheet. Regenerate on a side swap or a broken rotation; never trim away angles.
4. **Use it as generated.** Don't retime, interpolate, or re-encode a reference: identity gains nothing and artifacts can creep in. Its result URL works directly in `videos`.

## 6. Scenes

Each prompt names the character once with the locked string, gives every reference its job, and says what to ignore. Templates in `references/prompts.md`.

- **Images:** Mango 4 at the delivery aspect, `@kai` and `@kai-look` with the locked string, then the scene. On a back view or a profile, also pass the master as `image`. Guava 2 Pro takes only 3 images, mentions included.
- **Video, turntable route:** Lemon reference mode with the turntable in `videos`, the master as `image`, `@kai` (and `@kai-look`) in the prompt, `audio` as the brief needs. Say that Video 1 and image 1 only show the character, and nothing else from them appears. Write 3–4 timed shots, including the turn the job needs (walking away, a slow half orbit, a turn to the lens). Reference seconds plus `duration` must stay at or under 30.
- **Video, fixed shot:** the scene still on Mango 4 first, checked, then Lemon with it as `first_image` and no mentions (frame mode rejects them).
- **Video, final quality:** Cherry 2 Pro (`cherry`, `model_id: "cherry-2-pro"`) with the master as `image`, `@kai` and `@kai-look`, `Shot N` paragraphs without timestamps. Keep the motion simple: one or two actions per shot, no fights or crowds of look-alikes.
- **Drafts** at 480p, on the final's own route: Lemon with the same inputs and prompt for a Lemon scene; Cherry Mini (`model_id: "cherry-mini"`, 8 images) for a Cherry 2 Pro scene. Never give Cherry a turntable: its `videos` is one clip to edit, not a reference. A draft that passes doesn't approve the final render: check that too.

## 7. Two characters, new outfits

- **Two characters:** build each through stages 1–5 on their own. In the scene, name each with their mention and locked string ("Kai (@kai): … Mira (@mira): …") and say they are two different people who must not look alike. On Lemon, both turntables go in `videos` (6 s each fits the 15-second total) as Video 1 and Video 2, with both masters as images. One simple beat per shot.
- **New outfit:** edit only the clothes on the master (template Outfit change); never redescribe the person. Check the face and locked details didn't move, then make a new sheet, save it as a new `outfit` reference, and for video a new split frame and turntable. Name the new outfit in every scene from then on.

## 8. Recast the user's footage

When their clip's performance, camera, and timing must stay, use Magejutsu (`magejutsu`, `mode: "motion_transfer"`) with the source in `videos` (4–30 s; 4–15 s on Lite and Feather) and the images in order: the character in a scene still or the master, the face crop, the sheet. Template: Recast. `estimate_cost` answers `requires_media_measurement` for a source on another host: upload it with `create_upload` first. For a long or busy source, pilot its hardest 4–6 seconds at 480p. The source guides motion; it is not an identity reference, and the result keeps its length and frame rate.

## 9. Check every result

Open each result at full size, for video the hardest frames, next to the master and sheet, before anything builds on it. `references/checks.md` has the full list and the ffmpeg lines for pulling frames. The short version:

- Identity and proportions; every locked detail, on its side.
- Hair: the hairline, part, and back of the head match the sheet; no dark painted band or dotted edge near a highlight.
- Clothes by construction, not only colour: neckline, sleeves, buttons, hem.
- Light: the face lit by the scene's light, with shadows under the brow, nose, and chin falling the same way as the body's; feet and hands grounded.
- Video: the strongest turn, the back view, each contact, and the last close-up; eyes, mouth, and hands through the motion; no flicker, crawling texture, or doubled features.

Tell the user what failed and what you'll change. Without watching the whole clip at normal speed, smoothness and natural facial motion stay unchecked: say so.

## 10. Fix the cause

| What's wrong | Fix |
|---|---|
| Face changes between shots | The `@handle` and the locked string in every prompt; frame the face at medium or closer |
| Face right, body or outfit drifts | Add `@kai-look`: the character holds only the face |
| Back view or profile invented | The sheet on stills; the turntable on Lemon for video |
| A detail swaps sides | Fix the master, then rebuild the sheet and turntable from it |
| A blend of several people | Fewer references: the master, the sheet, the `@handle`, nothing redundant |
| The grey studio or split layout appears | Add the "ignore the grey studio and the split layout" line |
| Face pasted on, lit apart from the body | Rebuild the scene still under the scene's light, then animate again |

A retry changes something real (a reference, a role line, the route, the model), never an unchanged reroll. More causes in `references/checks.md`.

## Frame rate

Deliver the frame rate the model makes. A rate written in the prompt changes nothing. When the user asks for 60 fps or smoother motion, explain that the new frames are interpolated (made up between real ones, and they can warp eyes, hands, and hair), convert only the final clip, check it again, and say it was interpolated. `references/frame-rate.md` has the commands and checks; it needs a shell.

## Prices

Mage's defaults on 2026-11-11. Quote the real config with `estimate_cost` before every job.

| Step | Model | Gems |
|---|---|---|
| Master, 2K | Mango 4 | 42 |
| Sheet or split frame from the master | Mango 4 | 52 |
| Image scene with the master, `@kai`, and `@kai-look` | Mango 4 | 71 |
| Turntable at 720p, 10 s / 6 s | Lemon | 1,680 / 1,008 |
| 10 s scene at 720p with a 10 s / 6 s turntable | Lemon | 3,360 / 2,688 |
| 10 s scene at 720p | Cherry 2 Pro | 3,465 |
| 10 s draft at 480p with a 10 s / 6 s turntable | Lemon | 1,632 / 1,306 |
| 10 s draft at 480p | Cherry Mini | 600 |

## Errors

| Code | What to do |
|---|---|
| `insufficient_gems` | Give the price and the balance; Gems are added at https://www.mage.space/api?tab=billing. |
| `invalid_config` | The message names it: a handle that didn't resolve, frames mixed with references on Lemon, too many images, or reference video plus `duration` over 30 s. |
| `content_blocked` | The model's provider refused (`likeness`, `ip`, `nsfw`, `minors`, `audio`, `unspecified`); it's refunded. A photoreal reference refused for `likeness` on Cherry: offer Lemon with the same references. Never reroll it unchanged or try to slip past a filter. |
| `too_many_requests` | 20 generations are already running. Wait, then submit again. |
| `generation_failed` | Usually transient and refunded. Retry once with a new key. |
| `handle_taken` | Suggest another handle, or leave it out to derive one. |

`cancel_request` stops a request without refunding it.

## Deliver

```text
@kai is ready: the master, the sheet (@kai-look), and a 10 s turntable.
Scene 1, the rooftop (10 s, Lemon 720p, 3,360 Gems): https://…
Checked: face, the scar on his RIGHT cheek, the jacket's back, and the hairline through the turn at 0:06.
```

Offer once: the next scene, or a final render on Cherry 2 Pro.

## References

- `references/prompts.md`: every template (master, sheet, split frame, turntable, image and video scenes, two characters, outfit change, a still matched to real footage, recast), filled for Mage's image numbering.
- `references/checks.md`: what to inspect in stills and video, pulling frames with ffmpeg, and fixes by cause.
- `references/frame-rate.md`: measuring a clip's real cadence, removing padded repeats, and 60 fps on request.
