---
name: diorama-dither
description: 'Build a dithered isometric miniature on the pixel kernel with hard shadows, natural materials and a yard that fills the frame. Use it for a pixel diorama with ordered dither, a translucent ground shadow, and a tap that toggles one state. The pixel skill stays on its three default scenes; this one adds the dither finish and its examples.'
compatibility: Needs Node.js 20+ and Chrome or Chromium for the look. Do not edit the pixel kernel.
---

# Dither diorama

You are making one small place, drawn at 360 x 280 and enlarged with nearest-neighbour pixels. Surfaces use five close tones and a 4 x 4 ordered dither. The sun throws a hard shadow that darkens the ground's own colour. One or two people do one looping action. A tap toggles one state. There is no score, no audio, and no halo around a light.

The pixel kernel (`skills/diorama-pixel/kit/pixel.js`) is fixed. A change there shifts the three pixel scenes. Put new helpers in `kit-src/finish.js`, then run `node scripts/sync-dither-kit.mjs` from the repo root. Never set `glow` on a material: it forces a face up to a flat brightness and reads as a bloom. A lamp is a paper box. A beam is a thin box of hard pixels.

Write the scene as `skills/diorama-dither/examples/<name>.js`. One `Pixel.scene({ ... })`. `means` is one sentence, at most 140 characters. The scene file stays at or under 260 lines, and the built page at or under 70 KB (71680 bytes). `node scripts/validate.mjs` on the `.js` assembles that page and fails the size check when the page is over 71680 bytes. The comparison is `<=`, the same one the look uses. A pass prints the bytes left, for example `732 bytes left of 71680`. An empty scene assembles to 64823 bytes, so 6857 bytes remain for the scene source. That remainder assumes the default title, `Dither diorama`. The kernel takes the rest. A longer `title` spends some of that, because the shell writes the title. Two plants built by hand, one animal and a tent already have nothing left once a comma or a colon keeps a space, and the shore rocks are what get cut. Written with the spacing of `examples/forge.js`, that page was 72351 bytes, 671 over 71680. `node scripts/build.mjs examples/<name>.js` prints the path and the byte count. What to cut first is in section 6 and in `references/yard.md`.

## 1. Decide the picture before the code

Write four lines, then stop and check them against the rules below:

- **Ground.** A yard or a shore that fills the frame. Name the zones (meadow, earth, rock, sand, water).
- **Mass.** The one structure, where its front faces, and what must stay visible in front of it (a door, a course of stone, a person).
- **People.** Who, in the open, facing the work. Standing height is `h × cos(elevation) × scale` pixels. Two or three cloth colours.
- **Life.** What loops, and the one thing a tap toggles. The loop is a function of `q` that matches at `0` and `1`.

If a person, a door or the front of the structure would sit behind a post, a wheel, a sail or a roof, move the person or the occluder now. The camera does not move.

## 2. Frame

- `width: 360, height: 280`, `fps: 12`, `duration: 8`, `still: 2`, `bayer: 4`, `shadow: 'hard'`, `rim: true`, `wind: 8`.
- Camera `{ az: 45, el: 30, scale: 54 to 62 }`. `height` recenters and does not zoom, and it is not the summit. The fit reserves the yard edge. Start near `0.6` times the tallest point and correct from the still. A band of white above the mass means it is still too high. Too low and the roof is cut.
- Ground `rx` about `3.4` to `4.2`, `rz` about `2.6` to `3.2`, `wobble` `0.3` to `0.4`, `fade` `0.3` to `0.36`. Use `rect: true` for a walled yard. The coloured ground should cover roughly a third to four fifths of the frame. A wide white margin means the yard is too small or the scale is too low.
- `sun: Dither.sun(45, elevation, turn)`. Elevation `36` to `58` degrees. `turn` of `14` to `20` degrees spreads a rotor's shadow so the blades do not stack into one bar. Shadows fall to screen-right. Leave lit ground past the shadow, short of the right-hand wall.

## 3. Materials

Call `Dither.mat(name)` and put the result on `materials`. The names already carry the right texture:

