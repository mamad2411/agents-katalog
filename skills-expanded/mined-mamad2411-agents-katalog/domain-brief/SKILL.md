---
name: domain-brief
description: Produces a <DOMAIN>-BRIEF.md priming a pack's gates before a non-content, non-visual domain build. Use before that build; not for content (content-brief) or visuals (design-brief).
---

# domain-brief

The **generic** front-end of every domain pack — the systems-not-skills analogue of `content-brief`
(content) and `design-brief` (visual). Instead of one brief skill per domain, this ONE skill reads the
resolved domain pack **as data** (the same way the kernel does) and turns "what they're producing in this
domain" into a concrete **domain contract** (`<DOMAIN>-BRIEF.md`) **before the executor produces a thing**.
The deterministic scaffolder `brief-emit.py` pulls the pack's cross-cutting spec checks + the sub_target's
must-declares + the gates to prime; you (the skill) fill them with real values and push back on thin inputs.

## What this does / does not do

Does: resolve the domain + `sub_target` from `intake.json`, run `brief-emit.py --domain <id> --sub-target
<st>` to scaffold the pack's must-declares, fill them with concrete decisions (clarifying when thin), and
write `<DOMAIN>-BRIEF.md` that the pack's gates audit the deliverable against; write a domain-brief receipt.
Does **not**: produce the deliverable itself (the executor does, under this brief), run the verification
mode (the pack's gates do — this *primes* them), or override the two specialized briefs (content/visual).

## When NOT to use

- The domain is **content** — use `content-brief` (richer audience/voice/outline treatment).
- The work is the **visual design contract** — use `design-brief` (DESIGN.md + DTCG tokens).
- The domain is **software** — the kernel `specify` + the software overlay already carry the contract; no separate brief.
- A current, committed `<DOMAIN>-BRIEF.md` already fits and nothing changed — edit it; do not rewrite the contract the build depends on.

## Reference Routing

| Situation | Reference |
|---|---|
| Scaffold the brief from a pack | `./brief-emit.py --domain <id> --sub-target <st>` |
| The pack's checks · must-declares · gates | `../../../domains/<id>/acceptance/{overlay,sub-targets}.md` · `domain.yaml` |
| Per-sub_target vocabulary | `../../../domains/<id>/vocabulary.md` |

## Inputs

- The resolved `domain` + `sub_target` (from `state/intake.json`), or establish them via clarification.
- The domain pack at `library/domains/<id>/` (read as data — never hardcode a domain here).

## How to do it

1. **Resolve** domain + sub_target from `intake.json`. If the domain is content/visual/software, defer per *When NOT to use*.
2. **Scaffold**: `python brief-emit.py --domain <id> --sub-target <st> --out <DOMAIN>-BRIEF.md`. This pulls the pack's overlay checks + the sub_target's must-declares + the gates + the verification mode — all from pack data.
3. **Fill, do not default**: replace each scaffolded check with a concrete decision. An unfilled field is an open spec question — run the Clarification Protocol; push back on vague inputs (the pack's cold-start lists the thin-input traps for that domain).
4. **Confirm the must-declares** for the sub_target are all present (or N/A with a reason), so the brief primes the exact gates that will judge the deliverable.

## Output

- **`<DOMAIN>-BRIEF.md`** at the product root — persistence **Spec-Anchored** (versions with the deliverable). Carries the filled spec inputs, the sub_target's must-declares, and the gates + verification mode it primes.
- **receipt** (`<workspace>/receipts/domain-brief-receipt.json`): base schema + `domain`, `sub_target`, `checks_filled`, `gates_primed`, `verification_mode`, `brief_path`. persistence: Spec-Anchored.

## Proactive Triggers

- **A field left as the scaffold placeholder**: that is an unanswered spec question — clarify before the executor starts, do not let it default.
- **An unknown sub_target**: `brief-emit.py` flags it as not-in-matrix — resolve to a real sub_target so the must-declares load.
- **A sensitive domain (security-review)**: confirm the authorization context first (the pack's blocking gate) before writing the brief.

## Completion Criteria

**Done when:** a `<DOMAIN>-BRIEF.md` exists with every pack check filled (or N/A + reason), the sub_target's must-declares present, and a domain-brief receipt records the domain + gates primed.

**Not done if:** any field is still a scaffold placeholder; the sub_target was guessed; it was run for content/visual/software (those have their own path).

**Next step:** the executor produces the deliverable under the brief; the pack's gates verify it against the filled contract.

## Related Skills

- **content-brief / design-brief**: the two *specialized* briefs (content, visual); domain-brief is the *generic* one for the other domains — same role, pack-driven.
- **specify**: writes the task card (the what/why); domain-brief writes the *domain contract* (the pack's must-declares) for the deliverable. Complementary.
- **intake**: resolves the domain pack domain-brief reads.
