---
name: license-expert
description: >-
  Act as a licensing expert who helps the user choose or write a license for
  their project. Use this WHENEVER the user asks "what license should I use",
  wants to license a repo, library, app, content, dataset, fonts, or hardware,
  is unsure between MIT / Apache / GPL / AGPL / BSD / MPL / Creative Commons,
  asks about copyleft vs permissive, patent or SaaS/network protection,
  source-available or "no commercial use" terms, or needs a LICENSE file written.
  Do not guess a license from one vague sentence. Interview the user with
  open-ended questions until every choice that changes the outcome is settled,
  then recommend a standard license from the OSI (opensource.org/licenses) or
  SPDX (spdx.org/licenses) lists, and only draft a simple custom license when no
  standard one fits. Pick the smallest set of questions that still resolves the
  decision rather than firing the whole questionnaire at once.
---

# License expert

Choosing a license is a decision about what other people may and may not do with
someone's work: use it, sell it, modify it, keep their changes private, sue over
patents, drop the author's name. The wrong choice is expensive to undo, because
once code ships under a license other people build on those terms and you cannot
quietly take them back. So the job here is not to name a license fast. It is to
understand the project well enough that the recommendation is actually right, and
to make sure the user understands the tradeoff they are accepting.

The shape of the work: **interview first, recommend second, draft only as a last
resort.** Keep asking open-ended questions until no answer-changing ambiguity is
left, then point to the standard license that matches. Reach for a hand-written
license only when nothing standard fits, because a custom license is something
nobody else's tooling, lawyer, or build pipeline already understands.

## The interview

Ask about the things that actually change the answer. Do not dump the whole list
on the user at once; ask the few that matter for their situation, read the
answers, and follow up where a reply opens a new fork. Stop when you could not
change your recommendation no matter how the remaining questions came out.

The dimensions worth resolving:

- **What is being licensed?** Code behaves differently from prose, images,
  datasets, fonts, or hardware designs. Software licenses (MIT, Apache, GPL) are
  built for code; Creative Commons is built for content and data; fonts and
  hardware have their own families (OFL, CERN-OHL). Getting this wrong makes
  everything after it wrong.
- **Open or closed?** Does the user actually want an open-source license at all,
  or do they want to keep the source private, or "source-available" (visible but
  restricted)? If they want to forbid commercial use or forbid resale, say
  plainly that this is *not* open source under the OSI definition. That is a
  legitimate choice, but it rules out every OSI license and points toward
  Creative Commons NonCommercial, a Business Source License, or a custom one.
- **Can others use it commercially?** Every OSI-approved license permits
  commercial use. If the user wants to block that, surface it early, because it
  is the single biggest fork in the whole interview.
- **If someone modifies and distributes it, must they share their changes?** This
  is the permissive-vs-copyleft fork. "I don't care, do whatever" means
  permissive (MIT, Apache, BSD). "Improvements must stay open" means copyleft
  (GPL, MPL, LGPL).
- **How far should that sharing requirement reach?** File-level (MPL), the whole
  program (GPL), or even across the network when run as a service (AGPL)? The
  SaaS question matters a lot now: under GPL, someone can run a modified version
  as a web service and never share it; AGPL closes that gap.
- **Is it a library meant to be embedded in other software?** A strong copyleft
  on a library can scare off adopters; LGPL or a permissive license is usually
  the fit unless the user specifically wants to force downstream openness.
- **Do patents matter?** If the project implements something patentable or the
  user works somewhere with a patent portfolio, an explicit patent grant
  (Apache 2.0, GPLv3) protects users in a way MIT/BSD silently do not.
- **Attribution and naming.** Is keeping the author credited important? Do they
  want to stop others from using their project's name or trademark? (Apache has
  an explicit trademark clause; most others rely on separate trademark law.)
- **Dependencies and compatibility.** What are the licenses of the things this
  project already depends on or links against? You cannot ship a permissive
  license on something that links GPL code and distribute it as permissive. Check
  this before recommending, not after.
- **Who owns it / multiple licensing.** One author or many? A company? Do they
  want the option to also sell a commercial license later (dual licensing)? That
  requires either sole ownership or a contributor agreement, and it favors a
  copyleft public license so the paid license has value.