| Surface | Name | Why |
| --- | --- | --- |
| Grass yard | `meadow` | Grass grain, plus a fringe of `moss` blades at the edge so the rim is not a hard oval |
| Path, forge floor | `earth` | A zone, not a second slab |
| Courses of wall | `stone` or `rock` | The texture cuts joints. A wall is `Dither.wall`, which adds a coping |
| Roof | `tile` | Horizontal courses |
| Planks, posts, cart | `timber`, `beam`, `cart` | Grain along the long axis. A narrow pier with that grain on X reads as a wall: use `Dither.mat('timber', { grain: 'z' })` and a wide deck, about `2.2` by `0.1` by `1.1` |
| Sail, sack, paper screen | `sail`, `sack`, `paper` | Cloth, flat, no dither extreme |
| Sea, pond | `water`, `pond` | The texture already moves and sparks. A crest is a short box, not a soft band |
| Snow | `snow` | Light blue-white ground, sand grain. `Dither.report` on `#d5e6ee` must pass |
| Lamp, ember, ray | `lantern`, `ember`, `ray` | Solid faces. `ray` has dither `0`. A second, darker dithered tone on alternate segments keeps a ray from reading as one bar |

`Dither.report(hex)` must come back with five tones, a max gap of `0.08` or less, a cool dark step and a warm light step. Do not hand-build a ramp unless a preset cannot say the hue.

## 4. Build from helpers

These live on `Dither` and do not run for a pixel scene:

