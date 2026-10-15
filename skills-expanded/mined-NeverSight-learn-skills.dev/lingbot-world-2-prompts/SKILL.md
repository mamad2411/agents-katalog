---
name: lingbot-world-2-prompts
description: >
  Turn a loose scene idea (even a single short sentence, English or Chinese)
  into a production-ready LingBot-World 2 layered scene: a StructuredExample
  JSON — base / camera / movement layers with static+dynamic variants,
  stackable hold-key events (keys 1..9), and per-scene jump/crouch/stand
  prompts — that drops straight into the frontend's lib/lingbot-cases/, plus
  a derived seed-image prompt. Can also emit a single composed standalone
  prompt when the user wants just one prompt. Use whenever the user mentions
  LingBot 2, LingBot-World 2, lingbot-world-2, reactor/lingbot-world-2,
  layered scene, StructuredScene, composePrompt, isMoving, base/camera/
  movement layers, hold keys, event keys, jumpPrompt/crouchPrompt,
  lib/lingbot-cases, a "playable character" video prompt, or gives a rough
  idea they want expanded into an interactive world-model prompt ("make a
  lingbot 2 scene for a knight in the desert"). Also handles requests phrased
  in the legacy actions.json / f-g slot export format (see
  references/legacy-sessions.md). The separate lingbot-world skill covers the
  V1 JSON state-machine format.
---

You are authoring scenes for **LingBot-World 2** (model name
`reactor/lingbot-world-2`), an interactive video world model. The model
continuously generates video conditioned on a text prompt, and the frontend
**recomposes that prompt live** as input state changes. A scene is not one
prompt but a small set of orthogonal prose fragments that
`composePrompt(scene, isMoving, heldSlots, verticalPrompt)` concatenates
into a single string:

```
prompt = base + camera[isMoving] + movement[isMoving] + heldEvents + vertical
```

- `isMoving` flips to true while WASD is held → the `dynamic` variants of
  the camera and movement layers are selected; `static` otherwise.
- `heldSlots` are the hold-keys (1..9) currently pressed → their events'
  detail clauses are appended in press order and **stack**.
- `vertical` is the jump / crouch / stand sentence while Space or C is
  engaged.

The encoder only ever sees the composed prose; the layering is authoring
discipline, not a wire format. Two consequences drive every rule below:

1. **Every fragment is always read in the company of the others.** Each
   layer owns exactly one axis — base owns *what the world is*, camera owns
   *how it is framed and what look-input means*, movement owns *what the
   subject is doing*, events own *what just happened*. A fragment that
   encodes another layer's axis (a motion verb in `base`, a POV in an
   event) contradicts that layer's other variant the moment the input
   state flips, and the model splits the difference on screen.
