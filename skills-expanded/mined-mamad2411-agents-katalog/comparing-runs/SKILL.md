---
name: comparing-runs
description: 'Use when several finished runs have to become one table that survives review: ablation arms that differ in more than the thing under study, 消融臂不可比, 消融表, a baseline reproduced below its published number, an unfair comparison where one arm got a bigger tuning budget, how many seeds to run and what an error bar captures, 误差棒, seed 方差, and tracing a table row back to the commit and command that produced it. Do not use for diagnosing a single run that will not train, for drafting the prose around results, or for rendering a comparison as a figure.'
license: MIT
compatibility: Requires git for run provenance. No other tooling.
---

# Comparing Runs

One run being correct is a different problem from many runs being comparable. This skill owns the
second: turning a pile of finished runs into a table that survives a reviewer. It does not
diagnose a run that is training wrong, write the prose around the results, or draw the figure.

The failure it prevents: a matrix that ran to completion and cannot support the claim the paper
wants to make.

## The bar

A number belongs in a table when someone else can get it back. That means three things, and the
rest of this file is how each one is earned:

- **Comparable** — every arm differs from its neighbour in exactly the thing being studied.
- **Attributable** — each row names the run, the commit, and the command that produced it.
- **Bounded** — the number carries how much it moves when you change nothing that matters.

## Comparable arms

**Change one thing at a time.** Add signals, modules, or data sources one by one, and confirm each
one buys the gain you expected before adding the next. A matrix built by changing several things
at once cannot tell you which one paid.[^recipe]

**The killer is the difference nobody wrote down.** Metric-learning papers were re-evaluated under
one protocol and the reported gains largely evaporated; the differences that produced them were
architecture (ResNet50 against BN-Inception against GoogleNet), embedding dimension (512 or 1536
against 64), augmentation described as "simple" but actually `RandomResizedCrop`, crop size, and
whether BatchNorm was frozen — none of it in the comparison table.[^musgrave] So before an arm
counts, diff the resolved configs of every arm against each other and confirm the only differences
are the ones under study. Same backbone, same optimizer, same learning-rate schedule, same
augmentation, same embedding size, same stopping rule, same evaluation protocol.

**The tuning budget is itself a variable.** Standard LSTMs, given the same large black-box search
budget as the architectures that had displaced them, came back ahead — the difference was the
budget, not the model.[^melis] An arm that received a week of tuning and an arm that received an
afternoon are not two points on the same axis. Give every arm the same budget, or report the
budgets.

**Report the stopping point of each arm.** A reviewer who works out that one arm trained longer,
and had to work it out, starts auditing everything else in the paper.

## Baselines

**Assume reproduction will fail, and treat that as normal rather than as your mistake.** Of
eighteen neural recommender methods examined, seven could be reproduced with reasonable effort,
and six of those were beaten by simple nearest-neighbour or graph baselines — the paper named the
pattern *phantom progress* and traced it to incorrect data splitting, test data used during
training, default hyperparameters, and weak baselines.[^dacrema]

**Give the baseline the compute you gave yourself.** With enough hyperparameter search and enough
restarts most models reach similar scores, and reported improvements can come from a larger
budget rather than an algorithmic change.[^lucic] A baseline you ran once, at defaults, against a
method you tuned for a week, is not a comparison.

**When your reproduction lands below the published number**, the honest report is the budget, not
a single point: expected performance as a function of compute, which makes visible how much of the
gap is search. Published comparisons have reversed under this treatment.[^dodge] State the
protocol difference in the caption before a reviewer states it for you. A baseline reproduced
below its published number and reported bare reads as suppression, whatever the cause.

## Variance

**A fixed seed is hygiene, not statistics.** It buys you the same result twice from the same code.
It says nothing about how much the result moves.[^recipe]

**Do not tune the seed.** A method that only works on some seeds is not a robust contribution.
Five runs is a reasonable starting point, and every reported result aggregates over them.[^sinha]

**Randomising only the seed is the wrong economy.** Variance comes from data sampling, parameter
initialisation, and hyperparameter choice as much as from the seed, and randomising all of them
under a fixed budget approaches the ideal estimator at roughly a fifty-fold reduction in compute
against adding more seeds.[^bouthillier] So vary the data split and the initialisation too, rather
than buying the twentieth seed.