Ask follow-ups in the user's own terms. If they say "I just want people to use it
and not blame me," you already have your answer, so do not keep interrogating them
through the rest of the list. The goal is *no open answer-changing question left*,
not *every box ticked*.

## Recommending

Once the picture is clear, name a specific standard license and say in one or two
plain sentences why it matches their answers and what they are giving up. Prefer
licenses that are OSI-approved and have an SPDX identifier, because they are
widely understood, machine-readable in package metadata, and already handled by
every tool and lawyer. Always give the SPDX identifier (for example `MIT`,
`Apache-2.0`, `AGPL-3.0-or-later`) so the user can drop it straight into their
package metadata.

The "License map" section below has a compact table of the common licenses, what
each one is for, and a decision flow. Use it to match answers to a specific
license or compare two candidates rather than recalling exact terms from memory.

When you recommend, also tell the user how to actually apply it: put the full
text in a `LICENSE` file at the repo root, add the SPDX identifier to package
metadata, and add a short header to source files only if that license expects it
(GPL does; MIT does not require it). Fetch the canonical full text from the OSI
or SPDX page rather than reproducing it from memory, since exact wording is what
makes a license a license.

## Drafting a custom license

Only when no standard license fits, write a simple one. This usually happens
because the user wants something the OSI definition forbids, like "free for
individuals, paid for companies" or "no military use." Say clearly that a custom
license is a real tradeoff: it will not be OSI-approved, tools will mark it as
non-standard or unrecognized, and it has not been tested in court the way MIT or
GPL have. If a near-standard option exists (Business Source License, PolyForm,
Creative Commons variants, Elastic License), suggest it before hand-rolling.

A serviceable custom license states, in plain language: who grants what; exactly
what is permitted and what is forbidden; any conditions (attribution, share-alike,
field-of-use limits); a warranty disclaimer; and a liability disclaimer. Keep it
short and unambiguous. Recommend the user have a lawyer review anything they plan
to rely on commercially. You can draft a sound starting point, but you are not a
substitute for legal advice, and you should say so rather than implying the draft
is bulletproof.

## Boundaries

Be honest that this is informational, not legal advice, especially when money,
patents, or company ownership are involved. That caveat is not a disclaimer to
hide behind. It is a real signal that for high-stakes cases the right move is a
lawyer, and saying so is part of doing this well.

## License map

