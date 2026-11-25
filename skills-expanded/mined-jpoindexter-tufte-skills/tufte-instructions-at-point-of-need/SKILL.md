---
name: tufte-instructions-at-point-of-need
description: "Use when guidance is being written into a manual, help center, onboarding tour, or README instead of into the place where the action happens; when users keep getting a step wrong despite documentation; when designing signage, wayfinding, labels, or checklists; when a decision tree is growing branches; or when glare, reflections, or screen placement degrade a display in a real working environment."
tags: [tufte, instructions, wayfinding, documentation, checklists, interface-design, legibility]
---
# Instructions at Point of Need

## Overview

Chapter 6 of *Seeing With Fresh Eyes* (printed pp. 131–139) carries the book's most directly operational thesis, and its title is the whole argument: **instructions at point of need**. Guidance belongs at the exact place and the exact moment of the action — embossed in the sidewalk where the dance step happens, on the parking label at the moment you walk away from the car, on the surgical blanket while the needle count is being kept. A manual is where instructions go to be unread.

The chapter argues by accumulation rather than by rule, running from a Seattle sidewalk through Han-character stroke order, an Icelandic envelope, a Paris airport garage, and a heart-surgery instrument tray, and it carries two things most design writing on this topic lacks: a **counter-case** showing what happens when instructions are elaborated instead of located (the dishwasher manual, p. 18), and a **caveat about its own thesis** — signs are seen only a few times before becoming unseen (p. 130).

It closes with something no other chapter in the Tufte canon covers: a physical-environment analysis of glare, reflection, and optical noise on real working displays in operating rooms and flight decks (pp. 138–139). An instruction placed at the point of need is worthless if the surface it sits on cannot be read there.

> Related skills: `tufte-annotation-as-thinking` (the act of layering explanation onto evidence), `tufte-link-differentiation` (instructions as annotated verbs), `tufte-color-in-information-design` (frames, glare, and reflective surfaces).

---

## §1. The Core Move — Locate, Do Not Elaborate

The failure that produces manuals is treating instruction as a **body of text** to be authored, rather than as a **location problem** to be solved. Once instruction is a text, it grows: preambles, warnings, exceptions, cross-references, decision trees. Once instruction is a location, it shrinks — because only what fits at the point of action can be there.

| Instruction as text | Instruction as location |
|---|---|
| Lives in a manual, help center, or onboarding tour | Lives on the object, surface, or screen where the action occurs |
| Read once, before the task, if at all | Read at the moment of the task, by whoever is doing it |
| Grows branches to cover every case | Constrained to what fits at the point of need |
| Requires the user to have anticipated the need | Requires nothing of the user in advance |
| Failure mode: never opened | Failure mode: goes unseen through familiarity (§6) |

**Do / Don't:**

| Practice | Verdict | Why |
|---|---|---|
| Document the correct procedure in a README | Weak | Correct and unread |
| Put the constraint in the field that violates it | Strong | Arrives at the moment of the mistake |
| Add an onboarding tour explaining the interface | Weak | Explains before the need exists, forgotten by the time it does |
| Label the physical object with the three facts needed to act | Strong | No memory, no lookup, no prior reading |

---

## §2. The Case Library (SWFE pp. 130–133)

