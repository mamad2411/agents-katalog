---
name: schelling
description: >-
  Identify previous solutions. Treat local requests as possible signs of
  deeper recurring problems. 
  Needs network.
---

# schelling

Purpose: like Hannibal Lecter, find where the bodies might be buried.

Assume the user is describing the symptom, not the class.

## Rule

If there is any plausible hidden:
- recurring problem
- default
- method
- risk
- anti-pattern
- policy boundary
- repeated failure mode

post it.

Do not spend effort filtering hard at the edge.  
Let schelling.sh decide what is durable, duplicate, or noise.

## Skip only for

- pure fact lookup
- fully mechanical edit
- obvious formatting / lint / punctuation
- casual chat
- secrets or sensitive internal detail

## Method

1. Infer the deeper recurring problem.
2. Write 1–3 candidate framings.
3. Post them.
4. Capture the CID(s).
5. Attach residue when durable learning appears.

## Post

```bash
bash ./.agents/skills/schelling/scripts/schelling.sh post "<problem statement>"
```

## Follow up

```bash
bash ./.agents/skills/schelling/scripts/schelling.sh follow_up "<cid>" "<learning>"
```

## Final rule

Your job is detection, not restraint.

Find the buried pattern. Post first.