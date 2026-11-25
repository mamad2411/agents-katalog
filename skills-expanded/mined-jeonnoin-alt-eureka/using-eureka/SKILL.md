---
name: using-eureka
description: Use when starting any conversation involving research, hypotheses, experiments, data analysis, scientific claims, or manuscript writing — establishes how to find and use Eureka research skills
---

<SUBAGENT-STOP>
If you were dispatched as a subagent to execute a specific task, skip this skill.
</SUBAGENT-STOP>

<EXTREMELY-IMPORTANT>
If you think there is even a 1% chance an Eureka skill might apply to what you are doing, you ABSOLUTELY MUST invoke the skill.

IF A SKILL APPLIES TO YOUR TASK, YOU DO NOT HAVE A CHOICE. YOU MUST USE IT.

This is not negotiable. This is not optional. You cannot rationalize your way out of this.
</EXTREMELY-IMPORTANT>

## Instruction Priority

Eureka skills override default system prompt behavior, but **user instructions always take precedence**:

1. **User's explicit instructions** (CLAUDE.md, GEMINI.md, AGENTS.md, direct requests) — highest priority
2. **Eureka skills** — override default system behavior where they conflict
3. **Default system prompt** — lowest priority

If CLAUDE.md says "skip hypothesis registration for exploratory analysis" and a skill says "always register," follow the user's instructions. The user is in control.

### Coexistence with Superpowers

If `superpowers` skills are also available, they remain in force for **software engineering tasks**. Eureka adds research skills — it does not replace software ones.

- `superpowers:brainstorming` → feature design, component architecture
- `eureka:research-brainstorming` → hypothesis design, study architecture
- `superpowers:code-reviewer` → code quality, production readiness
- `eureka:research-reviewer` → scientific rigor, publication readiness

Use the namespace that matches the artifact: **code** → superpowers, **science** → eureka.

## How to Access Skills

**In Claude Code:** Use the `Skill` tool with the `eureka:` prefix. When you invoke a skill, its content is loaded and presented to you — follow it directly. Never use the Read tool on skill files.

**In Gemini CLI:** Skills activate via the `activate_skill` tool. Gemini loads skill metadata at session start and activates the full content on demand.

**In other environments:** Check your platform's documentation for how skills are loaded.

# Using Eureka Skills

## The Rule

**Invoke relevant or requested skills BEFORE any response or action.** Even a 1% chance a skill might apply means you should invoke it. If an invoked skill turns out to be wrong for the situation, you don't need to use it.

```dot
digraph eureka_flow {
    "User message received" [shape=doublecircle];
    "Research task detected?" [shape=diamond];
    "Already brainstormed\nresearch design?" [shape=diamond];
    "Invoke research-brainstorming" [shape=box];
    "Might any eureka skill apply?" [shape=diamond];
    "Invoke Skill tool" [shape=box];
    "Announce: 'Using [skill] to [purpose]'" [shape=box];
    "Has checklist?" [shape=diamond];
    "Create TodoWrite todo per item" [shape=box];
    "Follow skill exactly" [shape=box];
    "Respond (including clarifications)" [shape=doublecircle];

    "User message received" -> "Research task detected?";
    "Has formed research question?" [shape=diamond];
    "Invoke research-ideation" [shape=box];

    "Research task detected?" -> "Has formed research question?" [label="yes"];
    "Has formed research question?" -> "Already brainstormed\nresearch design?" [label="yes"];
    "Has formed research question?" -> "Invoke research-ideation" [label="no — only keywords,\ndataset, or vague interest"];
    "Invoke research-ideation" -> "Already brainstormed\nresearch design?";
    "Research task detected?" -> "Might any eureka skill apply?" [label="unclear"];
    "Already brainstormed\nresearch design?" -> "Invoke research-brainstorming" [label="no"];
    "Already brainstormed\nresearch design?" -> "Might any eureka skill apply?" [label="yes"];
    "Invoke research-brainstorming" -> "Might any eureka skill apply?";

    "Might any eureka skill apply?" -> "Invoke Skill tool" [label="yes, even 1%"];
    "Might any eureka skill apply?" -> "Respond (including clarifications)" [label="definitely not"];
    "Invoke Skill tool" -> "Announce: 'Using [skill] to [purpose]'";
    "Announce: 'Using [skill] to [purpose]'" -> "Has checklist?";
    "Has checklist?" -> "Create TodoWrite todo per item" [label="yes"];
    "Has checklist?" -> "Follow skill exactly" [label="no"];
    "Create TodoWrite todo per item" -> "Follow skill exactly";
}
```

## The Research Lifecycle

Each Eureka skill maps to a phase of the research lifecycle. The workflow is not strictly linear — failed experiments send you back to earlier phases, and that is expected.

