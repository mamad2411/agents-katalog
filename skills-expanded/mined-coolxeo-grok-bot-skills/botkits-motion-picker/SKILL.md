---
name: botkits-motion-picker
description: >-
  use this when choosing one animation library for a page, a diagram, or a
  short clip, and when applying the calm, snappy, or playful timing numbers.
  Keeps motion to one moment, names the license, and honors reduced motion
---
# Motion picker

Pick at most one library for one motion moment. If the page already communicates with no movement, add none.

## Rules

- One motion moment per page, or none.
- Always respect `prefers-reduced-motion`. When the visitor asks for less motion, show the end state and do not run the animation.
- No scroll hijacking. Lenis is marked `avoid by default`.
- Video output is short moving clips joined with fades. No stills, and no zoom-in or push-in moves.
- A web page follows the media query above. A video file is already motion; a page that embeds it should not autoplay that file when reduced motion is requested.
- Do not commit gif, mp4, webm, or rendered png files. Commit source (HTML, CSS, JS, inline SVG). Leave captures outside the repo.

## Presets

calm is the default. Use snappy or playful only when the user asks for that feel. These rows are fixed. Do not scale them, and do not treat them as the Soft, Snappy, and Chaos set from the source post (that post named the set and did not print numbers).

| Preset | Duration (ms) | Easing | Spring stiffness | Spring damping |
| --- | --- | --- | --- | --- |
| calm (default) | 420 | cubic-bezier(0.33, 0, 0.2, 1) | 140 | 24 |
| snappy | 180 | cubic-bezier(0.2, 0, 0, 1) | 420 | 32 |
| playful | 560 | cubic-bezier(0.34, 1.3, 0.64, 1) | 220 | 12 |

- Tweens and CSS use the duration and the cubic-bezier.
- Spring libraries (Motion, react-spring) use the stiffness and damping pair. Leave mass at the library's own default. If that API also requires a duration, use the duration column too.
- The playful curve rises above 1 so the value overshoots, then settles. Do not use it when reduced motion is on. Use no animation in that case, not a shorter playful curve.

## Pick one

One need, one library. If two rows seem to fit, pick the smaller tool and say what you rejected.

| Need | Library | License |
| --- | --- | --- |
| Multi-step tweens on one timeline | GSAP | unverified |
| Pointer input and shared-element moves in React | Motion | MIT |
| Tweens on styles and attributes, no framework | anime.js | MIT |
| Editing timing on a visual timeline | Theatre.js | Apache-2.0 (core); AGPL-3.0 (Studio) |
| Play back a Bodymovin JSON file | lottie-web | MIT |
| State charts driving a vector file | Rive | MIT |
| Program a video in React components | Remotion | Remotion License |
| Narrated explainers authored in code | Motion Canvas | MIT |
| Turn an HTML scene into a video file | HyperFrames | Apache-2.0 |
| WebGL meshes and cameras | three.js | MIT |
| Sketch-style generative drawing | p5.js | LGPL-2.1 |
| Lots of 2D sprites on WebGL | PixiJS | MIT |
| Boolean paths and scripted vectors | Paper.js | MIT |
| 2D rigid bodies that collide | matter.js | MIT |
| Decorative bursts and shape trails | mo.js | MIT |
| Ambient particle systems | tsParticles | MIT |
| Reveal an SVG stroke over time | Vivus | MIT |
| Letters arriving one at a time | Typed.js | GPL-3.0 |
| Smoothed scrolling | Lenis, avoid by default | MIT |
| React UI that moves on a spring | react-spring | MIT |

License names were read from each repo's LICENSE file on 14 Nov 2026. `unverified` means that file was not in the repo. Links to the files are in [Inspired by](#inspired-by). Paper.js is MIT from the file text (GitHub's SPDX detector returned no id). Typed.js is GPL-3.0 from the header of its LICENSE file (same detector result).

## Traps

