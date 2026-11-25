---
name: warrant
description: Keeps research honest. Use whenever the user does research with you, in ML/CS experiments, data analysis, science, statistics or mathematics. Typical moments are framing a research question, planning or running an experiment, comparing methods, reporting a result or metric, citing papers, reviewing a draft or bibliography, or writing up findings. Also use when the user asks you to review, referee or fact-check a paper or draft, check its references or statistics, or asks where a number came from.
---

# warrant: every number and citation must be earned

warrant checks your research output with plain code, never a model:

- **Numbers.** Every decimal and percentage in your final reply must trace to something that actually ran or was read. A value within rounding counts. So does a mean of logged values, or a difference or ratio of traced numbers. Text you wrote, or wrote and read back, is never evidence.
- **Citations.** DOIs, arXiv ids and quoted titles are looked up in doi.org, arXiv, OpenAlex and Crossref.
- **Statistics.** Every reported p-value is recomputed from its test statistic (t, F, chi2, r, z).
- **Enforcement.** Hooks capture tool output automatically. The Stop hook blocks a reply once if it fails any check.
- **Paper review.** `warrant review` reads the cited papers so you don't: you judge short evidence cards, and code verifies your quotes (section 7).

## Running the CLI

Try `warrant` first. If it is not found, run the plugin's copy:

```bash
W="$(ls -d ~/.claude/plugins/cache/warrant/warrant/*/ | sort -V | tail -1)bin/warrant.py"; python "$W" status
```

## 1. Start: turn it on

At the start of a research task, check for a `.warrant/` folder in the project. If there is none, run:

```bash
warrant init "<the research question, in one sentence>"
```

Tell the user it is on. Hooks stay silent in projects without `.warrant/`. If the question changes, run `warrant question "..." --hypothesis "..."`.

## 2. Before an experiment: pre-register

Commit to what would refute the claim, **before** you see results:

```bash
warrant claim "smoothing 0.1 improves val_acc over baseline"            # -> claim #N
warrant predict N '{"metric":"val_acc","op":"le","of":"baseline","margin":0.0}'
```

`op` is lt/le/gt/ge/eq/ne. `of` is `baseline` or `absolute` (then also give `threshold`). `margin` is relative slack. To compose several clauses, use `--mode all`.

## 3. After running: let code decide

```bash
warrant result N --observed val_acc=0.812 --baseline val_acc=0.809      # supported | refuted | inconclusive
warrant evidence N --log runs/seeds.log --metric val_acc=0.812 --seeds 3 --std 0.006 [--p 0.03]
```

Report the verdict as given. A refuted idea is buried in the graveyard. A missing metric means `inconclusive`: say so, do not round it up to a win.

## 4. Writing results

- **Run first, report second.** Each reported number comes from output in this session. You may compute it from that output (a mean, a difference, a ratio).
- **Mark estimates.** Write `~` before any number from memory, a paper, or a guess, e.g. "~76% top-1 reported by He et al.". Better: cite it with a DOI or arXiv id.
- **Match wording to evidence.**

| wording | needs |
|---|---|
| "significant(ly)" | >=3 seeds and p < 0.05 |
| "improves", "outperforms", "beats" | >=3 seeds, or a supported pre-registered predicate |
| "proves" | a proof a checker accepts: `warrant evidence N --type proof --ref X.lean` (no `sorry`), or a SymPy `.py` with asserts |
| "always", "never", "clearly" | a reason that holds every time; otherwise drop the word |

Strong evidence should not be hedged into "may slightly help". Weak evidence should not be inflated.
- **Citations.** Give a DOI or arXiv id when you know it. If you are not sure a paper exists, say so. Never invent a title, author list, venue or id.

## 5. When the Stop hook blocks you

The block message lists each untraced number or bad citation. For each one, do one of these:

1. run the command that produces it;
2. replace it with the traced value;
3. mark it `~` and say where it came from;
4. remove it.