- `wall(P, x, z, len, yaw, opt)` stone run plus a wider coping. `gate(P, x, z, yaw, opt)` for the opening. `opt.h` defaults to `0.66`. A yard is four runs and one gate, inside `rx` and `rz`.
- `folk(P, x, z, { h, yaw, name, shirt, pants, sleeve, hat, on })` a person the pointer can name. Standing pixels are `h × cos(elevation) × scale`. At elevation 30 and scale 58, `h` 0.4 is about 20. A pitched pose measures a little shorter. The yards use `h` 0.38 to 0.44 at scale 56 to 62. A figure of about 21 pixels reads as a splinter: the face, the sleeve and a case collapse into a few columns. At that camera `h` `0.42` is about 21 and `h` `0.40` is about 20. Keep a chief or a traveler at `h` `0.48` or above there, about 24 pixels, and under `0.55`, which outgrows the yard. A standing figure keeps the bind-pose sole about `0.01 × h` under the origin. `on` is a deck or other mesh: that sole meets its top exactly and the figure is seated on it. A later `root.position.y` replaces that. Shirt, pants and sleeve are three colours that sit far apart. A chief that still reads as cloth is shirt `#8e2f2a`, pants `#1c2433`, sleeve `#cbb892`. A traveler is shirt `#2c4f78`, pants `#6b3a2a`, sleeve `#d7c4a2`. After `P.pose`, set the arms so the forearms leave the torso: a `work` or `hold` pose, elbows bent, hands out. A case in the hand is a fourth colour, `sack`, not the sleeve: `Dither.afloat(P.box(0.11, 0.08, 0.13, 'sack', 0, -0.06, 0.05, handR), 'case', 'carried')`. `folk` sets `root.name` from `name:`, and that is enough for the read-out. `.name =` in the source is only for check 8.
- `hull(P, x, z, { h, y, amp, yaw, len, beam, mat, name })` a timber box in the water. `h` is the height, `y` the centre, `amp` the bob stored on the group. The default centre leaves the top just above the plane, so the water cuts the box. The tick sets `position.y` from `amp`. The mesh is `group.hull`.
- `tree`, `bush`, `fringe`, `fence`, `lamp`. `lamp` is a post, a paper box and a cap. Pass `shade: 'lantern'` or `'paper'`. Never a glow.
- An awning is a thin roof box, about `1.78` by `0.05` by `1.08`, seated on the front beam. `awning: Dither.mat('sail', { stripe: .18, alt: '#a33b32' })`. `stripe` is the band width along the grain. On a roof the default grain `x` runs the bands across X. Pass `grain: 'z'` to run them the other way. `alt` is the other ramp: a hex, a ramp name, or an array of hexes. Short valance boxes hang from the front lip and sit on the roof.
- A hung lantern is a cord and a box. `Dither.lamp` stands on the ground. The cord is at least `0.04` thick, about two pixels. A cord thinner than one voxel (`P.px`, about `0.017` at scale 60) misses the picture, or the gap to the beam fails support. The front beam, the cord and the lantern share local `z` `0.42`. At yaw about `0.68` that beam is the one toward the camera. Seat the cord on the beam and the lantern on the cord, with the faces touching. An `ember` face on the camera side toggles with `.visible` when it stays seated on the lantern. A core that travels is `Dither.afloat(core, 'ember', 'spark')`. Seating that core and then moving it fails support: `ember misses lantern by 0.091`. The afloat core passes support. Never `glow`. `look` needs the largest quarter-step over `0.002` of the frame. A step of `0.0003` or `0.0011` fails. One core of `0.09` by `0.10` by `0.03` stayed under that: `u * 0.8` measured `0.0010`, and a blink measured `0.0005`. A core twice that on each side, `0.18` by `0.20` by `0.06`, declared afloat and travelling out by `u * 0.35`, measured `0.0022` and passed `motion`.
- A pot is an 8-sided cylinder on the counter, a wider rim seated on the body, and a lid seated on the rim. `iron` is the blue-grey `#5c636c`. Hide the lid when the pot is open.
- Steam under a cover starts at the lip and travels out. Three `sail` boxes, the largest about `0.28` by `0.14` by `0.22`, `Dither.afloat(g, 'smoke', 'steam')`, phase `i / 3`, placed from `(q + phase) % 1`. Carry them out by `u * 0.35` from local `z` about `0.56`. Keep the centre at `y` of `0.80` or lower. At `y` `0.90` the puffs cross the awning and the step stays at `0.002` or under, so `motion` fails. At `0.80` and at `0.70` it passes. Under the awning at `y` `0.70` that run measured `0.0028`. In the open, `u * 0.20` measured `0.0018` and failed, and `u * 0.22` measured `0.00202` and passed. A sway of `0.03` with `u * 0.12` up and `u * 0.08` out measured `0.0007` under the cloth. Adding `u * 0.12` of rise to the `0.35` run measured `0.0017` under the awning and failed, because the puff climbs back into the cloth. `0.0003` and `0.0011` fail. If the puffs are the only motion, use the outward `u * 0.35`. Chimney smoke, above the roof, is the stack case in `references/yard.md`. The grey `smoke` preset disappears against timber.
- Two wheels on this side need two axles. One axle hides its far wheel behind the box. Yaw the cart about `0.85`, put an axle near each end, and seat each wheel with `Dither.seat(wheel, 'cart-wheel', 'ground', axle)`. The centre `y` is the radius, 10 sides, `rotation.x` of `π/2`. The bed sits on an axle. The far pair does not stay hidden: on the mill cart, about 20 pixels of those wheels show past the box, up by the rail, on the 360 by 280 canvas. `examples/windmill.js` builds it this way.
- `folkZoom` names the two people the look crops into `zoom-figure.png` and `zoom-carter.png`. The default is `['miller', 'carter']`. Set `folkZoom: ['cook', 'customer']` to fill those files from other hot groups. A name the hover misses writes no file, including a person listed in `folkZoom` who is hidden. Every hot group also gets `zoom-<name>.png` when the hover hits it. `look` still requires `pointer` and `figures`, so a hidden hot person fails both.
- `cap(P, tower, { y, r, over, h })` an upright cone. `y` is the tower top, `r` is that top's radius, `over` is the overhang (about `0.1`), `h` is the slope. A cylinder with `rotation.x` of `π/2` is a lid seen from above. Do not use one for a roof.
- `rotor(P, parent, { y, z, face, len, tilt })` four equal sails on a shaft. Yaw the parent so local `+Z` points toward the camera (about `0.74` at azimuth 45). `y` and `z` are the hub on that front face. `face` is back inside the cone, so the neck meets the cap. `tilt` (about `0.3`) is `rotation.x`: the shaft drops toward the camera. The cloth stays in front of the stone. Spin `rotation.z` only. A cross drawn on the roof is the shaft left at `tilt` `0`.
- `sway(P, node, base, t, amp, phase)` for plants. `carry(q)` for a lift that rests at both ends of the loop.
- `seat(node, name, on, join)` and `afloat(node, name, reason)`. Every solid mesh declares one, or sits inside a group that does and actually meets it. See Support.

Check 8 of `validate` requires the text `.name =` in the scene source, comments stripped, for each hot group. `parts.hot` lists them. `name:` is enough for the read-out: `folk` sets `root.name` from it. `name:` does not satisfy check 8. One `.name =` in the file passes the search. A string that contains `.name =`, or a comparison `a.name == 'b'`, matches too, without assigning a name. The `hint` says what to hover and names the tap target with the words `tap the <name>`.