| Case | What it does | Why it works |
|---|---|---|
| **Jack Mackie, *Steps on Broadway*** (Seattle, 1982) — dance-step footprints set into the sidewalk (p. 131) | Teaches a dance at the place a body can perform it | The instruction and the floor are the same object; no transcription step |
| **Kenya Hara and Yoshiaki Irobe, Nagasaki Prefectural Art Museum** (Hara Design Institute, p. 131) | Arrows and figure pictograms placed on the structure itself | Direction is given at the decision point, not on a map at the entrance |
| **Han-character stroke order** (Wikipedia Commons Stroke Order Project, p. 131) | **Black = stroke beginning, red = stroke ending**, so sequence, flow, width, and path are encoded into the character | The instruction *is* the thing being taught — no separate diagram, no numbered steps |
| **Fort Mason fish-advisory sign** (San Mateo County Environmental Health Services, p. 132) | PCB and mercury warnings, with eat-this / not-this fish images, posted on the pier | Placed where fishing happens, in the languages of the people fishing |
| **Palace Parking Garage 3D pointers** (San Francisco, p. 132) | Neon EXIT / ENTER / PARKING arrows projecting into the driving space | Marks up the world in three dimensions at immediate point of need |
| **Interlinear Roman-numeral guides** (manuscript, ~1090 CE, p. 133) | Tiny words written between the lines telling a reader how to *pronounce* numerals aloud | Placed between the lines, at the instant of reading, for the exact reader who needs it |
| **Charles de Gaulle parking label** (p. 133) | `Niveau -2 · Allée 09 · Place 032` — decomposed into floor, row, space | Three named dimensions, hierarchically ordered, photographable; drivers photograph it to memorize where the car is |
| **Surgical needle-count tray** (p. 133) | Real-time instrument inventory written with a single-patient-use, regular-tip, non-latex sterile marker in a **stacklist on the surgical blanket, 4 × 15 cm**, beside a foam-block needle count tray | The checklist is created and read inside the sterile field, in real time, by the people doing the counting |
| **Icelandic hand-drawn-map envelope** (2016, p. 130) | An exact address replaced by a sketched road map, the farm marked in red, plus a sentence about where the resident works | Delivered successfully — the instruction was built for the one reader who needed it, the postal carrier |
| **E. G. Lutz, learn-to-draw sequence** (1913, p. 130) | Cube → house → barn in stop-action increments ("Learn to draw in 4 easy steps!") | Each step is the previous step plus one visible increment |

**Pattern across the library:** every successful case is (a) at the location of the action, (b) reduced to what fits there, and (c) built for a *specific known reader* rather than for a generic audience.

---

## §3. Encoding the Instruction Into the Thing Itself

The strongest form is not an instruction *near* the object but an instruction *inside* it. Two cases in the chapter do this:

- **Stroke order as color** (p. 131). A Han character is drawn with the start of each stroke in black and the end in red. Sequence, direction, brush pressure, and path are all recoverable from the character as printed. There is no step list to follow, because the character carries its own construction history.
- **The decomposed parking address** (p. 133). `Niveau / Allée / Place` is not a code to be looked up; it is a three-level hierarchy with each level named in place above its value. The label teaches its own grammar.

**Generalization for interfaces:** prefer, in this order —

1. Make the correct action the only available one (constraint).
2. Encode the procedure into the artifact's own appearance (stroke order).
3. Name the parts in place, with the labels above the values (parking address).
4. Place a short instruction adjacent to the control (point-of-need text).
5. Write a manual (last resort, and assume it is unread).

---

## §4. Real-Time Stacklists — the Needle Count

The heart-surgery instrument inventory (p. 133) is worth isolating because it inverts every assumption about checklists. It is not printed in advance, not stored in a binder, and not reviewed afterward. It is **written during the procedure, on the blanket, in a 4 × 15 cm stack**, with a marker chosen for the environment (single-patient-use, non-latex, sterile, regular tip). The foam-block needle count tray beside it holds the physical objects the list refers to, so list and referent are in the same eyespan.

| Property | Conventional checklist | The needle-count stacklist |
|---|---|---|
| When authored | Before the task | During the task |
| Where it lives | Binder, screen, wall | On the working surface, inside the sterile field |
| Who writes it | A process author | The person doing the work |
| Relationship to the objects | References them by name | Sits beside the physical objects it counts |
| Size discipline | Grows with policy | Bounded by 4 × 15 cm of blanket |
| Failure it prevents | Forgetting a step | A needle left inside a patient |

**Do / Don't — checklists:**

| Practice | Verdict |
|---|---|
| A pre-printed list reviewed before the procedure | Necessary but insufficient — it cannot track state |
| A list written and updated in real time at the work surface | Strong — it *is* the state |
| A list on a screen across the room | Weak — the objects and the list are not in one eyespan |
| A list whose length is bounded by its physical medium | Strong — the medium enforces the discipline |

---

## §5. The Counter-Case — the Dishwasher Silverware Manual (p. 18)

Tufte's counter-example sits back in Chapter 1 but belongs to this argument. A dishwasher manufacturer's instructions for loading the silverware basket are reproduced under a heading about an authoritarian 3D grid micro-managing dishwasher loading:

> "This bizarre decision tree for placing silverware in a dishwasher challenges the computational powers of a chess champion." — Tufte, *Seeing With Fresh Eyes*, p. 18

The specific defects, all visible on the page:

- A **decision tree** where a constraint would do: handles up for knives and sharp utensils, handles down for forks and spoons, plus a rule about large or oddly-shaped items not nesting, plus a boxed WARNING restating the sharp-utensil rule in different terms (handles up vs. edges down).
- **Awkward linebreaks leaving lonely words dangling** at the ends of paragraphs — content-hostile typography inside a document whose entire job is comprehension (see `tufte-typography-for-data`).
- **Two separate loading-pattern grids** (Long Silverware Basket, Duo-Flex Silverware Basket) rendered as numeric matrices requiring a seven-item key.
- **The loading-pattern grid fails to show code number 5**, so the reader holding tablespoons (code 5 in the key) is left with no assigned slot for them. Tufte's summary of the effect is that the interface mutates into a stress test for domestic relationships.

**What went wrong, in one line:** the instruction was elaborated where it should have been located. Nothing in the manual appears on the basket.

**Named failure mode — Decision-Tree Creep.** When a rule acquires exceptions, the instinct is to branch. Every branch added off-site is a branch the user must evaluate at the point of action, from memory. *Fix:* push the distinction into the object (differently shaped slots), or accept a simpler rule with a worse edge case.

**Named failure mode — Orphaned Code.** A key, mapping, or enum where one of the values in play is defined but never used, or used but never defined. *Fix:* generate keys and mappings from the same value set, never author them by hand.

---

## §6. The Caveat the Chapter Applies to Itself

On p. 130, immediately after the case for direct instruction, Tufte undercuts it: direct instructions at point of need may encourage writers and programmers to divert diversions — or not, **because signs are seen only a few times before becoming unseen**.

This is the honest limit of the whole technique. Point-of-need instruction works on the naive user and decays toward zero for the habituated one. Design consequences:

| Situation | Implication |
|---|---|
| First-time or occasional users (tourists, patients, new hires) | Point-of-need signage is highly effective |
| Daily users of the same surface | Signage becomes invisible within days; do not rely on it for safety |
| Safety-critical steps for expert users | Use a *state-carrying* artifact (the real-time count) or a hard constraint, not a sign |
| A sign that must keep working | It has to change, move, or be re-encountered in a new context |

**Corollary:** an interface warning that appears every time is an interface warning that is seen no times. If a condition genuinely matters, block it or record it; do not narrate it.

---

## §7. Optical Noise — Whether the Instruction Can Be Read Where It Is (pp. 138–139)

The chapter ends with an analysis of the physical conditions under which real displays are actually read, based on Tufte's observation and photography of three heart surgeries (two robotic, one open-heart) with Dr. Marc Gillinov at the Cleveland Clinic. Reflections and glare exist wherever light exists; the question is whether they can be reduced at the point of need.

**Measured conditions in a high-level 2017 operating room:**

| Finding | Value / detail | p. |
|---|---|---|
| Display screens in the room | **25 total — 22 glossy, 3 matte** | 139 |
| Cost of matte | Glare reduced, but images slightly fogged | 139 |
| Reflective storage cabinets (glass + stainless steel) | **≈ 8 m² of optical noise**, behaving like dull distorting mirrors | 139 |
| Polished stainless steel | Accidentally creates anisotropic light — the same effect deliberately used in steel artworks | 139 |
| Brightness controls on a control-panel screen | Buried **five levels deep** in the settings hierarchy | 138 |
| Increasing brightness to beat glare | Converts the screen into a *source* of glare — the noisy-restaurant effect, where people talk louder because people are talking louder | 138 |
| Moving viewers | Glare and reflections move with them; motion attracts the eye-brain system | 139 |
| Working fix in use | Pre-op echocardiograms viewed in **alcoves** giving optical and acoustical serenity; the surgeon's live video feed viewed in a **darkened booth** on a reflection-free screen | 139 |
| Trend | Every new piece of surgical equipment introduces a new source of optical noise | 138 |

**The flight-deck precedent.** Tufte reproduces guidance from Asaf Degani's NASA report on the typography of flight-deck documentation (p. 138), noting it now applies to the far greater glare of the glossy laptop and iPad screens used for documents and flight maps:

> "In choosing a plastic cover or lamination, an anti-glare plastic that diffuses light is recommended; otherwise, some rays from the light source will be reflected to the pilot's eyes." — Asaf Degani, NASA, quoted in Tufte, *Seeing With Fresh Eyes*, p. 138

Degani's further points, all transferable: when the eye shifts between a directly lit document and darkened windows or panels it must constantly re-adapt to different luminances; severe luminance differences between the critical-vision object and the peripheral surroundings reduce visual discrimination, reading speed, and comfort; any strong unshielded light source in the field of view causes disability glare, and the closer it is to the line of sight, the worse the loss of visual efficiency.