Fix a bad citation, or remove it. Do not argue with the hook. Do not launder numbers through `echo`, `print` or files you write: the audit trail records every command.

## 6. Stay on the question

If work drifts from the recorded question, tell the user in one line and ask: is this a new sub-question, or a tangent? Never re-propose a graveyard idea without pre-registering what new result would justify it. `warrant claim` warns when an idea resembles a dead one.

## 7. Watching live experiments (`warrant watch`)

When you start a run that writes logs, start the sentinels in the background and keep working:

```bash
warrant watch runs/ &      # 0 tokens: NaN/inf, crashes, divergence, overfitting, leakage, stalls, refuted predictions
```

New alerts arrive in your context as single `[warrant watch] ...` lines. Act on red ones right away: stop or fix the run, don't wait for it to finish. Mention yellow ones to the user. Don't tail or re-read logs yourself to check on a run; the sentinels already do that.

## 8. Reviewing a paper or draft (`warrant review`)

Use this when the user asks you to review, referee, fact-check or vet a paper. That includes their own draft before submission. **Do not read the cited papers yourself.** warrant does the reading and hands you only what needs judgment.

1. **Run the code checks:**
   ```bash
   warrant review 1706.03762          # arXiv id, arXiv-hosted DOI, a LaTeX folder, or main.tex
   ```
   This writes `warrant-review/<paper>/report.md` and `cards.json`. Code already checked:
   - each reference exists;
   - each number attributed to a cited paper appears in that paper's full text;
   - abstract numbers appear in the body;
   - every reported p-value follows from its test statistic (statcheck);
   - means are possible for their n (GRIM);
   - "significant" comes with statistics.

   Report these findings as given. They are facts, not opinions.
2. **Judge the evidence cards.** Each card is one citing claim plus the 2 best-matching passages (~110 words each) from the cited paper. Read only the cards. For each card, decide:
   - `supports`: the passage says what the claim attributes to it;
   - `partial`: related, but the claim says more, or something different;
   - `contradicts`: the passage says the opposite;
   - `not_found`: the passages don't address the claim. This is not proof the paper lacks it, only that retrieval didn't surface it.

   Every verdict except `not_found` needs a **verbatim quote** copied from a passage. Write `verdicts.json` as `[{"card": 1, "verdict": "partial", "quote": "..."}]`.
3. **Verify:** run `warrant review --verify warrant-review/<paper>/verdicts.json`. Code rejects any verdict whose quote is not verbatim in the cited paper. Fix the rejected ones, never paraphrase.
4. **Write the referee report.** Lead with the code-verified problems, then the citation verdicts, then your own assessment of:
   - methods: design, controls, baselines, ablations, seeds;
   - reproducibility: code, data, hyperparameters;
   - whether the conclusions follow from the evidence;
   - the field's reporting guideline, where one applies: CONSORT (trials), PRISMA (reviews), ARRIVE (animals), or ML reproducibility checklists.

   Write each comment as **Location · Observation · Evidence · Why it matters · Requested action**. Label each comment `[verified by code]`, `[quote-verified]` or `[reviewer judgment]` so the reader knows what is checked and what is opinion. (Comment structure adapted from the MIT-licensed peer-review skill in K-Dense-AI/claude-scientific-skills.)

Other paper checks:

```bash
warrant stats draft.md                     # recompute every p-value (t, F, chi2, r, z) and GRIM-check means
warrant audit 10.1038/s41586-021-03819-2   # every reference in a paper: DOI, arXiv id, URL, or refs.bib / main.bbl
warrant cites draft.md              # citations in a draft
warrant trace draft.md --all        # where each number came from
warrant report --draft draft.md     # HTML: numbers green (hover = source line) or red
warrant status | warrant report --html
warrant dashboard                   # live local view for the user
```

"Not found anywhere" in `audit` is a lead, not proof. Tell the user to check it by hand before calling a reference fabricated.

Never edit `.warrant/`, captured outputs, or logs attached as evidence. Hashes detect it.
