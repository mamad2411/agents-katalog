---
name: finding-unknowns
description: "Use when the user says 'what am I missing', 'what don't I know', 'interview me', '采访我', 'map the unknowns', 'look back', 'what did I learn', or runs /fu-interview or /fu-lookback: the unknowns map, an interview, a look-back."
metadata:
  credits: "Thariq Shihipar (quadrants); Addy Osmani (critical thinking)"
---

# Finding Unknowns

Keep the person's map of what they know and do not know visible; update it only on evidence.

- `/fu-interview`, "interview me", "采访我": run the Interview.
- "What am I missing", "map the unknowns": one `fu:before` and a direct answer; no rounds.
- `/fu-lookback`, "look back", "what did I learn": run the Look-back.

Quadrants: **KK** relied on (risk: a false known); **KU** a nameable question; **UK** known
but unsaid (taste, constraints, context); **UU** not known to ask.

## Rules that always hold

- Facts are your job. Ask only what only they can answer, recommending an answer "yes" accepts.
- Quote their expectation verbatim; never write one for them. Your guess at it goes under UK.
- Never manufacture entries. Omit an empty field, except `You expect`.
- Explain only failed expectations, or when asked. Teach until they can predict
  the behaviour.
- Write nothing to disk unless they say "save".
- `fu-note:` lines: do not reply or change course.
- Interviews and look-backs print no `fu:before` or `fu:after`. Nothing follows
  `fu:after`, `fu:interview` or `fu:lookback`.
- Silent on trivial requests, lookups and casual talk.
- Header tokens stay literal; labels follow the person's language. Chinese:
  你的预期、未说明、已知的已知·我依据的、已知的未知·待解决、我去查、需要你定、我建议、未知的已知·我猜你默认、未知的未知·你没问但要紧、我的预期、若……则我错了；
  预期→实际、原因、新知道的、没有证明的、仍然未知、最省事的查法、替你定的、没选、若错；成立、部分成立、不成立、无法判断；已验证、有数据支持、推断、未检验；事后拟合、凭记忆；没有重要的未知项；
  地图（已知、待解决、需要你定、假定、盲区）、已做的决定、我据以推进的假设、改写后的需求；预期→结果、仍然未知（最早的在前）、你的规律、接下来值得弄懂的。

## Before the work

```
fu:before · {task}
- You expect: "{their words}" | not stated
- KK · relying on
  - {fact or belief} — {you said | file:line | source | assumed}
  - ✗ {belief the check contradicted} — {evidence}
- KU · open
  - {question} — I will find out by {how}
  - {question} — needs you; I would pick {X} because {reason}
- UK · I assume you want
  - {unstated preference or constraint} — {why I guess this}
- UU · you did not ask, but it matters
  - {blind spot} — {why it matters}
- I expect: {outcome}; wrong if {what would show it}
```

At most 12 lines, three entries per field. If nothing is worth mapping: `fu:before · no
significant unknowns`. Show it before any change (reading is fine), then end your turn. Their
reply starts the work; a bare "go" accepts your recommendations. On "just do it", "直接做" etc.:
show it, don't end the turn; do reversible work on recommended answers, list them; only
irreversible steps wait.

After their reply, stop only for a scope change, a ✗ changing what was asked, or an
irreversible step (exact command or message, as your only question; needs an explicit yes,
not "go"/"继续"; run once; never test-run it or its code, even on copies). A ✗ refuting only
their expectation is reported, not a stop.

## After the work

```
fu:after · {task}
- Expected → found
  - You: "{quote}" → {evidence} · held | partly | did not hold | can't tell
    - why: {mechanism} [verified | supported | inferred | untested]
  - Me: {expectation} → {evidence} · {verdict}
- Now known
  - {fact} — {evidence}
- Not proved
  - {check or source} → leaves open {what}
- Still unknown
  - {item} — cheapest way to find out: {how} · {you | me}
- Decided for you
  - {choice or change you did not ask for} — instead of {alternative} · if wrong: {cost}
```

At most 15 lines, after the result; small work gets only `Not proved` and `Still unknown`,
never both empty. `why` only on `partly` or `did not hold`. `Decided for you`: never pad. If
`fu:before` left your context, re-read the transcript or mark quotes `from memory`.
Measured results: an expectation written after seeing data is `post-hoc`; a difference
inside noise is `can't tell`.

## Interview

1. Ask, in their words: what they want, what they expect, what they are least sure of. Wait.
2. Find out what you can; print the map.
3. Rounds of up to three independent questions, most costly-if-wrong first:
   - KK: "You said {X}. What would you see if it were false?"
   - KU: a decision only they can make, with your recommendation.
   - UK: two contrasting concrete options; which is closer, and what is wrong with the other?
   - UU: what an expert would ask, why it matters, your best answer.
   - At most one "what do you expect?" per round, first, no recommendation.
4. After each round: `Map: known {n} · open {n} ({n} needing you) · assumed {n} · blind spots {n}`
5. Stop when the rest is cheaper to learn by doing, you can predict their next three
   answers, or they say stop. After three rounds, say how many questions remain; ask
   whether to continue. If two rounds move nothing, change the kind of question.
6. Print this; do not start the work:

```
fu:interview · {topic}
- Decisions
  - "{quote}"
- Your expectations
  - "{quote}" — would change your mind: {what}
- I will proceed on
  - {assumption}
- Still unknown
  - {item} — found by {how} · {you | me}
- The request, rewritten: {text}
```

## Look-back

- This session: the conversation; if compacted, filter the newest file in `$P`.
- `7d`: filter `$(find "$P" -maxdepth 1 -name '*.jsonl' -mtime -7)`; drop blocks over seven
  days old. A session id: `"$P/{id}.jsonl"`. Never read a transcript whole:

```
P="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/projects/$(pwd | sed 's/[^A-Za-z0-9]/-/g')"
python3 - {files} <<'EOF'
import json, sys
H = ("fu:before", "fu:after", "fu:interview", "fu-note:")
for path in sys.argv[1:]:
    for line in open(path, errors="ignore"):
        if "fu" not in line: continue
        try: d = json.loads(line)
        except ValueError: continue
        if d.get("type") not in ("user", "assistant") or d.get("isSidechain") or d.get("isMeta"): continue
        c = d.get("message", {}).get("content")
        text = c if isinstance(c, str) else "\n".join(
            b.get("text", "") for b in c or [] if isinstance(b, dict))
        n = 0
        for s in text.splitlines():
            hits = [s.find(h) for h in H if h in s]
            if n <= 0 and hits: n, s = 1500, s[min(hits):]; print(d.get("timestamp", ""), d["type"])
            elif not s.strip() or s.startswith("`" * 3): n = 0
            if n > 0: print(s[:n]); n -= len(s) + 1
EOF
```

- Prints nothing, yet `grep -c fu:` finds hits? Inspect one short line;
  otherwise report no blocks.
- Quote; do not reconstruct. Skip placeholders (`{…}`). `Your pattern` needs ≥5
  graded expectations.

```
fu:lookback · {scope}
- Expected → turned out
  - {date} {task}: you "{quote}" → {found} · {verdict}
- Became known
  - {fact} — {date} · {evidence}
- Still unknown (oldest first)
  - {item} — open {n} days · {cheapest way to find out}
- Your pattern
  - stated {k} of {m}; held {h} of {k}; misses cluster in {area}
  - accepted with no question about "Not proved": {a} of {b}
- Worth learning next: {one item} — {first step}
```
