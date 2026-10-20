---
name: mongo-hive
description: Use MongoHive's shared, eval-tested tools before re-deriving answers from project data. Use when a task matches a tool your team's hive already has (they appear as their own mongo-hive tools, e.g. advisory_owners), or when you just solved a data question that will come up again. Not for grading answers; only people give feedback.
---

# MongoHive

1. **Prefer a native hive tool.** If one of the `mongo-hive` tools matches the task by name or description, call it directly. Its promoted version already passed the hive's evals: answer from its result instead of re-deriving it.
2. **No match?** Call `find_capability` with the task in plain words; it also lists unverified tools and tells you if a better version exists.
3. **Nothing exists?** Investigate with `explore`, answer, then save the method with `propose_capability`: parameterize every value that came from the data with `{{param}}`. Publish it to a shared hive with `publish_capability` when it should help teammates.
4. **Never grade your own work.** Each run returns an `outputId`; only the person decides whether it was right (`/mongo-hive:accept` or `/mongo-hive:reject`). Don't try to mark results correct yourself.
5. If a reply carries `notices` (a teammate's tool took the lead, a new tool is available), mention them briefly and use the newer tool.