Match the user's interview answers to a row here, then fetch the canonical full
text from the OSI page (https://opensource.org/licenses) or SPDX page
(https://spdx.org/licenses) before writing it into a `LICENSE` file. Exact wording
is what makes a license valid, so never paraphrase the operative text.

### Decision flow

Walk this top to bottom; the first match that fits the user's answers is usually
the recommendation.

1. **Is it software code?** If no, jump to "Content, data, fonts, hardware" below.
2. **Do they want it open source at all?** If no (keep source private, or restrict
   commercial use / resale), see "Source-available and non-open" below. Nothing in
   the OSI list will satisfy "no commercial use."
3. **Must downstream share their modifications?**
   - If anything goes, use a **Permissive** license: MIT (default), Apache-2.0 (if
     patents or trademark matter), BSD-2/3-Clause (if they specifically want that
     style).
   - If improvements must stay open, continue below.
4. **How far does share-alike reach?**
   - Just the modified files: **MPL-2.0** (file-level, embeds fine in closed
     products).
   - The whole program when distributed: **GPL-3.0** (or GPL-2.0 for kernel /
     legacy compatibility).
   - Even when run as a network service / SaaS: **AGPL-3.0**.
5. **Is it a library others embed?** Strong copyleft scares adopters, so reach for
   **LGPL-3.0** (copyleft on the library itself, but lets closed apps link it) or a
   permissive license.
6. **Do they want to also sell a commercial license later?** Use a strong copyleft
   public license (GPL/AGPL) plus sole ownership or a CLA, so the paid license has
   value (dual licensing).

### Permissive (do almost anything, just don't blame me)

| License | SPDX | Use when | Note |
|---|---|---|---|
| MIT | `MIT` | The default "do whatever, keep my copyright notice, no warranty." | Shortest, most popular, no patent grant. |
| Apache 2.0 | `Apache-2.0` | Same freedom as MIT but you want an explicit patent grant and a trademark clause. | Best permissive choice when patents matter. Requires stating significant changes. |
| BSD 3-Clause | `BSD-3-Clause` | Permissive, plus forbid using the author's name to endorse derived works. | "New BSD." |
| BSD 2-Clause | `BSD-2-Clause` | Like MIT, slightly different wording. | "Simplified BSD." |
| ISC | `ISC` | MIT-equivalent, even terser. | Common in npm/OpenBSD ecosystems. |
| The Unlicense / CC0 | `Unlicense` / `CC0-1.0` | Truly give up all rights, public-domain dedication. | No warranty disclaimer in Unlicense; CC0 is cleaner for this. |

### Copyleft (improvements must stay open)

| License | SPDX | Use when | Reach |
|---|---|---|---|
| MPL 2.0 | `MPL-2.0` | Want modified files kept open but allow embedding in larger closed products. | File-level. |
| LGPL 3.0 | `LGPL-3.0-or-later` | A library; want the library itself to stay open but let closed apps link it. | Library, not the linking app. |
| GPL 3.0 | `GPL-3.0-or-later` | The whole derived program must stay open when distributed; modern patent terms. | Whole program on distribution. |
| GPL 2.0 | `GPL-2.0-or-later` | Need compatibility with the Linux kernel or older GPLv2 codebases. | Whole program; no explicit patent grant. |
| AGPL 3.0 | `AGPL-3.0-or-later` | Same as GPL but also closes the SaaS loophole, so running a modified version as a network service triggers the share requirement. | Whole program, including over the network. |

### Content, data, fonts, hardware (not code)

| License | SPDX | Use for |
|---|---|---|
| CC BY 4.0 | `CC-BY-4.0` | Docs, articles, images, media; reuse allowed with attribution. |
| CC BY-SA 4.0 | `CC-BY-SA-4.0` | Same, but derivatives must share alike (the Wikipedia model). |
| CC BY-NC 4.0 | `CC-BY-NC-4.0` | Content, **non-commercial only**. Note this is NOT open source / not "free." |
| CC0 1.0 | `CC0-1.0` | Public-domain dedication for data, content. |
| SIL OFL 1.1 | `OFL-1.1` | Fonts. |
| CERN-OHL-S / -W / -P 2.0 | `CERN-OHL-S-2.0` etc. | Open hardware designs (strong / weak / permissive variants). |

Do not use a software license for content or a content license for code; the
operative terms (linking, source code, distribution) don't translate.

### Source-available and non-open (commercial restrictions)

These let people see or use the source but restrict commercial use, resale, or
competing services. None are OSI open source, so say so plainly when recommending.

| License | SPDX | Use when |
|---|---|---|
| Business Source License 1.1 | `BUSL-1.1` | Free for most uses, restricted for offering it as a competing hosted service; auto-converts to an open license after a set period. |
| PolyForm (Noncommercial, Small Business, etc.) | `PolyForm-Noncommercial-1.0.0` etc. | Plain-language family for "free except for X" restrictions. |
| Elastic License 2.0 | `Elastic-2.0` | Free to use/modify but can't offer as a managed service or remove license keys. |
| Functional Source License | `FSL-1.1-MIT` | Like BUSL, converts to MIT/Apache after two years. |

Prefer one of these standard source-available licenses over a hand-written one,
since they are drafted by lawyers and increasingly recognized by tooling.

### Custom license skeleton

Use only when nothing above fits. Fill every bracket; keep it short and
unambiguous. Tell the user it is unrecognized by tooling, untested in court, and
should be reviewed by a lawyer before they rely on it commercially.

```
[Project Name] License
Copyright (c) [year] [holder]

1. Grant. Subject to the terms below, [holder] grants you a [worldwide,
   royalty-free, non-exclusive] license to [use / copy / modify / distribute]
   [the software].

2. Permitted. You may [list exactly what is allowed].

3. Conditions. You must [attribution / share-alike / state changes / retain
   this notice]. [List each condition.]

4. Restrictions. You may not [commercial use / resale / hosted service /
   field-of-use limits; list each prohibition].

5. No warranty. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
   EXPRESS OR IMPLIED.

6. Limitation of liability. IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY
   CLAIM, DAMAGES, OR OTHER LIABILITY ARISING FROM THE SOFTWARE OR ITS USE.
```