## Halt

A platform, a small steam locomotive, a wagon, a clock and a signal. Camera azimuth 45, elevation 30, `height` `0.78`, scale 58. `sun: Dither.sun(45, 38, 16)`. The platform group is `(-1.25, 0, 0.28)`, yaw `0.68`. The train group is `(0.05, 0, 1.02)`, yaw `0.95`. That scene passed support at one voxel `0.017`, frames `2`, `4`, `6` and `8`. The built page was 71567 bytes, 113 left. It fits only after the cuts in section 6. Full seating is in `references/yard.md`.

- Canopy. Deck `2.3` by `0.12` by `1.08`, timber grain `z`, centre `y` `0.06`, on the ground. Four posts `0.08` by `0.64` by `0.08` at local `(±0.92, 0.44, ±0.38)`, on the deck. Front beam `1.96` by `0.07` by `0.08` at `y` `0.795`, `z` `0.38`, on a front post. The back beam is the same size at the same `y`, at `z` `-0.38`, and it is seated on a back post. Tile roof `2.12` by `0.05` by `1.02` at `y` `0.855`, on the front beam.
- Clock. The disk that reads at 360 by 280 has radius `0.08` and depth `0.04`, `paper`, eight sides, `rotation.x` of `π/2`. At this camera that face is about 8 pixels tall (`0.16 × cos(30°) × 58`). Radius `0.08` is the minimum. A smaller disk is a speck. Group at local `(0.88, 0, -0.2)`, off the traveler. Seat that group on the deck, or on the surface that holds it. Without that `on`, support fails. Face at `y` `0.7`, `z` `0.05`, seated on a post `0.07` by `0.58` by `0.07`. Minute hand `0.02` by `0.09` by `0.02` on a group at `z` `0.072`. Hour hand `0.07` by `0.02` by `0.02` on a group at `z` `0.078`. Both are iron, seated on the face, in front of the disk. `minute.rotation.z = -q * TAU`. The hour is that divided by 12.
- Signal. Clear of the left wall. An arm inside the wall does not read. Group at local `(-0.35, 0, 0.78)`. Post `0.08` by `0.86` by `0.08`, centre `y` `0.43`. Blade `0.05` by `0.10` by `0.48` of `Dither.mat('sail', { stripe: .14, alt: '#a33b32' })`, on an arm group at `y` `0.78`, `z` `0.04`, the blade centred at local `z` `0.2`, seated on the post. Lowered `rotation.x` `0.1`. Raised `-1.25` when `c.active` is the chief's root.
- Rail. Five sleepers `0.12` by `0.05` by `0.58` at `y` `0.025`, `x` of `-1.05`, `-0.4`, `0.25`, `0.85`, `1.35`, each on the ground, parented to the train so they yaw with it. Two iron rails `2.6` by `0.04` by `0.06` at `y` `0.07`, `z` `±0.2`, `x` `0.15`, each seated on the last sleeper.
- Locomotive. Wheels radius `0.15`, thickness `0.07`, 10 sides, `rotation.x` of `π/2`, centre `y` `0.24`, `z` `±0.2`. Axles at `x` `-0.42` and `-0.08`, each `0.05` by `0.05` by `0.52`, seated on the near wheel. `Dither.seat(wheel, 'cart-wheel', rail, axle)`. Frame `0.92` by `0.08` by `0.26` at `y` `0.29`, `x` `-0.22`, on the axle. Boiler `P.cyl(0.12, 0.12, 0.62, 'iron', …, 8)`, `rotation.z` of `π/2`, centre `y` `0.43`, on the frame. Cab `0.38` by `0.38` by `0.3` at `(0.1, 0.52, 0)`, on the frame, with a paper window `0.12` by `0.10` by `0.04` at `z` `0.16`. Chimney `P.cyl(0.06, 0.07, 0.28, 'coal', -0.48, 0.63, 0, train, 6)`, on the boiler. The base is a little wider than the top. There is no chimney cap. That cap was cut to fit the page. Connecting rod `0.46` by `0.04` by `0.04` at `y` `0.32`, `z` `0.23`, seated on the near wheel, on the camera side of it. A rod against the boiler disappears. Crank `0.04` by `0.12` by `0.04` at the pin, `y` `0.29`. Smoke is three `sail` boxes, largest `0.26` by `0.13` by `0.20`, `Dither.afloat(g, 'smoke', 'smoke')`, phase `i / 3`, base `(-0.48, 0.88, 0)`, rise `u * 0.78`, out `u * 0.18`. That is the stack, not the awning recipe.
- Wagon. A second pair of the same wheels at `x` `0.64` and `1.08`, on the same rails. Bed `0.98` by `0.08` by `0.28` at `y` `0.29`, `x` `0.88`, on the axle. Coach `0.90` by `0.42` by `0.34` at `y` `0.54`, on the bed. Roof `0.96` by `0.06` by `0.40` at `y` `0.78`, on the coach. Link `0.24` by `0.06` by `0.08` between frame and bed. No door. The door was cut to fit the page.
- People. Chief `h` `0.42` and traveler `h` `0.40` on the deck are the sizes that seated, and they read as splinters. Use the taller band above. `name:` on each person is enough for the read-out. `.name =` in the source, as on `master.root`, is only for check 8.