```dot
digraph research_lifecycle {
    rankdir=TB;
    node [shape=box];

    stuck [label="STUCK — Don't know what to do?\neureka:whats-next\n(diagnoses state + routes to right skill)", shape=ellipse, style=dashed];
    journal [label="Session Journal\neureka:research-journal\n(narrative state writer)", shape=note, style=filled, fillcolor="#ffffcc"];
    rq [label="Research Question\neureka:research-brainstorming\n(includes literature gap +\nDevil's Advocate)"];
    hr [label="Hypothesis Registration\neureka:hypothesis-first\n(includes statistical plan)"];
    plan [label="Experiment Planning\neureka:experiment-design"];
    exp [label="Experiment Execution\n(your work)"];
    trouble [label="Troubleshooting\neureka:systematic-troubleshooting"];
    rev [label="Results Review\neureka:requesting-research-review"];
    write [label="Manuscript Writing\neureka:manuscript-writing\n(section-by-section with reviewer)"];
    figd [label="Figure Design\neureka:figure-design\n(chart-type + typography +\ncolorblind-safe palette +\nfigure-reviewer subagent)"];
    novelty [label="Novelty Audit\neureka:novelty-competitive-audit\n(pre-submission external\ncompetitiveness check +\npreemption detection +\nPASS/CONCERN/BLOCK)"];
    audit [label="Claims Audit\neureka:claims-audit"];
    pub [label="Submission Gate\neureka:verification-before-publication"];
    submit [label="Submit / Archive\neureka:submission-readiness"];
    ideation [label="Research Ideation\neureka:research-ideation\n(idea generation from\nkeywords/data/papers)"];

    ideation -> rq [label="idea selected"];
    rq -> hr [label="design approved\ngap verified"];
    hr -> plan [label="hypothesis registered"];
    plan -> exp [label="plan ready"];
    exp -> trouble [label="unexpected result"];
    trouble -> exp [label="root cause fixed"];
    trouble -> rq [label="hypothesis wrong"];
    exp -> rev [label="phase complete"];
    rev -> exp [label="FAIL: fix and re-run"];
    rev -> write [label="PASS"];
    write -> figd [label="section cites figure"];
    figd -> write [label="figure approved"];
    write -> novelty [label="manuscript complete"];
    novelty -> write [label="CONCERN/BLOCK:\nreframe or narrow"];
    novelty -> audit [label="PASS"];
    audit -> pub [label="audit PASS"];
    pub -> write [label="FAIL: revise"];
    audit -> write [label="FAIL: fix claims"];
    pub -> submit [label="PASS"];
    exp -> rq [label="pivot needed"];

    stuck -> rq [style=dashed, label="route"];
    stuck -> hr [style=dashed];
    stuck -> plan [style=dashed];
    stuck -> trouble [style=dashed];
    stuck -> rev [style=dashed];
    stuck -> write [style=dashed];
    stuck -> pub [style=dashed];
    stuck -> submit [style=dashed];
    stuck -> ideation [style=dashed];
    stuck -> figd [style=dashed];
    stuck -> novelty [style=dashed];

    ideation -> journal [style=dashed, label="capture"];
    rq -> journal [style=dashed, label="capture"];
    hr -> journal [style=dashed];
    plan -> journal [style=dashed];
    trouble -> journal [style=dashed];
    rev -> journal [style=dashed];
    write -> journal [style=dashed];
    audit -> journal [style=dashed];
    journal -> stuck [style=dashed, label="informs"];
}
```

## Red Flags

These thoughts mean STOP — you're rationalizing skipping a skill:

| Thought | Reality |
|---------|---------|
| "I just want to run a quick experiment" | Quick experiments become the paper. Design first. |
| "My hypothesis is obvious" | Unstated hypotheses get HARKed. Register it. |
| "I'll do the stats properly later" | Post-hoc statistics inflate Type I error. Lock them now. |
| "I can reproduce this from memory" | You cannot. Seeds, configs, environment must be recorded. |
| "The result is significant — that's enough" | Effect size, CI, and multiple-comparison correction are not optional. |
| "I know what the reviewer will say" | Invoke the reviewer. You are wrong. |
| "This is just a preliminary result" | Preliminary results become the paper. Rigor from day one. |
| "We can improve reproducibility later" | Reproducibility cannot be retrofitted. Build it in from the start. |
| "The claim is supported by the figure" | Trace the figure to its source file. If you can't, you can't publish it. |
| "This doesn't need a formal design" | Unexamined assumptions waste months. The design can be short, but it must exist. |
| "Let me just look at the data first" | Looking at data before locking your analysis plan is how p-hacking starts. |
| "The sample size should be fine" | Should be? Run the power analysis. |
| "Internal scores are high, we're ready to submit" | Internal scores don't check external preemption. `novelty-competitive-audit` catches the 6-12 months of field drift between design approval and submission — the most common desk-reject reason. |

## Skill Priority

When multiple skills could apply, use this order:

1. **Triage first** (whats-next) — when the user is stuck or unsure which phase they are in, route through `whats-next` to identify the right specialist
2. **Process skills second** (research-ideation, research-brainstorming, hypothesis-first) — these determine HOW to approach the research
3. **Review skills third** (requesting-research-review, claims-audit) — these validate execution
4. **Gate skills fourth** (verification-before-publication) — these approve transitions
5. **Continuity skills last** (research-journal) — run at session end or after major events to preserve narrative state for the next session

