---
name: outcomes-sync
description: >-
  Sync campaign outreach results and publish engagement into outcome ledgers, distilling
  learnings to promote into knowledge packs. Trigger when the user says "sync outcomes", "how
  did the campaign do", "update learnings", "what's working", "close the loop", or "pull
  campaign results".
metadata:
  version: "0.2.0"
  phase: "4"
  capability_tier: pipeline
---
This skill's implementation is part of the hosted product and is not included
in this distribution.

**Stop here.** Do not improvise a replacement procedure, and do not fall back to
another skill: report to the operator that this step is unavailable in this
distribution and end the run. A graph reaching this node cannot complete, and an
improvised substitute would spend budget producing something the pack does not
specify.

Its declared interface is above (`outcomes-sync`, tier `pipeline`).
Pack graph node(s) that invoke it: `outcomes-loop/outcomes-loop`.

See `docs/SKILLS.md` for the full skill roster.