- **GSAP.** [greensock/GSAP](https://github.com/greensock/GSAP) has no LICENSE file. The license API returned 404, and the repo root listing has no license filename. The [README](https://github.com/greensock/GSAP/blob/master/README.md#license) and [package.json](https://github.com/greensock/GSAP/blob/master/package.json) both point at [GreenSock's own no-charge license](https://gsap.com/standard-license). That grant is not OSI-approved. It also does not cover every paid product: the page describes a separate business membership when end users pay a fee to use what you built. The table stays `unverified` because the grant text is not a LICENSE file in the repo.
- **Remotion.** [LICENSE.md](https://github.com/remotion-dev/remotion/blob/main/LICENSE.md) is a custom Remotion license, not an OSI license. A paid company license is required above the team-size cap written in that file. The cap for a for-profit organization on the free tier is 3 employees.
- **Theatre.js.** [packages/core/LICENSE](https://github.com/theatre-js/theatre/blob/main/packages/core/LICENSE) is Apache-2.0. [packages/studio/LICENSE](https://github.com/theatre-js/theatre/blob/main/packages/studio/LICENSE) is AGPL-3.0 (GNU Affero General Public License version 3). Studio is the visual editor. Do not ship Studio unless that editor is part of the product. The repo root LICENSE contains both texts; trust the package files for which half you are using.
- **Copyleft neighbors.** p5.js is LGPL-2.1 and Typed.js is GPL-3.0. Read those files before linking either into a closed-source app.

## How to answer

1. Name the need in the user's words, then the one library, or say none.
2. Name the preset. calm unless they asked for snappy or playful.
3. Name the license and any trap that applies.
4. Say whether reduced motion, or a motion moment that already exists, means you should skip it.

Example: a docs page asks for a diagram that draws itself and nothing else. Use [botkits-diagram-design](../botkits-diagram-design/SKILL.md), then its optional line-draw, preset calm. Do not add Lenis. Do not add a second moment on the hero.

## Inspired by

- [N01ennn on X](https://x.com/N01ennn/status/2121695892738629808) (14 Nov 2026). A post that names 20 libraries and says the demos include Soft, Snappy, and Chaos presets. Does well: a wide map in one place. Missing: licenses, a reason to skip a tool, and numeric timing in the post text. This skill keeps the map, drops the hype, and defines its own three presets.

Files opened on 14 Nov 2026. The license column above comes from these files, not from memory.

| Library | What was read |
| --- | --- |
| GSAP | No LICENSE file in [greensock/GSAP](https://github.com/greensock/GSAP). [README license note](https://github.com/greensock/GSAP/blob/master/README.md#license), [package.json](https://github.com/greensock/GSAP/blob/master/package.json), and the [no-charge terms](https://gsap.com/standard-license) those files point at. |
| Motion | [LICENSE.md](https://github.com/motiondivision/motion/blob/main/LICENSE.md) in [motiondivision/motion](https://github.com/motiondivision/motion) |
| anime.js | [LICENSE.md](https://github.com/juliangarnier/anime/blob/master/LICENSE.md) in [juliangarnier/anime](https://github.com/juliangarnier/anime) |
| Theatre.js | [packages/core/LICENSE](https://github.com/theatre-js/theatre/blob/main/packages/core/LICENSE) and [packages/studio/LICENSE](https://github.com/theatre-js/theatre/blob/main/packages/studio/LICENSE) in [theatre-js/theatre](https://github.com/theatre-js/theatre) |
| lottie-web | [LICENSE.md](https://github.com/airbnb/lottie-web/blob/master/LICENSE.md) in [airbnb/lottie-web](https://github.com/airbnb/lottie-web) |
| Rive | [LICENSE](https://github.com/rive-app/rive-wasm/blob/master/LICENSE) in [rive-app/rive-wasm](https://github.com/rive-app/rive-wasm) |
| Remotion | [LICENSE.md](https://github.com/remotion-dev/remotion/blob/main/LICENSE.md) in [remotion-dev/remotion](https://github.com/remotion-dev/remotion) |
| Motion Canvas | [LICENSE](https://github.com/motion-canvas/motion-canvas/blob/main/LICENSE) in [motion-canvas/motion-canvas](https://github.com/motion-canvas/motion-canvas) |
| HyperFrames | [LICENSE](https://github.com/heygen-com/hyperframes/blob/main/LICENSE) in [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) |
| three.js | [LICENSE](https://github.com/mrdoob/three.js/blob/dev/LICENSE) in [mrdoob/three.js](https://github.com/mrdoob/three.js) |
| p5.js | [license.txt](https://github.com/processing/p5.js/blob/main/license.txt) in [processing/p5.js](https://github.com/processing/p5.js) |
| PixiJS | [LICENSE](https://github.com/pixijs/pixijs/blob/dev/LICENSE) in [pixijs/pixijs](https://github.com/pixijs/pixijs) |
| Paper.js | [LICENSE.txt](https://github.com/paperjs/paper.js/blob/develop/LICENSE.txt) in [paperjs/paper.js](https://github.com/paperjs/paper.js) |
| matter.js | [LICENSE](https://github.com/liabru/matter-js/blob/master/LICENSE) in [liabru/matter-js](https://github.com/liabru/matter-js) |
| mo.js | [LICENSE.md](https://github.com/mojs/mojs/blob/main/LICENSE.md) in [mojs/mojs](https://github.com/mojs/mojs) |
| tsParticles | [LICENSE](https://github.com/tsparticles/tsparticles/blob/main/LICENSE) in [tsparticles/tsparticles](https://github.com/tsparticles/tsparticles) |
| Vivus | [LICENSE](https://github.com/maxwellito/vivus/blob/master/LICENSE) and [readme.md](https://github.com/maxwellito/vivus/blob/master/readme.md) in [maxwellito/vivus](https://github.com/maxwellito/vivus) |
| Typed.js | [LICENSE.txt](https://github.com/mattboldt/typed.js/blob/main/LICENSE.txt) in [mattboldt/typed.js](https://github.com/mattboldt/typed.js) |
| Lenis | [LICENSE](https://github.com/darkroomengineering/lenis/blob/main/LICENSE) in [darkroomengineering/lenis](https://github.com/darkroomengineering/lenis) |
| react-spring | [LICENSE](https://github.com/pmndrs/react-spring/blob/next/LICENSE) in [pmndrs/react-spring](https://github.com/pmndrs/react-spring) |

## What this version adds

- One need mapped to one library, with a license taken from that repo's LICENSE file, or `unverified` when the file is absent.
- calm, snappy, and playful as fixed durations, cubic-beziers, and spring stiffness/damping. calm is the default.
- One motion moment per page or none, `prefers-reduced-motion` always, Lenis marked avoid by default, and video kept to short clips with fades and no zoom-in or push-in.
- The GSAP, Remotion, and Theatre.js traps above, checked against the files linked here.