2. **The model can only gate motion on real input channels.** Anything a
   fragment describes as moving will move on its own, forever. The camera
   layer carries the input contract ("look-input is the only source of
   camera motion"), and the static variants state the negative space —
   what specifically holds still or idles when nothing is pressed.

## Workflow

0. Decide the **deliverable**: a layered scene JSON (default), or a
   **single standalone prompt** when the user asks for just one prompt with
   no keys ("just the prompt", "no events", "single-shot"). The standalone
   prompt is simply the idle composition — `base + camera.static +
   movement.static` joined with spaces — so write those three fragments
   with full care either way, then skip the events.
1. Write the **base** layer (§1).
2. Write the **camera** pair (§2).
3. Write the **movement** pair (§3).
4. Write the **events** (§4) — 2 to 5 hold-keys is typical; ~3 for a
   casual ask, more when the idea implies an arsenal or a sequence.
5. Write the **vertical prompts** (§5).
6. Assemble the **scene JSON** (§6) and derive the **seed image** (§7).

For a one-line ask, do all of this without interrogating the user; only ask
when the idea is genuinely ambiguous. Write everything in **English** unless
the user's own idea is in Chinese (keep their base in their words) or they
ask for Chinese; the model handles both.

**Length budget.** The encoder silently truncates somewhere around ~2000
characters of composed prose, and events stack. Targets: `base` ≤600 chars,
each `camera` variant ≤300, each `movement` variant ≤350, each event ≤500.
Check the worst case you expect (base + dynamic camera + dynamic movement +
the two biggest events) stays under ~2000; if it doesn't, trim events
first — the base and contracts must never be the part that falls off the
tail.

## 1. The base layer — world identity

One to three sentences: **subject + environment + style/atmosphere**.
Nothing else. No point of view, no camera behaviour, no motion verbs, no
input language — those belong to layers that swap under the base, and a
base that pre-commits to "stands still" or "third-person view" fights the
dynamic variants every time the player moves.

> A lone uniformed police officer in dark blue tactical gear in a narrow
> urban alley at night. Dark brick walls, heavy rain falling, shiny puddles
> on the wet asphalt, yellow police tape, blue and red ambient light.
> Cinematic noir night, reflective wet surfaces.

Craft rules, all load-bearing:

- **Concrete visual casting.** The base is the only place the subject is
  introduced; give it enough visual detail to survive the whole session
  ("a warrior in green armor and a hood, mounted on a brown horse and
  holding a large curved blade"). Every other fragment refers back with a
  definite reference ("the officer", "the warrior") and never re-describes.
- **Populate event targets.** Mention the secondary objects your events
  will interact with (a dumpster, scattered debris, a distant campfire).
  An event that asserts an interaction with an entity the scene never
  established doesn't fail — it conjures the referent into frame to satisfy
  the sentence. Every target an event names must be placed by the base,
  be plausible in the scene, or be deliberately introduced by the event
  itself.
- **Pin landmark objects with explicit counts.** While the player drives
  around, the model is happy to hallucinate a second street lamp or a
  third door as the view sweeps. For objects that anchor the space, state
  the count and fix the position, in this blunt production-validated form:
  *"The world contains EXACTLY ONE tall street lamp on the right at a
  fixed position AND EXACTLY ONE glowing neon shop sign on the left at a
  fixed position."* Use it for the two to four objects that define the
  space, not for texture (rain, puddles, debris can stay unpinned).
- **Use-ready props.** If an event will have the subject use an object,
  establish it in the base (and the seed image) in a pose compatible with
  the use. "Holding a large curved blade" composes with a blade-swing
  event; "slung across its back" fights it, and since the base is present
  under every event, the model splits the difference and fuses duplicates.
- **Describe what is present, never what is absent.** The model renders the
  nouns you give it: "a street with no traffic" places traffic, and
  negation also hides in innocent-looking words (*empty*, *nothing*, *no
  one*). Use positive substitutes ("the street ahead stays quiet"). The
  earned exceptions are the contract language in the camera layer and the
  **disambiguation guards** of §4 — targeted negations that steer away
  from a known confusion, not scene description.

## 2. The camera layer — framing and the input contract

Two variants, selected by WASD state. These templates are near-verbatim
from production scenes; keep their structure and substitute the bracketed
parts — they are the sentences that make the world controllable instead of
a drifting video.

**`camera.static`** (no WASD held) — the subject is centred and the only
camera motion is look-input orbiting it:

> Third-person view, the [subject] locked at the exact centre of the frame
> at constant size and distance. Neither the [subject] nor the camera moves
> on its own; arrow-key look-input is the only source of camera motion,
> arcing the camera around the stationary, centred [subject] only while
> held.

**`camera.dynamic`** (WASD held) — strict rear-view tracking; look-input is
reinterpreted as steering:

> Strict third-person rear view, the [subject] locked at the exact centre
> of the frame as the camera holds a fixed position behind [it/him/her] and
> tracks [it/him/her] forward. The camera does not rotate around the
> [subject]; look-input becomes the [subject] changing heading.

Notes:

- **Never use unqualified motion verbs for the camera.** "The camera
  orbits" reads as continuous self-motion; "look-input … arcing the camera
  … only while held" ties the motion to the input channel.
- **Weapon / prop framing guard.** When the subject handles items the model
  loves to render in first person (guns, tools), add the guard to both
  variants: *"any weapon in his hands visible ahead — never a first-person
  view."* This is a disambiguation guard (§4), production-validated in the
  noir-alley scene.
- **First-person scenes** (a place, a cockpit, hands on a tool) adapt the
  same pair around a named foreground **anchor** instead of a subject:
  `static` keeps the anchor centred with look-input orbiting it; `dynamic`
  becomes *"Strict first-person view, the [anchor] holding steady at the
  centre of the frame as the viewpoint advances through the scene;
  look-input becomes the heading changing."*

## 3. The movement layer — what the subject does

Two variants, same `isMoving` switch. Don't restate the subject's
appearance or the environment here — the base already said it; spend the
words on behaviour.

**`movement.static`** — the idle. This is the negative space of the motion
contract and the rest state every event returns to, so it earns real craft:
the subject is stationary but never inert. Name two or three *specific*
micro-motions bound to the subject, and keep the pose interaction-ready:

> The officer stands still on the wet asphalt, weight settled, only his
> shoulders rising and falling with slow breaths as rain streams off his
> tactical gear and drips from his fingertips into the spreading puddles.

Without a specific idle, the model animates rain, fish, and traffic on its
own and the keys stop feeling causal. "Everything is static" doesn't work;
"the horse's breath steaming faintly and one hoof shifting in the mud"
does.

**`movement.dynamic`** — travel. Concrete motion verbs, ground contact, and
the environment responding:

> The jet ski surges forward across the water, its rear thruster churning
> the turquoise sea into a wake of white foam, spray fanning out to either
> side as the man leans into the ride and the hull skips over the swell.

When the subject could plausibly be shown side-on (animals, mounts,
characters), **re-assert the rear view inside `movement.dynamic`** by
describing the view the camera contract implies: *"moving directly away
from the camera so the pair stay in strict rear view — the horse's
hindquarters, rump, and streaming tail toward the viewer."* The camera
layer states the rule; the movement layer showing the same geometry from
the subject's side is what actually holds it (field lesson from the
battlefield-horseman scene).

## 4. Events — the hold keys

Each entry in `events` is one hold-key (array index 0 → key 1). An event is
a `name` (2–4 words, Title Case — it labels the key chip) and a `detail`
clause appended to the composed prompt while held. Events **stack**: any
two events may be held together, so each detail must read sensibly next to
any other and never depend on another event being absent.

Recurring shapes, mixable within one scene (group them so the keys read as
a kit — ranged / melee / maneuver, or escalating story beats):

- **Action beat** — the subject does one discrete thing: fires a pistol,
  swings a blade, rolls forward. Keep the classic arc: wind-up →
  trajectory → named target → material aftermath ("a spent casing clatters
  onto the wet asphalt"). In a beat with two figures, name both; a
  consequence hung on a bare pronoun attaches to whichever figure dominates
  the frame.
- **Environment transformation** — weather / lighting / season sweeping
  the scene while the subject stays untouched. Describe what it does to
  two or three named surfaces ("snow piling up over the muddy terrain, the
  warrior's armor and hood, the horse's back, and the scattered debris").
- **Contextual entrance** — a secondary creature or element appears. Open
  with the subject-preservation clause so the model doesn't re-imagine the
  frame: "The original focal subject remains the main subject, unchanged
  in pose and position, while [a small tan puppy emerges from the dunes to
  the right…]".
- **Staged spectacle** — a hazard or display that runs while held. Stage it
  **off the play axis**: *"far off near the horizon, away from the rider
  and never on the path ahead"* — a meteor the player can drive into
  breaks the scene. Pace repeating elements explicitly: "one by one",
  "one after another … before the next one follows"; otherwise the model
  merges them into one continuous smear.
- **Cause-and-effect spell** — physically implausible events land better
  staged as a chain the model can render step by step: the warrior raises
  the blade → storm-clouds gather → fireballs rain down. Give the magic a
  visible mechanism.
- **Chained sequence** — keys designed to be pressed in order, each link
  opening by resolving the previous one and closing with the new state
  established. Use for journeys, escalations, boss gauntlets; write the
  whole chain as one storyboard so the hand-offs are explicit (see the
  hospital-corridor and world-tour sessions in
  references/legacy-sessions.md — the shapes carry over verbatim).

**Detail can be `{static, dynamic}`** instead of a single string when the
event genuinely looks different mid-motion (a dog sits vs. leaps
mid-stride). Use the split only then; a single string is selected for both
states.

**Discipline for every event:**

- Definite reference only ("the officer", then pronouns) — never the
  base's full introduction, never a second caption sentence. The base
  casts the subject once; a re-description is a casting call for a
  duplicate.
- Don't restate the camera or input contract, and don't encode a movement
  state ("the officer stands still and fires") — the layers own those.
  The one allowed restatement is the contextual-entrance
  subject-preservation clause.
- **Disambiguation guards.** When a noun has a known failure mode, spend a
  clause steering away from it, placed right next to the risky noun:
  *"an RPG: a long, heavy cylindrical steel tube resting across his
  shoulder … not a handheld gun"*; *"one sustained, billowing stream of
  orange fire … that pours forward without pause, not separate shots"*.
  One guard per real risk. This is the earned exception to the
  no-negation rule — a guard against a specific misreading, never
  scene-painting by absence.
- Keep every claim frameable under the camera contract: an oversized
  entrance happens at a distance the framing can contain (down the alley,
  on the horizon), never "towering above" the subject; no hand-level
  close-up detail that invites a zoom the contract forbids. Given an
  impossible framing, the model breaks the camera rather than refuse the
  sentence.
- End action beats settled ("before coming to rest beside the pack";
  "rising smoothly back to his feet") so releasing the key reverts cleanly
  to the idle. Transformations and chains intentionally move the world
  forward instead — but still end each in a new *stable* state, never in
  open-ended accelerating motion. The model conditions on its own recent
  frames: during a long hold, drift accumulates and releasing the key
  cannot restore a world that has already drifted; a broken frame also
  outlives the prompt that caused it, so when testing a fix, restart from
  a clean frame before judging it.

## 5. Vertical prompts — jump, crouch, stand

Three per-scene fields, appended as the `vertical` segment while Space / C
is engaged. The old fixed jump string ("The current controllable subject
springs upward…") is retired — **write the jump for this subject**.

- **`jumpPrompt`** — scene-appropriate, and shaped as a complete symmetric
  arc: launch, airborne moment, return to the ground. The runtime's camera
  motion is a symmetric up-then-down arc, so prose that never lands fights
  the camera coming back down. Production examples: *"The officer springs
  upward off both feet, leaping high off the wet asphalt, his boots
  lifting clear of the ground before he drops back down and lands in a low
  crouch."* / *"The horse leaps upward, launching off its hind legs so all
  four hooves lift clear of the muddy ground, the warrior rising with it
  in the saddle before the horse comes back down and lands."*
- **`crouchPrompt`** / **`standPrompt`** — these are camera-height moves
  and the stock strings are used verbatim across production scenes; reuse
  them unless the subject makes them absurd (a vehicle), in which case
  adapt minimally:

> The camera lowers toward the ground as the character crouches down low,
> bending the knees and ducking the head into a compact, hunched stance;
> the viewpoint sinks smoothly to a low, near-ground vantage and settles
> there, close to the floor.

> The character straightens back up out of the crouch, rising to full
> standing height as the camera lifts smoothly back to its normal
> eye-level vantage.

## 6. Assemble the scene JSON

The deliverable is one **StructuredExample** JSON. If the user gives a
directory (or a frontend checkout), write it as
`lib/lingbot-cases/<slug>.json` (slug = kebab-cased name) and remind them
to list it in the loader manifest (`lib/lingbot-cases-examples.ts`);
otherwise emit the JSON inline.

```json
{
  "id": "<slug or the user's case id>",
  "name": "Noir Alley Patrol",
  "description": "Third-person noir alley — key 1 = fires pistol, key 2 = flamethrower, key 3 = forward roll",
  "image": {
    "label": "Noir Alley Patrol",
    "src": "/lingbot-cases/<id>.jpg"
  },
  "scene": {
    "base": { "default": "<base prose>" },
    "camera": { "default": { "static": "<…>", "dynamic": "<…>" } },
    "movement": { "default": { "static": "<…>", "dynamic": "<…>" } },
    "events": [
      { "name": "Fire Pistol", "detail": "<event prose>" },
      { "name": "Dog Reacts", "detail": { "static": "<…>", "dynamic": "<…>" } }
    ],
    "jumpPrompt": "<…>",
    "crouchPrompt": "<…>",
    "standPrompt": "<…>"
  }
}
```

Rules: `description` enumerates the keys ("key 1 = …, key 2 = …") — it's
the only place a human sees the key map at a glance; `image.src` is the
user's image path when they have one, otherwise the placeholder path the
seed image (§7) will land at; every layer registry needs its `default`
key. Then close with one short line inviting targeted edits ("want a
different key 2, or a portal world on a key?"). On feedback, edit only the
named fragments — the composition takes care of the rest.

**Layer versions (advanced, use only when the idea calls for it).** Each
layer is a registry keyed by version id; events select versions via
`baseVersion` / `cameraVersion` / `movementVersion` (omitted = default).
Two patterns earn the machinery:

- **Portal world** — a key that teleports the session to a different
  world: register `base.portal_world` (a second full base) and tag the
  event `"baseVersion": "portal_world"`. While held, the composed prompt
  swaps the whole base; events authored against other bases are suppressed
  (they can't share prose coherently), which is exactly what you want.
- **Scene-replace event** — an event whose detail is a complete
  self-contained prompt (subject + framing + world in one string):
  register empty versions on all three layers (`base.empty = ""`,
  `camera.empty` / `movement.empty` with empty static/dynamic) and tag the
  event with all three. Its prose becomes the only content sent. Use to
  preserve a known-good standalone prompt verbatim.

A big event may also swap just `cameraVersion` / `movementVersion` to a
registered compact variant, freeing budget for its own detail without
forcing other held events off the stack.

## 7. Generate a seed image

LingBot-World 2 starts a session from a **prompt and an image together**.
Generate the matching seed image as a standard part of every deliverable,
right after the layers are finalized — one per scene, seeding the idle
composition (events modify a running session, they don't start one).

**Derive the image prompt from the layers**, don't write it from scratch:

- Start from `base` — every noun, the pinned landmark objects in their
  stated positions, the atmosphere and style tags carry over unchanged.
- Take the framing from `camera.static`, recast as a still: "A third-person
  still frame of [subject] centred in frame at medium distance…". Drop
  every input clause — a still image has nothing to react to.
- Take the pose from `movement.static`, recast as plain description
  ("standing balanced, weight settled, hands resting on the handlebars").
- Make sure every prop the events will use is visible, in the use-ready
  pose the base describes. When text and pixels disagree, the pixels win:
  a key referencing an object the seed never showed makes the model
  improvise one, and the improvisation surfaces as artifacts.
- One paragraph, same subject noun phrase as the base.

Render it with any text-to-image model. LingBot-World 2 runs at
**1664 × 960**, so target a 16:9 landscape frame. Deliver the derived
image prompt alongside the scene JSON, and remind the user the session
needs the image and the composed prompt together to start.

## Worked example

Idea: *"a rubber duck in a bathtub"*.

- **base.default:** "A bright yellow rubber duck floating in a white
  porcelain bathtub filled with soap-clouded water. The world contains
  EXACTLY ONE chrome faucet at the tub's head at a fixed position AND
  EXACTLY ONE shampoo bottle on the far rim at a fixed position. Cozy
  bathroom, warm light from a frosted window, soap bubbles along the rim."
- **camera.default.static:** "Third-person view, the duck locked at the
  exact centre of the frame at constant size and distance. Neither the
  duck nor the camera moves on its own; arrow-key look-input is the only
  source of camera motion, arcing the camera around the stationary,
  centred duck only while held."
- **camera.default.dynamic:** "Strict third-person rear view, the duck
  locked at the exact centre of the frame as the camera holds a fixed
  position behind it and tracks it forward. The camera does not rotate
  around the duck; look-input becomes the duck changing heading."
- **movement.default.static:** "The duck bobs gently in place, ripples
  spreading faintly from its hull as drips fall from the chrome faucet
  into the still water."
- **movement.default.dynamic:** "The duck glides forward across the
  bathwater, its breast pushing a small bow wave through the soap clouds,
  a rippling wake trailing behind it."
- **events:** key 1 *Water Jet* (action beat: the duck tilts forward and
  spits a thin water jet that arcs across the tub and knocks the shampoo
  bottle off the far rim, ending settled); key 2 *Steam Fills Room*
  (environment transformation: steam fogging the mirror, the frosted
  window, and the tile walls, softening the light); key 3 *Ocean Portal*
  (`baseVersion: "open_ocean"` — a registered second base where the duck
  bobs on gentle sunset swells, the bathroom gone).
- **jumpPrompt:** "The duck pops upward off the water, its hull lifting
  clear of the surface for a moment before it drops back down and lands
  with a small splash."
- **crouchPrompt / standPrompt:** stock strings from §5.

## References

- `references/examples.md` — the three production layered scenes verbatim
  (noir-alley-patrol, battlefield-horseman, jet-ski-cruise) with notes on
  what each demonstrates. Read it when unsure how a layer or event should
  sound.
- `references/legacy-sessions.md` — the older monolithic base + addenda
  export sessions (f/g/numbered slots, actions.json). Read it when the
  user asks for the legacy export format, or for event-shape inspiration:
  the chained-encounter and teleport-tour storyboards there translate
  directly into layered events.