## Oasis

Sand, a pond, two palms, a one-mast tent, a well and a camel. Camera azimuth 45, elevation 30, `height` `0.92`, scale 58. `Dither.sun(45, 38, 16)`. The sizes that passed support are in `references/yard.md`. `Dither.tree` is a leaf canopy and is not a palm.

- Palm. A 6-sided `beam` trunk with grain on Y, a crown seated on the trunk, and six leaves in two segments (`rotation.z` `-0.48`, then `-0.42`). Each segment is seated on the previous one.
- Tent. Yaw near `-0.5` so local `+X` faces the camera. Mast, ridge, and two `sail` flaps pivoted on the ridge at `rotation.x` near `±0.95`, seated on the ridge and coming down to the sand. The end toward the camera stays open.
- Camel. The mule, plus a hump, and a second neck segment seated on the first. Each of the four legs ends in a hoof seated on the ground and on the leg.
- Well. A stone cylinder, a rim, a bar, a rope at least `0.04` thick (use `0.05`) seated on the bar, and a bucket seated on the rope.
- Feet. A person or an animal next to the pond stays outside the water ellipse. The guide, the traveler and the four camel hooves in that scene do.
- Sparks. A window of about `0.18` can miss every frame `look` samples (`q` of `0`, `0.25`, `0.5` and `0.75`). Put the phase so one of those four falls inside the window. Phase `0.795` does that at `q` `0.25` and `q` `0.75` (`u` `0.09`). Or send chimney smoke with the sparks: rise `u * 0.78`, out `u * 0.18`.

## Support

A piece either meets a surface or names why it does not. `npm run support` and the look both check the still and the frames at a quarter, a half, three quarters and the end of the loop, and exit 1 with the group's name. A mesh with no support fails as `has no support`. A mesh inside a seated group fails when the nearest mesh is more than one voxel away and the mesh's own bottom is above the ground. Sitting inside the group's box is not enough. A bottom within one voxel of the ground can pass, which is how a tuft or a crest stays. Two meshes that only meet each other still pass. An unnamed mesh is reported as its parent's name plus its child index.

- `Dither.seat(node, name)` rests on the ground. The bottom face is within one voxel of `y = 0` (`P.px`). Sitting slightly in the ground passes. Floating above it fails. `folk`, `wall`, `gate`, `fence`, `lamp`, `tree`, `bush` and `fringe` already do this.
- `Dither.seat(node, name, otherNode)` — the two solids meet within one voxel. A bed on an axle, a sail on the cap, a leg into the body, a screen on the floor, a shade on its post.
- The fourth argument is a second solid. A wheel uses both: `Dither.seat(wheel, 'cart-wheel', 'ground', axle)`. If the wheel already fails the ground, the axle line is not repeated.
- `Dither.seat(node, name, 'water')` — the water plane cuts the body (hull, fish). The bottom stays under `y = 0` at the highest point of a bob.
- `Dither.seat(node, name, 'surface')` — foam whose bottom sits on the water, in a water zone.
- `Dither.afloat(node, name, reason)` is the only leave-the-ground. The reason is a non-empty string: a carried sack, a ray, a spark, smoke, an hour mark. A blank reason fails as `floats without a reason`.

A figure whose body passes through a solid that is not the ground fails as `stands inside`. To stand on a plinth, raise the root to the top face and call `Dither.seat(root, name, plinth)` again.

