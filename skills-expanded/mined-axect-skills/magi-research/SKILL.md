---
name: magi-research
description: "Run research with three agents in fixed roles, the helpers living in adash terminals (adash's private tmux server): the main session (Claude Opus) plans, decides and edits; a permanent Argon session (Antigravity agy, Gemini 4 Argon) proposes options, designs and mockups; a permanent Astra session (omp, GPT-6.2-Astra; Codex fallback) criticizes and corrects. Use when a research task needs fresh alternatives (figure redesign, section structure, framing, experiment design: \"제안 받아봐\", \"창의적인 대안\", \"원점에서 다시\", \"다른 방식은 없어?\") or a hard check (\"검토받아\", \"비판해줘\", \"수락받아\", \"검토자들과 논의해봐\"), or when the user says magi. Use peer-agent-review alone for a single sign-off by one reviewer; this skill decides which agent to ask, in what order, and how to merge their answers."
---

# magi-research: propose with Argon, criticize with Astra, decide in the main session

Three roles, one rule: **ask Argon when you need options, ask Astra when you need judgment,
and keep every decision and every file edit in the main session.**

**Built on adash terminals.** The proposer and the critic are permanent sessions in adash
terminals (windows of adash's private tmux server) opened in the current worktree, reached
through `adash term`. `magi.py` stops with exit 6 when `adash` is not on PATH, or when the caller
is neither in an adash terminal (`$ADASH_HANDLE` unset) nor has `tmux`; there is no headless
substitute for the roles.

| Role | Agent | Good at | Weak at |
|---|---|---|---|
| Main (decider) | Claude Opus, this session | plans, verifies, edits, talks to the user | anchoring on its first idea; defends its own draft |
| Proposer | Argon: agy, `gemini-4-argon-<level>`, target `argon` | breaking out of the current form, reframing axes and structure, building runnable mockups (figures, scripts) fast | long and confident prose, overstated wording ("완벽히", "원천 차단"), invented section names or line numbers, slow (3 to 15 min) |
| Critic | Astra: omp, `gpt-6.2-astra`, target `astra`; fallback Codex (`codex -s read-only`, target `codex`) when omp is missing or the Astra session cannot be resolved or reached | fact and number checks, claim scope, statistical fairness, citation scope, counterexamples, exact replacement sentences | conservative: improves the current form rather than replacing it |

Observed on a PRX manuscript revision (2026-10): Astra caught a wrong claim in the main
session's draft (a shared lookup table read as "unused when out of window"), a pooled
band that inflated a figure's count fourfold, and a statistically wrong "within error"
sentence. Argon twice produced the figure the author picked after the main session and Astra
had only iterated on the existing layout. Argon's prose also contained a fabricated subsection
list and a misquoted line; every Argon fact must be checked before use.

## Transport

`scripts/magi.py` routes by role on top of `peer-agent-review` (same skill repo), which keeps one
permanent session per target in the worktree, so each agent remembers its earlier answers.

```bash
M=<skills repo>/magi-research/scripts/magi.py
python3 $M propose  --brief _guide/<topic>_brief_<date>.md --marker '<topic> propose'      # Argon (agy)
python3 $M critique --brief _guide/<topic>_apply_<date>.md --marker '<topic> v1 check'     # Astra (omp), accept
python3 $M critique --mode discuss --brief _guide/<topic>_brief_<date>.md --marker '<topic> critique'
python3 $M both     --brief _guide/<topic>_brief_<date>.md --marker '<topic> debate' --out-dir _guide/answers/<topic>
```

- Critic fallback: `critique` uses Astra through omp; if `omp` is not installed, or
  `peer_review.py` exits 2 (cannot resolve or launch) or 3 (not delivered), it re-sends the same
  brief to a read-only Codex session (marker suffixed ` (codex)`). Report which critic answered.
- Proposer: Argon through agy only. If agy is unavailable, say so and ask the user rather than
  substituting another model silently. `magi.py` launches Argon with
  `--dangerously-skip-permissions` (tool calls auto-approved, so mockups run unattended);
  `MAGI_ARGON_SAFE=1` keeps the prompting launch. The flag applies when the session is launched:
  an Argon session already registered keeps its old launch until
  `peer_review.py close -t argon` and the next `magi.py propose`.
- Lower level, same transport: `python3 <skills repo>/peer-agent-review/scripts/peer_review.py targets`
  shows what `astra`, `argon` and `codex` resolve to here; `ask -t <target> --mode …` sends directly.

- `propose` is the only non-hostile mode: alternatives with specs, trade-offs, risks and one
  recommendation, mockups only in the folder the brief names. Use it for Argon.
- `accept` and `discuss` are hostile by design. Use them for Astra.
- Argon answers through a file (`~/.cache/peer-agent-review/answers/argon/<marker>.md`); the
  helper waits for it. Never use a wrapper whose pointer forces "첫 줄은 수락 또는 수정 필요" on a
  proposal request: Argon then writes a verdict line and argues for it instead of proposing.
- Run the two asks in the background and keep working; send to both in parallel when the
  user asks for a discussion ("논의해봐").
- A marker is single use. Briefs live in the project (`_guide/…`), never `/tmp`.

## Which loop to run

### 1. Open problem (design, structure, framing, figure concept): propose → critique → decide

1. **Frame** (main). Write one brief: the user's words verbatim with date, the goal stated as
   the message the reader must get, hard constraints (author rules, data that exists, page
   budget), and what is *not* fixed. Say explicitly that the current form is not a constraint
   when the user says the work is biased toward it.
2. **Propose** (Argon, `propose`). Ask for 2 to 3 distinct options with specs, required reader
   knowledge, risks, and mockups in `<scratch>/<topic>/argon/`. Optionally ask Astra in
   `discuss` mode in parallel for its own option; Astra's option is the conservative baseline.
3. **Screen** (main). Open every mockup yourself. Verify every number and quotation Argon
   used against the files. Drop options that break a hard constraint. Show the user the
   survivors as images with paths and your recommendation; the user picks.
4. **Critique** (Astra, `discuss` or `accept`). Send the chosen option as implemented (not the
   raw proposal): what changed, files, backups, and the questions you are unsure about.
5. **Apply and close** (main). Verify each required fix, apply it, re-send `vN 확인` to Astra
   until 수락. Optional suggestions: apply or say why not.

### 2. Change to existing work (text edit, translation, merge): edit → critique

Main edits, Astra checks in `accept` mode until 수락. Add Argon only as a second reader when
the change is large; treat its "수락" as weak evidence (it has approved text Astra rejected).

### 3. Disagreement or a decision the user wants debated

Send the same `discuss` brief to both. Merge by role: Astra's factual corrections override
Argon's; Argon's alternatives widen the option list; where they recommend different options,
show the user both with the reason each gives and your own pick. Never average the two.

## Main-session duties (do not delegate)

- Re-derive every number either agent reports before you forward it or write it into the work.
  Agreement between two agents that read the same file is shared sourcing, not corroboration.
- When an agent says "your claim is wrong", check the file first; when it is right, say so to
  the user plainly, including when it corrected your own proposal.
- Keep the user's style rules and decisions in each brief; agents do not see the conversation.
- Report to the user: what each agent proposed or corrected, what you chose and why, what is
  still unverified. Do not paste the agents' answers.

## Brief checklist

- User instruction verbatim with date.
- Message or acceptance criterion in one sentence.
- Files to read (paths), backups of previous versions, data that may be used.
- Hard constraints (style rules, page or figure budget, no new measurements).
- Output contract: `propose` for Argon (folder for mockups), `accept`/`discuss` for Astra.
- Numbered questions you are unsure about.