**An error bar must say what it captures.** Whether it is a standard deviation or a standard
error, and which source of variation it spans, is part of the number.[^neurips] An unlabelled bar
is decoration.

## Provenance

**Commit before the run, and tag the result with the commit.**[^sinha] A number whose code you
cannot reconstruct is not evidence.

**Configuration lives in a file, not in the command line**, so the run's settings are an artifact
you still have next month. Track which data split each run used. Keep both the last and the best
checkpoint.[^sinha]

**Every row of the result table carries the command that regenerates it**, along with the
hyperparameters and any trick that was needed to get there.[^pwc] Write the compute each run cost
while you still know it — a reviewer asks, and so does the next person to run the matrix.[^neurips]

When a panel or a row cannot be traced to a run of your own, regenerate it rather than reasoning
about where it probably came from.

## When the matrix will not carry the claim

Sometimes everything ran and the numbers still do not say what the paper wants to say. Two moves,
in this order.

**Lay out the whole argument before deciding the matrix is finished.** Writing the full outline is
what reveals the experiments that are missing for the argument to hold together — the sequence
runs argument-first, not matrix-first. A paper sells one thing that was not there before; it is
not a report on the experiments you happened to run.[^phd] So the outline names the missing arm,
rather than the finished matrix being searched for a story.

**Then keep the claim inside what the evidence generalises to.** A claim has to match the results
in how far they can be expected to carry, and the limits that remain — few datasets, few runs —
belong in the paper rather than in your hope that nobody checks.[^neurips] The two failure shapes
to watch for are explanation drifting into speculation, and a gain whose source was never
isolated.[^lipton]

Reframing which honest claim to foreground is legitimate. Rerunning until a number flatters you,
or reporting the one split where you win, is not. If a new angle needs a new experiment, commit to
reporting whatever it returns before launching it.

## Done

- Every arm's resolved config was diffed against its neighbours, and the only differences are the
  ones under study.
- Each baseline states its source: reproduced locally with artifacts, or reported from a named
  paper. A reproduction below the published number carries the protocol difference.
- Every reported number aggregates over runs, and each error bar says what it captures.
- Every row of every table names the run, the commit, and the command that regenerates it.
- The claim the paper makes is one this matrix supports, and the limits it does not cover are
  written down.

[^recipe]: Karpathy, A. *A Recipe for Training Neural Networks*, 2019. <https://karpathy.github.io/2019/04/25/recipe/>
[^phd]: Karpathy, A. *A Survival Guide to a PhD*, 2016. <https://karpathy.github.io/2016/09/07/phd/>
[^musgrave]: Musgrave, K., Belongie, S., Lim, S.-N. *A Metric Learning Reality Check*, 2020. <https://arxiv.org/abs/2003.08505>
[^melis]: Melis, G., Dyer, C., Blunsom, P. *On the State of the Art of Evaluation in Neural Language Models*, 2017. <https://arxiv.org/abs/1707.05589>
[^dacrema]: Ferrari Dacrema, M., Cremonesi, P., Jannach, D. *Are We Really Making Much Progress?*, RecSys 2019. <https://dl.acm.org/doi/10.1145/3298689.3347058>
[^lucic]: Lucic, M., et al. *Are GANs Created Equal? A Large-Scale Study*, 2017. <https://arxiv.org/abs/1711.10337>
[^dodge]: Dodge, J., et al. *Show Your Work: Improved Reporting of Experimental Results*, EMNLP 2019. <https://aclanthology.org/D19-1224/>
[^sinha]: Sinha, K. *Practices for Reproducibility*. <https://koustuvsinha.com/practices_for_reproducibility/>
[^bouthillier]: Bouthillier, X., et al. *Accounting for Variance in Machine Learning Benchmarks*, MLSys 2021. <https://arxiv.org/abs/2103.03098>
[^neurips]: NeurIPS Paper Checklist guidelines. <https://neurips.cc/public/guides/PaperChecklist>
[^lipton]: Lipton, Z. C., Steinhardt, J. *Troubling Trends in Machine Learning Scholarship*, 2018. <https://arxiv.org/abs/1807.03341>
