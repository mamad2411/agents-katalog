---
name: record-decision
description: Records a significant technical or process decision as a numbered ADR in docs/decisions/. Use when choosing between real alternatives, reversing a past decision, or when asked why something is the way it is and no ADR exists.
---
# Record a decision

**Role:** architect (owns `docs/decisions/`). If the human asked you directly for the ADR, you are the architect for this task. Otherwise hand the decision over: a light item with `--status planned --owner architect`, or the handoff of the item it came from.

Follow `docs/dev/how-to/write-an-adr.md`; it is the single source for the steps. The rules that matter most:

- Create the file with `python3 tools/new_adr.py "Title"`. The number is allocated under a lock; never pick one by hand.
- Accepted ADRs are binding. To reverse one, supersede it: `new_adr.py "Title" --supersedes NNNN`. Never edit an accepted outcome.
- Significant, costly or irreversible decisions stay `proposed` until the human accepts them, asked through `question.py`, not in chat. A decision the human already made is recorded as `accepted`.
- Run `python3 tools/check.py` before you stop.

Write for a reader six months from now who was not here. State the decision in active voice: "We will use X because Y."
