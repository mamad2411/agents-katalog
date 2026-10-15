---
name: crux
description: "CRUX — Calibrated Reasoning under eXtreme uncertainty. 8 modes from quick assess to full adversarial analysis with subagents. /crux [mode] <question>. CIA SATs + superforecasting + Kahneman + Munger + Hegelian dialectic. Find the linchpin. Commit to the number."
---

# /crux — Calibrated Reasoning under eXtreme Uncertainty

Trigger: user says `/crux` followed by a question, decision, plan, or problem.

```
/crux [mode] <question or problem>
```

## Modes

| Mode | When to use | Depth | Subagents |
|------|-------------|-------|-----------|
| `assess` | Quick strategic read | Light | No |
| `analyze` | Deep structured analysis | Heavy | No |
| `debate` | Adversarial stress-testing with Delphi rounds | Heavy | Yes -- 2-3 agents |
| `forecast` | Calibrated prediction | Heavy | No |
| `decide` | High-stakes choice between options | Heavy | Yes -- 2 agents |
| `explore` | Map solution/possibility space exhaustively | Heavy | No |
| `root-cause` | Diagnose why something failed or isn't working | Medium | No |
| `full` | Maximum rigor -- all stages + 3 agents | Very heavy | Yes -- 3 agents |

Default mode if omitted: `analyze`

## Companions

| Command | What | Time |
|---------|------|------|
| `/cybw` | "Could You Be Wrong?" adversarial self-check | 60 sec |
| `/unstick` | Break through analysis paralysis | 2 min |
| `/retro` | Post-decision retrospective + calibration | 5 min |

## Phase Zero (Always -- Before ANY Output)

Before ANY structured analysis, wrestle with the problem organically:
1. What is the REAL question underneath the surface question?
2. What does your gut say? (System 1 -- untested hypothesis, not conclusion)
3. What would the smartest person who disagrees say?
4. Are you pattern-matching or actually thinking?

Full protocol: [RULES.md](RULES.md)

## Execution Router

For ANY /crux invocation:

1. **Read [RULES.md](RULES.md)** -- Iron Rules, Phase Zero, Anti-patterns, Quality Standards (always)
2. **Run Phase Zero** internally
3. **Load mode-specific files:**

| Mode | Load |
|------|------|
| assess | [modes/assess.md](modes/assess.md), [operations/emotional-political.md](operations/emotional-political.md) |
| analyze | [PRINCIPLES.md](PRINCIPLES.md), [modes/analyze.md](modes/analyze.md) |
| debate | [PRINCIPLES.md](PRINCIPLES.md), [modes/debate.md](modes/debate.md), [operations/agent-management.md](operations/agent-management.md) |
| forecast | [PRINCIPLES.md](PRINCIPLES.md), [modes/forecast.md](modes/forecast.md) |
| decide | [PRINCIPLES.md](PRINCIPLES.md), [modes/decide.md](modes/decide.md), [operations/agent-management.md](operations/agent-management.md) |
| explore | [modes/explore.md](modes/explore.md) |
| root-cause | [PRINCIPLES.md](PRINCIPLES.md), [modes/root-cause.md](modes/root-cause.md) |
| full | [PRINCIPLES.md](PRINCIPLES.md), [modes/full.md](modes/full.md), [operations/agent-management.md](operations/agent-management.md) |

4. **Adapt to user profile:** [profiles/profiles.md](profiles/profiles.md)
5. **Load techniques on demand** from [techniques/](techniques/) as analysis requires
6. **After analysis:** [operations/calibration.md](operations/calibration.md) for self-audit
7. **Heavy modes:** [operations/persistent-output.md](operations/persistent-output.md) for disk output

## Skill Integration

| When you need | Use |
|---------------|-----|
| Large-scale research (20+ topics) | `/enterprise-research` |
| Creative idea generation | `/brainstorming` |
| Code quality decisions | `/build-guardian` |
| Save conclusions for future | `/save-session` |

## Reference Files

| File | Contents |
|------|----------|
| [RULES.md](RULES.md) | Iron Rules, Phase Zero, Anti-patterns, Quality Standards |
| [PRINCIPLES.md](PRINCIPLES.md) | Core Principles, CLA, Munger Lattice, Meta-selector |
| [techniques/](techniques/) | 10 analytical techniques (analogies, contrarian, sensitivity, wargaming, evidence, EVPI, bias, confidence, so-what, expert-panel) |
| [operations/](operations/) | 8 operational files (agents, output, context, calibration, failure, cross-session, time-pressure, emotional-political) |
| [profiles/profiles.md](profiles/profiles.md) | 6 cognitive profiles + detection + adaptation |
| [companions/](companions/) | 3 micro-commands (cybw, unstick, retro) |
| [examples/worked-example.md](examples/worked-example.md) | Full worked example (K2 Build decision) |
| [citations/CITATIONS.md](citations/CITATIONS.md) | 10 research papers with specific findings |