A figure on the ground must not stand in a water zone. Feet are the figure's `x` and `z`. The kernel's `place` turns a missing or `NaN` coordinate into `0`, so `Dither.folk` checks `x` and `z` before that call and the support check reads the requested pair. A non-finite foot fails as `has no place to stand`. It does not stand at the origin and pass. Feet go on meadow, earth, sand, snow, rock, a pier deck, or inside a boat. Never on open water. A wheel is a cylinder with `rotation.x` of `π/2` and 10 sides, so a vertex sits at the bottom. Its centre `y` equals the radius, the axle passes through that hub, and the bed sits on the axle.

Checklist before the first render:

- Every solid mesh has `seat` or `afloat`, or sits in a group that does and meets the nearest mesh. A child parked in the air still fails when that mesh is more than one voxel away, even inside the group's box. A bottom within one voxel of the ground can pass.
- Wheels, legs and feet touch. The axle touches the box. Hooves and shoes touch a solid surface.
- A boat's hull is partly under the water. A bridge's piles stand on the banks. Posts reach the ground.
- Nothing floats unless `afloat` names the reason. The check covers a mesh with declared support, or a group that meets the nearest mesh. It does not cover a chain of loose pieces that only touch each other.

## 5. Motion and the tap

Pose from `c.t` and `c.q` only. A loop closes: `Math.sin(q * TAU)`, a full turn `q * TAU`, or `(q + phase) % 1`. Do not add speed each frame.

`c.active === root` is the toggled state. The still frame starts with `active` clear, so the first state is the one you want at `still`. The second state must change the picture by more than a few pixels at `still + 0.5` seconds: a hidden beam, a swapped screen, a forge mouth, a pose. A joint that moves a couple of pixels will not read and will fail the press check.

Reduced motion and `?still` hold the clock. Do not start your own timer.

## 6. Check, then look

From `skills/diorama-dither`:

1. `node scripts/validate.mjs examples/<name>.js`. The size check assembles the page. A scene under 260 lines still fails when that page is over 71680 bytes. A pass prints the bytes left, `732 bytes left of 71680`. An empty scene leaves 6857 bytes for the source, assuming the default title `Dither diorama`. The kernel takes the rest. If the page cannot be built, validate prints one line, `FAIL 7 size: page build failed: …`, and exits 1. Check 8 requires the text `.name =` in the scene source. A `name:` option on `folk` does not count for that check. `name:` is enough for the read-out. A string or `a.name == 'b'` matches that search as well. When the page is over, cut decoration before the action. On the halt the order that came under the cap was the grass fringe, a steam dome and a buffer beam (the page was still 72955), then a box helper and the chimney cap (still 72559), then no space after a comma or a colon, materials from one `'meadow earth …'.split(' ')`, and the wagon door (71565). Two handmade plants, an animal and a tent start in that tight spacing, and the shore rocks go before the action. Written with the spacing of `examples/forge.js`, that page was 72351 bytes, 671 over. A second copy of a building misses the frame budget as well as the byte cap. The helper, written tight, is `function(w,h,d,m,x,y,z,p,n,o,j){return Dither.seat(P.box(w,h,d,m,x,y,z,p),n,o,j);}`.
2. `npm run support` audits every file in `examples/`. One scene: `node scripts/support.mjs examples/<name>.js`. Then a lifted `cart-wheel`, a box at `y = 4.5` inside the mill, and a figure standing in the tower. Each must fail. The line is `ok negative` and the reason. It does not print `FAIL` for a miss that was required. Then the water cases. A host in the tea pond must fail. A figure in the lighthouse's open water must fail. A figure on the lighthouse rock must pass. A bad foot coordinate must fail. `folk(NaN)` and `folk(undefined)` must fail. A mesh with no support must fail. A blank float reason must fail. The same run checks the snow report, the gate height, the cold family, a tall sand-post stain, the figure sole and the hull.
3. `node scripts/look.mjs examples/<name>.js <outdir>` — the look runs the same support check on those frames. `motion` must be over `0.002` of the frame. A step of `0.0003` or `0.0011` fails. `shadow` must be `hard`. `soft` or `none` fails. A grass silhouette takes the strong cast check. A hard cast on earth, water, or a cold ground takes the sharp threshold. `sharp` reads the grass frame at `t` `0` and keeps the longest dark run. A dark strip on the right edge can beat the real cast: on the halt that strip won with `x1` `355` until the sun was `Dither.sun(45, 38, 16)` and the strip was gone. The counted cast was then `n` `313`, `w` `11`, `x1` `148`. On sand that sun does not do it alone. The sharp check does not ask for lit ground past the cast, so a run of width `105` that ends on the frame still passes: the first look gave `x1` `354` and `beyond` `0`. On sand the counted run has to leave `beyond` greater than `0`, and `x1` at least 40 pixels in from the right edge. If the mass sits on the right, move the mass. A post on sand `#d2c09a` leaves a tall narrow earth stain, and that stain counts when it is at least 28 pixels tall and at least three times as tall as it is wide. The scene name does not choose it. `zoom-figure.png` and `zoom-carter.png` use `folkZoom`, default `miller` and `carter`, and only when the hover hits that person. Each hot group also gets `zoom-<name>.png`.
4. Open the still, one moving frame, the hover, the press, the mobile shot and the figure zooms. Look at the wheels, the feet and anything that should meet a neighbour.