**Do / Don't — displays in real environments:**

| Practice | Verdict | Why |
|---|---|---|
| Specify glossy screens because they look better in the showroom | Wrong | Ceiling lights reproduce on them in the room where the work happens |
| Accept slight image fog for matte finish on working screens | Right | Legibility under real lighting beats contrast under ideal lighting |
| Bury brightness controls in a settings hierarchy | Wrong | The one control that fixes glare is unreachable at the point of need |
| Raise brightness to overcome ambient glare | Wrong | The screen becomes a glare source for every other screen in the room |
| Place critical viewing in an alcove or darkened booth | Right | Removes the light source rather than fighting it |
| Audit reflective surfaces (cabinets, glass, polished steel) by area | Right | 8 m² of accidental mirror is a design decision nobody made |

---

## §8. Failure Modes

**I1 — Manual Displacement.** The instruction exists, correctly written, somewhere the user is not. *Fix:* move it to the surface of the action; delete whatever does not fit.

**I2 — Decision-Tree Creep.** Rules branching to cover exceptions, evaluated by the user from memory at the point of action. *Fix:* push the distinction into the object, or simplify the rule.

**I3 — Orphaned Code.** A key and its mapping that fail to cover the same value set (the loading grid missing the key's code 5, p. 18). *Fix:* generate keys and mappings from data.

**I4 — Advance Instruction.** Onboarding tours, welcome modals, and training decks delivered before the need exists. *Fix:* deliver at the moment of first use of each control.

**I5 — Sign Blindness.** Relying on static signage for habituated users, who stop seeing it within days (p. 130). *Fix:* constraints or state-carrying artifacts for anything safety-critical.

**I6 — Detached Checklist.** A list that is not in the same eyespan as the objects it governs. *Fix:* put the list on the working surface, beside the things being counted.

**I7 — Unreadable Surface.** A correct instruction placed on a glossy, glare-struck, or badly lit surface. *Fix:* matte, alcove, or relocate — and audit reflective area (pp. 138–139).

**I8 — Buried Remedy.** The control that would fix a legibility problem hidden several levels deep in a settings hierarchy. *Fix:* surface the environmental controls at the point of need, like every other instruction.

**I9 — Brightness Escalation.** Fighting glare with luminance until the display becomes a glare source for its neighbors. *Fix:* reduce ambient light or change the surface, not the output.

**I10 — Grid-Loudest Display.** A dense instructional matrix whose rules dominate its content. Tufte's diagnostic on the *Catch-22* plotchart (p. 134) is to ask of any display or interface what its strongest visual element is — and the correct answer is never the grid lines. *Fix:* ghost the grid; let content spill softly across cells (see `tufte-layering-and-separation`).

---

## §9. Checklist

- [ ] Is each instruction at the place and moment of the action it governs?
- [ ] Could the instruction be replaced by a constraint that makes the wrong action impossible?
- [ ] Could the procedure be encoded into the artifact's own appearance instead?
- [ ] Are the named parts labeled in place, above their values?
- [ ] Is the instruction short enough to fit at the point of need, or is it an elaborated text?
- [ ] Does any key or legend omit a value that actually occurs?
- [ ] Is this audience naive or habituated — and does the design still work once the sign goes unseen?
- [ ] For safety-critical steps, is there a state-carrying artifact rather than a sign?
- [ ] Is the checklist in the same eyespan as the objects it governs?
- [ ] Can the surface actually be read under the real lighting of the real room?
- [ ] Have you counted the reflective area (glass, polished metal, glossy screens) in the working environment?
- [ ] Are brightness and glare controls reachable at the point of need, not five levels deep?
- [ ] Is the strongest visual element in the display its content, rather than its grid?

---

Source: Edward Tufte, *Seeing With Fresh Eyes: Meaning, Space, Data, Truth* (Graphics Press, 2020), Chapter 6, "Instructions at Point of Need," printed pp. 131–139, with p. 130 (Icelandic envelope, E. G. Lutz sequence, the signs-become-unseen caveat), p. 18 (dishwasher silverware manual), and p. 134 (*Catch-22* plotchart, ghost grids). Glare guidance quoted from Asaf Degani, *On the Typography of Flight-Deck Documentation* (NASA, 1992), as reproduced by Tufte on p. 138. Operating-room observations made with Dr. Marc Gillinov at the Cleveland Clinic. All passages paraphrased; quoted lines limited to single attributed sentences with page citations.
