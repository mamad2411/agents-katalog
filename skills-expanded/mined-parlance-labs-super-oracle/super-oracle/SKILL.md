---
name: super-oracle
description: "Run Claude and Codex gpt-6-astra reviews in parallel. Each reviewer gets one refinement pass before one provider writes the final synthesis. Use for deep code review, difficult cross-file debugging, architecture or refactor planning, research synthesis, and multi-model second opinions."
---

# Super Oracle

Run the council from the repository you want to review:

```bash
bash <this-skill-dir>/scripts/super-oracle.sh \
  -C /abs/path/repo -o /abs/path/oracle-round-N.md /abs/path/briefing.md
```

By default, two reviewers work separately and in parallel:

- The rolling `fable` alias selects the latest Claude Fable at `xhigh`.
- Codex `gpt-6-astra` runs at `xhigh`, with fast mode and the fast service tier.

Each healthy reviewer then checks all initial reports and writes one refined
report. The latest Opus combines the best available reports into one synthesis.

These flags change the run:

```text
-s claude|codex           skip a provider
-y opus|codex             choose the synthesizer
-m fable|opus             choose the starting Claude reviewer
-q 1..100                 set the Claude usage cutoff, default 93
-n                        disable Claude/Codex MCP for this run
-t                        use cheap test models, never an oracle verdict
```

Test mode has fixed models. `-m` is invalid with `-t`.

The wrapper skips a missing CLI and prints a warning. A run fails if an explicitly
chosen synthesizer is unavailable. When the default Opus synthesizer is
unavailable, the wrapper may use a healthy Codex provider.
Every run needs `jq` and `pgrep`. Production Claude runs also need `curl`.

## Write the briefing

The reviewers do not know the current conversation. Start with
`reference/briefing-template.md`. Include:

- State the exact goal and question.
- Give the working directory and review scope.
- Include the specification and repository instructions.
- List the relevant files, commands, and current test results.
- State the constraints and non-goals.
- Record the decisions from earlier review rounds.

The wrapper gives each reviewer
`reference/code-review-principles.md`. These principles are general engineering
guidance. They are not a checklist or a required report format.

## Read the output

The `-o` file contains one synthesis for you to judge. The wrapper prints every
active path before it starts the models. With the default artifact directory,
the paths are:

```text
OUTPUT.artifacts/reviews/claude.md
OUTPUT.artifacts/reviews/claude.partial.md
OUTPUT.artifacts/reviews/claude.fable.partial.md
OUTPUT.artifacts/reviews/claude.refined.md
OUTPUT.artifacts/reviews/claude.refined.partial.md
OUTPUT.artifacts/reviews/claude.refined.fable.partial.md
OUTPUT.artifacts/reviews/codex-gpt-6-astra.md
OUTPUT.artifacts/reviews/codex-gpt-6-astra.partial.md
OUTPUT.artifacts/reviews/codex-gpt-6-astra.refined.md
OUTPUT.artifacts/reviews/codex-gpt-6-astra.refined.partial.md
OUTPUT.artifacts/reviews/synthesis.md
OUTPUT.artifacts/reviews/synthesis.partial.md
OUTPUT.artifacts/reviews/synthesis.fable.partial.md
```

The three `*.fable.partial.md` files get content only when an interrupted Fable
attempt has a checkpoint. The wrapper does not create files for skipped
providers. Use a new output file and artifact directory for every review round.

When a refinement fails, the wrapper uses the labeled initial report for
synthesis. It does not copy the initial report into the refined file. The
refined file may keep partial text.

A result marked `DEGRADED` has reduced coverage. This includes runs with only
one reviewer, even when you intentionally skip a provider. It cannot prove
convergence. A synthesis failure ends the run with an error and keeps the source files.

## Decide what to fix

1. Read the synthesis. Read source reports when you need to check evidence,
   disagreement, or review coverage.
2. Judge every finding against the repository. Model agreement is not proof,
   and you may reject a finding.
3. Fix only accepted findings. Make the smallest sufficient change and test it.
4. Run a new production council with the same providers. Add short notes about
   earlier decisions when a repeated finding could cause churn.
5. Continue until a non-degraded run has no finding that you agree should be
   addressed.

Rejected findings do not keep the cycle open without new evidence. The same is
true for duplicate, speculative, cosmetic, or out-of-scope advice. Ask the user
when a finding needs a product decision or new authority.

## Keep the run safe

Child processes bypass permission checks and sandboxing. Use a trusted working
directory. Claude may use only first-party subscription authentication. The
wrapper clears Anthropic API credentials and gateways. It checks subscription
usage before and during production Claude stages. A paid overage event stops the
Claude stage.

Reviewers may use subagents for separate investigations that matter to the
change. Each reviewer chooses those investigations from the code and the
engineering principles. The prompt blocks forced checklist fan-out, unrelated
workflow work, and recursive Super Oracle calls.

Claude `Agent` and `Workflow` stay enabled. Claude child skills, slash commands,
and session persistence stay disabled.