The look checks fill, the loop seam, picking, hover, the tap, reduced motion, a hidden tab, off-screen pause, and a median frame at or under `83.3` ms, including CPU throttle 4. A pass is not a picture. Judge the still yourself: the action, the materials, the shadow, and whether the front of the structure is still readable.

`node scripts/record.mjs examples/<name>.js <outdir>` writes a silent loop.

`node scripts/sync-dither-kit.mjs --check` must pass after every helper change. Re-hash the three pixel scenes (`pier`, `flower-stall`, `allotment`) at their still frame if the pixel kernel was touched. If it was not, those hashes stay put because a pixel page never loads this finish.

## Before the first render

Walk this list. Each line is a failure that already shipped once:

- A rotor drawn on the roof, or a flat disk wider than the tower. The cap is a cone with a small overhang and a visible slope. The shaft and the four sails sit on the front face, tilted down toward the camera, and a person stands on the ground at the door with the sack in the hand.
- A wheel, a hoof, a foot or a post with daylight under it. The axle meets the box. A person stands on ground, rock, a pier or in a boat, never on open water. A hull sits in the water, not on it. Anything else that leaves the ground has `afloat` and a reason.
- A sail, cart, bush, lamp or gate post crossing the person. With a step in the yard, feet go on meadow or earth, at least `1.2` inside the near wall and `0.4` clear of a step or a slab. The coping covers anyone standing in the opening.
- A shadow that is a flat grey bar, or that runs through the right-hand wall. Hard veil, one sun, lit ground beyond. Do not add a second light for a lamp, a ray or dusk. The sharp check measures grass at `t` `0` and keeps the longest dark run. A dark strip on the right edge can be that run. Use `Dither.sun(45, 38, 16)` and do not leave the strip. On sand that sun is not enough: a width of `105` at `x1` `354` and `beyond` `0` still passes. Leave `beyond` greater than `0` and keep `x1` at least 40 pixels in from the edge. If the mass is on the right, move it.
- A standing figure under about 16 pixels (`h × cos(elevation) × scale`) merges, and one near 21 reads as a splinter. At elevation 30 and scale 58, `h` `0.42` is about 21. Keep a chief or a traveler at `h` `0.48` or above there, about 24, and under `0.55`. Shirt, pants and sleeve far apart. A case is `sack`, not the sleeve. `name:` is enough for the read-out. `.name =` in the source is only for check 8.
- A yard that leaves a wide white band above the roof. `height` is not the summit: start near `0.6` times the tallest point and correct from the still.
- A lamp or a beam with `glow`, or one thick box that reads as a bar. A ray is several segments, thinner toward the tip, one of them a darker dithered tone. Paper and ember stay flat.
- A tap whose only change is one joint. Hide or swap a mass the size of a door, a screen or a ray.
- A night that moves the sun or sets `glow`. The light is fixed when the page is built. Evening is dark cloth, a striped awning, `lantern` panels and a small `ember` core you show and hide. The ground stays the day palette. A black sky and a pool of light are outside this finish. The tea house dusk swaps the paper, the lantern cores and one hard disk.

## References

- `references/yard.md`: sizes, the yard recipe, rotor numbers, the halt, the oasis, and the shadow and figure checks in one place.
- `skills/diorama-pixel/references/scene-api.md`: primitives, the tick context, the pointer. Read that for `P.box` and `P.pose`. Do not copy its soft shadow or its 320 x 240 frame into a dither scene.
