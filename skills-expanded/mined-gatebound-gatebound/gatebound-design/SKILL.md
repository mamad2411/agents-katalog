---
name: gatebound-design
description: Read a Figma file, screenshots, HTML files, a live site URL, a design preset, or a user pattern file and derive a design specification with patterns, components, and design tokens, recording everything the source does not show as an assumption. Korean triggers — "이 사이트처럼 만들어줘", "디자인 패턴 정리해줘", "레퍼런스 사이트에서 뽑아줘", "디자인 프리셋 적용해줘". English triggers — "make it look like this site", "extract design patterns from this reference", "apply this design preset". NOT for a mockup's screen list and flows — use gatebound-mockup for that.
user-invocable: false
---

# gatebound-design

Invoke `/gatebound:design` with the user's Figma URL, screenshot or HTML paths,
live site URL, preset name, or pattern file as the argument.

Do not read the source or extract anything here.
`plugin/commands/design.md` is the execution instruction; this file only
routes to it.

If the user wants a screen-by-screen spec with flows and per-screen states,
use `gatebound-mockup` instead. If the user wants the design implemented as
working code, this is not the right skill.

Under a host without slash commands (Codex), `/gatebound:design` does not exist:
read `commands/design.md` two directories above this skill's folder and follow
it, applying `policy/codex.md` from the same plugin.
