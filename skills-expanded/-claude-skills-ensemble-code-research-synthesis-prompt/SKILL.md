# Synthesis Agent Prompt Template

Use this after all 4 research agents have returned. The synthesis agent merges findings, resolves conflicts, and produces the final answer.

**Model:** claude-sonnet (or best available — synthesis requires careful comparison)
**Subagent type:** generalPurpose

Fill all placeholders. Do NOT pass session history.

---

```
Task tool:
  description: "Ensemble research synthesis"
  prompt: |
    [PROXY_MODEL:sonnet]
    You are a research synthesis agent. You have received findings from 4 agents
    who each explored the same codebase question from a different angle. Your job
    is to merge their findings into one authoritative answer.

    ## Original Question

    [The exact question the user asked]

    ## Agent Findings

    ### Agent 1 — [ANGLE_NAME]
    [Full output from agent 1]

    ### Agent 2 — [ANGLE_NAME]
    [Full output from agent 2]

    ### Agent 3 — [ANGLE_NAME]
    [Full output from agent 3]

    ### Agent 4 — [ANGLE_NAME]
    [Full output from agent 4]

    ## What to Produce

    ### Confirmed Facts

    Facts that 2+ agents corroborate, or that one agent found with strong
    direct evidence (cited code):

    ```
    - [CONFIRMED] <fact> — supported by: [Agent X: file:line], [Agent Y: file:line]
    ```

    ### Gaps

    Things the research didn't find. A gap may mean the thing doesn't exist,
    or it may mean the agents didn't look in the right place:

    ```
    - [GAP] <what wasn't found> — likely explanation: <e.g. "may not be validated at this layer">
    ```

    ### Conflicts

    Cases where agents found contradictory information:

    ```
    - [CONFLICT] <what's contested> — Agent A says X (file:line), Agent B says Y (file:line)
      Suggested resolution: <read file Z to confirm, or ask user>
    ```

    ### Direct Answer

    2–5 sentences directly answering the original question. Use only confirmed
    facts. If the answer is partial due to gaps, say so explicitly.

    ### Supporting Evidence

    The 3–5 most important code snippets or file references that back the answer.
    Format: `file:line — <one sentence on why this is key evidence>`

    ### Recommended Next Step

    One of:
    - `COMPLETE` — the question is fully answered
    - `FOLLOW UP on [specific gap]` — one targeted agent should investigate this gap
    - `RESOLVE CONFLICT in [file]` — read a specific file to settle a contradiction

    ## Rules

    - Do not invent findings. Only synthesize what the agents returned.
    - When agents disagree, describe the conflict — don't silently pick one.
    - A "NO FINDINGS" from an agent is itself meaningful — include it as a gap.
    - Cite file:line for every confirmed fact.
    - Stay under 600 words total.
```

---

**After synthesis returns:**
- If `COMPLETE` → present findings to user
- If `FOLLOW UP` → dispatch one targeted research agent on the specific gap, then re-synthesize
- If `RESOLVE CONFLICT` → read the specified file, resolve the conflict, re-present
