---
description: Devil's advocate. Runs the output bias self-check against a claim, recommendation, or decision so the OS turns its skepticism on the position on the table. Say "challenge this", "what's the counter", "steelman the other side", "am I just agreeing with myself", "check your bias", "play devil's advocate", "poke holes", or run /founder-os:devil before committing to a consequential call. Read-only.
argument-hint: <the claim, recommendation, or decision to challenge>
allowed-tools: ["Read"]
---

# Devil's advocate

Turn the bias lens on the position itself, not on the person holding it. The target is the strongest honest case against, plus an honest confidence read. This runs the output self-check in `rules/biases.md` on demand.

Argument: `$ARGUMENTS` (the claim, recommendation, or decision to challenge). If empty, challenge the most recent opinion in this conversation. If there is none, reply `What should I challenge? Re-run as /founder-os:devil <claim>.` and stop.

## Procedure

1. Read `rules/biases.md` for the six output biases and the contract.
2. If the claim touches live state (a lead, a decision, a relationship, a spend), read the relevant context file first so the challenge is grounded, not generic. Read `brain/.snapshot.md` if it exists.
3. Name which one of the six biases is most likely loading the original position. One, not all six.
4. Build the counter. Do not soften it. Do not perform balance. The job here is the other side.

## Output format

```
DEVIL: <one-line restatement of the position being challenged>

MOST LIKELY BIAS: <one of the six> - <one line on how it shows up here>

THE COUNTER-CASE
-> <strongest argument against, specific>
-> <second, only if there is a real one>

CONFIDENCE: high / medium / low - <the one fact that would move it>
ABSENT: <what evidence is missing that would change the call>
IF YOU DO NOTHING: <what actually happens if this is not acted on>

HONEST READ: <does the position survive the challenge or not, one line, no hedging>
```

## Rules

- Challenge the position, never the person. No "you're being biased".
- If the position survives the challenge, say so plainly. The goal is truth, not a kill.
- Anti-theater: if you cannot build a real counter, say "low confidence, thin evidence", never "all clear".
- No em dashes, no en dashes. No banned words. No rule-of-three.

## Cross-refs

- Runs: `rules/biases.md` (the output bias self-check)
- Companion to `/founder-os:forcing-questions` (whether to START something) and the `decision-framework` skill (choosing between options). This one stress-tests a position already on the table.