"I want to test whether X causes Y" → research-brainstorming first, not experiment execution.
"My experiments are done" → requesting-research-review first, not manuscript writing.
"I don't know what to do next" → whats-next first, then whatever it routes you to.
"Session is wrapping up" → research-journal to capture decisions before context is lost.
"I have this dataset but don't know what to study" → research-ideation first, not research-brainstorming.
"Make a figure" / "the figure looks wrong" / "update fig X" → figure-design first, then manuscript-writing if a caption or section update is also needed.
"Manuscript is ready but not sure it's still novel" / "worried about preemption" / "rigor scores high but nervous about field overlap" → novelty-competitive-audit, which blocks submission-readiness until it PASSes.

## Skill Types

**Rigid** (follow exactly, do not adapt away discipline):
- using-eureka
- hypothesis-first
- claims-audit
- verification-before-publication
- novelty-competitive-audit

**Flexible** (adapt principles to domain and context):
- research-ideation
- research-brainstorming
- experiment-design
- systematic-troubleshooting
- requesting-research-review
- receiving-research-review
- submission-readiness
- whats-next
- research-journal
- manuscript-writing
- figure-design

The skill itself tells you which type it is.

## User Instructions

Instructions say WHAT to research, not HOW to ensure rigor. "Run experiment X" or "Analyze dataset Y" does not mean skip the research workflow.

## Announcement language (multi-locale allowance)

The skill invocation announcement ("Using [skill] to [purpose]") **may be in the user's ambient language** — if the user writes in Korean, announce in Korean (e.g., "research-brainstorming 스킬을 사용해 연구 질문을 정의합니다"); if the user writes in English, announce in English; if another language, match the user's language.

**Skill body and structured output** (design documents, registration YAML frontmatter, research-reviewer reports, claims-audit tables, etc.) **remain in English** — plugin standard for portability, CI parsing, and cross-team reuse. Announcements are the only user-facing surface that flexes by locale.

This allowance addresses the "Korean researchers code-switch every skill invocation" friction surfaced in external feedback. Korean speakers can now trigger skills naturally via Korean descriptions (already supported since v1.4.1) and receive Korean announcements without breaking skill-internal structure.

## Canonical output paths (skill artifacts)

Skills that produce durable artifacts should write to canonical locations under `docs/eureka/` so downstream skills can find them:

| Skill / Agent | Canonical output path |
|---|---|
| `research-brainstorming` | `docs/eureka/designs/YYYY-MM-DD-<topic>-design.md` |
| `hypothesis-first` | `docs/eureka/registrations/YYYY-MM-DD-<topic>-registration.md` + updates to `docs/eureka/registrations/INDEX.md` |
| `experiment-design` | `docs/eureka/plans/YYYY-MM-DD-<topic>-experiments.md` |
| `claims-audit` | `docs/eureka/audits/YYYY-MM-DD-claims-audit.md` |
| `research-reviewer` agent | `docs/eureka/reviews/YYYY-MM-DD-review.md` |
| `novelty-competitive-audit` | `docs/eureka/novelty-audits/YYYY-MM-DD-novelty-audit.md` |
| `verification-before-publication` | `docs/eureka/verifications/YYYY-MM-DD-verification.md` |
| `research-journal` | `docs/eureka/journal/YYYY-MM-DD.md` |

**Freshness metadata** — every artifact includes YAML frontmatter:

```yaml
---
generated_at: <ISO-8601 timestamp>
manuscript_hash: sha256:<hex>      # or N/A for pre-manuscript artifacts
results_hash: sha256:<hex>          # content digest of results/ (see helper below)
status: passed | failed | in_progress
---
```

**Computing the hashes** — use the shipped helper script:

```bash
# Get both hashes ready to paste into YAML frontmatter:
hooks/freshness-hash.sh both paper/main.tex results/

# Individual hashes:
hooks/freshness-hash.sh manuscript paper/main.tex
hooks/freshness-hash.sh results results/
```

The `results_hash` is a content digest: `sha256(concat(sorted(per-file-sha256)))` over all files in `results/` excluding common build artifacts (`.aux`, `.log`, `.synctex.gz`, `.DS_Store`, etc.). Deterministic across filesystems because files are sorted by path. Adding a file, renaming a file, or changing file contents all drift the hash; LaTeX recompilation alone (which regenerates `.aux`/`.log`) does not.

**Downstream freshness check** — `verification-before-publication` and `submission-readiness` read upstream artifacts and soft-warn (not block) if hashes mismatch. Soft warning rather than hard block because file-level hash is sensitive to trivial whitespace changes; users can tighten to hard block by preference.

This addresses the "no state sharing between skills" feedback: prerequisite skills can now verify upstream artifacts exist and are fresh without dispatching the upstream skill again.
