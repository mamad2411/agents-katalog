---
name: urlpattern
description: >-
  URL Pattern: The URL Pattern Standard provides a web platform primitive for matching URLs based on a convenient pattern syntax. Covers URL Pattern Living Standard. Use when matching URLs with a pattern. Triggers: URLPattern.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# URL Pattern

The URL Pattern Standard provides a web platform primitive for matching URLs based on a convenient pattern syntax.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when matching URLs with a pattern.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: URL Pattern Living Standard (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **URL Pattern.** "Developers should refer to the Living Standard for the most current error corrections and other developments."
2. **1.6. Constructor string parsing.** "A constructor string parser has an associated input , a string, which must be set upon creation."
3. **1.6. Constructor string parsing.** "A constructor string parser has an associated token list , a token list , which must be set upon creation."
4. **1.6. Constructor string parsing.** "It must be one of the following: " init " " protocol " " authority " " username " " password " " hostname " " port " " pathname " " search " " hash " " done " The URLPattern constructor string algorithm is very similar to the basic URL parser algorithm, but some differences prevent us from using that algorithm directly."
5. **2. Pattern strings.** "It can be parsed to produce a part list which describes, in order, what must appear in a component string for the pattern string to match."
6. **2.1.1. Tokens.** "It must be one of the following: " open " The token represents a U+007B ( { ) code point."
7. **2.1.2. Tokenizing.** "A tokenize policy is a string that must be either " strict " or " lenient "."
8. **2.1.3. Parts.** "A part has an associated type , a string, which must be set upon creation."

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in [`references/requirements.md`](references/requirements.md) and implement each one that applies to the role.
   -> [`references/requirements.md`](references/requirements.md)
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the heading it came from.
3. **Upgrade** (only when asked). Follow the upgrade section from the source line to the target.
   -> [`references/versions.md`](references/versions.md)
   ✓ The result cites the target line and no longer depends on a requirement that only the old line stated.

## Verify before done

- [ ] The artifact cites the target line's revision from [Sources](#sources).
- [ ] Every applicable quoted requirement in [`references/requirements.md`](references/requirements.md) holds.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [URL Pattern Living Standard](https://urlpattern.spec.whatwg.org/review-drafts/2026-09/): Review Draft, Review Draft 2026-09 (Review Draft, 2026-09), checked 2026-10-06.
