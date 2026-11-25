---
name: use-testing
description: "Build process. How work is PROVEN here — before you say «done», «it works», «ready to check». Load it when you are about to report a result, when a gate goes green and you feel finished, when something must be verified on the node, and when the owner asks for proof («show me the proof», «докажи»). The rule that changes behaviour: two proofs from DIFFERENT planes, one of them with a negative control, and a build log is never one of them — it reads the same whether the capability works or not."
---

# use-testing

**Process: build.** A hint, not a law, in HOW you prove: know a better way for the case in front of you — use it and say so.

## 1. Two proofs, from different planes

A step or a substep closes on **two** proofs from different planes — otherwise the same thing was measured twice.

| Plane | Answers |
|---|---|
| the tree | is the code well-formed — guards, types, structure |
| the wire | what the node actually answers — status, headers, body of a door or a page |
| the eye | what a person sees — a real browser, both themes, a narrow screen, a real mouse |
| the data | what was written — a row, a file, a commit, a tag on GitHub |
| the story | is this the thing that was ASKED for — the owner's word |

A proof has four fields: **what was run** · **the verbatim output** · **what it proves** · **how it would look without the change**. The
last field separates a proof from a ritual. A build log is never one of the two: «it compiles», «200», «RC=0» say nothing of the capability.

## 2. Green was green BEFORE your change — so one proof carries a negative control

Every guard passed before you touched anything. So one proof breaks the thing on purpose, sees it fail, and puts it back: spoil the input
(a wrong name, a missing section, a returned row), remove the fix (old code, same probe), or ask about something known to be absent. A
guard that stays green on a spoiled input is blind — and that is a finding, not a pass. When the live data cannot be changed without the
owner (a published element, a person's records), spoil the input on the way instead: a copy in a temporary folder, or the door's answer
replaced inside the browser (CDP `Fetch.fulfillRequest`).

## 3. The defects no guard catches

Markup can be correct and wrong: a page that reads like another site, blocks that do not tell a story, a section repeated in another guise.
The proof is comparison — the page and its neighbour side by side — and the owner's eye. Scrolling, timing, anything a page does by itself
is proven in a real browser with a person's timing, not by a fixed pause.

## 4. Measurements that lied here — each looked like success

- **`/api/health` → `commit`** is the commit the process started on; `builtAt` is the build. After a rebuild also count the page's
  `/_next/static/*` files that do not answer 200.
- **`npm run build | tail`** prints tail's exit code, always 0. Log to a file, `RC=$?` right after npm, require a marker.
- **pm2 `online`** for a process in an endless restart loop: watch the restart count, uptime GROWING between two samples, and who holds
  the port.
- **A page whose data an island fetches after load** has none of that data in its server HTML — a `curl` finds nothing even when it
  works. Prove it in a browser, or ask the door the island asks.
- **A search over a whole page** finds the navigation: menus, crumbs and footers print every page's title. Address the element that
  belongs to this page (`<h1>`, a `data-*` mark); the same check on ANOTHER page must answer differently.
- **`git status` under `core.autocrlf`** shows «M» for a file rewritten with the same text; ask `git diff --cached HEAD` after `git add`.
- **Search by meaning always returns the nearest neighbour** — «nothing found» needs a threshold or a filter.
- **`grep` in Git Bash**: `-P` fails on the locale and reads as 0, `-i` does not fold Cyrillic, `-c $'\r'` counts every line. Zero is not
  «not there» until a known-present item gives one.
- **The service worker serves yesterday's build** in today's browser: unregister it AND clear `caches`.
- **A hidden browser tab reports width 0**; check `document.visibilityState` before trusting an automated measurement.

## 5. What cannot be proven — say it, never substitute

No key, the owner's session, a phone, a Telegram account — name the missing proof in the report, in the same message, and do not replace it
with something easy to obtain. Never simulate what the owner does in five seconds (a voice note, a sign-in, a payment): the simulation
checks another path. When the proof needs a live run of an agent with a model, it runs only by the owner's word, with its price named.

## 6. The form — and the owner's command

The owner may ask for proof at any moment («show me the proof», «докажи», «покажи доказательства» — one request). Answer with what is done
by that minute, in this form — an empty field is visible, prose hides it:

```
PROOF 1 — plane <which>
  ran:          <command / request / action>
  output:       <verbatim>
  proves:       <which line means it works>
  without it:   <how the same output would look without the change>
PROOF 2 — plane <another>
  …
NEGATIVE CONTROL
  case:         <the input whose answer must differ>
  answer:       <and it differed — like this>
DELIVERY (not a proof)
  build / release / restart: <exit codes, hashes, tags>
NOT PROVEN
  <what needs the owner or is out of reach, and why>
```

## 7. Before you say «done»

1. Name the two planes and paste the verbatim output of each.
2. Say what would have looked different without the change.
3. Say what remains unproven — plainly, in the same message.

If point 1 cannot be filled, the work is not finished: it is unmeasured.
