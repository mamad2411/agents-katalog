---
name: advisor
description: Get one second opinion or convene two contrasting model families for root-cause analysis and a plan. Use when the user asks for an advisor, a second opinion or what another model thinks, before a risky design or fix, or when stuck, looping on failed fixes, or facing a hard planning or design problem.
user-invocable: true
argument-hint: "[--agent claude|codex|antigravity|zcode] <question>"
---

# Advisor

For a committee of two contrasting families, load [references/committee.md](references/committee.md) and follow that procedure instead. Load it only for a committee: stuck or looping work, or a very hard planning or design problem. The procedure below is for one second opinion.

For a choice among given options while an away lease is live (`afk` "Decide"), load [references/choose.md](references/choose.md) and follow that choose mode instead: it returns exactly one option with its reason, or `none`, and there the advisor decides, not you.

The procedure below is the open mode. One agent reads the situation and gives a judgement. You stay the decider; the advisor does not drive the work.

**User's request:** $ARGUMENTS

## When to run

Propose an advisor and wait for the user's yes, because each run spends quota. Propose it when the decision cannot be undone or changes a contract, or when your own analysis leaves you unsure. A user who asks for one needs no proposal. During a live away lease use the choose mode. When the user is away without a lease, run one without the yes when a decision would otherwise wait for them, as `delegate` says for an absent user, and record who settled it.

**Advisory (agent judgment):** Talk to the user in the language they are using, including questions and option labels; keep command names, flags, file paths, skill names and other technical names unchanged.

## Picking the advisor

1. An agent the user names wins.
2. Otherwise route through the assignment matrix (`## Assignment matrix` in the host config): the helper whose line lists `roles ... advisor`, when it is of a family other than yours (a `claude<suffix>` command is the claude family). Without one, run `route_pick.py pick --kind advisor --level <n> --coordinator <your family>` (`delegate` scripts; `<n>` is the question's difficulty, 1 easy to 5 ultra hard) and take the first candidate line whose agent is of a family other than yours; a `drop` line or `no preference` names no one. Without either, prefer contrast: a model family other than the one you run on, among those `delegate` `references/models.md` lists and the host config shows present. When the pick is your own family, say so. All read-only. The tier follows the question's difficulty: strong for an easy or medium question (a mid-priced model is enough), frontier for a hard or very hard one. Advisory (agent judgment); `route_pick.py` only orders candidates and grants nothing.
3. When the picked family is out of quota or unreachable, try the next candidate of another family, and each of its models. Use a subagent of your own host with fresh context only when every model of every other family is out of quota or unreachable, and say that the opinion comes from the same family.

Load the `delegate` skill and the host config for the invocation commands and read-only flags. Requires the `delegate` skill installed beside this one. When it is missing, tell the user to add it (`npx skills add finolabs/vibecode --skill delegate`, or install the whole plugin) and stop.

## The briefing

The advisor has zero context:

- the question, sharply;
- what you have considered and ruled out;
- relevant files by path, for the advisor to read itself;
- the ask: "Give me a recommendation, with reasoning and the evidence you used."

If the arguments reference another skill (`/name` or `$name`), tell the advisor: "Invoke the `<name>` skill against this task before anything else," and pass the remaining arguments as that skill's input.

End every briefing with:

```
This is analysis only. Do NOT edit, create, or delete any files. Do NOT write code.
```

## Run and synthesize

Dispatch with a budget and hard cap from `delegate` "Budget and liveness" and record it in the ledger with `--kind advise` and the question's difficulty as `--grade`. Read the answer, check its claims against the code where they matter, then give the user the advisor's verdict and your own recommendation, saying where you agree and where you differ. Where you differ on a point that changes direction, give the user both arguments and let them decide. When the user is away without a lease, take the option that can be undone, record who settled it, and hold the part of the work that depends on a point you cannot undo until the user answers; never settle it by weighing the two opinions.

For ongoing input, send follow-ups to the same advisor: a session or a resumable run keeps its context; a one-shot headless run gets a new prompt that carries the earlier question and answer. Start fresh when the topic shifts.
